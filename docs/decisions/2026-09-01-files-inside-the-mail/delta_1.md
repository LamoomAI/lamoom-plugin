# Iteration 1 — what changed by writing them down

## What breadth cost, and what it bought

Four options went in. One died on contact, and one changed shape.

- **The strawman I killed.** My first sketch of option 2 had the agent base64 the bytes into an
  HTML `<img src="data:...">` in the body. It cannot exist: `send_email` says "body is MARKDOWN,
  rendered as a branded Lamoom HTML email; write natural markdown, no HTML". Any option that
  needs the client to emit HTML is refused by A3 before it is designed. Deleted rather than
  scored, because a comparison table with a dead option in it flatters the winner.
- **Option 2 changed shape.** It started as "the client does the whole job" and ended as "the
  client does the job it can do on the console, and cannot do it at all through `run.email`".
  That is not a weakness I argued into it — `run.email(run_id, subject, body)` has no `files`
  argument, and the contract says an argument sent to the wrong call is refused. So the option
  the request literally names is the option the client cannot serve.
- **What I learned that reframes the whole thing.** There are two stores and two mails, not one.
  `manage_file list scope=user` on console.lamoom.com returned 1560 files laid out
  `YYYY/MM/DD/{loop}/...`, and none of them is under `SoftwareEngineer_JohnCarmack/`, where this
  run's own files went. So "path" means one thing on the console and another on mcp.lamoom.com,
  and a grammar written once must resolve against whichever root the call it rode in on belongs
  to. Neither option had said that. It is now the first thing the decision has to answer.

## What is still open going into iteration 2

- Which root a bare path resolves against, said as a rule and not as an example.
- What `inline` does when the file is not an image.
- What happens to the eleventh reference, and to the file over 7MB (A4).
- Whether a reference is allowed to appear inside a fenced code block, where a person is
  showing somebody the grammar rather than using it.
