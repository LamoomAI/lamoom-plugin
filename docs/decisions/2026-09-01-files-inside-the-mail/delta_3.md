# Iteration 3 — what the attacks changed

The choice did not change. Five things in it did.

1. **The falsifier ran, and it came back negative.** Two probe mails through the live
   `send_email`, one of them referencing a path that certainly does not exist, both sent without
   complaint and neither reporting an attachment. So nothing resolves `{{...}}` today. Before
   this, "does it already exist?" was the open question the whole implementation plan hung on.
   Now the plan starts at "build the resolver" and says so with evidence rather than an
   assumption.
2. **The three forms stopped being three renderings of one idea.** Attach and inline copy the
   bytes and freeze them at send time; link points at the live path. That is now a reason to
   choose between them — freeze a result you are reviewing, link a document that keeps changing
   — and it is written in the decision rather than left to be discovered.
3. **A rule appeared that nobody would guess.** Run files die 30 days after their last write, so
   `{{link:}}` to a run-scope file is a dead link in an archive. Link permanent things; attach or
   inline scratch. This is the sentence most likely to save somebody a confusing morning.
4. **The seam grew a return type.** It returns the rewritten body, the attachments and the inline
   parts — not a finished HTML string — so a second surface can render the same three forms
   without a second parser. One return type, bought against a caller that does not exist yet.
5. **Fenced code blocks are skipped.** Caught by writing this document: the delivery mail for
   this run has to contain `{{link:path}}` as text. A resolver that reads inside code fences
   makes the grammar impossible to explain in the product that has it.

## What is now settled that was open

- Which root a path resolves against: the root of the call it rode in on, and nothing in the
  token says which. A path that climbs out of that root is refused by the rule that already
  exists.
- What inline does to a non-image: it attaches it, and says so.
- The eleventh reference and the oversized message: refused before sending, naming the count or
  the size.

## Still not known, and it needs an eye rather than a return value

Whether probe 1 arrived in Kate's inbox with the braces printed in it. Everything above is
consistent with that, and nothing in a return value can prove it. If that mail arrived with a
picture in it, this iteration's central finding is wrong and the run should be told so.
