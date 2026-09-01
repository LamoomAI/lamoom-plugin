# Iteration 2 — the decision, and what depth changed

## The Decision

**Chosen: option 1 — the server expands the body, in the one function that already builds the
mail.** `{{inline:path}}` becomes an embedded part with a `cid`. `{{path}}` becomes an
attachment and the token leaves the line. `{{link:path}}` becomes
`[name](https://studio.lamoom.com/path)`. A path is written exactly as it is everywhere else in
Lamoom, and a path that does not resolve refuses the send and names itself.

**Runner-up: option 2 — the client expands before it sends.** It is the runner-up because it is
the same grammar and it ships today; it is not the choice because through `run.email` — the call
the request actually names — it cannot attach anything at all, and because a rule that lives only
in a prompt sends Kate a mail with `{{...}}` printed in it the first time a session forgets.

Option 2 is the runner-up, **not a stage one**. Shipping the grammar into the skill before the
server resolves it is the one move that makes things worse than doing nothing: every client
starts writing tokens that print literally.

## What depth changed

- **The 7MB cap stopped being a footnote.** Measured on Kate's library: 11 files over 7MB, 14
  folders holding more than 10 files, largest 41.3 MB (`python3 measure_library.py`). So
  `{{link:path}}` is not the polite third form for people who like links — it is the only form
  that can deliver a `motion-video` result. That moved `link` from "also supported" to "the
  default for anything big", and it is now written that way.
- **Two roots, one grammar.** The console's store and mcp.lamoom.com's store are different
  layouts under different roots. A path therefore resolves against the root of the call it rode
  in on, and nothing about the token says which. Written as a rule in the decision document
  rather than left to an example.
- **A tie at 2 that is not a tie.** Both live options score 2 on the minimum. Option 2's 2 is
  correctness, which never improves. Option 1's 2 is time-to-ship, which a calendar fixes. The
  scoring rule was doing what it exists to do — stopping an average from hiding a flaw — and it
  was about to hide the flaw that matters, so the tie-break is written down beside the table
  instead of being silently applied.

## Still open, and going into iteration 3

- Whether either server already resolves `{{...}}` today. Nothing read so far says either way,
  and the console repository is not reachable from here. This is answered by sending one mail
  with the tokens in it and looking at what arrives — the falsifier, run in iteration 3.
- What `inline` does when the file is not an image.
- A reference inside a fenced code block, where somebody is showing the grammar rather than
  using it.
