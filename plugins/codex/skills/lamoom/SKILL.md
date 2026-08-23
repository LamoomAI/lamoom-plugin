---
name: lamoom
description: Run apps from the Lamoom marketplace (lamoom.com) inside Claude, ChatGPT, Codex or any MCP client, and build and publish your own loops as apps. Use for a bare "/lamoom" with nothing after it — you work out which app is meant — and for "/lamoom {a requirement}", matched against the loops they own or ran before the catalog is read. Also when the user names a Lamoom app, pastes a lamoom.com app link, says "run the X app", asks to browse the Lamoom catalog, asks to BUILD or UPDATE a loop / "make a loop for X", or wants to publish one.
---

# Lamoom

A Lamoom **app** is a loop someone else built and published. It has a README.md,
a list of steps, and a panel of judges. You run it. The platform saves the run,
the files, the reasoning log and the judge scores in the runner's account.

## 0. `/lamoom` with nothing after it

You work out which app is meant. Answer with a running app. Never ask, never
show a menu. If there are no Lamoom tools at all, go to §1 and say so.

```
read the case off the last few turns: the thing they were just working on

manage_loop action=find query={that case, in their own words}
  ├─ used[] has a match  -> take the server's `pick`. Run it.
  └─ used[] empty        -> the top of catalog[]. Run it.

nothing to read off the conversation:
manage_loop action=find            (no query)
  -> the top of used[]: pinned first, then most-run, then best-rated. Run it.
```

Then `manage_workflow action=create kind=… ref=… setup_id=…`. Use
`public_loop_id=` for a catalog app they have never run. Fill the brief per §3a,
then work §4.

| Rule | |
|---|---|
| Always a new run | never look for an open one. Create a new run every time, unless they say continue or resume |
| Name the pick in one clause | "Running Daily News — the one you run most." Then go |
| Never ask which | not public or private, not which setup, not which judges. You pick the judges too |
| Never shop | if `used[]` matched, do not read the catalog |
| A wrong guess is cheap | they say no, you `mute` it and take the next one. Asking costs more |
| Nothing used yet | run the loop they own. If they own none, show the catalog |

**Leave the next session a shortcut.** After a run, and as soon as they correct
a pick:

```
manage_loop action=note kind=… ref=… when_to_use="…" aliases=["what they call it"]
manage_loop action=note … pinned=true            the one they run daily
manage_loop action=mute kind=… ref=… reason="…"  rejected; never suggest again
```

Write `when_to_use` for a session with no context. Put the words that should
trigger it, not a description. Aliases are the user's own words, exactly as they
say them.

## 0a. `/lamoom` + a requirement

"write my week in review" is a requirement, not an app name. Same rules as §0.
Read their own shelf before the catalog.

```
requirement
  │
  ├─ manage_loop list ─────── loops they OWN ─┐
  ├─ manage_loop find q="…" ─ used[], RAN ────┴─> best fit ──> run it
  │       fit = alias/when_to_use > pinned > same OUTPUT shape > same input
  │       muted = never, at any score
  ├─ nothing of theirs fits ── catalog[] top ──> run it (§3b first if paid)
  └─ catalog empty too ─────── §6 build ──────> run it
```

The requirement is the brief. It goes in `key_role.md` and the other declared
files (§3a). It never goes into the loop's logic.

Only a different output shape sends you off their shelf. "Not perfect" is not
"does not fit".

## 1. Connect once

Claude Code:

```
claude mcp add lamoom --transport http https://console.lamoom.com/mcp
```

Then run `/mcp` once to sign in. Sign-in is Google or email.

claude.ai: Settings → Connectors → Add custom connector → URL
`https://console.lamoom.com/mcp` → sign in.

ChatGPT: Settings → Connectors → Add custom connector → same URL →
authenticate in the browser. Then ask ChatGPT to use the Lamoom connector.

Codex:

```
codex mcp add lamoom --url https://console.lamoom.com/mcp
codex mcp login lamoom
```

Lamoom's server handles OAuth discovery and client registration itself. Do not
pin a static Cognito client. MCP clients use random localhost ports, and Cognito
needs the exact callback URI registered first.

