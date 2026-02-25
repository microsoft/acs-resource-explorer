# Agent Skills

Universal AI agent skills following the [Agent Skills open standard](https://agentskills.dev) (Linux Foundation / AAIF).

Compatible with Claude Code, GitHub Copilot, Cursor, Windsurf, Cline, Gemini CLI, OpenCode, and 20+ other AI agents.

---

## Structure

```
.agent/skills/
├── azure/          ← Generic skills — work with ANY Azure product
│   ├── 1-azure-auth-check/
│   ├── 2-azure-subscription-select/
│   ├── 3-azure-resource-scan/
│   ├── 4-azure-channel-detect/
│   ├── 5-azure-metrics-collect/
│   ├── 6-azure-impact-analyze/
│   └── 7-azure-report-generate/
│
└── acs/            ← ACS-specific skills — Azure Communication Services
    ├── 0-acs-full-scan/          (orchestrator — start here)
    ├── 1-acs-resource-scan/
    ├── 2-acs-channel-detect/
    ├── 3-acs-metrics-collect/
    ├── 4-acs-impact-analyze/
    └── 5-acs-report-generate/
```

---

## Quick Start

### Run the full ACS assessment (recommended)
```
/0-acs-full-scan
```
or say: *"Run an ACS deprecation scan"* / *"Do a full ACS impact assessment"*

### Run step-by-step
```
/azure/1-azure-auth-check
/azure/2-azure-subscription-select
/acs/1-acs-resource-scan
/acs/3-acs-metrics-collect      ← full detection (recommended)
/acs/4-acs-impact-analyze
/acs/5-acs-report-generate
```

---

## Azure Skills (Generic)

These skills work with **any Azure product** — ACS, Storage, SQL, Compute, etc.

| Skill | Description |
|-------|-------------|
| [1-azure-auth-check](azure/1-azure-auth-check/SKILL.md) | Verify Azure authentication, display tenant and account info |
| [2-azure-subscription-select](azure/2-azure-subscription-select/SKILL.md) | Interactive subscription selection (default / all / specific) |
| [3-azure-resource-scan](azure/3-azure-resource-scan/SKILL.md) | Discover resources of any type across subscriptions |
| [4-azure-channel-detect](azure/4-azure-channel-detect/SKILL.md) | Fast feature detection via child resources (~30 sec) |
| [5-azure-metrics-collect](azure/5-azure-metrics-collect/SKILL.md) | Comprehensive usage detection via Azure Monitor (1-93 days) |
| [6-azure-impact-analyze](azure/6-azure-impact-analyze/SKILL.md) | Calculate severity and migration effort with custom thresholds |
| [7-azure-report-generate](azure/7-azure-report-generate/SKILL.md) | Export to CSV, Markdown, or JSON |

**Use these skills when:** Analyzing deprecation impact for Azure services other than ACS, or when you need full control over each step with custom configuration.

---

## ACS Skills (Azure Communication Services)

These skills are pre-configured for the [retiring ACS standalone SDKs and APIs](https://aka.ms/acs-retirement).

| Skill | Description |
|-------|-------------|
| [0-acs-full-scan](acs/0-acs-full-scan/SKILL.md) | **Orchestrator** — runs the complete ACS workflow end-to-end |
| [1-acs-resource-scan](acs/1-acs-resource-scan/SKILL.md) | Scan for `Microsoft.Communication/CommunicationServices` resources |
| [2-acs-channel-detect](acs/2-acs-channel-detect/SKILL.md) | Fast: Email + Phone Numbers via child resources (~30 sec) |
| [3-acs-metrics-collect](acs/3-acs-metrics-collect/SKILL.md) | Full: All 5 channels via Azure Monitor metrics (~3-5 min) |
| [4-acs-impact-analyze](acs/4-acs-impact-analyze/SKILL.md) | ACS severity rules, retirement dates, migration guide links |
| [5-acs-report-generate](acs/5-acs-report-generate/SKILL.md) | ACS-specific CSV (19 columns), Markdown with guide links, JSON |

### Retiring ACS Channels Covered

| Channel | Fast Detection | Full Detection | Retirement |
|---------|---------------|----------------|------------|
| Email Service | ✅ | ✅ | 2027-12-31 |
| Phone Numbers SDK | ✅ | ✅ | TBD |
| SMS API | ❌ | ✅ | TBD |
| Chat SDK | ❌ | ✅ | TBD |
| Calling SDK | ❌ | ✅ | TBD |

---

## Workflow Sequences

### Full ACS Assessment (recommended)
```
azure/1-azure-auth-check
  └─ azure/2-azure-subscription-select
       └─ acs/1-acs-resource-scan
            └─ acs/3-acs-metrics-collect  (90-day lookback)
                 └─ acs/4-acs-impact-analyze
                      └─ acs/5-acs-report-generate
```

### Fast ACS Check (Email + Phone Numbers only)
```
azure/1-azure-auth-check
  └─ azure/2-azure-subscription-select
       └─ acs/1-acs-resource-scan
            └─ acs/2-acs-channel-detect
                 └─ acs/4-acs-impact-analyze
                      └─ acs/5-acs-report-generate
```

### Generic Azure Product Assessment
```
azure/1-azure-auth-check
  └─ azure/2-azure-subscription-select
       └─ azure/3-azure-resource-scan       (choose any resource type)
            └─ azure/5-azure-metrics-collect
                 └─ azure/6-azure-impact-analyze
                      └─ azure/7-azure-report-generate
```

---

## How Skills Relate

The ACS skills are **specialized implementations** of the generic Azure skills:

| ACS Skill | Based On | What's Pre-configured |
|-----------|----------|----------------------|
| `acs/1-acs-resource-scan` | `azure/3-azure-resource-scan` | ResourceType = `Microsoft.Communication/CommunicationServices` |
| `acs/2-acs-channel-detect` | `azure/4-azure-channel-detect` | Email, Phone Numbers child resource types |
| `acs/3-acs-metrics-collect` | `azure/5-azure-metrics-collect` | All 5 ACS channel metric names |
| `acs/4-acs-impact-analyze` | `azure/6-azure-impact-analyze` | ACS severity thresholds, retirement dates, guide links |
| `acs/5-acs-report-generate` | `azure/7-azure-report-generate` | 19-column ACS CSV, ACS migration guide links |

Auth and subscription selection are **shared** — both workflows use `azure/1-azure-auth-check` and `azure/2-azure-subscription-select`.

---

## Adapting for Other Azure Products

To create a skill set for another retiring Azure product, use the `azure/` skills as the foundation:

1. Use `azure/1-azure-auth-check` + `azure/2-azure-subscription-select` as-is
2. Run `azure/3-azure-resource-scan` with your product's resource type
3. Configure `azure/5-azure-metrics-collect` with your product's metric names
4. Configure `azure/6-azure-impact-analyze` with your product's severity rules
5. Use `azure/7-azure-report-generate` for export

---

## Migration Guides

| Channel | Guide |
|---------|-------|
| Email Service | [migration-guides/email/email-service-migration.md](../../migration-guides/email/email-service-migration.md) |
| SMS, Chat, Calling, Phone Numbers | https://aka.ms/acs-transition-guides |

---

## References
- [Agent Skills Open Standard](https://agentskills.dev)
- [ACS Retirement Announcements](https://aka.ms/acs-retirement)
- [ACS Transition Guides](https://aka.ms/acs-transition-guides)
