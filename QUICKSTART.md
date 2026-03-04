# Quick Start — ACS Transition Agent

Run a full ACS deprecation impact assessment in under 5 minutes.

---

## Prerequisites

- **Git** — [Download](https://git-scm.com/downloads)
- **Azure CLI** — [Download](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)
- **An AI agent** — GitHub Copilot (free) or Claude Code
- **Azure access** — Reader + Monitoring Reader on target subscription(s)

---

## Setup (first time only)

**1. Install the Azure CLI** (if not already installed):
- Download from https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest and follow the installer for your OS

**2. Sign in to Azure:**
```bash
az login
```

**3. Clone this repository:**
```bash
git clone https://github.com/jameelaesa/ACS-Transition-Agent-v0.git
cd ACS-Transition-Agent-v0
```

---

## Option A — GitHub Copilot (Free)

1. Open this repo in VS Code
2. Open Copilot Chat: **Ctrl+Alt+I** (Windows/Linux) or **Ctrl+Cmd+I** (macOS)
3. Type:
   ```
   Run an ACS deprecation scan
   ```
4. Follow the interactive prompts — the agent guides you through all 6 steps

---

## Option B — Claude Code

1. Open this repo in VS Code (with Claude Code extension) or in a terminal:
   ```bash
   cd ACS-Transition-Agent-v0
   claude
   ```
2. Type:
   ```
   Run an ACS deprecation scan
   ```
3. Follow the interactive prompts

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

Reports are saved to `./exports/` in CSV, Markdown, and JSON formats.

- Review detected channels per resource
- Start with resources using the most channels
- Retirement & Breaking Changes guide: https://aka.ms/acs-retirement-and-breaking-changes-guide
- Channel guides: https://aka.ms/acs-email-migration | https://aka.ms/acs-sms-migration | https://aka.ms/acs-chat-migration | https://aka.ms/acs-calling-migration | https://aka.ms/acs-phone-migration
