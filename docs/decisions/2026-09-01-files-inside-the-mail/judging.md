# The judging

Six judges, one fresh session each, in parallel, each handed only its own criteria and the
artifact. None was told what to conclude and none saw another's verdict. The criteria were
reconstructed from the judge names, because the criteria files in the procedure's folder are not
readable from this session.

## Round 1 — minimum 2

| Judge | Score | The sentence that lost the point |
|---|---|---|
| architecture-reviewer | 4 | "The braces are resolved **on the server**, in the one function that already turns a body into a mail, so both `run.email` and `send_email` get the same grammar from one implementation." (decision_doc.md) |
| abstraction-owner | 3 | "The resolver returns three things rather than a finished HTML string on purpose … `cid:` means nothing there, and a string would force that surface to parse the braces itself." (decision_doc.md) |
| cost-and-pricing-owner | 3 | "The cost is not the money, it is the N places a send can now fail before a mail exists." (pricing.md) |
| five-whys-auditor | **2** | "Because it stores nothing and decides nothing." (whys.md) |
| implementer | 3 | "A path that climbs out of it — `..`, a leading `/`, another user's root, an id in front — is refused by the rule that already exists …" (attacks.md) |
| worst-case-operator | 3 | "\| a `{{link:}}` to a run-scope file, opened 30 days later \| nothing at the time — this one cannot be caught at send \| a dead link. Prevented by the rule, not by the code \|" (failure_modes.md) |

**The lowest, and what it actually said.** The five-whys-auditor caught the design escaping its own
axiom. A5 says the lambda is dumb storage and the agent thinks; the chain under "why the server
resolves it" ended at *"Because it stores nothing and decides nothing"* — and that is false, since
the resolver decides whether a file is an image, what name to show, and whether to refuse. The
decision document had then quietly restated A5 as the weaker "the lambda stores nothing", which is
a test the wrong design also passes. It also found `{{path}}` deleting its own token with no why
under it, rebuilding the exact defect used to kill the do-nothing option.

## What each verdict changed

| Judge | The change it forced |
|---|---|
| five-whys-auditor | A5 answered head-on rather than weakened: this is the one place a decision is knowingly put on the server, and the argument is that none of the three decisions is one the caller could make better, because the caller does not hold the bytes. `{{path}}` now leaves the file's name behind, with its own chain of whys. classes.md's closing line, which said the unreachable repository "picks the option", now says it decides the order and not the design |
| worst-case-operator | The 30-day dead link stopped being a rule in a prompt and became a refusal at send: the store knows a path's retention, so an expiring `{{link:}}` is refused now. Three unnamed states named: an unclosed `{{`, a file deleted between counting and reading (one pass, so no window), the same path referenced twice. The send failure now carries the mail service's message id |
| implementer | grammar.md, written from that judge's thirteen questions: the path character set, prefix matching by exact word rather than colon-splitting, whitespace, code spans, what counts toward the caps, duplicates, how "is it an image" is decided, and the shape of a refusal. The resolver now takes a read function rather than a root string, so the search chain stays with the caller. A step 0 was added naming the repository that must be opened first |
| abstraction-owner | The rewritten body carries `![name](inline:{n})`, not `cid:`, so the return type stops leaking MIME into every future surface and "`cid:` exists in exactly one place" becomes true. The second implementation is named as arriving on day one across two hosts, with the shared test suite as what keeps them equal |
| cost-and-pricing-owner | The extra round trips are priced — under a millionth of a dollar each — so the Cost lens is rescored as a tie at 5 and the round trips are counted under Operability where they actually hurt. N is labelled an assumption. The 100x line gets a denominator. attacks.md's unmeasured "300MB" becomes 20 MB, from the measured 209KB average |
| architecture-reviewer | "One function" replaced by the truth: two services, one design, implemented twice or shared, and never one grammar reimplemented per client. The seam's description made consistent — paths and content types, never MIME |

## Round 2 — minimum 3

Same six criteria, six fresh sessions, told the bar was raised and that a 5 must be earned.

| Judge | Score | The sentence that lost the point |
|---|---|---|
| architecture-reviewer | 4 | "The store knows a path's retention, so this is refused now and the refusal says to attach it or copy it to the library first — a mechanism, not a rule somebody has to remember." (decision_doc.md) |
| abstraction-owner | 3 | "If they do not, it is one file copied verbatim into both, and the test suite is copied with it…" (decision_doc.md) |
| cost-and-pricing-owner | 3 | "Nothing here scales with anything but the number of mails, and the number of mails is the number of finished runs — the number Lamoom charges for anyway, so the cost line grows only where the revenue line does." (pricing.md) |
| five-whys-auditor | 3 | "A5 exists to keep judgement — what to research, what to write, what is good — off the lambda, not to keep arithmetic off it." (whys.md) |
| implementer | 3 | "`read` is a function from a path to `(bytes, content_type)` or nothing." (grammar.md) |
| worst-case-operator | 3 | "The store knows a path's retention at send time, so the resolver refuses it then." (failure_modes.md) |

