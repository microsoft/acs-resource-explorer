# Migration Guides

Migration guidance for retiring Azure Communication Services (ACS) channels.

**Retirement & Breaking Changes (comprehensive reference):**
https://aka.ms/acs-retirement-and-breaking-changes-guide

---

## Channel-Specific Migration Guides

| Channel | Guide |
|---------|-------|
| Email Service | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email |
| SMS API | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms |
| Chat SDK | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat |
| Calling SDK | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk |
| Phone Numbers SDK | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer |

---

## Migration Targets

| Channel | Recommended Path |
|---------|-----------------|
| Email | Evaluate Azure Marketplace alternatives (Exchange / HVE is NOT a replacement) |
| Chat | Microsoft Teams Chat (via Microsoft Graph APIs) |
| Calling | Microsoft Teams (Phone Extensibility, Meeting Interop, or Click-2-Call) |
| SMS | Port numbers to a third-party SMS provider via LOA |
| Phone Numbers | Port to Teams Phone Extensibility or a third-party provider |

---

**Last Updated:** 2026-02-27
