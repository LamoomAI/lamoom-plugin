# A1..A9 — what no option may repeal

Each one with the why, because an invariant with no why is a preference someone will
overrule at three in the morning.

- **A1. A path is written from the person's root, with no id in front, and it is already an
  address.** `https://studio.lamoom.com/` + path opens the file. Why: the contract says it in
  those words, and "a path with an id on it is refused". An option that invents a second path
  grammar for the mail body breaks the one thing about paths that is true everywhere else.
- **A2. Mail goes only to the signed-in account's own address.** Why: `send_email` takes no
  recipient, by design. Nothing here is a way to mail a third party.
- **A3. The body is markdown and the server renders it into the branded HTML mail.** Why:
  "body is MARKDOWN, rendered as a branded Lamoom HTML email; write natural markdown, no HTML."
  So a `{{...}}` form must survive as markdown, or be replaced before the markdown is rendered.
- **A4. Ten files, seven megabytes.** Why: `send_email` says so. Every option must say what
  happens to the eleventh reference and to the file that is too big, and "it silently drops"
  is not an answer.
- **A5. The lambda is dumb storage; the agent does the thinking.** Why: key_role. Work the
  client can do — reading a body, finding a token, resolving a path it already holds — belongs
  to the client, and only what the client physically cannot do belongs on the server.
  *(The chosen design meets this for `{{path}}` and `{{inline:}}`, which a client physically
  cannot do, and takes a named exception for `{{link:}}`, which it could. whys.md §2.5 argues
  that exception and comparison.md scores it. This axiom is not restated anywhere to make it
  easier to pass.)*
- **A6. No GSI, no row kind only an agent reads, no binary in DynamoDB.** Why: key_role. This
  change stores nothing new; it references files that already exist.
- **A7. A reference that does not resolve stops the mail and names itself.** Why: R2 — Kate
  reads the mail to review the result. A mail that goes out with a hole in it is a result she
  reads as complete and is not, and she has no way to tell. The refusal names the reference and
  the call that fixes it, so the pager at three in the morning reads which one broke.
- **A8. The same string works in the body and in a `manage_file` read.** Why: she copies a path
  out of the data the server just handed her and pastes it into the body. Two grammars is the
  next bug, and it is a bug nobody reports because the mail still sends.
- **A9. Nothing goes in that cannot say who reads it and what it changes for them.** Why: RULE 1,
  R4. Named here so an option that adds a fourth form, a config flag or a new row is refused
  by this document rather than by a review three days later.
