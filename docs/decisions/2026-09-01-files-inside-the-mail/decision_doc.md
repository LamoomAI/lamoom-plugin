# Files inside the mail: the `{{...}}` grammar

**Run** 2026/09/01/204815849 · **Role** SoftwareEngineer_JohnCarmack · **Loop**
well-architected-design · **Date** 2026-09-01

## The decision, in one paragraph

A finished run writes its mail body with the files in it. `{{inline:path}}` shows the picture in
the message, `{{path}}` hangs the file off it, `{{link:path}}` is a link into
studio.lamoom.com. The braces are resolved **on the server**, in one resolver that both mail calls
call before they build a message. `run.email` is on mcp.lamoom.com and `send_email` is on
console.lamoom.com — two services, so this is one design implemented twice, or once in a shared
library if those services already share one. What it is not is one grammar implemented
differently in every client, which is what leaving it to the caller means. A path is written exactly as it is written everywhere else in Lamoom — from the
person's root, no id in front — and a path that does not resolve **refuses the send and names
the reference**, so no mail ever goes out with a hole in it.

**Runner-up: the client expands the braces before it calls.** Same grammar, ships today, no
server change. Rejected because `run.email(run_id, subject, body)` has no `files` argument, so
through the server the request actually names it could attach nothing at all — and because a rule
that lives only in a prompt sends Kate a mail with `{{...}}` printed in it the first time a
session forgets. It is **not a stage one**: teaching the grammar before the server resolves it is
the one move that is worse than doing nothing.

## What was asked

[requirements.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/requirements.md) — R1 to R9, quoted and dated.
[axioms.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/axioms.md) — A1 to A9, the invariants no option may repeal.
[classes.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/classes.md) — every class touched, tagged VERIFIED / INFERRED / UNVERIFIED.

## The options

| | |
|---|---|
| [1 — the server expands the body](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/1_server_expands_the_body.md) | **chosen** |
| [2 — the client expands before it sends](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/2_client_expands_before_it_sends.md) | runner-up |
| [3 — do nothing new](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/3_do_nothing_new.md) | the baseline, scored honestly |
| [4 — a public url per file](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/4_public_share_url_per_file.md) | rejected on privacy |

[comparison.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/comparison.md) — seven lenses, scored by the minimum, and why a tie at 2 is
not a tie. [whys.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/whys.md) — five whys under each boundary.
[pricing.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/pricing.md) — the numbers and the command that produced them.

## The grammar

| Written in the body | What the body becomes | What the message carries | When to use it |
|---|---|---|---|
| `{{inline:path}}` | an image piece naming part `n` | the bytes as part `n` | a picture she should see without doing anything |
| `{{path}}` | `name`, as plain text | the bytes as an attachment | a document she will open |
| `{{link:path}}` | `[name](https://studio.lamoom.com/path)` | nothing | anything big, and anything that keeps changing |

`name` is the last segment of the path. Three forms, no fourth. The full parseable rule — what is
and is not a path, whitespace, code spans, the counts, duplicates — is in
[grammar.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/grammar.md), and it is the file to write the parser from.

Three rules that are not obvious and are the reason this document exists:

- **`{{path}}` leaves the file's name behind rather than deleting itself**, so the sentence names
  the attachment. Deleting it would rebuild the defect that killed the do-nothing option: a body
  saying "the chart is attached" beside a list saying `chart.png`, with nothing joining them.
- **Attach and inline freeze; link follows.** `{{path}}` and `{{inline:path}}` copy the bytes at
  send time, so the mail holds what the file was. `{{link:path}}` points at the live path, so it
  shows what the file becomes.
- **A `{{link:}}` to a path that expires is refused at send.** A run's own files die 30 days after
  their last write, so such a link is a mail that reads as complete and quietly is not, weeks
  later. The refusal says to copy it to the library first, then link it — which is also the answer
  for a result too big to attach: a run's close already writes what it made into the library, so
  the permanent copy exists before the mail does.
  **This rule depends on one capability nobody here has read: `stat` returning `expires_at`.** The
  store holds retention — `manage_file` takes `expire_in` and has `set_expiry` — but that it is
  visible at stat time is assumed, not verified. Build step 1 checks it first; if it is not
  exposed, exposing it is the first change, and until then this rule cannot ship and must not be
  claimed.

Measured, and the reason `link` is not the polite third option: one page of Kate's library holds
11 files over 7MB and 14 folders with more than ten files, largest 41.3 MB
(`python3 measure_library.py`, in pricing.md). An option that only attaches cannot deliver a
video result at all.

## Schema

