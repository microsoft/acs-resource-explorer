# ACS Channel Status — Retirement vs. Breaking Change

**Source:** https://aka.ms/acs-retirement-and-breaking-changes-guide
**Planned Announcement Date:** July 22, 2026
**Effective Date:** July 31, 2028
**Last Verified:** 2026-04-21

---

## Retired Services (will no longer be available after July 31, 2028)

| Service | Status Type | Effective Date | What Happens | Guide |
|---------|------------|---------------|-------------|-------|
| **ACS Email** | 🔴 Retirement | 2028-07-31 | Service completely removed. No direct Microsoft replacement — evaluate Azure Marketplace. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email |
| **ACS SMS** | 🔴 Retirement | 2028-07-31 | Service completely removed. Port numbers to another provider. ⚠️ New number acquisition restricted after July 22, 2026. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms |
| **ACS Advanced Messaging (WhatsApp)** | 🔴 Retirement | 2028-07-31 | Service completely removed. Migrate to Dynamics 365, Copilot Studio, or another BSP. | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| **ACS Chat** | 🔴 Retirement | 2028-07-31 | Service completely removed. Migrate to Microsoft Graph APIs + Teams Chat. Export chat history before retirement. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat |
| **ACS Chat for Teams Meeting Interop** | 🔴 Retirement | 2028-07-31 | Service completely removed. Migrate to Microsoft Graph Chat APIs. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat |
| **ACS Rooms** | 🔴 Retirement | 2028-07-31 | Service completely removed. Migrate to Teams Meetings via Microsoft Graph API. | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| **ACS Number Management (Direct Offer)** | 🔴 Retirement | 2028-07-31 | Service completely removed. ⚠️ New customers cannot acquire numbers after July 22, 2026. Port to Teams Phone Extensibility or third-party provider. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer |
| **ACS Job Router** | 🔴 Retirement | 2028-07-31 | Service completely removed. Evaluate Azure Marketplace alternatives. | https://aka.ms/acs-retirement-and-breaking-changes-guide |

---

## Breaking Change Services (standalone use unsupported after July 31, 2028)

| Service | Status Type | Effective Date | What Happens | Guide |
|---------|------------|---------------|-------------|-------|
| **ACS Voice/Video Calling SDK** | 🟡 Breaking Change | 2028-07-31 | Standalone use unsupported. Must integrate with Teams Phone Extensibility, Teams Meeting Interop, or Teams Click-2-Call. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Call Diagnostics** | 🟡 Breaking Change | 2028-07-31 | Must use in conjunction with a supported Teams-aligned service. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Call Automation** | 🟡 Breaking Change | 2028-07-31 | Must integrate with Teams Phone Extensibility or Teams Meeting Interop. New major-version SDK provided. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Audio Streaming** | 🟡 Breaking Change | 2028-07-31 | Must use with a supported Teams-aligned service. No standalone replacement in Microsoft Marketplace. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Call Recording** | 🟡 Breaking Change | 2028-07-31 | Must use with a supported Teams-aligned service. Export existing recordings before retirement. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Closed Captions** | 🟡 Breaking Change | 2028-07-31 | Must use with a supported Teams-aligned service. | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Web UI Library SDK** | 🟡 Breaking Change | 2028-07-31 | Open source; remains available during retirement period. No new features — break/fix only. Customers may fork independently. | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| **ACS Mobile UI Library SDK** | 🟡 Breaking Change | 2028-07-31 | Open source; remains available during retirement period. No new features — break/fix only. Customers may fork independently. | https://aka.ms/acs-retirement-and-breaking-changes-guide |

---

## Definitions

**🔴 Retirement** — The service is permanently discontinued. After July 31, 2028, operations will no longer be permitted and APIs/SDKs will return errors. Customers must migrate to a replacement before the retirement date.

**🟡 Breaking Change** — The service continues but standalone use (human-to-human or application-to-human without Teams) will no longer be supported. Customers must integrate with one of the following Teams-aligned services:
- Microsoft Teams Phone Extensibility
- Microsoft Teams Meeting Interoperability
- Microsoft Teams Click-2-Call for Teams Voice Apps

---

## Key Per-Service Notes

### Email — Retirement
- Can still onboard new resources during the retirement period
- No direct Microsoft-provided migration path; evaluate Azure Marketplace alternatives
- Exchange is NOT a replacement (different use case — person-to-person, not application-to-recipient)
- SMTP follows the same retirement timeline as Email

### SMS — Retirement
- Existing customers with phone numbers before July 22, 2026 can continue to acquire additional numbers
- New ACS resources created after July 22, 2026 cannot acquire new numbers or short codes
- Port existing numbers to another provider (LOA required; short codes can also be ported)

### Advanced Messaging (WhatsApp) — Retirement
- ACS WhatsApp deprecation applies only to Azure Communication Services — not Dynamics 365 or Copilot Studio
- Existing integrations continue to function during the retirement period
- Migrate to: Dynamics 365, Copilot Studio WhatsApp channels, or another Business Solution Provider (BSP)

### Chat — Retirement
- Chat history maintained per storage policies until July 31, 2028 — export before retirement
- Recommended path: Microsoft Graph APIs with Microsoft Teams

### Rooms — Retirement
- No direct migration path from ACS Rooms to Teams Meetings
- Migrate to Teams Meetings via Microsoft Graph API (similar functionality, different environment)

### Number Management (Direct Offer) — Retirement
- **Immediate impact (July 22, 2026):** New customers creating ACS resources after the planned announcement cannot acquire phone numbers
- Existing customers with pre-existing ACS resources and phone numbers can continue acquiring numbers up to quota
- Can port numbers to Teams Phone Extensibility (submit Azure Support ticket)
- Remove phone numbers before deleting an ACS resource to avoid orphaned number charges

### Voice/Video Calling SDK — Breaking Change
- No immediate changes; all deployed calling scenarios continue until July 31, 2028
- New major-version SDK will be provided for Teams-aligned integration
- Supported paths: Teams Phone Extensibility, Teams Meeting Interop, Teams Click-2-Call

### Call Automation — Breaking Change
- Teams Phone Extensibility (TPE) is the recommended path
- Bidirectional Streaming, Cognitive Services, and AI Integration remain supported through retirement period

### Call Recording — Breaking Change
- Export existing recordings from built-in temporary storage before retirement date

### UI Libraries (Web & Mobile) — Breaking Change
- Will remain open source during retirement period until July 31, 2028
- Microsoft will not accept upstream changes, feature additions, or dependency upgrades
- Virtual Appointments scenarios on Teams interop continue to be supported during retirement period

---

## Dynamics 365 Customers
If using ACS via Dynamics 365, see the separate guide:
https://aka.ms/D365ACSDeprecationGuide

---

## General Timeline

| Date | Event |
|------|-------|
| July 22, 2026 | Planned announcement date — retirement period begins |
| July 22, 2026 | **Immediate:** New customers cannot acquire phone numbers or short codes |
| July 31, 2028 | All retired services decommissioned; breaking change enforcement begins |