---
name: project-stage2-money
description: "Stage 2 money module — what's shipped, known bugs, what's pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7f7624e3-1c8d-4e99-944a-8c0c8e4ec8de
---

**Shipped 2026-07-15 — Stage 2 money module:**

Schema (`apps/api/schema/money/`):
- `commercial-catalog.zmodel` — EntityCommercialProgram, CommercialProduct, CommercialProductEntitlement
- `contract-ledger.zmodel` — SubscriptionContract, PaymentInstruction, EntitlementAccount, LedgerEntry
- `redemption.zmodel` — RedemptionIntent, RedemptionCommit
- `affiliations.zmodel` — ProfileCommercialAffiliation now has `subscription_id` mirror + `membership_tier`

Services (`apps/api/src/money/`):
- `CommercialCatalogService` — enableProgram, createProduct, ensureSubscriberPosition
- `SubscriptionContractService` — createPendingCashContract (affiliation-first / PC9)
- `ContractActivationService` — confirmCashAndActivate (D5 saga: payment → ledger → Kind B ACTIVE → Kind A)
- `EntitlementLedgerService` — creditPurchase, debitRedemption, sumBalance
- `RedemptionService` — createIntent (patron QR), commitByNonce (staff scan), peekByNonce
- `SubscriptionSummaryService` — getPatronSummary
- `PaymentInstructionService` — thin wrapper over ContractActivationService (candidate for removal)

Stage 2 also shipped (membership commit `a5a01ae`):
- `OperationalAffiliationService` — grantOperationalAffiliation, listOperationalAffiliations
- `EntityPermissionService` upgraded — isOwnerOrActiveKindCOrAdmin, assertOwnerOrAdmin

**Known bugs / tech debt:**
- `commitByNonce`: `sumBalance` called OUTSIDE transaction → race condition under concurrent redemptions. Fix: move balance check inside the $transaction block.
- `confirmCashAndActivate`: `periodEnd.setUTCDate(+30)` should be `setUTCMonth(+1)` for correct monthly billing.
- `membership_tier: product.slug` — tier is coupled to slug naming. Add `tier_key` field to CommercialProduct.
- `PaymentInstructionService` is a pointless pass-through — delete it, export ContractActivationService directly.
- `ensureStaffPosition` and `ensureSubscriberPosition` are duplicated — extract to shared utility.
- Subscription activation fires no `MEMBERSHIP_MEMBER_JOINED` domain event (tx path skips publishing). Downstream welcome/analytics flows won't see subscription-bundled joins.

**Test gaps:**
- `ContractActivationService` — no success/happy-path test for D5 saga. Only forbidden path tested.
- `RedemptionService` — no commit-success test; no expired-intent test.

**Pending (before Stage 2 smoke):**
- `pnpm run prisma:migrate:dev` in `apps/api` (commercial_affiliation_id migration)
- GAF cash smoke: enable → product → contract → confirm → summary → redeem
- Multi-entitlement product create

**Why:** Stage 2 goal is cash-only subscription for a real venue operator, bundling community membership automatically (Kind A + Kind B, always together).
**How to apply:** Don't touch payment rail beyond CASH yet. No card/mobile-money until Stage 3+. Any new subscription work should go through the affiliation-first (PC9) path.
