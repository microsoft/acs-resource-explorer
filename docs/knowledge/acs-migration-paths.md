# ACS Migration Paths

**Source:** https://aka.ms/acs-retirement-and-breaking-changes-guide
**Last Verified:** 2026-04-21
**Update This File When:** Microsoft publishes updated migration guidance.

---

## Retired Services — Action Required

| Service | Action Required | Replace With | Effort | Guide |
|---------|----------------|-------------|--------|-------|
| **ACS Email** | Migrate before 2028-07-31 | Evaluate Azure Marketplace alternatives (Exchange is NOT a replacement) | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email |
| **ACS SMS** | Migrate before 2028-07-31; port numbers early | Azure Marketplace SMS providers; port via LOA | Low | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms |
| **ACS Advanced Messaging (WhatsApp)** | Migrate before 2028-07-31 | Dynamics 365, Copilot Studio WhatsApp channels, or another BSP | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| **ACS Chat** | Migrate before 2028-07-31; export chat history | Microsoft Graph APIs + Microsoft Teams Chat | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat |
| **ACS Chat for Teams Meeting Interop** | Migrate before 2028-07-31 | Microsoft Graph Chat APIs | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat |
| **ACS Rooms** | Migrate before 2028-07-31 | Teams Meetings via Microsoft Graph API | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| **ACS Number Management (Direct Offer)** | Port numbers before 2028-07-31 | Teams Phone Extensibility (port via support ticket) or third-party provider | Low | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer |
| **ACS Job Router** | Migrate before 2028-07-31 | Evaluate Azure Marketplace alternatives | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide |

---

## Breaking Change Services — Integration Required

| Service | Action Required | Integrate With | Effort | Guide |
|---------|----------------|---------------|--------|-------|
| **ACS Voice/Video Calling SDK** | Integrate with Teams before 2028-07-31 | Teams Phone Extensibility, Teams Meeting Interop, or Teams Click-2-Call | High | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Call Diagnostics** | Integrate with Teams before 2028-07-31 | Teams-aligned calling service | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Call Automation** | Integrate with Teams before 2028-07-31 | Teams Phone Extensibility (recommended) or Teams Meeting Interop | High | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Audio Streaming** | Integrate with Teams before 2028-07-31 | Teams-aligned calling service | High | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Call Recording** | Integrate with Teams before 2028-07-31; export recordings | Teams-aligned calling service | Medium | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Closed Captions** | Integrate with Teams before 2028-07-31 | Teams-aligned calling service | Low | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| **ACS Web UI Library SDK** | Transition before 2028-07-31 or fork for ongoing maintenance | Teams-native experiences or custom UI with Teams extensibility | High | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| **ACS Mobile UI Library SDK** | Transition before 2028-07-31 or fork for ongoing maintenance | Teams-native experiences or custom UI with Teams extensibility | High | https://aka.ms/acs-retirement-and-breaking-changes-guide |

---

## Breaking Change — Supported Teams-Aligned Services

To continue receiving support after July 31, 2028, breaking change services must be used with one of:

1. **Microsoft Teams Phone Extensibility (TPE)** — recommended for PSTN/Call Automation scenarios
2. **Microsoft Teams Meeting Interoperability** — recommended for meeting/conferencing scenarios
3. **Microsoft Teams Click-2-Call for Teams Voice Apps**

---

## Per-Service Migration Detail

### ACS Email
- Exchange is NOT a replacement (Exchange = person-to-person; ACS Email = application-to-recipient)
- SMTP follows the same retirement timeline as Email

### ACS SMS
- Port numbers using carrier LOA process; short codes can also be ported
- Re-verification with SMS aggregator required after porting (possible downtime)
- Engage new provider early — short code provisioning timelines vary

### ACS Advanced Messaging (WhatsApp)
- Dynamics 365 and Copilot Studio WhatsApp channels are NOT affected — only ACS-based integration
- Phone number migration to another BSP available if target BSP supports the migration process

### ACS Chat
- Archive chat history before retirement date
- Teams interop chat: migrate to Microsoft Graph Chat APIs

### ACS Rooms
- ACS Rooms and Teams Meetings are similar but exist in different environments — no direct migration path
- Use Microsoft Graph API to create and manage Teams meetings programmatically

### ACS Number Management (Direct Offer)
- Remove phone numbers BEFORE deleting ACS resource (orphaned numbers continue to incur charges)
- Port to Teams Phone Extensibility: open support ticket with Service Desk - TNM

### ACS Call Automation
- Teams Phone Extensibility (TPE) is the recommended path
- Bidirectional Streaming, Cognitive Services, and AI Integration remain supported through retirement period

### ACS Call Recording
- Export recordings from built-in temporary storage before retirement date

### ACS UI Libraries (Web & Mobile)
- Libraries remain open source but Microsoft will not accept upstream changes or PRs
- Fork and maintain independently if ongoing evolution is needed
- Virtual Appointments on Teams interop: continue to be supported during retirement period

---

## Microsoft Transition Resources

| Resource | URL |
|----------|-----|
| Retirement & Breaking Changes (comprehensive) | https://aka.ms/acs-retirement-and-breaking-changes-guide |
| Email Retirement Guide | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email |
| SMS Retirement Guide | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms |
| Chat Retirement Guide | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat |
| Calling SDK Breaking Change Guide | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| Phone Numbers Retirement Guide | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer |
| Dynamics 365 customers | https://aka.ms/D365ACSDeprecationGuide |