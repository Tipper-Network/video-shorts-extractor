# Instincts

Behavioral rules agents internalize. Unlike skills (how to use tools), instincts define **judgment calls** and **non-negotiables**.

## How to Use

1. Every pipeline agent reads [content-pipeline.md](content-pipeline.md) before acting
2. Role-specific instinct files add constraints for that domain
3. When an agent makes a bad call, add a rule here — don't just fix the one manifest

## Files

| File | Audience |
|------|----------|
| [content-pipeline.md](content-pipeline.md) | All pipeline agents |
| [llm-planning.md](llm-planning.md) | Chapter Planner, Shorts Planner (Cursor agent) |
| [orchestration.md](orchestration.md) | Orchestrator |
| [qa-review.md](qa-review.md) | QA Reviewer |

## Instinct vs Skill vs Agent Doc

| Layer | Question it answers |
|-------|---------------------|
| **Instinct** | What must never happen? What does good judgment look like? |
| **Skill** | What commands, schemas, and steps to execute? |
| **Agent doc** | Who owns which inputs/outputs and handoffs? |

## Updating

When adding an instinct:

```markdown
<!-- added: YYYY-MM-DD | reason: one-line why -->
- Rule text as imperative (Always / Never / Prefer)
```

Mark superseded rules instead of deleting when history matters.
