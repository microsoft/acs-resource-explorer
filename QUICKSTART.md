# Quick Start — ACS Transition Agent

Run a full ACS deprecation impact assessment in under 5 minutes.

---

## Prerequisites

1. **PowerShell 7** — [Download](https://aka.ms/install-powershell-windows)
2. **Azure PowerShell Az module:**
   ```powershell
   Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
   ```
3. **Azure authentication:**
   ```powershell
   Connect-AzAccount
   ```
4. **Access level required:** Reader + Monitoring Reader on target subscription(s)

---

## Option A — GitHub Copilot (Recommended)

1. Open this repo in VS Code
2. Open Copilot Chat: **Ctrl+Alt+I** (Windows/Linux) or **Ctrl+Cmd+I** (macOS)
3. Type:
   ```
   Run an ACS deprecation scan
   ```
4. Follow the interactive prompts — the agent guides you through all 6 steps

---

## Option B — Claude Code

1. Open this repo in VS Code (with Claude Code extension installed)
2. Open Claude chat and type:
   ```
   Run an ACS deprecation scan
   ```
3. Follow the interactive prompts

---

## Option C — PowerShell Script (No AI agent required)

```powershell
# Navigate to the scripts directory
cd scripts/powershell

# Fast scan (resource detection only, ~30 seconds)
.\acs-impact-assessment-tool.ps1

# Full scan with Azure Monitor metrics (~3-5 minutes)
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# Scan a specific subscription
.\acs-impact-assessment-tool.ps1 -SubscriptionId "your-subscription-id" -IncludeMetrics
```

Reports are saved to `./exports/` in CSV format.

---

## What the Scan Detects

Five impacted ACS channels across all your subscriptions (effective **March 31, 2029**):

| Channel | Status Type | Effective Date |
|---------|------------|---------------|
| Email Service | 🔴 Retirement | 2029-03-31 |
| SMS API | 🔴 Retirement | 2029-03-31 |
| Chat SDK | 🔴 Retirement | 2029-03-31 |
| Calling SDK | 🟡 Breaking Change — must integrate with Teams | 2029-03-31 |
| Phone Numbers SDK | 🔴 Retirement | 2029-03-31 |

---

## After the Scan

- Review the severity summary (Critical → Warning → Info)
- Prioritize Critical resources first
- Retirement & Breaking Changes guide: https://aka.ms/acs-retirement-and-breaking-changes-guide
- Channel-specific guides: https://aka.ms/acs-email-migration | https://aka.ms/acs-sms-migration | https://aka.ms/acs-chat-migration | https://aka.ms/acs-calling-migration | https://aka.ms/acs-phone-migration
