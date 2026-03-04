# Migration Guides

Migration guidance for retiring Azure Communication Services (ACS) channels.

**Retirement & Breaking Changes (comprehensive reference):**
https://aka.ms/acs-retirement-and-breaking-changes-guide

---

## Channel-Specific Migration Guides

| Channel | Guide |
|---------|-------|
| Email Service → M365 HVE | https://aka.ms/acs-email-migration |
| SMS API | https://aka.ms/acs-sms-migration |
| Chat SDK | https://aka.ms/acs-chat-migration |
| Calling SDK | https://aka.ms/acs-calling-migration |
| Phone Numbers SDK | https://aka.ms/acs-phone-migration |

---

## Migration Targets

| Channel | Recommended Path |
|---------|-----------------|
| Email | Microsoft 365 High-Volume Email (HVE) |
| Chat | Microsoft Teams Chat (via Microsoft Graph APIs) |
| Calling | Microsoft Teams (Phone Extensibility, Meeting Interop, or Click-2-Call) |
| SMS | Port numbers to a third-party SMS provider |
| Phone Numbers | Port to Teams Phone Extensibility or a third-party provider |

---

**Last Updated:** 2026-02-27