**Three judges converged on one defect, from three directions.** The seam was
`resolve(read, body)` where `read` returned `(bytes, content_type)` — and the design's own
headline rule, refusing a link to a file that expires, needs retention, which is not in that
tuple. The caps had no argument to live in. The "attached instead of placed" note had no channel
to travel down. The rule was unbuildable at the seam that documented it, and the implementer,
the operator and the architect each found it by a different route. That is what a panel is for.

**And the five-whys-auditor caught the axiom being bent to fit.** A5 says work the client can do
belongs to the client; whys.md had answered it by narrowing A5 to "judgement, not arithmetic",
which is the axiom rewritten to pass. The honest answer was available and is now written:
attaching bytes and building an inline part are things a client physically cannot do, so those
two forms are on the server *by* A5; `{{link:}}` could be client-side, so it is a **named
exception** with its price stated, and A5 is left as it was.

## What round 2 changed

- **The seam split in two.** `find_references(body)` is the grammar, pure and surface-neutral —
  the piece a Slack post or a studio preview would reuse. `resolve_for_mail(stat, fetch, body,
  limits, extra_files)` is allowed to know it is making a mail. The first draft's attempt at one
  surface-neutral function produced a body with `inline:{n}` in it that a second surface would
  have had to parse again — the same defect `cid:` was disqualified for.
- **`stat` replaced `read` as the primary call**, carrying existence, size, content type and
  expiry. That makes the expiring-link rule buildable, checks the caps before a byte is fetched,
  and stops a `{{link:}}` pulling a 41.3 MB video to prove it exists.
- **The assumption underneath it is now flagged rather than assumed.** Nothing this session could
  read says a stat exposes expiry. It is build step 1: check, and expose it if it is missing,
  because until it exists that rule cannot ship and must not be claimed.
- **Copy-paste stopped being the answer** to two hosts running one grammar. A conformance
  fixture — one checked-in file of body-in, references-out cases that both suites run — is a
  mechanism; copied tests are a hope.
- **The bill was computed rather than waved at.** One eighthundredth of a dollar per typical send,
  and the attachment byte term, which the earlier 100x paragraph silently dropped, turns out to be
  96% of the cost at scale. That is also the commercial argument for `{{link:}}`.
- **Twelve parser questions answered** in grammar.md: lazy single-line matching, code spans of any
  length, unclosed fences, `inline:{n}` indexing, the non-image fallback's body text, what an "id
  in front of a path" concretely is, and what `files=[…]` does and does not share with `{{path}}`.

## Round 3 — minimum 2, and it was my arithmetic

| Judge | Score | The sentence that lost the point |
|---|---|---|
| architecture-reviewer | 4 | "A design in which every result is attached costs roughly thirty times one in which the big ones are linked." (pricing.md) |
| implementer | 4 | "A leading `/` makes it not a path, and so does any character outside that set — a space inside, a second colon, an empty body." (grammar.md) |
| abstraction-owner | 3 | "so the mechanism is a **conformance fixture**: one checked-in file of `body in -> references out` cases that both hosts run in their own suites." (decision_doc.md) |
| five-whys-auditor | 3 | "`files=[...]` keeps working and means the same as `{{path}}`" (1_server_expands_the_body.md) |
| worst-case-operator | 3 | "the resolver reads each path once, and counts what it read. Count and read are one pass." (failure_modes.md) |
| cost-and-pricing-owner | **2** | "100 x 3 x 209KB = 61 GB/mo -> 2.0 GB/day x $0.12 = $0.24 / day" (pricing.md) |

**The lowest was a plain arithmetic error, and it inverted a conclusion.** 100 × 3 × 210KB is
61 megabytes a day, not 61 gigabytes a month. The byte term was inflated 33-fold, and the
paragraph built on it announced that bytes were 96% of the bill and that attaching everything
costs thirty times linking. Corrected: sends are the larger half, and the multiple is under two.
The section now carries the correction rather than a quiet edit, because a document that promises
"the command beside every number" and then gets a unit wrong should say so where it was wrong.

## What round 3 changed

- **The seam split again, and this time in the right place.** The abstraction-owner pointed out
  that sharing `find_references` shares a regex while every rule that can put a hole in an inbox
  stays copy-pasted. So the policy moved into its own pure function, `plan`, and the conformance
  fixture now pins `find_references` **and** `plan` — the caps, the dedupe, the precedence, the
  fallback, the expiry refusal, the refusal fields. `render_for_mail` is what is left, and it is
  a join.
- **`plan` returns pieces, not a body.** The `inline:{n}` marker inside a returned string was
  `cid:` with a different name on it, and a second surface would still have had to parse it.
