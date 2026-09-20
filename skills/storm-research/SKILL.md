---
name: storm-research
description: Produce a grounded, heavily-cited research article on a topic using a verification-first adaptation of Stanford's STORM method (perspective-guided question asking + simulated retrieval conversations), hardened against STORM's known failure modes — red herrings, over-association, and source-bias transfer. Every factual sentence is traced to a fetched, quoted source; contradictions are preserved; speculation is quarantined or cut. Use when the user wants reliable, verifiable, citation-grade research rather than a quick overview, says "STORM", "grounded research", "cited research article", "fact-checked deep dive", or invokes /storm-research.
---

# STORM-Research: Verification-First Grounded Article Generation

Adapts Stanford's STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question
asking) into a workflow Claude executes directly. STORM's published weakness is **not** hallucination —
it is *red herrings* (relevant-sounding but off-claim content), *over-association* (two true facts
joined into a false implication), and *source-bias transfer* (laundering one origin's bias into
neutral-looking prose). This skill keeps STORM's strength — perspective-guided retrieval produces broad
coverage — and adds the verification gate STORM lacks.

**Prime directive: the output's value is reliability, not fluency. A shorter, fully-verified article
beats a longer, partly-speculative one. No factual sentence ships without a fetched, quoted source
behind it. When evidence is thin, say so explicitly — never fill the gap with plausible prose.**

The topic is the skill argument (`[TOPIC]`). If none was given, ask what to research before starting.
If the topic is ambiguous in scope, time-frame, or audience, ask **one** tight clarifying question, then
proceed.

---

## Tools

- **Search (find leads):** Brave Search via the bundled helper —
  `bash ~/.claude/skills/storm-research/scripts/brave_search.sh "your query" [count]`. It returns
  title + URL + snippet per result (default 8). The key is read from `~/.claude/brave_key`. Snippets are
  *leads, not evidence*.
- **Read (to cite):** `WebFetch` the actual page and pull an **exact quote**. **Never cite a snippet you
  haven't fetched.** If a page is a client-side JS dashboard `WebFetch` can't render, say so and fall
  back to a fetchable source — never cite numbers you couldn't load.
- **Scale-up (optional):** for large or high-stakes topics, the `deep-research` skill can fan out
  retrieval; still run Phases 3 and 6 here on its output.

---

## How this runs — a staged workflow with confirmation gates

This skill runs as a **staged workflow**, not one long generation. The research phases (0–3) are
separated from the writing phases (4–6) by **three confirmation gates** where you stop, present what you
have, and let the user steer with a simple choice before continuing. **No writing begins until the user
confirms at Gate C.**

At every gate, use the **`AskUserQuestion`** tool so the user answers with a click (they can always pick
"Other" to type a custom instruction). Present the stage's findings *first* as plain text, then ask the
gate question. If the user picks an "adjust / redo / gather more" option, loop within that stage and
re-present the gate. Do not silently skip a gate.

Maintain a running **Evidence Ledger** (schema below) throughout — it is the single source of truth that
the final article is built from. Do not write prose from memory; write only from the ledger.

```
Phase 0 Scope ─▶ ⛔ GATE A ─▶ Phase 1 Perspectives ─▶ ⛔ GATE B ─▶
Phase 2 Retrieval ─▶ Phase 3 Verify ─▶ ⛔ GATE C (writing gate) ─▶
Phase 4 Outline ─▶ Phase 5 Write ─▶ Phase 6 Self-audit
```

---

### Phase 0 — Scope
State, in 2–3 lines: the exact question, the time-frame (e.g. "as of 2026"), and what a complete answer
covers. This frames retrieval and prevents drift.

### ⛔ GATE A — Confirm scope
Present the scope. Ask via `AskUserQuestion`:
- **Question:** "Is this the right scope and framing for the research?"
- **Options:** `Looks right — proceed` · `Adjust scope/time-frame` · `Different angle entirely`
- If not "proceed", revise and re-present. Then continue to Phase 1.

### Phase 1 — Perspective discovery (de-monocultured)
STORM mines perspectives from existing encyclopedia structure, which reproduces a single source's
framing. Instead, deliberately assemble **4–6 distinct perspectives** spanning stakeholders and
disciplines. **Two are mandatory:**
- a **primary-source / originator** perspective (the people/institutions who made or own the thing), and
- a **skeptic / critic** perspective (who disputes the mainstream account and why).

Do not derive all perspectives from one source. Name each perspective and the *kind* of source likely to
serve it (primary docs, practitioners, regulators, critics, peer-reviewed studies, etc.).

