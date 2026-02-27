# ACS Retirement Dates

**Source:** https://aka.ms/acs-retirement
**Last Verified:** 2026-02-27
**Update This File When:** Microsoft confirms retirement dates for SMS, Chat, Calling, or Phone Numbers.

---

## Retirement Status by Channel

| Channel | Status | Retirement Date | Announcement |
|---------|--------|----------------|-------------|
| Email Service (standalone ACS SDK) | Deprecated | **2027-12-31** | Confirmed |
| SMS API (standalone ACS SDK) | Deprecated | TBD | Monitor https://aka.ms/acs-retirement |
| Chat SDK (standalone ACS SDK) | Deprecated | TBD | Monitor https://aka.ms/acs-retirement |
| Calling SDK (standalone ACS SDK) | Deprecated | TBD | Monitor https://aka.ms/acs-retirement |
| Phone Numbers SDK (standalone ACS SDK) | Deprecated | TBD | Monitor https://aka.ms/acs-retirement |

> **Note:** "Standalone ACS SDK" means the service accessed via ACS directly. Resources that use these channels through Microsoft Teams or M365 integrations are **not** affected.

---

## Urgency Tiers (for impact analysis)

| Days Until Retirement | Urgency | Effect on Severity |
|-----------------------|---------|-------------------|
| < 30 days | IMMEDIATE | Override to Critical regardless of usage |
| < 90 days | HIGH | Escalate severity one level |
| < 180 days | ELEVATED | Add urgency flag to report |
| > 180 days | NORMAL | Standard severity thresholds apply |

---

## What Is NOT Retiring

The following **continue to work** and are the recommended migration targets:

- Microsoft 365 High-Volume Email (HVE) — replaces ACS Email
- Microsoft Teams telephony and calling — replaces ACS Calling SDK
- Microsoft Teams Chat — replaces ACS Chat SDK
- Azure Communication Services resource itself — only the standalone SDKs are retiring

---

## Key Links

- Retirement announcements: https://aka.ms/acs-retirement
- Transition guides: https://aka.ms/acs-transition-guides
- This project's full guide (Email): [migration-guides/email/email-service-migration.md](../../migration-guides/email/email-service-migration.md)
