---
name: project-tipper
description: "Core platform overview — stack, monorepo structure, and active roadmap state"
metadata: 
  node_type: memory
  type: project
  originSessionId: 91fa3306-f460-4761-9dd7-328dde31ac87
---

Tipper is an invite-only social platform (community-based, entity/community model). Monorepo: `apps/api` (NestJS + Prisma/ZModel), `apps/web` (Next.js App Router), `packages/shared` (enums, contracts).

**Active work (2026-07-16):** Stage 2 — Subscription structure. Stage 1 (membership A/B/C structure) shipped 2026-07-15.
**Why:** Stage 2 completes the commercial layer: Kind B + Kind A bundle activation, cash payment, entitlement ledger, redemption.
**How to apply:** All new work should fit Stage 2 money module or be deferred. No Nest reorg, no Tipper SaaS tiers yet.

**Stage sequence:**
- Stage 1 — Membership structure ✅ FINAL (2026-07-15): A/B/C, D1–D7, Kind C grant, D4 helper.
- Stage 2 — Subscription structure ← ACTIVE: commercial catalog, contracts, cash/redeem, affiliation-first (PC9). Migration pending (`commercial_affiliation_id` in schema). GAF cash smoke not yet done.
- Stage 3 — Hard Port working project (deferred)
- Stage 4 — Partnerships platform-wide (deferred)

**Money module (Stage 2) — shipped 2026-07-15:**
- Schema: `apps/api/schema/money/` (commercial-catalog, contract-ledger, redemption)
- Services: `apps/api/src/money/` (catalog, contract, activation, ledger, redemption, summary, payment)
- Controller: `POST/GET money/*` endpoints live

**Next actions (Stage 2):**
1. `pnpm run prisma:migrate:dev` in `apps/api` (commercial_affiliation_id migration pending)
2. GAF cash smoke: enable → product → contract (PENDING B) → confirm → summary → redeem
3. Patron catalog: `entitlements[]` multi-item create
4. Web flows after smoke

**Known bugs introduced 2026-07-15:**
- Balance check in `RedemptionService.commitByNonce` is outside the transaction (race condition)
- Billing period uses 30-day hardcode, not calendar month
- Subscription activation fires no `MEMBERSHIP_MEMBER_JOINED` domain event (ensureActiveMembership called with tx skips event)
- `getCommunityAccess` has hardcoded PUBLIC privacy (pre-existing)

Planning docs: `todaysgoals.md`, `inprogress.md`, `tomorrow.md`, `done.md` at repo root.
Schema source of truth: `apps/api/schema/` (ZModel → Prisma). Shared enums: `packages/shared/src/enums/`.
