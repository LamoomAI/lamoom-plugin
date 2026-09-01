# 01 — files inside the mail

# end: Kate opens the mail a finished run sent her and the result is already in it — the picture showing in the message, the document attached, the rest links she taps straight into studio.lamoom.com — and she never opened a terminal or pasted a path anywhere.

Walking back from that, each line being what has to be true one step before the line above it.

1. She reads the mail and everything is there. True only if the message that left the server
   carried an embedded image, a real attachment and anchors into the studio.
2. It carried those. True only if something between the mail call and the sender read the body,
   found every `{{...}}`, and turned each one into the right thing: `{{inline:path}}` into an
   embedded part with a `cid`, `{{path}}` into an attachment, `{{link:path}}` into a link to
   `https://studio.lamoom.com/` + path.
3. That something can turn a path into bytes and into a URL. True only if the path it is handed
   resolves against the person's root the way every other path in Lamoom does — so the same
   string the server hands back in `files` data works verbatim in a mail body, and a path with
   an id on it is refused there as it is everywhere.
4. Someone writes such a path. True only if the three forms are said in one place the writer
   already reads — the mail call's own prompt and the skill's delivery line — and not in a
   README.
5. A reference that cannot be resolved does not vanish quietly. True only if a missing path
   refuses the send and names the reference, rather than mailing a body with a broken box in it.
   Kate reads the mail to review the result; a mail that lies reads as complete.
6. Any of it can be written at all. True only if the shape is decided first: where the
   substitution lives, what `inline` means for something that is not an image, what happens past
   ten files and seven megabytes, and what the refusal says. **This needs nothing. The work
   starts here.**

So the order is: decide the shape and name the runner-up; build the resolver; wire it into the
two mail calls; send one real mail and open it; and only then teach the grammar in the skill.

## What this run did, and what it did not

It did step 6. The decision is in `docs/decisions/2026-09-01-files-inside-the-mail.md`, chosen
against three other options, attacked, and priced against a measurement of Kate's own library.

It did not touch `plugins/*/skills/lamoom/SKILL.md`, on purpose. Those two files are byte-identical
and are generated from `backend/mcp/skills/lamoom/SKILL.md` in the Lamoom console, which this
session cannot open. More importantly, the order matters: two probe mails sent through the live
`send_email` — one of them referencing a path that certainly does not exist — both sent without
complaint and reported no attachment, so **nothing resolves the braces today**. Teaching the
grammar in the skill before the server resolves it makes every client write tokens that print
literally in Kate's inbox. Server first, skill second.

## The falsifier

Send one mail through the live product with all three forms in the body, and open it. Picture
showing, file attached, link opening the studio: done. Any brace surviving into the message:
not done, whatever the tests say.