| Path | Purpose |
|---|---|
| `/.well-known/oauth-protected-resource` | points the client at Lamoom as the auth server |
| `/.well-known/oauth-authorization-server` | advertises `/register` and Cognito's endpoints |
| `POST /register` | creates or reuses a Cognito PKCE client for that exact callback URI |
| `/oauth2/authorize` | strips `resource` and redirects to Cognito |

Cognito rejects `resource=https://console.lamoom.com/mcp` when the scope is
`lamoom-console-mcp/access`. The scope stays. Only `resource` is removed.

If a client says *"does not support dynamic client registration"*, it is too
old. Point it at the pre-made client in `.mcp.json`:

```json
{ "mcpServers": { "lamoom": {
  "type": "http", "url": "https://console.lamoom.com/mcp",
  "oauth": { "clientId": "2ljmnlgqsvptabgeo5cr0bajpt", "callbackPort": 8080,
    "scopes": "openid email profile lamoom-console-mcp/access",
    "authServerMetadataUrl": "https://console.lamoom.com/.well-known/oauth-authorization-server" }
} } }
```

If a tool is missing, the connector is not added. Say so. Do not improvise.

## 2. Find the app

| You have | Do |
|---|---|
| a name ("True-ish Stories") | `manage_loop action=find query=true-ish-stories` |
| a lamoom.com/app/{slug} link | the slug is the query |
| a `public_loop_id` | skip find |
| a requirement, not a name | §0a — their own loops first |
| nothing at all | §0 |

`find` ranks. It never picks. You pick, and you name it in one clause as you
start. `used[]` always beats `catalog[]`.

## 3. Run it

### Commit and push before the run starts

Do this first, before the brief and before you launch anything. A run rewrites
files. "Revert" only works if there is a commit to go back to.

```
work is in a git repo?
   ├─ yes  -> git add {scoped paths} ; git commit ; git push    THEN launch
   └─ no   -> say so in one clause, then launch
```

| | |
|---|---|
| Scope the paths | never `commit -a`. A repo can hold thousands of stale changes from elsewhere |
| Read the index first | run `git diff --cached --name-only`. A scoped `git add` still commits what someone else already staged. Unstage it, or say it rode along |
| Uncommitted work is not a reason to skip | that is exactly what a restore point is for. Commit it |
| Push too | a commit on one laptop is not a restore point for anything else |
| Nothing to commit | fine. Say nothing and launch |

Skip this and a user who says "revert" is told the only restore point is
yesterday.

### Open the run

```
manage_workflow action=create public_loop_id={plid}
```

Pass your own `workflow_id` to make it safe to retry. The same id returns the
same run instead of starting a second one.

The response hands you the app's README.md, its judges,
`customization_files`, `to_fill`, and two things worth reading before you touch
anything:

- **`plan`** — EVERY step of this run, in order, with its step-tasks and their
  status. Step 0 is the backward walk (§3d) and it is first. `working_on` points
  at where to start; `progress` counts what is left.
- **`flow`** — the whole cycle, stage 1 to stage 7, so you never have to work out
  where you are from a single `next` hint:

```
1 find      manage_loop action=find                -> the loops that fit
2 create    manage_workflow action=create          -> the full plan + this flow
3 work      manage_steps action=report_step_task   -> the ONE next step-task
4 finish    the last step-task                     -> submit the result
5 judge     judge_result action=tasks -> submit    -> the judges, then the verdict
6 below     a failing verdict                      -> next iteration, the WHOLE
                                                      plan back to todo, from step 0
7 above     judge_result action=finalize           -> mailed, result ATTACHED
```

Follow that README.md as if it were your own project's.

## 3a. Write the brief, then start

Every app declares files it reads before step 1. There is always `key_role.md`:
who this run is for, how it must sound, what it must never do. Often there is
one more saying what to work on.

| Field | Meaning | What you do |
|---|---|---|
| `customization_files` | already written | obey them. They beat your own defaults |
| `to_fill` | declared, not written yet | write each one in full, before step 1 |

```
manage_customization action=write file=key_role.md content=<the whole file>
```

Write it from what the user just said, their other setups and their library. One
pass. No questions and no interview. The `template` in `to_fill` is the shape.
Fill every heading. A half-filled brief is worse than none, because the run
reads the gaps as deliberate and invents around them.

