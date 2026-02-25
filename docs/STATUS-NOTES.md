# Azure Transition Agent — Status Notes

**Date:** 2026-02-25
**Project:** Azure Transition Agent (ACS first implementation)
**Repo:** [ACS-Transition-Agent-v0](https://github.com/jameelaesa/ACS-Transition-Agent-v0)
**Stage:** Forming — Active Development / Pre-MVP

---

## Problem & Solution

**Problem:** Azure customers, PMs, and support teams face a time-intensive manual process when retiring a service — they must help customers identify which subscriptions and resources are actively using the retiring services, across potentially hundreds of subscriptions.

**Solution:** We're building Azure Agent Skills that automate the full assessment workflow: scan resources, detect usage and impact, report urgency, and provide migration guidance — for any Azure service retirement.

ACS (Azure Communication Services) is the first implementation. The generic `azure/` skills establish a reusable pattern any Azure team can adopt when retiring their own services.

---

## Current Development Stage

The project has progressed through several phases since initial conception in late January 2026. The most recent sprint established an **AI-first, skills-based architecture** — composable agent skills that automate the full deprecation assessment workflow without manual intervention.

---

## What's Been Built

### Phase 1–2: Core Application (January 2026)
- Full **Next.js web application** with Azure AD authentication
- Azure Resource Manager SDK integration for resource discovery
- Azure Monitor SDK integration for metrics collection (90-day lookback)
- Detection logic for all 5 retiring ACS channels: Email, SMS, Chat, Calling, Phone Numbers
- Severity and migration effort calculation engine
- CSV export functionality
- **Email Service migration guide** (Microsoft 365 HVE path only, policy-compliant)

### Phase 3: PowerShell Assessment Tool (January–February 2026)
- **`scripts/powershell/acs-impact-assessment-tool.ps1`** — production-ready multi-subscription scanner
- Supports fast mode (resource detection only, ~30 sec/subscription) and full mode (Azure Monitor metrics, ~3–5 min/subscription)
- Scan was run live on 2026-02-02: 2 ACS resources found, 0 retiring services in use (JameelaPayAsYouGo subscription)

### Phase 4: Agent Skills Layer (February 2026) ← Most Recent
Created **13 composable AI Agent Skills** in two namespaces following the [Agent Skills open standard](https://agentskills.dev) (Linux Foundation / AAIF), committed to `.agent/skills/`:

#### `azure/` — Generic Skills (any Azure product)

| Skill | Purpose |
|-------|---------|
| `azure/1-azure-auth-check` | Verify Azure authentication and display tenant/subscription context |
| `azure/2-azure-subscription-select` | Interactive subscription selection (default / all / specific) |
| `azure/3-azure-resource-scan` | Generic resource discovery — works with any Azure product |
| `azure/4-azure-channel-detect` | Fast feature detection via child resources (~30 sec) |
| `azure/5-azure-metrics-collect` | Full metrics collection via Azure Monitor (1–93 day lookback) |
| `azure/6-azure-impact-analyze` | Severity and migration effort with configurable thresholds |
| `azure/7-azure-report-generate` | Export to CSV, Markdown, or JSON |

#### `acs/` — ACS-Specific Skills (Azure Communication Services)

| Skill | Purpose |
|-------|---------|
| `acs/0-acs-full-scan` | **Orchestrator** — runs complete ACS workflow end-to-end |
| `acs/1-acs-resource-scan` | Scan for `Microsoft.Communication/CommunicationServices` (pre-filled) |
| `acs/2-acs-channel-detect` | Fast: Email + Phone Numbers via child resources |
| `acs/3-acs-metrics-collect` | Full: All 5 ACS channels via Azure Monitor — pre-configured metrics |
| `acs/4-acs-impact-analyze` | ACS severity thresholds, retirement dates, migration guide links |
| `acs/5-acs-report-generate` | 19-column ACS CSV, Markdown with guide links, JSON |

**Key design decisions:**
- `azure/` skills are fully **product-agnostic** — the reusable pattern for any Azure service retirement
- `acs/` skills are the **first implementation** of that pattern, pre-configured for ACS retiring channels
- Auth and subscription selection are **shared** — both workflows use `azure/1-2`
- No PowerShell dependency — skills implement workflows directly, compatible with any AI agent
- `acs/0-acs-full-scan` is the single entry point for a complete ACS assessment

Skills are compatible with Claude Code, GitHub Copilot, Cursor, Windsurf, Cline, and 20+ other AI agents.

---

## What's Pending

### Immediate (Testing Phase)
- [ ] Test `azure/` skills 1–7 end-to-end with a real Azure subscription
- [ ] Test `acs/` skills 1–5 + `0-acs-full-scan` orchestrator end-to-end

### MVP Work
- [ ] 4 remaining migration guides (SMS, Chat, Calling, Phone Numbers) — use email guide as template
- [ ] Clean up SendGrid references in `src/config/retiring-features.ts` (lines 231–260) — policy compliance
- [ ] UI polish and internal testing
- [ ] Customer pilot (5–10 friendly customers)
- [ ] Production deployment

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Agent Skills as the primary delivery mechanism | Meets customers and teams where they already work — inside their AI agent of choice |
| Two-namespace structure (`azure/` + `acs/`) | `azure/` is the reusable open pattern; `acs/` is the first ACS implementation; easy to add more products |
| No PowerShell dependency in skills | Skills work across any AI agent and any OS — not limited to PowerShell environments |
| All 5 ACS channels (not just Email) | Same detection infrastructure, only +1 week effort, complete customer picture |
| No database / persistent storage | Reduces complexity and security scope; runtime analysis only |
| Microsoft first-party recommendations only | Policy compliance — no third-party marketplace partners (e.g., SendGrid) |
| `.agent/skills/` open standard | Universal cross-platform compatibility (25+ AI tools); not locked to any one AI vendor |
| Single subscription in MVP web app | Scope management for small team; multi-sub in Phase 2 |

---

## Team

- **Owner:** jameelaesa (PM Lead)
- **Teammates:** TBD
- **Team Size Target:** 3 PMs + 1 Engineer
- **Timeline:** 12 weeks to MVP production

---

## Milestones

| Date | Milestone |
|------|-----------|
| 2026-01-26 | Full application architecture built, Email migration guide created, MVP scope finalized |
| 2026-01-28 | PowerShell assessment tool created and committed |
| 2026-02-02 | Live scan executed — 2 ACS resources found, 0 retiring services in use |
| 2026-02-06 | 8 Agent Skills created in `.agent/skills/` per universal open standard |
| 2026-02-25 | Skills restructured into `azure/` (7 generic) + `acs/` (6 ACS-specific) namespaces; old skill 8 replaced by `acs/0-acs-full-scan` orchestrator with no PowerShell dependency |

---

## Open Questions for V-Team

1. Approval for MVP development? (3 PMs + 1 engineer, 12 weeks)
2. M365 team commitment for Email → HVE migration guide validation?
3. Which 5–10 friendly customers for pre-launch pilot?
4. Phase 3 M365 telemetry integration — can we get a commitment?

---

**Document Owner:** jameelaesa
**Last Updated:** 2026-02-25 (restructured skills into azure/ + acs/ namespaces)
