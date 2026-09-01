# Failure modes, and what the person sees

Each row is a thing that will happen, what the caller gets, and what Kate gets. The rule behind
every row: nothing leaves half-sent, and nothing arrives looking complete when it is not.

| What happens | What the caller is told | What Kate gets |
|---|---|---|
| a referenced path does not exist | refused before anything is sent, naming the reference and the path in it | nothing. There is no mail to misread |
| the path climbs out of the caller's root | refused, the same refusal as every other read of such a path | nothing |
| more references in one body than the cap | refused, naming the count and the cap | nothing |
| the message would exceed what the mail service accepts | refused, naming the total size and which references make it up | nothing |
| the file exists as a name but the bytes were never PUT (`size 0`) | refused, saying the path is a name with no file behind it | nothing |
| `{{inline:}}` on something that is not an image | refused, reason `not an image`, fix: use `{{path}}` | nothing. It is not quietly demoted — the notice would go to an agent that is gone before she reads the mail |
| the send itself fails after the mail service accepted the message | reported as a send failure, explicitly not a reference failure, and NOT retried automatically | possibly one mail, possibly none |
| a `{{link:}}` to a path that expires | refused at send, saying to copy it to the library and link that | nothing. The dead link never leaves |
| a `{{link:}}` to a permanent path that somebody deletes later | nothing — no send-time check can see a future deletion | a dead link. This design narrows the silent dead link; it does not abolish it |
| a path gone or resized between `stat` and `fetch` | refused before the message reaches the mail service, reason `gone or resized between stat and fetch` | nothing |
| a path rewritten to exactly the same size between `stat` and `fetch` | nothing — undetectable without an etag, which `facts` does not carry | whichever version won. Named rather than denied |
| the mail service accepted the message but the call then failed | reported as a send failure, carrying the message id if the service returned one, and NOT retried | possibly one mail, and the message id says which |

Everything except the last row is caught before a mail exists, which is why refusing is cheap.
The send failure is the only one that cannot be undone, so it is the only one never retried on
the caller's behalf, and it carries the mail service's message id precisely so that "possibly one,
possibly none" can be answered.

**The link that expires used to be on this list as uncatchable, and the scheduled half of it is not.** A run's files die
30 days after their last write, so a `{{link:}}` to one is a mail that reads as complete and is not
— weeks later, silently, which is the failure this whole design exists to narrow. Retention is
knowable at send time, so a scheduled death is refused then. A file somebody deletes by hand next
month is not knowable at send time and is not caught; that row is above, and it stays there rather
than being written out of the table.

Every refusal carries five fields — the token verbatim, the path inside it, the reason, `where`
(which call, on which host, refused) and the fix — so the person at three in the morning does not
have to guess which of the two services they are looking at. A body with three mistakes returns
three refusals, not the first one: fixing a body should cost one round trip.

Four states that were unnamed and now are:

- **`{{` with no closing `}}` on the same line, outside code** — refused, naming the line. An
  unclosed brace is the beginning of a reference somebody meant.
- **A file changed or deleted between `stat` and `fetch`** — there *is* a window, and it is
  deliberate: facts are gathered without pulling bytes so that a `{{link:}}` never downloads a
  41.3 MB video to prove it exists. A path gone by fetch time, or one whose bytes are not
  `facts.size`, is refused before the message reaches the mail service. A rewrite that lands on
  exactly the same size is not detectable without an etag and is carried. An earlier draft claimed
  one pass and no window; that was wrong, and so would be claiming the window is fully closed.
- **The same path twice** — one part, referenced twice. See grammar.md.
- **The same path in `files=[…]` and as `{{path}}`** — one part. `files=[…]` is the older,
  positionless way to attach: it puts bytes on the message and nothing in the body. It is not the
  same thing as `{{path}}`, and saying it "means the same" was wrong.

# Read-through migration

There is nothing to migrate. The design stores no row, changes no key and rewrites no file. Every
body written before this change contains no `{{`, so a server carrying the resolver treats every
old body exactly as it treats it today — the migration is a no-op by construction, which is the
reason to prefer a grammar that is inert in old text.

The order, however, is not optional:

1. The resolver ships on the server. Nothing changes for anyone, because nobody writes braces yet.
2. One mail is sent through the live product with all three forms, and somebody opens it.
3. Only then does the skill teach the grammar, in both bundles.

Reverse steps 1 and 3 and every client starts writing tokens that print literally in Kate's inbox
— which is not a prediction, it is what the two probe mails in attacks.md did.