These files belong to the user. The publisher never sees them, and a new version
never overwrites them. If the user states a lasting preference mid-run, rewrite
the matching section with `action=write` or `action=append`.

Say once, in your last line, that you wrote it and they can edit it. Never
discuss it mid-run.

## 3b. What it costs

Two separate things:

1. a **Lamoom subscription** — $20/month, what Lamoom costs
2. **credit in the wallet** — what the automation costs

`manage_wallet action=get` shows both, plus every app and how many times this
user has run it.

| The app charges | What happens |
|---|---|
| per run | the wallet is debited when the run is created. No run, no charge |
| monthly | `manage_wallet action=subscribe_app public_loop_id={plid}`, then runs are free for 30 days |
| buyout | `manage_wallet action=buy_app public_loop_id={plid}`. The source becomes their own editable loop |

| The user wants | Call |
|---|---|
| to use Lamoom at all | `manage_wallet action=subscribe_lamoom` — $20/month, $20 credit now and every month, cancel any time |
| more credit this month | `manage_wallet action=topup amount_cents=…` |

`payment_required` is the server asking the user to decide. It is not a failure.
Read `basis` and hand over exactly one thing:

| `basis` | What it means | What you say |
|---|---|---|
| `subscription_required` | not a subscriber. Nothing ran, nothing charged | `subscribe_url`. Do not mention top-ups |
| a shortfall | subscriber, out of credit | `topup_url`. Do not pitch the subscription they already pay for |
| `purchase_required` | the app is not sold per run | the `offers`, then ask which |

Never spend their money without a yes.

## 3c. A long run goes in a fresh session

A run fills the screen with steps, files, judge questions and logs. In the
asking session it buries the conversation. Any run longer than a few minutes
gets its own session.

```
asked in session A
   A  commits and pushes                        the restore point, first
   A  picks the loop, names it in one clause    "Running Motion Video Director."
   A  writes brief.md                           the requirement, in the run folder
   A  launches session B                        one background task, deadline first
   A  keeps working, checks B's output path
   B  create → follow `next` → finalize         §4
   A  at the deadline                           kill B, check the path once more,
                                                then finish inline
```

```bash
# probe once. A sandboxed shell kills nested sessions at exit 144 with EMPTY
# output, which looks exactly like a run that found nothing.
claude -p "Write OK into ./_probe.txt" --permission-mode acceptEdits --allowedTools "Read,Write"
# then, sandbox disabled, one background task per session:
claude -p "$(cat brief.md)" --permission-mode acceptEdits \
  --allowedTools "mcp__Lamoom,mcp__claude-in-chrome,Read,Write,Edit,Bash,Glob,Grep,WebFetch,WebSearch"
```

`--allowedTools` is required. `acceptEdits` only covers file writes, so without
it every MCP call is denied and the session comes back having done the work with
nothing submitted.

| rule | |
|---|---|
| one task per session | use `run_in_background`. Never `( … ) &` — the subshell dies with the tool call and the log is empty |
| deadline before launch | write the number down first. A build run is about 25 minutes |
| check after the kill | a session a minute late still wrote the file. Look again before saying it returned nothing |
| two silent in a row | stop launching. Say so and finish inline |
| no probe file | nested sessions do not work here. Say so in one line, then work inline |

## 3d. Think backward

Every step, every file, every judge round starts at the end and walks back.
Never start from what is easy or from what the tools happen to offer.

```
1  END      what exists when this step is DONE, observable
            "the email is in their drafts", not "work on the email"
2  PROOF    the check that says so: a file at a path, a score, a link
3  BACK     what must be true one move before the proof passes?
            repeat until a move needs nothing
4  START    the last move you derived is the first one you make
```

| Case | Backward move |
|---|---|
| a step task | name its output file before writing a line |
| the brief | write the delivery the runner sees, then what earns it |
| a failing judge | start at the score, walk back to the file that caused it |
| building a loop | write the last step first, then what feeds it |
| a deadline | count back from the date, never forward from today |

Say the end in one line before you work: `# end: {observable result}`. Put it in
`log_reasoning` when the step is bigger than one file.

