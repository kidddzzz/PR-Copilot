# Pitch Deck Outline — PR Copilot

A 48-hour hackathon deck should be short and demo-forward: 8-9 slides max.
Judges skim fast — the live demo carries most of the weight, not the slides.

## Slide 1 — Title
Project name, one-line tagline, team name/members, "Built with IBM Bob 2.0."

## Slide 2 — The Problem
State it in numbers, not adjectives: "Developers spend X hours/week on code
review. Y% of that time goes to repetitive checks (style, missing tests,
obvious bugs) instead of architectural judgment."

## Slide 3 — Our Solution (one sentence + visual)
"PR Copilot runs 5 specialized AI reviewers in parallel on every PR, then
merges their findings into one prioritized report — so human reviewers
spend time only where judgment is actually needed." Show a simple
before/after: messy PR → clean prioritized report.

## Slide 4 — How It Works (architecture)
Diagram: PR opened → dispatched to 5 subagents in parallel (Style,
Security, Correctness, Testing, Docs) → orchestrator merges/ranks →
posted back to PR. Keep this visual, not text-heavy — judges study this
slide the most.

## Slide 5 — Bob 2.0 Features We Used
Map the build directly to the challenge requirements:
- **Agent mode** → Correctness agent traces logic across functions
- **Subagents** → 5 specialized reviewers, each scoped narrowly
- **Parallel tasks** → all 5 run simultaneously, not sequentially
- **Document understanding** → Style agent reads CONTRIBUTING.md, Docs
  agent reads README.md

## Slide 6 — Live Demo
(Placeholder slide — switch to the actual live demo here.) Run PR Copilot
against demo-repo/, show the real merged output.

## Slide 7 — Impact (the numbers slide)
"Manual review of this PR: ~X min, caught Y of 4 issues. PR Copilot: ~Z
seconds, caught 4 of 4, auto-flagged 2 as blocking." Bar chart or simple
side-by-side works better than a paragraph.

## Slide 8 — What's Next
1-2 lines on what you'd build with more time (auto-fix for trivial
issues, learning from reviewer feedback, multi-language support).

## Slide 9 — Team & Thank You
Names, roles, link to the GitHub repo.

---

## Video tip
Since submission needs a video: screen-record slides 1-3 narrated
briefly, then spend most of the video on the live demo (slide 6) and
impact numbers (slide 7) — that's what judges actually remember.
