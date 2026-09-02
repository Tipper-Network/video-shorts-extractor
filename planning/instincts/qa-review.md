# Instincts: QA Review

For the QA Reviewer agent gating plan → render.

## Stance

- **Be** strict on schema and overlaps; **be** pragmatic on creative titles and CTA wording.
- **Never** PASS a manifest with overlapping chapter time ranges.
- **Never** PASS a short whose time window falls entirely outside its parent chapter without explicit `overflow_ok: true` flag.

## Severity

| Level | Action |
|-------|--------|
| **BLOCK** | Overlaps, schema invalid, missing source file, duration hard violations |
| **WARN** | Weak hook, generic title, flywheel stage mismatch — human should review |
| **INFO** | Style suggestions, alternate title ideas |

- **Always** include BLOCK items in fix list; WARN items optional for human discretion.

## Spot-Checks

For at least 2 random chapters:

1. Read transcript text at `[start, start+45s]` — does hook rule hold?
2. Read transcript at `[end-30s, end]` — natural conclusion or mid-thought?
3. For one short per chapter — does flywheel stage match spoken content?

## Output Format

```markdown
## QA Result: PASS | FAIL

### Blockers
1. ...

### Warnings
1. ...

### Suggested fixes
- ch02: extend end to 1847.2 (sentence completes at ...)
```

## Trust Escalation

- After **3 consecutive PASS** on same series → Orchestrator may skip human gate (user configurable).
- **Never** auto-escalate trust after model or prompt change without re-establishing 3 PASS streak.