- **The window I denied is real and is now named.** Facts are gathered before bytes on purpose, so
  there is a gap between `stat` and `fetch`; a file changed in it is caught by the fetch, before
  the message reaches the mail service, with its own refusal reason.
- **The silent dead link is narrowed, not abolished.** A scheduled expiry is knowable at send
  time and refused. A file somebody deletes by hand next month is not, and that row stays in the
  table instead of being written out of it.
- **The path character set widened.** `[A-Za-z0-9._-]` would have made `Q3 report.png`
  unreferenceable, and A8 says the exact string a listing returns must resolve. A grammar that
  cannot name a file the product created is broken on day one.
- **Nine more implementer questions answered:** the refusal reason enum in full, `span` as
  codepoint offsets, body-only and never subject, a reference nested in markdown, a path naming a
  folder, and where the two caps' real values come from rather than being invented.
- **A third unverified assumption admitted:** that a run's result reaches the permanent library.
  It is the escape hatch for both the 7MB ceiling and the expiring link, and nothing read here
  says it happens by default.

## Round 4 — minimum 3, and the panel stopping here

| Judge | Score | The sentence that lost the point |
|---|---|---|
| implementer | 4 | "A grammar that cannot name a file the product itself created is broken on day one, so the rule is the other way round…" (grammar.md) |
| architecture-reviewer | 4 | "S3 is read-after-write consistent, so the mail gets whichever write finished first, and nothing tears." (attacks.md) |
| worst-case-operator | 4 | "If neither says image, the file is **attached instead**, and the caller is told it was attached rather than placed." (grammar.md) |
| abstraction-owner | 3 | "A second surface — a Slack post, a webhook, a studio preview — reuses `find_references` **and `plan`**, and writes only its own renderer." (grammar.md) |
| cost-and-pricing-owner | 3 | "So on money the two options tie, and the comparison table scores them both 5 on Cost." (pricing.md) |
| five-whys-auditor | 3 | "…a run's close already writes what it made into the library, so the permanent copy exists before the mail does." (decision_doc.md) |

## What round 4 changed

- **The last silent failure was removed by reversing a rule.** `{{inline:}}` on a non-image was
  quietly demoted to an attachment with a note in the return — and the operator pointed out the
  note goes to an agent that stops existing minutes later, while the person reads the mail after
  that, which is the exact argument this design uses to *refuse* an expiring link rather than warn
  about it. It refuses now. That deleted the `notes` channel, which had no other user.
- **`content_type` was promoted to a checked assumption beside `expires_at`.** The image test
  turned on it, and it was as unread as the capability that got a build-step check and a "must not
  be claimed". A store that answers `application/octet-stream` for everything would have demoted
  every inline image in the product, silently.
- **The concurrency answer stopped contradicting the refusal.** `facts` has no etag, so a rewrite
  landing on the same byte count is undetectable at this seam: gone or resized is refused, same
  size is carried, and both documents now say that same sentence.
- **The surface-neutrality claim for `plan` was withdrawn.** `plan` takes `extra_files`, which
  exists only because one caller has a `files?` argument, and its body is mail policy. The
  genuinely reusable piece is `find_references`, and the split now justifies itself on purity and
  on what the fixture can pin, which is true, rather than on a second surface, which was not. A
  second fixture pins `render_for_mail`, the piece written twice if the hosts share nothing.
- **Both sides of the cost comparison are now counted the same way** — a stat per path and a fetch
  per part, against a `manage_file get` per reference — and the "100x" is labelled a round number
  rather than a multiple of a volume nobody measured.
- **A misparse was retracted.** "more pages True" came from reading the listing's `next` field as
  a pagination cursor; it is a prose instruction. Whether 1560 files is the whole library is
  simply unknown, and the counts no longer claim to be floors.
- **Seven more implementer questions answered:** percent-encoding and bracket-escaping for names
  with spaces, the cap measured in raw bytes with the encoding headroom taken by the caller,
  `files=[…]` counted but not subject to the new refusals, existence checked for `{{link:}}` too,
  all refusals returned rather than the first, and where `render_for_mail` sits relative to the
  markdown renderer.

## Where the panel was stopped, and what is still open

Four rounds, twenty-four cold readings, minimum 2 → 3 → 2 → 3. The remaining threes are not
defects in the design; they are three honest limits that more rounds would restate rather than
remove:

1. **`plan` is one caller's abstraction.** True, and now said so in the document instead of
   being argued away. It becomes false the day a second surface exists, and not before.
2. **The cost comparison rests on list prices and an unmeasured volume.** Every input is
   labelled. The totals are cents at any plausible volume, so no decision here turns on it.
3. **Three capabilities are assumed, not read** — `expires_at` and `content_type` on stat, and
   whether a run's close copies its result to the library. All three are the first thing build
   step 1 checks, and each is named where it is relied on.

A judge that keeps finding the same three named limits is confirming them, not catching them.
That is the point to stop.
