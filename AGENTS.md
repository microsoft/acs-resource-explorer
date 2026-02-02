# Agents

## ACS Transition Agent

Purpose: Help customers assess Azure Communication Services (ACS) deprecations and navigate migration guidance to Microsoft 365 integrated solutions.

Primary capabilities (skills):
- ACS deprecation scan (detects usage across Email, SMS, Chat, Calling, Phone Numbers)
- Migration guide retrieval (per retiring feature)
- Severity classification (Critical/Warning/Info based on retirement timeline and usage)
- CSV export of results (per resource and channel)

Skill manifests:
- .github/skills/acs-deprecation-scan/SKILL.md

Execution targets:
- Web app API (Next.js routes)
- CLI wrappers (optional)

Authentication:
- Azure AD (MSAL) for user-delegated access to subscription data

Data handling:
- No persistent storage required for MVP. Results are generated on demand.
