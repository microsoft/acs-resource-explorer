# ACS Transition Agent — Status Notes

**Date:** 2026-02-25
**Project:** Azure Communication Services (ACS) Transition Agent
**Repo:** [ACS-Transition-Agent-v0](https://github.com/jameelaesa/ACS-Transition-Agent-v0)
**Stage:** Forming — Active Development / Pre-MVP

---

## Current Development Stage

The project has progressed through several phases since initial conception in late January 2026. The most recent sprint shifted focus from the web application to an **AI-first, skills-based approach** for automating the deprecation assessment workflow.

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
- `azure/` skills are fully **product-agnostic** — reusable for any Azure service retirement
- `acs/` skills are **ACS-specific implementations** of the azure/ skills, with all configuration pre-filled
- Auth and subscription selection are **shared** — both workflows use `azure/1-2`
- No PowerShell script calls — skills implement workflows directly via Azure SDK/CLI
- `acs/0-acs-full-scan` replaces the old `8-acs-deprecation-scan` (which called PowerShell directly)

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
| All 5 ACS channels in MVP (not just Email) | Same detection infrastructure, only +1 week effort, complete customer picture |
| No database / persistent storage | Reduces complexity and security scope |
| Microsoft first-party recommendations only | Policy compliance — no third-party marketplace partners (e.g., SendGrid) |
| Two-namespace skill structure (`azure/` + `acs/`) | Generic skills reusable by any Azure team; ACS skills pre-configured for immediate use |
| `acs/` skills replace PowerShell orchestrator | Skills implement workflow directly — no PowerShell dependency, works across all AI agents |
| `.agent/skills/` directory standard | Universal cross-platform compatibility (25+ AI tools) vs. Claude-only `.claude/skills/` |
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
