# ACS Migration Paths

**Policy:** Microsoft first-party solutions only. No third-party or marketplace partners (e.g., SendGrid, Twilio).
**Source:** https://aka.ms/acs-retirement-and-breaking-changes-guide
**Last Verified:** 2026-02-27
**Update This File When:** Microsoft publishes updated migration guidance.

---

## Action Required by Channel

| Channel | Status Type | Action Required | Replace With / Integrate With | Effort | Guide |
|---------|------------|----------------|------------------------------|--------|-------|
| **Email Service** | 🔴 Retirement | Migrate before 2028-07-31 | Evaluate Azure Marketplace alternatives (no direct Microsoft replacement) | Medium | https://aka.ms/acs-email-migration |
| **SMS API** | 🔴 Retirement | Migrate before 2028-07-31; port numbers now if needed | Azure Marketplace SMS providers | Low | https://aka.ms/acs-sms-migration |
| **Chat SDK** | 🔴 Retirement | Migrate before 2028-07-31; export chat history | Microsoft Graph APIs + Microsoft Teams Chat | Medium | https://aka.ms/acs-chat-migration |
| **Calling SDK** | 🟡 Breaking Change | Integrate with Teams before 2028-07-31 | Microsoft Teams Phone Extensibility, Teams Meeting Interop, or Teams Click-2-Call | High | https://aka.ms/acs-calling-migration |
| **Phone Numbers (Direct Offer)** | 🔴 Retirement | Port numbers before 2028-07-31 | Teams Phone Extensibility (port via support ticket) or third-party provider | Low | https://aka.ms/acs-phone-migration |

---

## Effort Rationale

| Channel | Why That Effort | Key Migration Challenge |
|---------|----------------|------------------------|
| Email | Medium | No direct Microsoft replacement; evaluate alternatives; SPF/DKIM/DMARC changes |
| SMS | Low | Port numbers to new provider; re-verification required; LOA process |
| Chat | Medium | Export chat history; update to Graph API; thread/participant model differences |
| Calling | High | Teams integration architecture; PSTN routing; new major-version SDK required |
| Phone Numbers | Low | Number porting and routing reconfiguration; submit support ticket for Teams port |

---

## Calling SDK — Breaking Change Detail

The Calling SDK is a **Breaking Change**, not a retirement. The service continues but standalone use (without Teams) loses support after July 31, 2028.

**Supported paths to continue receiving support:**
1. Microsoft Teams Phone Extensibility (TPE) — recommended for PSTN/Call Automation scenarios
2. Microsoft Teams Meeting Interoperability — recommended for meeting/conferencing scenarios
3. Microsoft Teams Click-2-Call for Teams Voice Apps

A new major-version SDK will be provided. Customers have until July 31, 2028 to migrate to the new SDK.

---

## Local Migration Guides

No local migration guides are present in this repository. All guides are available via Microsoft's official resources below.

---

## Microsoft Transition Resources

| Resource | URL |
|----------|-----|
| Retirement & Breaking Changes (comprehensive) | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| Email Retirement Guide | https://aka.ms/acs-email-migration |
| SMS Retirement Guide | https://aka.ms/acs-sms-migration |
| Chat Retirement Guide | https://aka.ms/acs-chat-migration |
| Calling SDK Breaking Change Guide | https://aka.ms/acs-calling-migration |
| Phone Numbers Retirement Guide | https://aka.ms/acs-phone-migration |
| Dynamics 365 customers | https://aka.ms/D365ACSDeprecationGuide |
