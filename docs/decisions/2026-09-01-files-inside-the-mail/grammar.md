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

From the content type the store holds for that path. If the store has none, from the last
segment's extension: `.png .jpg .jpeg .gif .webp`. If neither says image, the file is **attached
instead**, and the caller is told it was attached rather than placed. This is not a judgement the
caller could have made better — the caller does not hold the bytes.

## The seam, in three functions

    find_references(body)                        -> [ (span, form, path) ]
    plan(references, facts, limits, extra_files) -> Plan | Refusal
    render_for_mail(plan, fetch)                 -> (body, attachments, inline, notes)

    facts       -> { path: (exists, size, content_type, expires_at) },   gathered by the host
    limits      -> (max_parts, max_total_bytes)
    extra_files -> the paths passed in `files=[…]`, or empty
    fetch(path) -> bytes

    Plan(pieces, parts, notes)   pieces: text and part-markers in order; parts: paths to carry
    Refusal(reference, path, reason, where, fix)

**`find_references` and `plan` together are the whole design; `render_for_mail` is a join.** The
first is the grammar. The second is every rule that can put a hole in somebody's inbox — dedupe,
inline-versus-attach precedence, the caps and how `extra_files` counts toward them, the non-image
fallback, the expiry refusal, and the five fields a refusal carries. Both are pure: data in, data
out, no store, no network, no mail. The third fetches the bytes the plan names and builds MIME,
and it is the only part that knows it is making a mail.

That split is the point. A second surface — a Slack post, a webhook, a studio preview — reuses
`find_references` **and `plan`**, and writes only its own renderer. An earlier draft put the
policy inside the mail renderer and shared only the tokenizer; then the reusable piece was a
regex and every rule that matters was copy-pasted per host. The conformance fixture below covers
`find_references` and `plan`, which is why it is a mechanism rather than a gesture.

Four things this shape exists to make possible, each of which an earlier draft claimed and could
not do:

- **`facts` carries `expires_at`,** so the expiring-link rule is implementable. Without it that
  rule is a wish. See the warning below.
- **`facts` carries `size`,** so the caps are decided before a single byte is fetched, and a
  `{{link:}}` never pulls a 41.3 MB video just to prove it exists.
- **`limits` and `extra_files` are arguments to `plan`,** so the caps have somewhere to live and
  `files=[…]` is counted in the same total instead of being counted by nobody.
- **`notes` comes out of `plan`,** so "this was attached instead of placed" has a channel and is
  decided in the shared, tested half rather than per host.

The host gathers `facts` — one stat per distinct path — because the four-step search a
`manage_file` read does (run, then loop, then the library, then customizations) is the caller's
business and differs between the two mail calls. `plan` never touches a store, so its whole test
suite is a dictionary and a table.

## The conformance fixture

One checked-in file of cases, each `(body, facts, limits, extra_files) -> (plan | refusal)`. Both
hosts run it in their own suites. Two implementations that pass the same fixture are the same
grammar and the same policy; one that stops passing it fails its own build rather than surfacing
in somebody's inbox. It covers `find_references` and `plan` — everything except the join — and it
is written whether or not the two services end up sharing a library, because it is what makes
"one grammar" checkable instead of asserted.

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
- **The non-image fallback** puts `name` in the body — exactly what `{{path}}` does — and adds a
  note saying it was attached rather than placed.
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

## The refusal reasons, in full

Every refusal carries five fields — `reference` (the token verbatim), `path`, `reason`, `where`
(which call on which host), `fix` — and `reason` is one of exactly these:

    no file at that path
    the bytes were never written        (stat says size 0)
    not a path                          (empty, a bad segment, a stray brace body)
    no closing brace on that line
    climbs out of the root              (a leading /, a "..", an id in front)
    is a folder
    nested in markdown
    the path expires                    (expires_at is set; copy it to the library, then link)
    too many parts (n of m)
    too large (n of m)
    changed between stat and fetch

The last one is the window the two-pass design creates and must own: `plan` decides from facts
gathered by `stat`, and `render_for_mail` fetches afterwards. If a path is gone, truncated or
rewritten in between, the fetch is the one that notices — and it notices **before** the message
is handed to the mail service, so it is still a refusal and still nothing sent. An earlier draft
claimed there was no window because count and read were one pass; the two-pass shape is
deliberate, so the window is real and named instead.

## The limits

`limits` is `(max_parts, max_total_bytes)` and the design invents neither number. `send_email`
documents "max 10, 7MB"; whether the 7MB is per message or per file is confirmed against the live
service in build step 4, and until it is known the stricter per-message reading is used.
`run.email` documents no cap at all, so its values are read from the mail service the same way in
build step 5 rather than guessed here.

## What a refusal says

Nothing is sent. The error carries three things and the call that fixes it:

    reference   the exact token text, braces included
    path        the path inside it
    reason      no file at that path | the bytes were never written | not a path |
                too many parts (n of m) | too large (n of m)

So the person at three in the morning reads which token, in which body, and why — without the
author, and without opening the message, because there is no message.
