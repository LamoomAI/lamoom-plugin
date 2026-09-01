# The grammar, written so a parser can be written from it

Every rule here exists because a question was asked that the examples did not answer.

## What a reference is

A reference is `{{`, then a body, then `}}`, where the body — after ASCII spaces and tabs are
trimmed from both ends — matches:

    reference := [ "inline:" | "link:" ] path
    path      := segment ( "/" segment )*
    segment   := 1..200 characters, none of them "/", "{", "}" or a control character,
                 and the segment is not "." and not ".."

So `{{ inline:a/b.png }}` and `{{inline:a/b.png}}` are the same reference. A leading or trailing
`/`, an empty segment, and an empty body all make it not a path.

**The character set is deliberately wide.** An earlier draft allowed only `[A-Za-z0-9._-]`, which
would have made `Q3 report.png` and `chart(1).png` unreferenceable by any of the three forms —
and A8 says the exact string a `files` listing returns, pasted into a body, must resolve. A
grammar that cannot name a file the product itself created is broken on day one, so the rule is
the other way round: a segment is anything that is not a separator and not a brace.

**The prefix is decided by exact match, not by splitting on a colon.** The text before the first
`:` is a prefix only if it is exactly `inline` or `link`. A colon anywhere else is an ordinary
path character, so `{{notes/2026-09-01: draft.md}}` is a reference to a file with a colon in its
name — and refuses as missing if there is no such file, which is the right answer.

## Every `{{...}}` is either resolved or refused

There is no third case, and this is the whole reason the grammar is safe: a body cannot reach
Kate with braces in it. `{{notes/x.md}}` resolves or refuses. `{{ user.name }}` refuses, naming
itself, because Lamoom's mail body is not a template engine and a brace nobody meant is still a
brace she would have read.

The one place braces are left alone is code:

- a fenced block, ``` or ~~~
- an inline code span in single backticks
- a block indented by four spaces

That is where the grammar is explained, including in this document and in the mail that ships it.

## What each form produces

| Form | The body gets | The message gets |
|---|---|---|
| `{{inline:path}}` | an image piece naming part `n` | the bytes as part `n` |
| `{{path}}` | `name`, as plain text | the bytes as an attachment |
| `{{link:path}}` | `[name](https://studio.lamoom.com/path)` | nothing |

`name` is the last segment of the path.

**`{{path}}` leaves the name behind rather than deleting the token.** A body that says "the chart
is attached" beside an attachment list that says `chart.png`, with nothing joining them, is the
defect that killed the do-nothing option; deleting the token would rebuild it. Leaving the name
means the sentence names the file, and it also means no question about what happens to a token
alone on its line.

An image piece names a part by index; it is not a URI and not MIME. `render_for_mail` is what
turns that piece into an `<img>` with a `cid:`; another surface turns it into whatever it has.
`cid:` exists in exactly one place, and nothing that plans is that place.

## The counts

- **Parts:** attachments and inline parts count together, and `files=[…]` passed to `send_email`
  counts in the same total. `{{link:}}` counts toward nothing — it carries no bytes.
- **Size:** the cap is read as the total of all parts, not per file. If the live limit turns out
  to be per file, the total reading is the stricter one and still holds. This reading is
  confirmed against the live service in build step 4, not assumed forever. See The limits, below.
- **The same path twice** is one part, referenced twice — dedupe by path.
- **The same path as both `{{inline:}}` and `{{path}}`** is one part. Inline wins the placement;
  the other token still leaves its name behind.

## Is it an image?

From the content type the store holds, and from the last segment's extension —
`.png .jpg .jpeg .gif .webp` — whenever the store has no content type or answers a generic one
like `application/octet-stream`. If neither says image, `{{inline:path}}` is **refused**, reason
`not an image`, fix: use `{{path}}` to attach it.

**It refuses rather than quietly attaching, and that reversal is the point.** An earlier draft
demoted a non-image inline to an attachment and put a note in the return. But the note goes to the
agent that sent the mail, which stops existing minutes later, while the person reads the mail
after that — which is the exact argument this design uses to refuse an expiring link rather than
warn about it. Applying it in one place and not the other was inconsistent, and the silent
demotion was the last failure that still reached Kate without anyone being told.

That deleted the `notes` channel, which had no other user. `plan` returns `Plan(pieces, parts)`.

> **`content_type` is as unread as `expires_at`.** Nothing this session could read says `stat`
> returns it. It gets the same treatment: **build step 1 checks both.** If the store answers a
> generic type for everything PUT into it, the extension fallback is what actually decides, which
> is why the fallback runs on a generic answer and not only on a missing one.

## The seam, in three functions

    find_references(body)                        -> [ (span, form, path) ]
    plan(references, facts, limits, extra_files) -> Plan | Refusal
    render_for_mail(plan, fetch)                 -> (body, attachments, inline)

    facts       -> { path: (exists, size, content_type, expires_at) },   gathered by the host
    limits      -> (max_parts, max_total_bytes)
    extra_files -> the paths passed in `files=[…]`, or empty
    fetch(path) -> bytes

    Plan(pieces, parts)          pieces: text and part-markers in order; parts: paths to carry
    Refusal(reference, path, reason, where, fix)

**`find_references` and `plan` together are the whole design; `render_for_mail` is a join.** The
first is the grammar. The second is every rule that can put a hole in somebody's inbox — dedupe,
inline-versus-attach precedence, the caps and how `extra_files` counts toward them, the non-image
fallback, the expiry refusal, and the five fields a refusal carries. Both are pure: data in, data
out, no store, no network, no mail. The third fetches the bytes the plan names and builds MIME,
and it is the only part that knows it is making a mail.

**What the split is for, said without overclaiming.** It is not surface-neutrality. `plan` takes
`extra_files`, which exists only because console `send_email` has a `files?` argument, and
`limits`, which is a message size cap — its whole body is mail policy, and a webhook would inherit
rules that are inert there. The genuinely reusable piece is `find_references`, and that is all.

The split earns its keep for two other reasons. First, `plan` is pure, so every rule that can put
a hole in an inbox is testable with a dictionary and a table instead of a mail server. Second,
that is what lets the conformance fixture bind the rules rather than the tokenizer — an earlier
draft shared only `find_references`, which is a regex, and left the caps, the precedence, the
fallback and the expiry refusal copy-pasted per host.

Four things this shape exists to make possible, each of which an earlier draft claimed and could
not do:

- **`facts` carries `expires_at`,** so the expiring-link rule is implementable. Without it that
  rule is a wish. See the warning below.
- **`facts` carries `size`,** so the caps are decided before a single byte is fetched, and a
  `{{link:}}` never pulls a 41.3 MB video just to prove it exists.
- **`limits` and `extra_files` are arguments to `plan`,** so the caps have somewhere to live and
  `files=[…]` is counted in the same total instead of being counted by nobody.
- **`plan` is where a refusal is decided,** not the renderer, so every rule that can stop a send
  is in the pure, fixture-pinned half.

The host gathers `facts` — one stat per distinct path — because the four-step search a
`manage_file` read does (run, then loop, then the library, then customizations) is the caller's
business and differs between the two mail calls. `plan` never touches a store, so its whole test
suite is a dictionary and a table.

## The conformance fixture

One checked-in file of cases, each `(body, facts, limits, extra_files) -> (plan | refusal)`. Both
hosts run it in their own suites. Two implementations that pass the same fixture are the same
grammar and the same policy; one that stops passing it fails its own build rather than surfacing
in somebody's inbox. It is written whether or not the two services end up sharing a library,
because it is what makes "one grammar" checkable instead of asserted.

**A second fixture pins the join**, because `render_for_mail` is the piece written twice if the
hosts share nothing, and it owns the `gone or resized between stat and fetch` refusal. Its cases
are `(plan, a fetch stub) -> (body, parts)`, and the stub is what makes "the file changed" a case
you can write rather than a race you hope to see.

**Where `render_for_mail` sits.** It emits **markdown**, not HTML: an ordinary markdown image
whose target is the part's `cid:` URL. The existing markdown-to-branded-HTML renderer runs after
it, unchanged, exactly as it does for a body with no references in it. Nothing new emits HTML, so
A3 holds.

> **The one capability this design assumes and did not read.** `expires_at` on `stat`. The store
> holds retention — `manage_file` takes `expire_in` on writes and has `set_expiry` — but nothing
> this session could read says a stat exposes it. **Build step 1 starts by checking.** If it does
> not, exposing it is the first change, and until it exists the expiring-link rule cannot ship and
> must not be claimed. It is written here rather than discovered by the person implementing it.

## The details a parser needs

- **Matching is lazy and single-line.** A `{{` pairs with the first `}}` after it on the same
  line. `{{{{x}}}}` therefore has body `{{x`, which is not a path, so it is refused.
- **A `{{` with no `}}` on its line, outside code, is refused,** naming the line.
- **Code spans of any length are protected** — one backtick, two, three — by the ordinary markdown
  rule that N backticks open and N close. Fenced blocks and four-space indented blocks likewise.
  An unclosed fence makes the rest of the body code.
- **The rewritten body is not a string with markers in it.** `plan` returns `pieces` — runs of
  text and part-markers, in order — so no surface ever parses a body that a previous stage wrote.
  `render_for_mail` joins them with `cid:`; another surface joins them its own way. An earlier
  draft returned a body containing `![name](inline:{n})`, which was the same defect `cid:` was
  disqualified for, one rename away.
- **`{{inline:}}` on something that is not an image** is refused, not demoted. See *Is it an image?*
- **A path in both `files=[…]` and `{{path}}`** is one part. The `{{path}}` token still leaves its
  name in the body; a `files=[…]` entry leaves nothing, because it was never in the body. So
  `files=[…]` is the older, positionless way to attach, and it is not the same thing as `{{path}}`
  — it attaches without saying where.
- **An id in front of a path** is what A1 refuses, and concretely it is the account's own uuid as
  the first segment — `d1eba590-5001-708c-b0ce-866313672025/SoftwareEngineer_JohnCarmack/…`. That
  is what the storage key looks like and what a path must never look like. The test is a first
  segment matching a uuid.
- **`span` is a codepoint offset**, not bytes and not UTF-16 units, and the conformance fixture
  says so. Two hosts in two languages agreeing on this is the difference between the fixture
  meaning something and it passing on one host for any body containing an accent.
- **Only `body` is scanned.** Never `subject`. A subject line cannot carry a picture, and a
  subject that refused a send because of a brace would be a surprise.
- **A reference inside a markdown link or image target** — `![c]({{inline:c.png}})` — is refused,
  reason `nested in markdown`. The substitution would produce markdown inside markdown, and the
  writer meant `{{inline:c.png}}` on its own.
- **A path that names a folder** is refused, reason `is a folder`. `stat` says it exists; it has
  no bytes to carry and no page to open.
- **The expiring-link rule is `expires_at` is not null**, not a window. A file with any retention
  set is a file that will be gone; when it goes is not the point.

## Writing the link, when the name has spaces in it

The character set admits spaces, parentheses and brackets, so the output side has to say what it
does with them or `Q3 report.png` produces broken markdown:

- the URL is `https://studio.lamoom.com/` + the path **percent-encoded per segment**, and the
  target is wrapped in angle brackets — `[Q3 report.png](<https://studio.lamoom.com/2026/Q3%20report.png>)`;
- in the visible name, `[`, `]` and a backslash are backslash-escaped.

## What the caps are measured on

`limits.max_total_bytes` is a budget in **raw** bytes, and the host derives it from the mail
service's message limit before calling — divide by 1.37 for base64, leave room for headers.
`plan` never sees an encoded size, only `facts.size`, which is what keeps it pure and is why the
conversion belongs to the caller. Without this a 6.9MB file passes a 7MB cap and the assembled
message is over it.

## `files=[…]` and what it is not subject to

`extra_files` counts toward `max_parts` and, when the host knows their sizes, toward
`max_total_bytes`. It is **not** put through the reference refusals: a `files=[…]` path that is
missing or expiring behaves exactly as it does today. Anything else would break sends that work
now, and `files=[…]` is the old way in — the new rules apply to the new grammar.

## Existence is checked for all three forms

Including `{{link:}}`, which carries no bytes. A link to a path that does not exist is a link to
a page that will not open, and the whole point of refusing is that the mail is the review surface.

## The refusal reasons, in full

Every refusal carries five fields — `reference` (the token verbatim), `path`, `reason`, `where`
(which call on which host), `fix` — and `reason` is one of exactly these:

    no file at that path
    the bytes were never written        (stat says size 0)
    not a path                          (empty, a bad segment, a stray brace body)
    no closing brace on that line
    climbs out of the root              (a leading /, a "..", an id in front)
    is a folder
    not an image                        ({{inline:}} on something that is not one)
    nested in markdown
    the path expires                    (expires_at is set; copy it to the library, then link)
    too many parts (n of m)
    too large (n of m)
    gone or resized between stat and fetch

The last one is the window the two-pass design creates and must own, and it is named for exactly
what it can detect. `plan` decides from facts gathered by `stat`; `render_for_mail` fetches
afterwards. If the path is gone by then, or the bytes it returns are not `facts.size`, the fetch
refuses — **before** the message reaches the mail service, so nothing is sent. A rewrite that
lands on the same byte count is **not** detectable at this seam: there is no etag and no version
in `facts`, the store hands back a whole object so nothing tears, and the mail carries whichever
version won. That is the honest boundary. Adding an etag to `facts` would close it, and is not
worth a field until somebody has seen it happen.

## The limits

`limits` is `(max_parts, max_total_bytes)` and the design invents neither number. `send_email`
documents "max 10, 7MB"; whether the 7MB is per message or per file is confirmed against the live
service in build step 4, and until it is known the stricter per-message reading is used.
`run.email` documents no cap at all, so its values are read from the mail service the same way in
build step 5 rather than guessed here.

## What a refusal says

Nothing is sent, and **every** bad reference is reported, not the first — a body with three
mistakes in it should cost one round trip to fix, not three. The call returns a list of refusals,
each carrying the five fields and the full reason enum given above under *The refusal reasons*.

So the person at three in the morning reads which tokens, in which body, on which host, and why —
without the author, and without opening the message, because there is no message.