**No pk, no sk, no row, no index.** The literal schema change is the empty string. Every
reference is a read of a path that already exists under the caller's root; nothing is written and
nothing is remembered. This is the whole answer to A6, and it is what makes the migration a
no-op.

## Classes and the seam

| Class | Change | Its seam |
|---|---|---|
| `find_references(body)` | **new** | pure. Body in, `[(span, form, path)]` out. No store, no bytes, no mail. This is the grammar, and it is the piece another surface reuses |
| `plan(references, facts, limits, extra_files)` | **new** | pure, and this is where the design lives: dedupe, inline-versus-attach precedence, the caps and how `files=[…]` counts toward them, the non-image fallback, the expiry refusal. Returns `Plan(pieces, parts, notes)` or `Refusal(reference, path, reason, where, fix)`. `facts` is one stat per path — existence, size, content type, expiry — gathered by the host without pulling bytes |
| `render_for_mail(plan, fetch)` | **new** | the join. Fetches the bytes the plan names, builds the MIME, mints the `cid`. The only part that knows it is making a mail |
| the mail builder | reads those three instead of `body` + `files` | turns attachments and inline parts into MIME. The only place `cid:` exists |
| `run.email(run_id, subject, body)` | calls the resolver first | signature unchanged |
| `send_email(subject, body, workflow_id?, files?)` | calls the resolver first, passing `files=[…]` in as `extra_files` | `files=[…]` keeps working and keeps counting toward the same caps. It is not the same as `{{path}}`: it attaches without saying where |
| the file store | unchanged, read only | already answers "does this path exist, what type, what bytes" |

**Why three functions and not one.** The reusable thing is the grammar, not the rendering. A future
surface — a Slack post, a webhook, a preview in the studio — calls `find_references` **and
`plan`** and writes only its own renderer. That matters: `plan` is where the caps, the dedupe, the
inline-versus-attach precedence, the non-image fallback, the expiry refusal and the five refusal
fields live, and an earlier draft shared only the tokenizer, which left every rule that can put a
hole in an inbox copy-pasted per host. `plan` returns pieces — text and part-markers in order —
not a body string, so no surface ever re-parses what a previous stage wrote; an earlier draft
returned a body containing `inline:{n}`, which is the same defect `cid:` was disqualified for with
a different name on it.

**Why facts before bytes.** The expiring-link rule, the caps and the non-image fallback all need
facts about a file — expiry, size, content type — and they must be known *before* any bytes move,
or a `{{link:}}` to a 41.3 MB video downloads it to prove it exists. So the host stats each
distinct path, `plan` decides from those facts alone, and `fetch` runs only for what became a
part. That is two passes, and the window between them is real: a path changed or deleted in
between is caught by the fetch, before the message reaches the mail service, and refused like any
other. The window is named in failure_modes.md rather than denied.

**The second implementation arrives on day one.** `run.email` and `send_email` are on two
different hosts. If they already share a library, this is one file. If they do not, copy-paste
plus copied tests is not an invariant — copies drift and no test on one host can see the other —
so the mechanism is a **conformance fixture**: one checked-in file of
`(body, facts, limits, extra_files) -> (plan | refusal)` cases that both hosts run in their own
suites. It covers `find_references` and `plan` — the grammar and every rule — because a fixture
that covered only the tokenizer would bind the half that cannot hurt anybody. Two implementations
that pass it are the same grammar and the same policy; one that stops passing it fails its own
build rather than surfacing in an inbox. Whether the two services share a library or copy the
file is decided on opening the repository; the fixture is written either way.

Fenced code blocks are skipped, so the grammar can be explained inside a mail that has it. That
rule was caught by writing this document.

[grammar.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/grammar.md) — the parseable rule, written from the questions a fresh implementer
asked of the first draft.
[attacks.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/attacks.md) — the falsifier and every attack.
[failure_modes.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/failure_modes.md) — what each failure says, and the migration order.

## Implementation plan, in build order

0. **Open the Lamoom console repository.** It holds `backend/mcp/`, the mail code and the skill
   source, and it is not among the repositories this session could reach — `list_repos` returned
   32 and none of them is it. Everything below happens in there, in whatever language and test
   runner that repository already uses, beside the code that today turns `files=[…]` into
   attachments. This is step zero because it is the one thing that blocks step one, and naming it
   is cheaper than a fresh session rediscovering it.
1. **Check that `stat` can return `expires_at`,** and expose it if it cannot. The expiring-link
   rule is unbuildable without it, and everything below assumes it.
