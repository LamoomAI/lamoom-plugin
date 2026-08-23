# Lamoom

Run somebody else's way of working, judged until it is good. [lamoom.com](https://lamoom.com)

## Install

    claude plugin marketplace add LamoomAI/lamoom-plugin
    claude plugin install lamoom@lamoom

Restart, then type `/lamoom`.

Codex: Settings → Plugins → Add marketplace → `https://github.com/LamoomAI/lamoom-plugin`

Anything else — **https://lamoom.com/setup?get=claude_code**
It opens on the client you are in and hands you the one line for it.

## What this is

Two halves, and it needs both:

| | |
|---|---|
| `/lamoom` | how your agent runs somebody else's loop, step by step, and scores what it made |
| the connector at `https://console.lamoom.com/mcp` | where the runs, files, reasoning and scores are kept |

Sign in when the connector asks. Free, $20 of run credit, no card.

## This repo

A marketplace, not a plugin. `plugins/claude` and `plugins/codex` are the
bundles, and both are generated — an edit here is overwritten on the next ship.
The source is `backend/mcp/skills/lamoom/SKILL.md` in the Lamoom console.
