# ACS Retirement Dates

**Source:** https://aka.ms/acs-retirement-and-breaking-changes-guide
**Planned Announcement Date:** 2026-07-22
**Effective / Retirement Date:** 2028-07-31
**Last Verified:** 2026-04-21
**Update This File When:** Microsoft publishes updates to the retirement guide.

---

## Retired Services (will no longer be available after July 31, 2028)

| Service | Status Type | Effective Date | Notes |
|---------|------------|---------------|-------|
| ACS Email | 🔴 Retirement | **2028-07-31** | No direct Microsoft replacement; evaluate Azure Marketplace |
| ACS SMS | 🔴 Retirement | **2028-07-31** | ⚠️ New number acquisition restricted for new ACS resources after 2026-07-22 |
| ACS Advanced Messaging (WhatsApp) | 🔴 Retirement | **2028-07-31** | Migrate to Dynamics 365, Copilot Studio, or another BSP |
| ACS Chat | 🔴 Retirement | **2028-07-31** | Migrate to Microsoft Graph APIs + Teams Chat |
| ACS Chat for Teams Meeting Interop | 🔴 Retirement | **2028-07-31** | Migrate to Microsoft Graph Chat APIs |
| ACS Rooms | 🔴 Retirement | **2028-07-31** | Migrate to Teams Meetings via Microsoft Graph API |
| ACS Number Management (Direct Offer) | 🔴 Retirement | **2028-07-31** | ⚠️ New customers cannot acquire numbers after 2026-07-22 |
| ACS Job Router | 🔴 Retirement | **2028-07-31** | Evaluate Azure Marketplace alternatives |

---

## Breaking Change Services (must integrate with Teams/Dynamics 365/Copilot Studio after July 31, 2028)

| Service | Status Type | Effective Date | Notes |
|---------|------------|---------------|-------|
| ACS Voice/Video Calling SDK | 🟡 Breaking Change | **2028-07-31** | Must integrate with Teams Phone Extensibility, Teams Meeting Interop, or Teams Click-2-Call |
| ACS Call Diagnostics | 🟡 Breaking Change | **2028-07-31** | Must use with supported Teams-aligned service |
| ACS Call Automation | 🟡 Breaking Change | **2028-07-31** | Must integrate with Teams Phone Extensibility or Teams Meeting Interop |
| ACS Audio Streaming | 🟡 Breaking Change | **2028-07-31** | Must use with supported Teams-aligned service |
| ACS Call Recording | 🟡 Breaking Change | **2028-07-31** | Must use with supported Teams-aligned service |
| ACS Closed Captions | 🟡 Breaking Change | **2028-07-31** | Must use with supported Teams-aligned service |
| ACS Web UI Library SDK | 🟡 Breaking Change | **2028-07-31** | Open source; no new features; break/fix only during retirement period |
| ACS Mobile UI Library SDK | 🟡 Breaking Change | **2028-07-31** | Open source; no new features; break/fix only during retirement period |

---

> **Retirement** = service completely removed; operations will fail after effective date.
> **Breaking Change** = service continues but standalone use loses support; Teams integration required.

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

- Microsoft Teams Phone Extensibility — allows ACS Calling/Call Automation to continue with Teams
- Microsoft Teams Meeting Interoperability — allows ACS Calling SDK to continue with Teams
- Microsoft Teams Click-2-Call for Teams Voice Apps
- Microsoft Graph Chat APIs — replacement for ACS Chat
- Dynamics 365 / Copilot Studio WhatsApp channels — replacement for ACS Advanced Messaging
- ACS Identity — continues to operate in conjunction with supported services
- Azure Communication Services resource itself — only the standalone SDK usage is affected

---

## Key Links

- Retirement & Breaking Changes (comprehensive): https://aka.ms/acs-retirement-and-breaking-changes-guide
- Email: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email
- SMS: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms
- Chat: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat
- Calling (Breaking Change): https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk
- Phone Numbers: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer
- Dynamics 365 customers: https://aka.ms/D365ACSDeprecationGuide