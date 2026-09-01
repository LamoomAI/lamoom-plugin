# The comparison, scored by the minimum

Each option scores 1 to 5 on every lens. Its score is its **lowest** lens, because a design is
as good as its worst dimension and an average hides the thing that will hurt.

The seven lenses, named so the scoring can be argued with:

1. **Correctness** — does it do what R1 says, for all three forms?
2. **Operability** — when it goes wrong, can somebody who was not here read what broke?
3. **Cost** — money and round trips per send.
4. **Privacy** — who can read a file because of this change who could not before?
5. **Simplicity** — how many places must be right for one mail to be right?
6. **Evolvability** — what does the second mail surface, or the second client, cost?
7. **Time to ship** — one person, days.

| | 1 server expands | 2 client expands | 3 do nothing | 4 public url |
|---|---|---|---|---|
| R1 three forms | 5 all three, everywhere | 2 `{{path}}` cannot attach through `run.email` | 1 no grammar at all | 4 all three, links only |
| R2 review online | 5 | 3 inline decays when the url expires | 2 by hand | 4 |
| A4 10 files / 7MB | 4 link is the escape, and it is measured as the common case | 3 same escape, weaker | 2 nothing over 7MB is deliverable | 5 the cap stops binding |
| A7 refuse on missing | 5 the store knows | 2 a prompt is not a mechanism | n/a | 5 |
| A8 one path grammar | 5 | 4 | 2 the studio url is written by hand | 3 a public url is a second address for the same file |
| A5 client does what it can | 3 met for attach and inline, which a client cannot do; a named exception for `link`, which it could | 5 nothing on the server at all | 5 | 2 a whole new server-side reader |
| **Correctness** | 5 | 2 | 1 | 4 |
| **Operability** | 5 named refusal, one place to look | 2 fails differently in every client, and N extra places to fail before a mail exists | 4 nothing to break | 3 a url that outlives the mail |
| **Cost** | 5 | 5 tied — the extra round trips price out under a millionth of a dollar each (pricing.md) | 5 | 4 |
| **Privacy** | 5 nothing becomes readable | 5 | 5 | 1 bytes readable with no sign-in |
| **Simplicity** | 4 one function, two callers | 3 every client must obey a prompt | 5 | 2 a third system with its own lifetime |
| **Evolvability** | 5 a new mail surface inherits it | 2 every new client reimplements it | 3 | 3 |
| **Time to ship** | 2 needs the console repo, which this session cannot open | 5 two files, today | 5 | 2 |
| **SCORE (minimum)** | **2** | **2** | **1** | **1** |

**Cost was rescored after it was priced.** It first read 5 against 3, on the extra round trips
the client option makes. Priced, those are a rounding error, so the lens is a tie and the round
trips are counted where they actually hurt — Operability. A lens that cannot tell two options
apart must not be allowed to look like it did.

## Reading a table where two options tie at two

Option 1 and option 2 both score 2, and they are not the same 2.

Option 2's 2 is **Correctness** and **Operability** — it is wrong in the case the request names,
and it is wrong differently in every client. Time makes that worse: every new session is another
chance to send Kate a mail with `{{...}}` printed in it.

Option 1's 2 is **Time to ship**, and it is the only 2 on the row. Time to ship is the one lens
that a calendar fixes: it is low because of who is holding the keyboard today, not because of
anything about the design. Every other lens is a 4 or a 5.

A minimum score is meant to stop an average from hiding a flaw. It is not meant to make "I
cannot reach the repository this afternoon" outrank "it does the wrong thing forever".
So the tie is broken by asking which 2 is still a 2 next week: option 1's is not.
