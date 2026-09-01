# Classes touched

Every named thing this change can reach, and how I know it.
VERIFIED = I read it in this session. INFERRED = it follows from something I read.
UNVERIFIED = I could not open it; the repository that holds it is not reachable from here.

## Reachable in this session

| Name | Where | What it is | Tag |
|---|---|---|---|
| `plugins/claude/skills/lamoom/SKILL.md` | LamoomAI/lamoom-plugin | the /lamoom skill, 771 lines. Line 348 is the delivery line: `deliver  send_email the result, the FILE ATTACHED, never retyped into the body` | VERIFIED |
| `plugins/codex/skills/lamoom/SKILL.md` | LamoomAI/lamoom-plugin | byte-identical to the claude one (`diff` printed nothing). Any edit lands twice | VERIFIED |
| `plugins/claude/.mcp.json` | LamoomAI/lamoom-plugin | the connector: http, `https://console.lamoom.com/mcp` | VERIFIED |
| `README.md` | LamoomAI/lamoom-plugin | "both are generated — an edit here is overwritten on the next ship. The source is `backend/mcp/skills/lamoom/SKILL.md` in the Lamoom console." | VERIFIED |

## The tool contracts, as the client is handed them

| Call | Signature, verbatim from the schema this session was given | Tag |
|---|---|---|
| `send_email` (console.lamoom.com/mcp) | `send (subject, body, workflow_id?, files?)` — "body is MARKDOWN, rendered as a branded Lamoom HTML email; write natural markdown, no HTML. files are paths to ATTACH, resolved like a manage_file read (the run's files when workflow_id is set, else your library); max 10, 7MB." | VERIFIED |
| `run.email` (mcp.lamoom.com) | `run.email(run_id, subject, body)`. There is no files argument, and "an argument belongs to one call and is refused by every other" | VERIFIED |
| `manage_file action=get` | returns `{path, content}` for text, or `{size, download_url}` for binary. `size 0` means the bytes were never PUT | VERIFIED |
| `manage_file` read resolution | "from a run, a PLAIN path (README.md, customizations/key_role.md, iterations/000001/x.md) resolves run -> loop -> your library -> your customizations, first match wins. You never prefix a path" | VERIFIED |
| `run.files(run_id, upload)` | hands back an address to PUT bytes at | VERIFIED |
| the studio address | "the file is at https://studio.lamoom.com/ followed by that path" — a path is already a URL | VERIFIED |

## Not reachable

| Name | Why it matters here | Tag |
|---|---|---|
| `backend/mcp/skills/lamoom/SKILL.md` in the Lamoom console | the source of both SKILL.md bundles. An edit to lamoom-plugin is overwritten from here on the next ship | UNVERIFIED |
| whatever renders `body` into the branded HTML mail | it is the one place a `cid:` part could be attached to an inline image | UNVERIFIED |
| whatever turns `files[]` into MIME attachments | it decides whether an attachment can also be referenced from the body | UNVERIFIED |

The Lamoom console is not among the repositories this account exposes
(`list_repos` returned 32 and none of them holds `backend/mcp`; `LamoomAI/platform`
was cloned and checked — `grep -rl "manage_loop\|manage_workflow\|judge_result"` over it
printed nothing, so it is a different product). Every server-side row in the table above is
therefore UNVERIFIED and stays UNVERIFIED until someone opens that repository.

That fact decides the **order** of the work, not which design is right. A design that needs a
server change cannot be finished in this session; it can still be the correct design, and this
row is here so that nobody later reads "unreachable today" as "rejected".
