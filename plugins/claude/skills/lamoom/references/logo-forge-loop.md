# Logo Forge Loop

Use this reference when creating or running a Lamoom loop for logos, symbols, wordmarks, favicons, app icons, or visual identity systems.

## Loop Purpose

`logo-forge` is for making logos through repeated attention, not one-shot decoration. The loop should help Codex move from signal to symbol: extract the brand's living tension, generate strong alternatives, judge them honestly, refine without sentimentality, and stop only when the result is simple, memorable, usable, and true.

This loop is inspired by the creative discipline often associated with Rick Rubin's writing: listen first, keep the channel open, remove what is false, trust taste, and return repeatedly until the work feels inevitable. Do not quote the book unless the user provides text to use.

## Loop Library

When creating or repairing the loop, store these files in the Lamoom loop if they do not already exist:

- `CLAUDE.md`: concise operating rules for logo creation.
- `references/logo-brief-template.md`: questions and structure for extracting brand signal.
- `references/logo-deliverables.md`: required output formats and production expectations.
- `judges/brand-truth.md`: evaluates whether the logo expresses the brand's core idea.
- `judges/distinctiveness.md`: evaluates memorability and ownability.
- `judges/simplicity.md`: evaluates reduction, clarity, and silhouette strength.
- `judges/usability.md`: evaluates favicon, monochrome, dark/light, small-size, and layout use.
- `judges/craft.md`: evaluates typography, spacing, geometry, polish, and professional finish.
- `judges/iteration-depth.md`: evaluates whether the workflow tried enough real alternatives and improved from evidence.

Prefer Lamoom judge tools for judge criteria. Keep detailed judging criteria in judges, not in `CLAUDE.md`.

## CLAUDE.md Seed

Use or adapt this for the loop's `CLAUDE.md`:

```md
# Logo Forge

Create logos through deliberate iteration.

Start by listening for the brand's core tension: what it is, what it refuses to be, who it serves, and what should feel inevitable when the mark appears.

Do not settle after the first plausible direction. Generate divergent routes, name why each exists, judge them, then refine the strongest route by subtraction.

Every workflow must produce evidence of:

- brand signal extraction
- at least three distinct creative directions
- a recommended route
- judge scores with specific reasoning
- at least one improvement pass after judging
- practical logo assets or asset specifications

Favor simple forms with memorable behavior. Remove cleverness that does not help recognition. Keep the wordmark, symbol, and system usable in small, monochrome, dark, and light contexts.
```

## Step Template

Seed or update loop steps so workflow runs follow this order:

1. **Receive Signal**: collect the user's brief, references, audience, values, category, constraints, and emotional temperature.
2. **Distill Essence**: write the brand thesis, tensions, visual metaphors, anti-goals, and success criteria.
3. **Map the Field**: identify category conventions, cliches to avoid, and opportunities for distinctiveness. Use web research only when current competitor/category context matters.
4. **Diverge**: create at least three materially different routes. Each route needs a name, rationale, visual grammar, typography direction, color/material direction, and use-case fit.
5. **Make Artifacts**: produce sketches, SVGs, prompts, mood directions, or asset specs appropriate to the workflow.
6. **Judge**: run Lamoom judges. Score every judge 0-10 with concrete evidence, not vibes.
7. **Iterate**: improve the strongest route based on judge feedback. If a route scores below pass threshold, either revise it or explicitly choose another route.
8. **Reduce**: simplify the mark and wordmark. Remove ornamental parts that do not improve recognition, meaning, or usability.
9. **Package**: store final/recommended assets, rationale, usage notes, and next-step production requirements as workflow files.
10. **Finalize or Continue**: finalize only when judge scores pass. Otherwise continue with the next useful iteration.

If the existing loop has vague steps, use Lamoom step tools to replace or supplement them with this template. Keep the workflow cursor as the source of truth while running.

## Judge Criteria

Use a default pass score of 8 unless the loop already defines another threshold.

### brand-truth

Score high when the logo visibly expresses the brand's core thesis and emotional promise. Penalize generic beauty, category cosplay, or forms that could fit any brand.

### distinctiveness

Score high when the route has a memorable silhouette, ownable behavior, and recognizable system. Penalize obvious symbols, overused AI gradients, generic tech loops, and marks that disappear in a competitive set.

### simplicity

Score high when the idea survives reduction. Test whether the logo works as a one-color mark, tiny favicon, and fast mental sketch. Penalize unnecessary parts and clever details that need explanation.

### usability

Score high when the logo can work across app icon, favicon, nav wordmark, social avatar, deck, docs, and dark/light surfaces. Penalize fragile gradients, unreadable type, or marks that only work in a hero image.

### craft

Score high for optical balance, spacing, curve quality, typography fit, palette discipline, and production-ready finish. Penalize awkward geometry, weak alignment, accidental tangents, and unpolished type.

### iteration-depth

Score high when the workflow genuinely tried, compared, judged, and improved. Penalize single-shot outputs, cosmetic variants, or iteration that does not respond to evidence.

## Workflow Files

For each workflow, write durable files like:

- `brief.md`
- `brand-thesis.md`
- `directions.md`
- `judge-results.md`
- `iteration-log.md`
- `recommended-route.md`
- `assets/primary-logo.svg`
- `assets/concept-sheet.svg`
- `assets/favicon.svg`
- `assets/usage-notes.md`

Use upload URLs for binary references or generated bitmap assets.

## Creative Rules

- Listen before making.
- Prefer the inevitable over the impressive.
- Make at least one route that is quieter, one that is stranger, and one that is more commercially direct.
- Let iteration change the work; do not only defend the first draft.
- Use subtraction as an active step.
- Keep trying until the best route is no longer merely good, but hard to unsee.
