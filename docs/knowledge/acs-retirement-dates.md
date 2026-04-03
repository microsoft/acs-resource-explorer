# ACS Retirement Dates

**Source:** https://aka.ms/acs-retirement-and-breaking-changes-guide
**Planned Announcement Date:** 2026-07-15
**Last Verified:** 2026-02-27
**Update This File When:** Microsoft publishes updates to the retirement guide.

---

## Channel Status by Project Scope

| Channel | Status Type | Effective Date | Notes |
|---------|------------|---------------|-------|
| Email Service | 🔴 Retirement | **2028-07-31** | Updated 2026-04-02 |
| SMS API | 🔴 Retirement | **2028-07-31** | ⚠️ New number acquisition restricted for new ACS resources after 2026-07-15 |
| Chat SDK | 🔴 Retirement | **2028-07-31** | Confirmed |
| Calling SDK | 🟡 Breaking Change | **2028-07-31** | Service continues — standalone use unsupported; must integrate with Teams |
| Phone Numbers (Direct Offer) | 🔴 Retirement | **2028-07-31** | ⚠️ New customers cannot acquire numbers after 2026-07-15 |

> **Retirement** = service completely removed, operations will fail after effective date.
> **Breaking Change** = service continues but standalone use loses support; Teams integration required.

> **Note:** "Standalone ACS SDK" means the service accessed via ACS directly without Teams/Dynamics 365/Copilot Studio. Resources using these channels through Microsoft Teams integrations are **not** affected.

---

## Urgency Tiers

| Days Until Effective Date | Urgency |
|--------------------------|---------|
| < 30 days | IMMEDIATE |
| < 90 days | HIGH |
| < 180 days | ELEVATED |
| > 180 days | NORMAL |

---

## What Is NOT Retiring

The following **continue to work** and are the recommended paths forward:

- Microsoft 365 High-Volume Email (HVE) — alternative for ACS Email workloads
- Microsoft Teams Chat (via Graph API) — alternative for ACS Chat workloads
- Microsoft Teams Phone Extensibility — allows ACS Calling SDK to continue with Teams
- Microsoft Teams Meeting Interoperability — allows ACS Calling SDK to continue with Teams
- Azure Communication Services resource itself — only the standalone SDK usage is affected

---

## Key Links

- Retirement & Breaking Changes (comprehensive): https://aka.ms/acs-retirement-and-breaking-changes-guide
- Email: https://aka.ms/acs-email-migration
- SMS: https://aka.ms/acs-sms-migration
- Chat: https://aka.ms/acs-chat-migration
- Calling (Breaking Change): https://aka.ms/acs-calling-migration
- Phone Numbers: https://aka.ms/acs-phone-migration