**Step 0 comes back from the server.** Every plan opens on it, whatever the
loop's author wrote — `outline`, four step-tasks, labelled `0`, before step 1:

```
0.1 end_state    the run's end state in one line, observable
0.2 proof        the one check that says it is real
0.3 walk_back    each move before that proof, until a move needs nothing
0.4 first_move   the last one derived is the first one you make -> outline.md
                 plan disagrees with the walk? fix the plan, then step 1
```

Report it like any other step (`report_step_task`, `reasoning` = the walk
itself). Never skip it to "get started" — that is the thing it exists to stop.

**The close comes back from the server too.** The mirror of step 0, last in
every plan, whatever the author wrote:

```
submit     judge_result action=submit, EVERY judge scored, one fresh session each
verdict    passed -> finalize; failed -> iterate and work the plan again
deliver    send_email the result, the FILE ATTACHED, never retyped into the body
mistakes   every wrong turn this run took, appended to the user-library file
           named in `user_files` — one line each
insights   what you learned about the USER — their answers, corrections,
           preferences — appended to the user-library file in `user_files`
```

The last two are what a run owes the next one. A run that only delivers leaves
the same wrong turn to be taken again and the same question to be asked of the
same person a third time. `user_files` arrives with the step-task itself and
lists every file already in that library — write to one of those paths before
inventing a new one.

## 4. Follow `next`

Every response carries a `next` field. It is the server telling you the one
legal next move. Follow it. Never stop because a step looked finished.

| Move | Tool |
|---|---|
| write a declared brief before step 1 | `manage_customization action=write` |
| take the next step | `manage_steps action=report_step_task` |
| write an output file | `manage_file action=put` (plain paths, no scope prefix) |
| change the app's own logic | `manage_file action=put purpose=logic_update` |
| record why you did something | `log_reasoning` |
| submit for judging | `judge_result action=submit` |
| close the run | `judge_result action=finalize` |
| leave the lesson behind | `manage_file action=put scope=user` — the paths in `user_files` |

A run is done only when every judge passes the app's bar and you finalize. A
failed round opens the next one automatically. Keep going. The bar belongs to
the app's author, not to you.

### A failing judge is not a stopping point

Do not stop. Make another iteration. Never write "want me to continue?" or
"should I revise?" after a failed round. Asking is the failure. If the turn ran
long, pick the last `next` back up and continue.

```
judge_result action=submit iteration={n} scores=[EVERY judge]
    -> passed=false, failing_judges=[…]

judge_result action=iterate workflow_id={wid} target_ref={the file being judged}
    -> copies it into iterations/{n+1}/ and carries the failing judges forward
    -> and the WHOLE plan is already back to todo, from step 0

work the plan again from the first step, reporting each step-task as you go.
Each step's `history` holds what the failed round did and why. Where the judges
faulted the PLAN rather than the file, change the plan (plan_step / insert_step)
instead of redoing the same steps.

judge_result action=submit iteration={n+1} scores=[EVERY judge, re-scored]
    passed=false -> iterate again. No new question
    passed=true  -> judge_result action=finalize, then the app's delivery step
```

**One fresh session per judge.** Spawn a subagent for each one, in parallel.
Give it that judge's instructions and the thing being judged. Nothing else. Not
the other judges, not their scores, not what you changed. You made the thing, so
you will score what you meant instead of what is there. Two judges sharing one
context are one judge. Submit what they return, unedited.

Re-score every judge each round, including ones that already passed. An edit for
one judge can break another. Never finalize a round that did not pass, never
lower a score to make it pass, and never deliver before finalize.

## 5. Where the run lands

Files go to the scope the app declared (`save_scope`):

- `workflow` — the run's own files, kept apart per run
- `global` — the runner's own memory, under `GLOBAL/{YYYY}/{MM}/{DD}/{loop}/`

The user library has an enforced layout. Every path is one of two shapes:

- `YYYY/MM/DD/{loop}/…` — a day's output
- `{loop}/…` — that loop's library: indexes, entities, state the next run reads

A bare `root/file.md` becomes `{loop}/file.md`. Anything else is refused.
`GLOBAL/`, `customizations/` and `notes/` are reserved.

