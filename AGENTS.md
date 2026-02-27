# Agents

## Azure Transition Agent — ACS Edition

**Purpose:** Automate the assessment of retiring Azure Communication Services (ACS) resources — scanning subscriptions, detecting active usage across all retiring channels, analyzing migration urgency, and generating reports with migration guidance.

**Skills location:** `.agent/skills/`

---

## Skill Namespaces

### `azure/` — Generic Skills (any Azure product)

| Skill | Trigger | Description |
|-------|---------|-------------|
| `azure/1-azure-auth-check` | "Check my Azure auth" | Verify authentication and display tenant/account info |
| `azure/2-azure-subscription-select` | "Select subscriptions to scan" | Interactive subscription selection |
| `azure/3-azure-resource-scan` | "Scan for [product] resources" | Discover any Azure resource type across subscriptions |
| `azure/4-azure-channel-detect` | "Quick feature check" | Fast detection via child resources (~30 sec) |
| `azure/5-azure-metrics-collect` | "Collect usage metrics" | Full detection via Azure Monitor (1–93 day lookback) |
| `azure/6-azure-impact-analyze` | "Analyze migration impact" | Severity + effort calculation with configurable thresholds |
| `azure/7-azure-report-generate` | "Generate a report" | Export to CSV, Markdown, or JSON |

### `acs/` — ACS-Specific Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `acs/0-acs-full-scan` | "Run an ACS deprecation scan" | Orchestrator — runs complete workflow end-to-end |
| `acs/1-acs-resource-scan` | "Find my ACS resources" | Scan for `Microsoft.Communication/CommunicationServices` |
| `acs/2-acs-channel-detect` | "Quick ACS channel check" | Fast: Email + Phone Numbers via child resources |
| `acs/3-acs-metrics-collect` | "Collect ACS metrics" | Full: all 5 channels — Email, SMS, Chat, Calling, Phone Numbers |
| `acs/4-acs-impact-analyze` | "Analyze ACS impact" | ACS severity rules, retirement dates, migration guide links |
| `acs/5-acs-report-generate` | "Generate ACS report" | 19-column CSV, Markdown with guide links, JSON |

---

## Primary Capability

**ACS deprecation assessment** — detects active usage of all 5 retiring ACS channels:
- Email Service (ACS standalone)
- SMS API (ACS standalone)
- Chat SDK (ACS standalone)
- Calling SDK (ACS standalone)
- Phone Numbers SDK (ACS standalone)

Outputs: severity rating (Critical/Warning/Info/None), migration effort (High/Medium/Low), and links to migration guides.

---

## Authentication

- Azure authentication via PowerShell Az module (`Connect-AzAccount`)
- Uses delegated user identity — no stored credentials
- Requires Reader + Monitoring Reader permissions on target subscriptions

---

## Data Handling

- No persistent storage — all analysis is performed at runtime
- Results exported to `./exports/` directory on demand
- Azure Monitor metrics queried live (1–93 day lookback window)

---

## Execution

Primary: AI Agent Skills via `.agent/skills/` (Claude Code, GitHub Copilot, Cursor, etc.)
Alternative: Standalone PowerShell script at `scripts/powershell/acs-impact-assessment-tool.ps1`
