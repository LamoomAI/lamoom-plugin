# Five whys, under every boundary this design draws

There is no new key here — the chosen option stores nothing — so the whys go under the six places
a decision was actually made: the token, the boundary, the failure, the name left behind, the
name shown, and the link that would have died.

## 1. Why a token in the body rather than another argument on the call

1. **Why not `files=[...]`?** Because `run.email(run_id, subject, body)` does not have one, and
   the contract says an argument sent to a call that does not take it is refused.
2. **Why not add one to `run.email`?** It would attach, but it could never place. An attachment
   list has no position, so "the chart, then the two numbers under it" cannot be said.
3. **Why does position matter?** Because R2 is "to allow user to review online results". Review
   is reading the result, and a result whose picture is detached from the sentence about it is
   a result she has to reassemble.
4. **Why does the body have to carry it, rather than a convention like "attachment 1 is first"?**
   Because a convention is a thing to remember, and the person writing the body is a fresh
   session that has never read this document.
5. **Why is a token the smallest thing that solves that?** Because it is where she already
   writes: she says what the file is in the sentence, and the reference sits in the sentence.

## 2. Why the server resolves it and not the agent

1. **Why not the agent, which is where thinking goes?** Because this is not thinking. It is a
   lookup of bytes the agent does not hold.
2. **Why does it matter who holds the bytes?** Because inline means an embedded part with a
   `cid`, and only the thing that builds the message can add one. The agent can only pass a URL.
3. **Why is a URL not enough?** A `download_url` from the store is presigned and expires. The
   mail is right today and a row of broken boxes next week — and the mail is the archive.
4. **Why not a URL that never expires?** That is option 4, and it means bytes readable without
   signing in. Rejected on A6 and on what Lamoom's runs actually hold.
5. **Does this violate A5 as A5 is actually written?** A5 says: work the client can do belongs
   to the client, and only what the client physically cannot do belongs on the server. Held to
   that line: attaching bytes and building an inline part are things the client physically
   cannot do — `run.email` has no `files` argument and no client can add a part to a message it
   does not build — so `{{path}}` and `{{inline:}}` are on the server **by A5, not despite it**.
   `{{link:}}` is different: it needs no bytes, and a client could expand it. Putting it on the
   server too is a deliberate exception to A5, and its price is one sentence: one grammar
   resolved in two places is two grammars within a month, and the second one drifts silently
   because it lives in a prompt. That is the whole argument. It is an exception, it is named as
   an exception, and A5 is not rewritten to make it disappear.

## 3. Why a missing reference refuses instead of degrading

1. **Why not just leave the token as text?** Kate would receive a mail with `{{...}}` printed
   in it and no way to tell whether the file was missing or the grammar was wrong.
2. **Why not silently drop it?** Worse: the mail reads as complete. She reviews a result with a
   piece missing and does not know a piece is missing.
3. **Why is that the worst outcome?** Because R2 makes the mail the review surface. A review
   surface that lies is not a smaller feature, it is a wrong one.
4. **Why refuse the whole send rather than send the rest?** A half-sent mail cannot be unsent,
   and the fix — write the path correctly and send again — costs one call.
5. **Why name the reference in the refusal?** So the pager at three in the morning reads which
   one broke without opening the body.

## 4. Why `{{path}}` leaves the file's name behind instead of deleting itself

1. **Why not just remove the token?** Because then the body says "the chart is attached" and the
   attachment list says `chart.png`, and nothing joins them.
2. **Why does that matter?** It is the exact defect that killed the do-nothing option. Rebuilding
   it inside the chosen one would be choosing the same failure with more code.
3. **Why the name rather than a link?** A link would take her out of the mail to fetch a file
   that is already in the mail.
4. **Why not leave the token itself?** Because braces in her inbox are the thing this whole
   design exists to prevent.
5. **Why does this settle it?** Because it also deletes a question — what happens to whitespace
   when a token was alone on its line — instead of answering it.

## 5. Why the name shown is the last segment of the path

1. **Why show a name at all?** A link with no text is a URL, and a URL from the person's root is
   long and unreadable in a mail.
2. **Why the last segment?** It is what a person calls the file: `chart.png`, `decision_doc.md`.
3. **Why not a title read out of the file?** It would work for markdown and not for a PNG, so
   the rule would have exceptions in it on day one.
4. **Why not let the writer name it?** That is a fourth form, and A9 asks who reads it and what
   it changes. She can already write her own text around the reference.
5. **Why does this settle it?** Because the answer is the same for all three forms, so there is
   one rule to remember and no branch to get wrong.

## 6. Why a `{{link:}}` to a file that expires is refused rather than sent

1. **Why refuse a link that works today?** Because run files die 30 days after their last write,
   and the mail is Kate's archive. The link works the week she gets it and is dead the month she
   goes back to it.
2. **Why is that worse than an ordinary broken link?** Because nobody is told. She opens a mail
   that reads as complete, taps, and gets nothing — and there is no run, no refusal and no error
   anywhere that says a thing went wrong.
3. **Why not warn instead of refusing?** A warning goes to the agent that sent the mail, which
   stops existing minutes later. The person who needs it reads the mail weeks after that.
4. **Why not attach it instead, quietly?** Because the file may be past the size a mail can carry
   — that is often exactly why it was linked — and a silent substitution makes the writer's
   sentence wrong.
5. **Why is copy-to-the-library the fix rather than a longer retention?** Because retention is a
   storage decision with its own costs and this is a delivery problem. The copy is one
   `manage_file copy` with `to_scope`, and the destination's retention wins. **Who makes that call
   is the writer of the mail**, prompted by the refusal — not the resolver, which reads and never
   writes, and not the run's close, which may or may not already do it (assumption 0 in the
   decision document).

**And where this rule stops.** It catches a *scheduled* death, because `expires_at` is knowable at
send time. It cannot catch a file someone deletes by hand next week — no send-time check can — so
this design narrows the silent dead link, it does not abolish it, and saying otherwise would be
the same overclaim this rule exists to correct.
