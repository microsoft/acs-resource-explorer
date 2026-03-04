# ACS Channel Status — Retirement vs. Breaking Change

**Source:** https://aka.ms/acs-retirement-and-breaking-changes-guide
**Announcement Date:** March 18, 2026
**Effective Date:** March 31, 2029
**Last Verified:** 2026-02-27

---

## Project Channel Status (5 channels in scope)

| Channel | Status Type | Effective Date | What Happens | Guide |
|---------|------------|---------------|-------------|-------|
| **Email Service** | 🔴 Retirement | 2029-03-31 | Service completely removed. Must migrate before retirement date. | https://aka.ms/acs-email-migration |
| **SMS API** | 🔴 Retirement | 2029-03-31 | Service completely removed. Port numbers to another provider. | https://aka.ms/acs-sms-migration |
| **Chat SDK** | 🔴 Retirement | 2029-03-31 | Service completely removed. Migrate to Microsoft Graph APIs + Teams Chat. | https://aka.ms/acs-chat-migration |
| **Calling SDK** | 🟡 Breaking Change | 2029-03-31 | Service continues but standalone use unsupported. Must integrate with Teams. | https://aka.ms/acs-calling-migration |
| **Phone Numbers (Direct Offer)** | 🔴 Retirement | 2029-03-31 | Service completely removed. ⚠️ New customers cannot acquire numbers after March 18, 2026. | https://aka.ms/acs-phone-migration |

---

## Definitions

**🔴 Retirement** — The service is permanently discontinued. After March 31, 2029, operations will no longer be permitted and APIs/SDKs will return errors. Customers must migrate to a replacement before the retirement date.

**🟡 Breaking Change** — The service continues but standalone use (human-to-human or application-to-human without Teams) will no longer be supported. A new major-version SDK will be provided. Customers must integrate with one of the following Teams-aligned services:
- Microsoft Teams Phone Extensibility
- Microsoft Teams Meeting Interoperability
- Microsoft Teams Click-2-Call for Teams Voice Apps

---

## Full ACS Impacted Services (all channels, not just project scope)

### Retired after March 31, 2029
- ACS Email
- ACS SMS
- ACS Advanced Messaging w/ WhatsApp
- ACS Chat
- ACS Chat for Teams Meeting Interop
- ACS Rooms
- ACS Number Management (Direct Offer)
- ACS Job Router

### Breaking Change — must use with Teams/Dynamics 365/Copilot Studio
- ACS Voice/Video Calling SDK
- ACS Call Diagnostics
- ACS Call Automation
- ACS Audio Streaming
- ACS Call Recording
- ACS Closed Captions
- ACS Web UI Library SDK
- ACS Mobile UI Library SDK

---

## Key Per-Channel Notes

### Email — Retirement
- Can still onboard new resources during the retirement period
- No direct Microsoft-provided migration path; evaluate Azure Marketplace alternatives
- Exchange is NOT a replacement (different use case — person-to-person, not application-to-recipient)
- SMTP follows the same retirement timeline as Email

### SMS — Retirement
- Existing customers with phone numbers before March 18, 2026 can acquire additional numbers
- New ACS resources after March 18, 2026 cannot acquire new numbers
- Port existing numbers to another provider (LOA required; short codes can also be ported)

### Chat — Retirement
- Chat history maintained per storage policies until March 31, 2029 — export before retirement
- Recommended path: Microsoft Graph APIs with Microsoft Teams

### Calling SDK — Breaking Change
- No immediate changes; all deployed calling scenarios continue until March 31, 2029
- New major-version SDK will be provided for Teams-aligned integration
- Supported paths: Teams Phone Extensibility, Teams Meeting Interop, Teams Click-2-Call

### Phone Numbers (Direct Offer) — Retirement
- **Immediate impact (March 18, 2026):** New customers creating ACS resources after announcement cannot acquire phone numbers
- Existing customers with pre-existing ACS resources and phone numbers can continue acquiring numbers up to quota
- Can port numbers to Teams Phone Extensibility (submit Azure Support ticket)
- Can port numbers to third-party providers

---

## Dynamics 365 Customers
If using ACS via Dynamics 365, see the separate guide:
https://aka.ms/D365ACSDeprecationGuide

---

## General Timeline

| Date | Event |
|------|-------|
| March 18, 2026 | Microsoft notification date — retirement period begins |
| March 18, 2026 | **Immediate:** New customers cannot acquire phone numbers or short codes |
| March 31, 2029 | All retired services decommissioned; breaking change enforcement begins |
