# Azure Transition Agent — ACS Edition

**Automate the assessment of retiring Azure Communication Services (ACS) resources across your Azure subscriptions — detecting which channels are in active use, how urgently you need to migrate, and where to go next.**

---

## The Problem

When Microsoft retires an Azure service, customers, PMs, and support teams face a time-intensive manual process: identifying which subscriptions and resources are actively using the retiring service across potentially hundreds of subscriptions.

## The Solution

A set of composable **AI Agent Skills** that automate the full assessment workflow:

1. **Scan** — discover all ACS resources across your subscriptions
2. **Detect** — identify which retiring channels are in use (Email, SMS, Chat, Calling, Phone Numbers)
3. **Analyze** — calculate severity and migration effort based on actual usage
4. **Report** — export results to CSV, Markdown, and JSON with links to migration guides

The `azure/` skills are a **reusable open pattern** for any Azure service retirement. The `acs/` skills are the first implementation, pre-configured for ACS.

---

## Getting Started

### What You'll Need

Before running the ACS assessment, you need four things installed on your computer:

| Requirement | Why | Time to install |
|-------------|-----|----------------|
| [Git](#1-install-git) | Clone this repository | ~2 minutes |
| [PowerShell](#2-install-powershell) | Run Azure commands | ~5 minutes |
| [Azure PowerShell Module](#3-install-azure-powershell-module-az) | Connect to your Azure subscriptions | ~5 minutes |
| [Claude Code](#4-install-claude-code) | Run the AI Agent Skills | ~3 minutes |

> **Already have these?** Jump to [Clone the Repository](#5-clone-the-repository).

---

### 1. Install Git

Git is used to download (clone) this project to your computer.

**Windows:**
1. Go to https://git-scm.com/download/win
2. Download and run the installer
3. Accept all default options
4. Open a new Command Prompt or PowerShell window and verify: `git --version`

**macOS:**
```bash
# If you have Homebrew installed:
brew install git

# Or install Xcode Command Line Tools (includes git):
xcode-select --install
```

**Linux:**
```bash
sudo apt-get install git        # Ubuntu/Debian
sudo dnf install git            # Fedora/RHEL
```

---

### 2. Install PowerShell

The skills use PowerShell to communicate with Azure. Windows users already have PowerShell installed. macOS and Linux users need to install PowerShell 7.

**Windows:** Already installed — skip this step.

**macOS:**
```bash
# Using Homebrew:
brew install --cask powershell

# Verify installation:
pwsh --version
```

**Linux (Ubuntu/Debian):**
```bash
# Add Microsoft repository and install:
wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y powershell

# Verify installation:
pwsh --version
```

For other Linux distributions, see: https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux

---

### 3. Install Azure PowerShell Module (Az)

This module lets PowerShell connect to your Azure subscriptions.

**Open PowerShell** (search "PowerShell" in your Start menu on Windows, or type `pwsh` in your terminal on macOS/Linux) and run:

```powershell
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
```

> **Note:** This may take 3–5 minutes to download. If prompted about an "untrusted repository," type `Y` and press Enter.

**Verify it installed:**
```powershell
Get-Module -Name Az.Accounts -ListAvailable | Select-Object Name, Version
```

You should see the Az.Accounts module listed with a version number.

**If you see an error about execution policy** (Windows only):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 4. Install Claude Code

Claude Code is the AI agent that reads and runs the skills in this repository.

**Install via npm** (requires Node.js — see below if you don't have it):
```bash
npm install -g @anthropic-ai/claude-code
```

**If you don't have Node.js installed:**
1. Go to https://nodejs.org
2. Download and install the **LTS** version (the recommended one)
3. Open a new terminal window and run: `npm install -g @anthropic-ai/claude-code`

**Verify Claude Code is installed:**
```bash
claude --version
```

**First-time setup:**
```bash
claude
```
This will prompt you to log in with your Anthropic account. If you don't have one, create a free account at https://claude.ai.

> **Alternative AI Agents:** The skills in `.agent/skills/` follow the open Agent Skills standard and work with GitHub Copilot, Cursor, Windsurf, Cline, and other compatible AI agents. See [Agent Skills compatibility](#agent-skills-compatibility) for details.

---

### 5. Clone the Repository

Open a terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
git clone https://github.com/jameelaesa/ACS-Transition-Agent-v0.git
cd ACS-Transition-Agent-v0
```

---

### 6. Connect to Azure

Before running the assessment, connect PowerShell to your Azure account.

**Open PowerShell** and run:
```powershell
Connect-AzAccount
```

A browser window will open asking you to sign in with your Azure credentials. Sign in with the account that has access to the subscriptions you want to scan.

**Verify you're connected:**
```powershell
Get-AzContext
```

You should see your account email, tenant ID, and current subscription.

> **Permissions required:** You need at least **Reader** access on the subscriptions you want to scan. For usage metrics, you also need **Monitoring Reader** access.

---

### 7. Run the ACS Assessment

Open Claude Code in the project directory:

```bash
cd ACS-Transition-Agent-v0
claude
```

Then run the full ACS assessment using one of these methods:

**Option A — Type a natural language request:**
```
Run an ACS deprecation scan
```

**Option B — Use the slash command:**
```
/0-acs-full-scan
```

Claude will guide you through the complete workflow interactively:

```
Step 1: Verify Azure authentication         ← checks you're logged in
Step 2: Select subscription(s) to scan     ← choose default, all, or specific
Step 3: Discover ACS resources             ← finds all CommunicationServices resources
Step 4: Choose detection mode              ← fast (30 sec) or full (3-5 min with metrics)
Step 5: Analyze impact                     ← severity + migration effort per resource
Step 6: Generate reports                   ← saves CSV, Markdown, JSON to ./exports/
```

---

### 8. Find Your Results

After the scan completes, your reports are saved in the `exports/` folder:

| File | Format | Best for |
|------|--------|----------|
| `YYYY-MM-DD_ACS_Impact_Assessment.csv` | CSV | Opening in Excel, filtering and sorting |
| `YYYY-MM-DD_ACS_Impact_Assessment.md` | Markdown | Sharing with your team |
| `YYYY-MM-DD_ACS_Impact_Assessment.json` | JSON | Automated processing |

**To open the CSV in Excel:**
1. Open File Explorer and navigate to the `exports/` folder
2. Double-click the `.csv` file
3. Excel will open it automatically

---

## Running Individual Steps

You can also run each step of the workflow individually. This is useful if you want to re-run a specific step or customize the process.

### Shared Steps (work with any Azure product)

```
/azure/1-azure-auth-check          Check if you're authenticated to Azure
/azure/2-azure-subscription-select Choose which subscription(s) to scan
```

### ACS-Specific Steps

```
/acs/1-acs-resource-scan           Find all ACS resources in selected subscriptions
/acs/2-acs-channel-detect          Fast check: Email + Phone Numbers only (~30 seconds)
/acs/3-acs-metrics-collect         Full check: all 5 channels via Azure Monitor (~3-5 min)
/acs/4-acs-impact-analyze          Calculate severity and migration effort
/acs/5-acs-report-generate         Export results to CSV, Markdown, and JSON
```

**Example — run just the fast detection:**
```
/azure/1-azure-auth-check
/azure/2-azure-subscription-select
/acs/1-acs-resource-scan
/acs/2-acs-channel-detect
```

---

## What the Assessment Detects

The full scan (`/acs/3-acs-metrics-collect`) checks for active usage of all 5 retiring ACS channels over the past 90 days:

| Channel | What's Retiring | Detection |
|---------|----------------|-----------|
| Email Service | ACS standalone Email SDK | ✅ Full (metrics) |
| SMS API | ACS standalone SMS API | ✅ Full (metrics) |
| Chat SDK | ACS standalone Chat SDK | ✅ Full (metrics) |
| Calling SDK | ACS standalone Calling SDK | ✅ Full (metrics) |
| Phone Numbers SDK | ACS standalone Phone Numbers SDK | ✅ Full (metrics) |

**Severity levels assigned:**

| Severity | Meaning | Example |
|----------|---------|---------|
| 🔴 Critical | High usage — immediate action needed | Email >1,000 messages in period |
| 🟡 Warning | Moderate usage — plan migration soon | Email >100 messages in period |
| ℹ️ Info | Low usage detected | Any usage below Warning threshold |
| ✅ None | No usage found | Zero activity in last 90 days |

---

## Migration Guides

After your assessment, use these guides to plan your migration:

| Retiring Service | Migration Guide | Status |
|-----------------|----------------|--------|
| Email Service | [migration-guides/email/email-service-migration.md](migration-guides/email/email-service-migration.md) | ✅ Available |
| SMS API | Coming soon | 🚧 In progress |
| Chat SDK | Coming soon | 🚧 In progress |
| Calling SDK | Coming soon | 🚧 In progress |
| Phone Numbers SDK | Coming soon | 🚧 In progress |

All migration paths follow Microsoft first-party solutions only (Microsoft 365 HVE, Teams integration).

---

## Troubleshooting

### "pwsh: command not found" or "powershell: command not found"
- **Windows:** Search for "PowerShell" in your Start menu and open it from there
- **macOS/Linux:** Install PowerShell 7 — see [Step 2](#2-install-powershell) above

### "Get-AzContext: command not found" or "Az module not found"
The Azure PowerShell module isn't installed or loaded. Run:
```powershell
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
```

### "Execution of scripts is disabled on this system" (Windows)
Run this in PowerShell, then try again:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Connect-AzAccount" fails or browser doesn't open
Try the device code login method:
```powershell
Connect-AzAccount -UseDeviceAuthentication
```
Copy the code shown, go to https://microsoft.com/devicelogin, and enter the code.

### "No ACS resources found" but I know I have some
- Make sure you selected the correct subscription
- Verify your account has Reader access: check in the Azure Portal under **Subscriptions → Access control (IAM)**
- Try specifying the subscription directly:
  ```powershell
  Set-AzContext -SubscriptionId "your-subscription-id"
  ```

### Metrics show 0 for all channels but I know we use ACS
- Check that you have **Monitoring Reader** permissions on the subscription
- Try extending the lookback period when prompted (up to 93 days maximum)
- Some metrics may not be available if the resource is in a region that doesn't support Azure Monitor for that channel

### Claude Code doesn't find the skills
Make sure you opened Claude Code **inside the repository directory**:
```bash
cd ACS-Transition-Agent-v0
claude
```

---

## Agent Skills Compatibility

The skills in `.agent/skills/` follow the [Agent Skills open standard](https://agentskills.dev) (Linux Foundation / AAIF) and are compatible with:

| AI Agent | Compatible |
|----------|-----------|
| Claude Code | ✅ |
| GitHub Copilot | ✅ |
| Cursor | ✅ |
| Windsurf | ✅ |
| Cline | ✅ |
| Gemini CLI | ✅ |
| OpenCode | ✅ |

---

## Project Structure

```
ACS-Transition-Agent-v0/
│
├── .agent/skills/                  ← AI Agent Skills (main feature)
│   ├── azure/                      ← Generic skills (any Azure product)
│   │   ├── 1-azure-auth-check/
│   │   ├── 2-azure-subscription-select/
│   │   ├── 3-azure-resource-scan/
│   │   ├── 4-azure-channel-detect/
│   │   ├── 5-azure-metrics-collect/
│   │   ├── 6-azure-impact-analyze/
│   │   └── 7-azure-report-generate/
│   └── acs/                        ← ACS-specific skills
│       ├── 0-acs-full-scan/        ← Start here
│       ├── 1-acs-resource-scan/
│       ├── 2-acs-channel-detect/
│       ├── 3-acs-metrics-collect/
│       ├── 4-acs-impact-analyze/
│       └── 5-acs-report-generate/
│
├── scripts/powershell/             ← Standalone PowerShell tool (alternative)
│   └── acs-impact-assessment-tool.ps1
│
├── migration-guides/               ← Step-by-step migration documentation
│   └── email/
│       └── email-service-migration.md
│
├── exports/                        ← Assessment reports saved here
│
└── docs/                           ← Project documentation
    ├── STATUS-NOTES.md
    ├── MVP-SCOPE.md
    └── CONVERSATION-NOTES.md
```

---

## Alternative: PowerShell Script (No AI Agent Required)

If you prefer not to use an AI agent, a standalone PowerShell script is also available:

```powershell
# Navigate to the scripts directory
cd scripts/powershell

# Fast scan — Email and Phone Numbers only (~30 seconds)
.\acs-impact-assessment-tool.ps1

# Full scan — all 5 channels with 90-day usage metrics (~3-5 minutes)
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# Scan a specific subscription
.\acs-impact-assessment-tool.ps1 -IncludeMetrics -SubscriptionId "your-sub-id"
```

See [scripts/powershell/README.md](scripts/powershell/README.md) for full documentation.

---

## Support

- **Questions or issues:** Open an issue in this repository
- **Migration assistance:** Contact the ACS team or Microsoft FastTrack
- **ACS retirement details:** https://aka.ms/acs-retirement
- **Migration guides:** https://aka.ms/acs-transition-guides

---

**Last Updated:** 2026-02-27
**Maintained By:** Azure Transition Agent Team
**Current Phase:** Phase 1 — Agent Skills + PowerShell Tool + Email Migration Guide
