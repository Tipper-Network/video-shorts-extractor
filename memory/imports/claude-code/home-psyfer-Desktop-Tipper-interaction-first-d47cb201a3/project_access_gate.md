---
name: project-access-gate
description: "Access gate / earn-access slice — what's shipped, what gaps remain, key files"
metadata: 
  node_type: memory
  type: project
  originSessionId: 91fa3306-f460-4761-9dd7-328dde31ac87
---

**Shipped:** `POST /auth/access/check-email` + `POST /auth/access/request-invite`, `PartialUserService`, `AuthValidateWizard`, intent resolver, earn-access UI flow.

**Known gaps (from `access-gate-remaining.md`):**
- §0 Partial account spine: `submitPlatformAccessRequest` creates `User` only — no `Profile` yet. Blocks pre-auth data attachment (visits, vibes).
- §1 Admin approve → invite email: not built.
- §2 Server-side signup/OAuth gate: `POST /auth/signup` and Google OAuth still open to anyone bypassing UI.
- §3 Locale strings: all earn-access copy is hardcoded English.

**Suggested order (per .md):** §0 → §3 → §2 → §1.

**Why:** Creating `User` + `Profile` must NOT grant access. JWT only after conversion (password set or federated + email_verified + optional platform approval).
**How to apply:** Don't add Profile creation without ensuring partial users cannot receive JWT. `JwtStrategy` already requires a profile id — partial accounts must remain blocked until `upgradePartialUser` completes.