2. **`find_references`, alone, with the conformance fixture.** Pure: a body in, spans out, no
   network in the tests. Write it from [grammar.md](https://studio.lamoom.com/SoftwareEngineer_JohnCarmack/uploaded-files/2026/09/01/grammar.md).
3. **`plan`, against a dictionary.** `facts`, `limits` and `extra_files` are handed in, so there
   is nothing to mock and no network. This is where every rule above is enforced, where every test
   below lives, and what the conformance fixture pins. `render_for_mail` comes with step 4 — it is
   a join, and it is the only piece written twice if the two hosts share nothing.
4. **Wire it into `send_email`.** The console path first, because it already turns `files=[…]`
   into attachments, so only the body pass is new. Confirm here whether the documented
   "max 10, 7MB" is per message or per file; until it is known the design takes the stricter
   reading.
5. **Wire it into `run.email`.** The call the request names. Nothing else about it changes.
6. **Send one real mail through the live product** with all three forms, and open it. Not a test —
   an eye on a message.
7. **Then, and only then, the skill.** `plugins/claude/skills/lamoom/SKILL.md` and
   `plugins/codex/skills/lamoom/SKILL.md` in LamoomAI/lamoom-plugin, which are byte-identical, and
   whose source of truth is `backend/mcp/skills/lamoom/SKILL.md` in the console. The delivery line
   there today reads `deliver  send_email the result, the FILE ATTACHED, never retyped into the
   body`; it is replaced — not added to — by the three forms and the rules above.

There is no store step, no REST step and no SPA step in this plan, because nothing is stored and
no screen changes. Steps 2 to 6 are the deploy, and step 7 is a different repository on a later
day.

## The tests that prove each axiom

| Axiom | The test |
|---|---|
| A1 path from the root, no id | a body with an id in front of a path is refused, and the refusal names that reference |
| A2 mail goes to the account only | no test — there is no recipient argument to get wrong |
| A3 body is markdown | a resolved `{{link:}}` is markdown `[name](url)`, and the resolver emits no HTML |
| A4 ten files, seven megabytes | eleven `{{path}}` references refuse, naming the count; a body whose attachments exceed the cap refuses, naming the size |
| A5 the lambda is dumb storage, the agent thinks | the resolver's test suite runs against a dictionary, with no writer and no network. The three things it decides — image or not, the name, refuse or not — are each decided from bytes the caller does not hold, and whys.md §2 argues that against the real axiom rather than a weaker restatement of it |
| A6 no row, no index | the diff touches no table definition. Falsified by any migration file appearing in it |
| A7 refuse, never a hole | a body with one bad reference among three good ones sends nothing, and the refusal names the token, the path, the reason, `where` (which call on which host refused) and the fix |
| A8 one path grammar | the exact string returned by a `files` listing, pasted into a body, resolves |
| A9 nothing unexplained | a fourth form, e.g. `{{cid:path}}`, is refused rather than guessed at |

| grammar is parseable | `{{ inline:a/b.png }}` and `{{inline:a/b.png}}` resolve the same; `{{2026-09-01: x.md}}` refuses as not-a-path; `{{` with no `}}` on the line refuses; the same path twice makes one part |
| the link that expires | a `{{link:}}` to a path with a 30-day retention refuses at send, saying to attach it or copy it first |

And the two behaviours that are the point of the whole thing:

- a body with all three forms produces a message with one inline part, one attachment and one
  anchor to `https://studio.lamoom.com/` — asserted on the built message, not on the return value;
- a body containing `{{link:path}}` inside a fenced code block sends with those characters intact.

## The falsifier

Send one mail through the live product with all three forms in the body, and open it. If the
picture is showing, the file is attached and the link opens the studio, it is done. If any brace
survives into the message, it is not — whatever the tests say.

## The three things this document assumes and could not check

Each is checked by opening something, not by reasoning, and each is named here rather than left
for the person implementing it to hit.

0. **That a run's result reaches the permanent library.** The fix for both a file too big to
   attach and a link that would expire is "copy it to the library, then link that". `manage_file`
   documents `copy` with `to_scope`, and the destination's retention wins — so the call exists —
   but nothing read here says a run's close does it by default. Until it does, the copy is a step
   the writer takes, not something the system guarantees.
1. **That `stat` exposes `expires_at`.** If it does not, the expiring-link rule cannot ship until
   it is exposed. Build step 1.
2. **That nothing resolves `{{...}}` today.** Two probe mails were sent through the live
   `send_email`, one of them referencing a path that certainly does not exist, and both were
   accepted without complaint and reported no attachment — which is strong, but the eye-check is
   whether the first probe arrived in the inbox with braces printed in it. If it arrived with a
   picture instead, this document's central finding is wrong and the whole plan changes.
