# ACS Migration Paths

**Policy:** Microsoft first-party solutions only. No third-party or marketplace partners (e.g., SendGrid, Twilio).
**Source:** https://aka.ms/acs-transition-guides
**Last Verified:** 2026-02-27
**Update This File When:** Migration guides are published for SMS, Chat, Calling, or Phone Numbers.

---

## Migration Target by Channel

| Channel | Retiring | Replace With | Base Effort | Guide Status |
|---------|----------|-------------|-------------|-------------|
| **Email Service** | ACS standalone Email SDK | Microsoft 365 High-Volume Email (HVE) | Medium | [Available](../../migration-guides/email/email-service-migration.md) |
| **SMS API** | ACS standalone SMS API | Azure Communication Services SMS (new API) | Low | Pending — https://aka.ms/acs-sms-migration |
| **Chat SDK** | ACS standalone Chat SDK | Microsoft Teams Chat integration | Medium | Pending — https://aka.ms/acs-chat-migration |
| **Calling SDK** | ACS standalone Calling SDK | Microsoft Teams Calling / Azure Communication Services Calling (new API) | High | Pending — https://aka.ms/acs-calling-migration |
| **Phone Numbers SDK** | ACS standalone Phone Numbers SDK | Azure Communication Services Phone Numbers (new API) | Low | Pending — https://aka.ms/acs-phone-migration |

---

## Channel Effort Rationale

| Channel | Why That Effort | Key Migration Challenge |
|---------|----------------|------------------------|
| Email | Medium | Template migration, delivery tracking, SPF/DKIM/DMARC setup for M365 HVE |
| SMS | Low | Simple send/receive API swap; minimal business logic |
| Chat | Medium | Thread history, participant management, UI integration |
| Calling | High | Real-time communications architecture, PSTN routing, SIP trunks |
| Phone Numbers | Low | Number porting and routing configuration only |

---

## Local Migration Guides

| Channel | Local Guide | Status |
|---------|------------|--------|
| Email | [migration-guides/email/email-service-migration.md](../../migration-guides/email/email-service-migration.md) | Complete |
| SMS | migration-guides/sms/sms-migration.md | Not yet created |
| Chat | migration-guides/chat/chat-sdk-migration.md | Not yet created |
| Calling | migration-guides/calling/calling-sdk-migration.md | Not yet created |
| Phone Numbers | migration-guides/phone-numbers/phone-numbers-migration.md | Not yet created |

---

## Microsoft Transition Resources

| Resource | URL |
|----------|-----|
| ACS Retirement overview | https://aka.ms/acs-retirement |
| All transition guides | https://aka.ms/acs-transition-guides |
| Email → M365 HVE | https://aka.ms/acs-email-migration |
| SMS migration | https://aka.ms/acs-sms-migration |
| Chat SDK migration | https://aka.ms/acs-chat-migration |
| Calling SDK migration | https://aka.ms/acs-calling-migration |
| Phone Numbers migration | https://aka.ms/acs-phone-migration |