It is the runner's account either way, visible at studio.lamoom.com. An app
never writes into another app's data.

## 5a. Local files: one workspace

Some loops also write to the machine: a project, a download, a screenshot, a
render, a script. All of it lives under one root. Nothing goes outside it.

Find the root. Stop at the first hit:

| # | Source | Wins when |
|---|---|---|
| 1 | `$LAMOOM_HOME` | set in the environment |
| 2 | the `workspace_root` customization | the user said where they want it |
| 3 | `~/Downloads/Lamoom` | `~/Downloads` exists |
| 4 | `~/Lamoom` | there is no `~/Downloads` |
| 5 | `/mnt/data/Lamoom` | ChatGPT code interpreter |
| 6 | `./Lamoom` | a container with no home |

`~/Downloads` is the default because it is not synced to iCloud and people empty
it freely.

If the user wants it somewhere else, they are right. Set it, say you set it, and
never raise it again:

```
manage_customization action=set key=workspace_root value=/absolute/path/Lamoom
```

Always an absolute path. A literal `~` creates a folder named `~`. If the old
root holds work, move it.

Four shapes under the root, and no others:

| Path | Holds |
|---|---|
| `{root}/{loop}/{YYYY-MM-DD}_{slug}/` | one run's working files |
| `{root}/{loop}/_library/` | what builds up across runs of that loop |
| `{root}/_scripts/` | shared executables, rewritten each run, never hand-edited |
| `{root}/_cache/` | anything you can make again. Safe to delete at any time |

Loop first, then date. People ask the disk "where are my videos".

One project is one folder. Inputs, attempts, scratch and the result all live in
it, so the whole thing moves or deletes as one:

```
{root}/{loop}/{YYYY-MM-DD}_{slug}/
    input/          the source material, copied in. Never read in place
    attempts/001_{idea}/     each attempt: its build, its cut, its verdict
             002_{idea}/     a kill opens the next number HERE
    out/            the deliverable, plus a stable {slug}.mp4 meaning "latest"
    references/     what the run collected or measured
    notes/          plot, promise, cuts, delivery
```

Then say the path. If the user asks "where's the output?", it was not obvious.

1. **Never write outside the project folder.** Not the cwd, not `~/Desktop`, not
   `/tmp`, not the repo the session started in. Handing over a file means
   handing over its path.
2. **Paths come from `workspace_root`,** never written out literally. One
   `action=set` moves the whole footprint.
3. **Make the folder. Do not ask.** `mkdir -p` at step 1.
4. **The run folder is scratch.** Copy anything that matters to the platform
   before finalize.
5. **One project, one folder.** A new idea is `attempts/{n+1}_{slug}/` in the
   same project, never a folder next door.
6. **Heavy things you can remake go in `_cache/`.**
7. **Artifacts are not source.** A screenshot about the user's repo still lives
   here. Only code they asked you to change goes in their project.
8. **Secrets never live in the workspace.** Keys stay in their env file, named by
   `secrets_env_file`.

## 5b. How much to write

Everything here is read by a stranger in a hurry. A loop dies of length long
before it dies of missing detail. Nobody skips a short judge and everybody skims
a long one. Main ideas only.

| Artifact | Budget | It failed when |
|---|---|---|
| step title | 8 words. A verb and its object | it explains why |
| step intent | one sentence, or nothing | it is a paragraph, or repeats README.md |
| step-task | one line, naming the file it writes | it is prose |
| judge | 12 lines: who they are, one question, what caps the score | it is a character study or a rubric |
| README.md | one screen | something in it belonged in `rules/` |
| `rules/*.md` | a table, a tree, or pseudocode | paragraphs |
| customization default | 5 lines | it is a form |

Five rules that produce those sizes:

1. **Adding starts with deleting.** See §6.0.
2. **One sentence at a time.** Write one, then ask if it needs another. Most do
   not.
3. **One idea per artifact.** Two ideas means two artifacts.
4. **Never say it twice.** A fact lives in one file. If README.md and a step both
   carry it, the step keeps it.
5. **No justification.** A rules file says what to do. It never argues for
   itself.

