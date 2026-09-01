# Iteration 3 — the attacks, and what each one did to the design

## The falsifier, run first

**Does either mail call already resolve `{{...}}`?** Not read anywhere — measured. Two mails
sent through the console's `send_email` with nothing in `files`:

    send_email action=send subject="Probe: does {{...}} in a mail body resolve today?"
      body: {{inline:2026/08/04/cofounder-metrics/shots/catalog_mobile_annotated.png}}
            {{well-architected-design/about-the-user.md}}
            {{link:2026/08/14/pain-to-pitch/final.png}}
    -> {"sent": true, "to": "kate.yanchenka@gmail.com"}

    send_email action=send subject="Probe 2 of 2: a path that does not exist"
      body: {{link:this/path/does/not/exist_2026-09-01.md}}
    -> {"sent": true, "to": "kate.yanchenka@gmail.com"}

The second one is the decisive one: a server that resolved the braces would have to fail on a
path that does not exist, and it sent without complaint. Neither reply reported an attachment.
**So the grammar does not exist today and has to be built.** The one thing left to see with an
eye rather than a return value is whether probe 1 arrived with braces printed in it; if it did
not, this whole finding is wrong and the run should be told.

## Concurrent writers

A run rewrites `chart.png` while a mail that references it is being built. S3 is read-after-write
consistent, so the mail gets whichever write finished first, and nothing tears.

But the three forms behave differently and the difference must be said out loud rather than
discovered: **`{{path}}` and `{{inline:path}}` copy the bytes into the message, so they freeze
what the file was at send time. `{{link:path}}` points at the live path, so it shows whatever
the file is when she taps it.** That is not a bug in either — it is the reason to pick one. A
result she is reviewing wants the frozen copy; a document that keeps being updated wants the
live link. Written into the decision.

## Retry

Resolution is pure and reads only, so a send refused during resolution is safe to retry as many
times as you like. The send itself is not: once SES has the message, a retry is a second mail.
So the refusal has to say which side of that line it failed on, and "the send failed" must never
be reported the same way as "the reference failed". Two shapes, named in the failure modes.

## Rollout window

The dangerous order is the obvious one. If the skill teaches `{{...}}` before a server resolves
it, every client writes tokens that print literally — which is exactly what the two probes above
did, on purpose. So: **the server ships first and is a no-op (no existing body contains `{{`),
then the skill teaches the grammar.** Nothing needs a flag and nothing needs migrating, because
nothing is stored.

## Deletion, and the link that dies

Run files are scratch: `manage_file` says each one dies 30 days after its last write. So a
`{{link:path}}` to a run-scope file is a link that works this week and 404s next month, in a mail
that is Kate's archive. The rule that falls out: **link to permanent things, attach or inline
anything that lives in a run's scratch** — or copy it to the library first. This is the least
obvious rule in the whole design and it belongs in the skill, not in a comment.

## 100x, and the body with two hundred references

Cost is in pricing.md and is cents. The shape that actually breaks is one body with a hundred
references building a message too big to send: at the mean file size over one page of Kate's
library — 318.2 MB over 1560 files, so 210KB each (`python3 measure_library.py`, which prints
`average per file 210 KB`) — a hundred references is about 21 MB, well past what the mail will
take. That mean is a stand-in for what a mail would carry, not a measurement of it. The resolver refuses over the cap,
naming the count, rather than assembling 20 MB and letting the mail service reject it with
something nobody can read.

## Privacy

Every path resolves under the caller's own root, the same as every other read. A path that
climbs out of it — `..`, a leading `/`, another user's root, an id in front — is refused by the
rule that already exists ("a path with an id on it is refused"), not by a new rule invented here.
The mail goes only to the account's own address (A2). So no file becomes readable by anyone who
could not already read it. That is the whole privacy story, and it is short because the design
adds no reader.

## Attack on the abstraction: the day the second implementation arrives

`cid:` is a MIME idea. The moment a second surface wants the same grammar — a Slack post, a
webhook, a preview inside the studio — `cid:` means nothing there, and if the resolver returned a
finished HTML string, that surface would have to parse the braces itself. Two parsers, and they
drift within a month.

So the seam returns **three things, not a string**: the rewritten body, the files to attach, and
the files to place inline with the name each placeholder used. The mail builder turns those into
MIME. Another surface turns the same three into whatever it has. This is the one piece of the
design that exists for a caller that does not exist yet, and it costs one return type.

## The reference that is being shown, not used

This run's own delivery mail has to contain the text `{{link:path}}` to explain the grammar. If
the resolver reads inside fenced code blocks, that mail cannot be written. So the resolver skips
fenced code blocks, and that is where anyone documenting the grammar puts it. One rule, one
reader, a decision it changes: caught by writing this very document.