### ⛔ GATE B — Approve the perspectives
List the proposed perspectives (name + source type) as text. Ask via `AskUserQuestion`:
- **Question:** "These are the perspectives I'll research from. Approve, or change the mix?"
- **Options:** `Approve all` · `Add a perspective` · `Drop or swap one` · `Re-prioritize`
- Apply edits (use the user's "Other" text if given), re-present if changed, then begin retrieval.

### Phase 2 — Grounded question asking (simulated conversation)
For each approved perspective, generate focused questions. For each question: **Brave search** (helper
script) → pick promising results → `WebFetch` the source → extract an **exact supporting quote**. Then ask follow-up questions as
your understanding updates (this is STORM's "simulated conversation"). Log every usable finding to the
Evidence Ledger. **Prefer primary sources; tier and label every source.** Stop a thread when follow-ups
stop yielding new grounded facts.

### Phase 3 — Verification gate (the core; this is what STORM omits)
For **every** ledger entry, before it is allowed into the article:
1. **Grounding / entailment check** — does the quoted excerpt *actually state* the claim? If the source
   only implies, adjacently mentions, or sounds related, mark **Unsupported** and drop it. This kills
   red herrings.
2. **Over-association check** — if a claim joins two facts ("X, therefore Y" / "X is because of Y"),
   confirm the *link* is in a source, not just the two facts separately. If the link is your inference,
   relabel it inference (Phase 5 quarantine) or drop it.
3. **Independence / corroboration** — cross-check each material claim against **≥2 independent** sources.
   Mark single-source claims **Single-source**. Flag clusters where every source traces to one origin as
   a **bias cluster** (this is source-bias transfer — surface it, don't hide it).
4. **Contradiction** — when sources disagree, mark **Contested** and keep *both* positions with their
   citations. Never average them into a false consensus.

Present a short **Verification Summary** before the gate: counts of `Verified / Single-source / Contested
/ Unsupported(dropped)`, the contested claims, the single-source claims, and any bias clusters — so the
user can see the evidence quality *before* committing to writing.

### ⛔ GATE C — The writing gate (no prose before this passes)
This is the decisive checkpoint. After presenting the Verification Summary, ask via `AskUserQuestion`
(up to two questions in one call):

- **Question 1 — proceed?** "Evidence is verified. Ready to write the article?"
  **Options:** `Write it now` · `Gather more on the gaps first` · `Show me the full ledger` · `Stop here`
- **Question 2 — how to handle weak/contested claims?**
  **Options:** `Verified-only (safest)` · `Include contested + single-source, clearly labeled` ·
  `Include + add an inference section`

If the user chooses to gather more, loop back into Phase 2 on the named gaps and re-present Gate C. Only
on "Write it now" do you proceed to Phase 4. Honor the Question-2 choice when writing.

### Phase 4 — Outline from evidence only
Build the outline from verified evidence clusters — not from what a topic "should" contain. Coverage gaps
become an explicit **"Not established / open questions"** section, never filler. Show the outline as the
first thing in the writing stage (a lightweight confirmation; proceed unless the user objects).

### Phase 5 — Write, every factual sentence cited
- Every factual sentence carries an inline citation `[n]` to a ledger source. **Zero uncited factual
  claims.**
- Inline-mark **(contested)** and **(single-source)** claims; don't state them as settled.
- A dedicated **"What remains unverified / contested"** section is required.
- **Speculation and inference are quarantined** into a clearly labeled "Analysis / inference (not
  sourced)" block, or cut. They never appear in the main body as if sourced. No hedge-filler ("some say",
  "it is believed") standing in for a citation — cite it or cut it.
- Honor the Gate C handling choice (verified-only vs. labeled contested vs. +inference).

### Phase 6 — Adversarial self-audit
Re-scan the finished draft as a hostile fact-checker. Flag and fix: any sentence not traceable to the
ledger; any citation that doesn't support its sentence on re-read; any single-source claim phrased as
settled; any smoothed-over contradiction; any inference that leaked into the sourced body. Report what
you changed.

---

## Evidence Ledger schema

One row per finding:

```
[id] | claim (one sentence) | source URL | exact supporting quote | tier (primary/secondary/tertiary) |
date | independent? (or "derives from [id]") | status (Verified/Single-source/Contested/Unsupported)
```

---

## Final output format

1. **Answer up front** — the verified bottom line in 3–5 sentences (lead with the conclusion).
2. **Article body** — sectioned per the Phase 4 outline; every factual sentence cited `[n]`; contested/
   single-source claims marked inline.
3. **What remains unverified / contested** — gaps, disputes, single-source claims, bias clusters.
4. **Analysis / inference (not sourced)** — optional, clearly fenced off from the sourced body.
5. **Sources & independence** — numbered list with tier and which sources are independent vs. derivative.
6. **Verification summary** — counts: claims verified / single-source / contested / dropped, and a one-
   line confidence statement.

---

## Hard rules (non-negotiable)

- Snippets are leads; **fetch before you cite**.
- **No factual sentence without a quoted, fetched source.**
- Prefer **primary** sources; always label source tier.
- **Preserve contradictions**; never manufacture consensus.
- **Quarantine or cut speculation** — never disguise inference as fact.
- Track **source independence**; expose bias clusters instead of laundering them.
- When evidence is insufficient, **say "not established"** — that is a successful outcome, not a failure.