Delete on sight: *Note that · It's important to · In other words · Make sure to ·
Remember that · This means that · As mentioned above · The goal here is.*

A judge is a name, one question, and one score cap. The whole thing:

```markdown
# Judge: Nadia the Scroller
## Lens
At which exact second did I stop being here?
## How to reason
Reward the second something new arrives. Punish a held frame with nothing left
to read.
## Scoring
0-10 from this lens only. One second of dead air caps this at 6.
```

If a judge needs more than that, it is two judges, or it is a rules file.

**Every panel gets a deletion judge** — one whose only question is what can come
out, of the result and of the code that made it. Without it every round adds.

## 5c. A correction is a missing mechanism

Never just fix the result. Build the thing that makes the mistake impossible.

```
1  WHY        keep asking until the answer names something MISSING.
              "I chose the wrong tone"                     a symptom
              "no step ever asked what register this was"  the answer
2  MECHANISM  judge = a taste nobody owned · step-task = work nobody was given
              rules file = a decision made from memory · customization = a value
              that changes per person · script = a check nobody does by hand
3  THEN fix the instance.
```

A stranger can check a mechanism. "Be more careful" is not one. Say which
mechanism you added. The same note twice means you patched and did not build
anything.

## 6. Building a loop

A loop is built only once a fresh session has run it end to end and the output
passed judging. Do these in order.

**0. Delete before you add.** First move of every build and every update.

```
about to add a step / file / rule / line
   ├─ what does it REPLACE?  -> delete that, in the same edit
   └─ replaces nothing?      -> it does not go in yet
after the edit: read the whole file back and cut what nobody would miss

a folder looks like a mess
   ├─ did YOU write these?  -> delete them now, in this session
   └─ the user's?           -> say which ones and why, delete on their word
```

Cut more than you added. Two files saying the same thing means the loop follows
whichever it read last. The duplicate is the bug.

**1. Read the source first.** If they are porting something they already ran,
read it before writing: its rules, its schemas, its step names, its failure
notes. A loop that reinvents what worked is a downgrade.

**2. Knobs go in customizations, never in files.** Every role list, place, size,
count, time, tone and identity is `manage_customization action=define` with a
real default. Files hold the method. Customizations hold the targeting. Test:
could a stranger run this by changing only customizations?

**2a. If it touches disk, it declares one root key.** `workspace_root`, per §5a.
A rules file never contains an absolute path, `~/Desktop`, `/tmp`, or "the
current directory".

**2b. The workspace is for artifacts, never the user's own tooling.** Anything a
launchd job or cron entry runs stays where it is. Moving it breaks a schedule
and the failure looks like nothing happening. Check `~/Library/LaunchAgents` and
`crontab -l` before moving any folder.

**3. Write loop files with `purpose=logic_update`.** `manage_file put
scope=loop` otherwise routes the write to the user library. Check the response
says `"saved"` with no `routed` block.

**4. Keep README.md short. Put detail in `rules/`.** README.md is the contract:
where files land, the sequence, the hard rules, the never-stop clause. One
`rules/*.md` per real decision. Tables and pseudocode. Over budget means cut,
not reword.

**5. Choose `save_scope` deliberately.** `workflow` is scratch for 30 days.
`global` is permanent. Any loop that builds up over time writes to user scope at
stable paths, plus an index (`*_index.tsv`) the next run reads to skip
duplicates.

**6. Judges are the spec, and you pick them.** Three to five, each a named person
with a stake, never an abstract quality. Hand over the panel already written.
One question and one score cap each. Set `pass_score` high enough to force a
second round. Judges live in `manage_judge`, never in README.md.

**7. Steps follow the real sequence, output last.** Every step-task names the
file it writes. A step-task that only produces a decision in the model's head
disappears when the session ends.

**7a. Every loop carries a data-flow table.** The most common way a loop dies is
a step that cannot tell what the last step left behind. README.md gets a
`## Data flow` section, one row per step:

| Step | Reads | Writes | Done when |
|---|---|---|---|
| 2 signals | `cycles/{DATE}/knobs.md`, `companies_index.tsv` | `cycles/{DATE}/queue.csv`, `logs/{DATE}_signals.log` | queue.csv exists and every enabled signal has a `_summary` line |

- **Steps hand off through files, never through context.** Step N+1 opens what
  step N wrote. If two steps only work in one session that remembers both, they
  are one step. Merge them, or add the file between them.
- **Every "Writes" is a real path**, openable with `manage_file action=get`.
- **State the promotion rule once**: which scope things move to and when, which
  step does it, and what gets left behind on purpose.
- **Name the accumulator.** Say which step appends to the index and with which
  key, so the next run can skip duplicates.

**7b. Work out the current step from the file tree, not from memory.** README.md
gets a `## Where am I` block. The first check that fails is the current step:

```
cycles/{DATE}/knobs.md missing        -> step 1
queue.csv missing                     -> step 2
queue.csv has status=queued rows      -> step 3
qualified company with no people/     -> step 4
person.md without a connect note      -> step 5
connect_list.md missing               -> step 6
otherwise                             -> step 7
```

`manage_steps action=list` gives the server's cursor. The file tree gives the
truth. When they disagree the files win, and the step plan gets corrected. A
step marked done whose output file does not exist was never done.

**8. Run it in a fresh session.** The session that built the loop will paper over
its gaps.

```
claude -p "Run the Lamoom loop {loop_id}: manage_workflow action=create loop_id={loop_id},
then follow every `next` field until finalize. Report what was ambiguous." \
  --permission-mode acceptEdits \
  --allowedTools "mcp__Lamoom,mcp__claude-in-chrome,WebFetch,WebSearch,Read,Write,Edit,Glob,Grep"
```

Drop `mcp__claude-in-chrome` if the loop does no browsing.

**9. Check the artifacts, not the transcript.** `manage_file action=list` the
output paths. An empty folder with a confident summary is a failed run.

**10. Patch the loop, then run again.** Every unclear thing the fresh session hit
becomes a step-task, a judge or a customization (§5c). Then a second fresh run
to prove it.

**Always write into a file** — reasoning, data, rejected options, conflicting
sources. A run with an empty output folder failed, whatever got figured out.

## 7. Publishing a loop as an app

`manage_app` is the publisher surface. `action=create` from one of your own
loops, `action=update` for listing and pricing, `action=submit` to freeze a
version and queue it for review.

Submit refuses until all of these are true:

1. `save_scope` is `workflow` or `global`. A `loop`-scoped loop shares one
   library across every runner and can never go public.
2. `description_md` is written.
3. There is at least one screenshot or a YouTube URL.
4. Nothing that looks like a credential is anywhere in the loop's files.

Then a human reviews it. Approved means live on the version that was reviewed.
Editing the source loop afterwards changes nothing live until you submit again.

### Declare what varies

Before submitting, take everything that would differ between two strangers —
topics, roles, place, language, tone, an address, a headcount, a time of day —
out of the loop's files and declare it:

```
manage_customization action=declare loop_id={lid} file=what_to_collect.md \
  role="which news this person wants collected" template=<the headings>
```

Then name the file in README.md: `read customizations/what_to_collect.md before
step 1`. A declared file that no instruction names is a file no run reads.

A declaration is a name and a shape, never content. The file lives in each
runner's own library and you never see it. Write the template for a stranger.
Assume nothing about their country, job, language or age.

### Improving a live app: read the runs

An app gets better from what strangers' runs actually did, not from guesses.

```
manage_app action=improve public_loop_id={plid}
manage_app action=run workflow_id={one of worst_runs}
```

`improve` shows where runs stall, which judge keeps failing, what reviews say,
and how many rounds it takes. `run` opens one run in full, including the
reasoning logs. Read those for what the agent was **missing** — an instruction
that never said which currency, a customization nobody filled — not for what it
produced. Fix that in the source loop, then submit.

You can see a run only until its runner erases it. Erasing deletes the files and
logs for you too. What stays is that it ran and how it scored. So when a run
tells you something, change the loop then.

### Erasing a run

If the user asks to delete what a run produced, that is `manage_workflow
action=erase workflow_id=…`. First say plainly what goes — the run's files, its
logs, its tool calls, the brief it ran with, for the publisher too — and what
stays: that it ran, and its scores. Get a yes. It cannot be undone.
