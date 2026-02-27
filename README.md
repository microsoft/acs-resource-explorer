# Azure Transition Agent — ACS Edition

**ACS Transition Agent that utilizes Agent Skills to automate the full retirement impact workflow which can scan, detect Azure Communication Services (ACS) resources, channels with usage, output the last 90 days usage, and report impact and urgency. It also can use knowledge articles to provide migration guidance, for Azure Communication Services along with other Azure Services.**

---

## The Solution

A set of composable **AI Agent Skills** that automate the full assessment workflow:

1. **Scan** — discover all ACS resources across your subscriptions
2. **Detect** — identify which retiring channels are in use (Email, SMS, Chat, Calling, Phone Numbers)
3. **Analyze** — calculate severity and migration effort based on actual usage
4. **Report** — export results to CSV, Markdown, and JSON with links to migration guides

The `azure/` skills are a **reusable open pattern** for any Azure service retirement. The `acs/` skills are the first implementation, pre-configured for ACS.

---

## Getting Started

### Choose Your Path

There are three ways to run this assessment. Pick the one that fits your situation:

| Path | Cost | Best for |
|------|------|----------|
| [Option A — GitHub Copilot Free](#option-a-github-copilot-free) | Free | Users with a GitHub account who want no cost |
| [Option B — Claude Code](#option-b-claude-code-paid) | ~$20/month (Claude Pro) | Most seamless, fully guided experience |
| [Option C — PowerShell script only](#option-c-powershell-script-no-ai-agent) | Free | Users who don't want an AI agent at all |

All three options require **Git**, **PowerShell**, and the **Azure PowerShell module** — covered in steps 1–3 below.

> **Already have Git, PowerShell, and the Az module?** Jump to [Choose your AI Agent](#4-choose-your-ai-agent).

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

The skills use PowerShell to communicate with Azure. Install PowerShell 7 for your operating system below.

**Windows:**
1. Go to https://aka.ms/install-powershell-windows
2. Download the **MSI installer** (the `.msi` file labeled for your architecture — most users want `x64`)
3. Run the installer and accept all default options
4. Open a new terminal window and verify:
```powershell
pwsh --version
```

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

### 4. Choose Your AI Agent

#### Option A: GitHub Copilot Free

**Cost:** Free with any GitHub personal account (no credit card required).

GitHub Copilot Free gives you 50 AI chat messages per month — enough for occasional ACS scans. It runs inside **VS Code**.

**Step 1 — Install VS Code** (if you don't already have it):
1. Go to https://code.visualstudio.com
2. Download and run the installer for your operating system

**Step 2 — Install the GitHub Copilot extension:**
1. Open VS Code
2. Click the Extensions icon in the left sidebar (looks like four squares)
3. Search for **GitHub Copilot**
4. Click **Install**

**Step 3 — Sign in to GitHub Copilot:**
1. After installing, click the GitHub Copilot icon in the bottom status bar
2. Click **Sign in to GitHub**
3. Complete the browser sign-in with your GitHub account
4. When asked about a plan, select **GitHub Copilot Free**

**Step 4 — Open the project in VS Code:**
```bash
# After cloning the repo (Step 5 below), open it in VS Code:
code ACS-Transition-Agent-v0
```

> **Note:** GitHub Copilot Free includes 50 chat messages per month. A full ACS scan typically uses 5–10 messages. If you run scans frequently, consider upgrading to GitHub Copilot Pro ($10/month).

---

#### Option B: Claude Code (Paid)

**Cost:** Requires a Claude Pro subscription (~$20/month) or Anthropic API credits.

Claude Code is the most seamless option — it fully understands the Agent Skills format and guides you interactively through each step.

**Step 1 — Install Node.js** (if you don't already have it):
1. Go to https://nodejs.org
2. Download and install the **LTS** version (the one labeled "Recommended for most users")
3. Open a new terminal window to pick up the installation

**Step 2 — Install Claude Code:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Step 3 — Verify installation:**
```bash
claude --version
```

**Step 4 — Sign in:**
```bash
claude
```
This opens your browser to sign in with your Anthropic account. If you don't have one, go to https://claude.ai and create an account, then subscribe to Claude Pro.

---

#### Option C: PowerShell Script (No AI Agent)

**Cost:** Free — no AI agent needed.

If you prefer not to use an AI agent, the standalone PowerShell script performs the same assessment automatically. Skip to [Option C: PowerShell Script](#option-c-powershell-script-no-ai-agent-1) in the Run section below.

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

#### Option A: GitHub Copilot Free

Make sure you've opened the project folder in VS Code (`code ACS-Transition-Agent-v0`), then:

1. Open the **Chat** panel: press `Ctrl+Alt+I` (Windows/Linux) or `Ctrl+Cmd+I` (macOS)
2. In the chat input, type:
   ```
   Run an ACS deprecation scan
   ```
3. GitHub Copilot will read the skills from `.agent/skills/acs/0-acs-full-scan/SKILL.md` and guide you through the workflow

> **Tip:** If Copilot doesn't automatically find the skill, point it directly:
> ```
> Follow the instructions in .agent/skills/acs/0-acs-full-scan/SKILL.md and run the ACS assessment
> ```

---

#### Option B: Claude Code (Paid)

Open Claude Code in the project directory:

```bash
cd ACS-Transition-Agent-v0
claude
```

Then start the assessment using either method:

```
Run an ACS deprecation scan
```
or:
```
/0-acs-full-scan
```

Claude guides you through the complete workflow interactively:

```
Step 1: Verify Azure authentication         ← checks you're logged in
Step 2: Select subscription(s) to scan     ← choose default, all, or specific
Step 3: Discover ACS resources             ← finds all CommunicationServices resources
Step 4: Choose detection mode              ← fast (30 sec) or full (3-5 min with metrics)
Step 5: Analyze impact                     ← severity + migration effort per resource
Step 6: Generate reports                   ← saves CSV, Markdown, JSON to ./exports/
```

---

#### Option C: PowerShell Script (No AI Agent)

No AI agent or installation beyond PowerShell and the Az module is required.

```powershell
# Navigate to the scripts directory
cd scripts/powershell

# Full scan — all 5 channels with 90-day usage metrics (recommended)
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# Fast scan — Email and Phone Numbers only (~30 seconds)
.\acs-impact-assessment-tool.ps1
```

Results are saved to `exports/ACS_Impact_Assessment.csv`. See [scripts/powershell/README.md](scripts/powershell/README.md) for all options.

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

## Running the Skills

### Full Scan — One Command

The fastest way to run a complete assessment. Start here.

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Run an ACS deprecation scan` |
| GitHub Copilot | `Do a full ACS impact assessment` |
| GitHub Copilot | `Check my subscriptions for retiring ACS services` |
| Claude Code | `/0-acs-full-scan` |
| Claude Code | `Run an ACS deprecation scan` |

---

### Individual Steps

Run steps one at a time when you want to re-run a specific part, pick a different detection mode, or customize the workflow.

#### Step 1 — Verify Azure Authentication

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Check my Azure authentication` |
| Claude Code | `/azure/1-azure-auth-check` |

#### Step 2 — Select Subscriptions

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Select subscriptions to scan` |
| Claude Code | `/azure/2-azure-subscription-select` |

#### Step 3 — Find ACS Resources

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Find my ACS resources` |
| Claude Code | `/acs/1-acs-resource-scan` |

#### Step 4a — Fast Channel Detection *(Email + Phone Numbers only, ~30 sec)*

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Quick ACS channel check` |
| Claude Code | `/acs/2-acs-channel-detect` |

#### Step 4b — Full Metrics Collection *(all 5 channels, ~3–5 min)*

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Collect ACS usage metrics` |
| Claude Code | `/acs/3-acs-metrics-collect` |

#### Step 5 — Analyze Impact

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Analyze ACS impact` |
| Claude Code | `/acs/4-acs-impact-analyze` |

#### Step 6 — Generate Report

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Generate ACS report` |
| Claude Code | `/acs/5-acs-report-generate` |

---

### Common Workflows

**Full assessment — all 5 channels (recommended):**
```
1-azure-auth-check  →  2-azure-subscription-select  →  1-acs-resource-scan
  →  3-acs-metrics-collect  →  4-acs-impact-analyze  →  5-acs-report-generate
```

**Fast check — Email + Phone Numbers only:**
```
1-azure-auth-check  →  2-azure-subscription-select  →  1-acs-resource-scan
  →  2-acs-channel-detect  →  4-acs-impact-analyze  →  5-acs-report-generate
```

**Re-export only** *(already have scan results)*:
```
5-acs-report-generate
```

---

### PowerShell Script (no AI agent)

```powershell
# Navigate to the scripts directory
cd scripts/powershell

# Full scan — all 5 channels with 90-day usage metrics (recommended)
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# Fast scan — Email and Phone Numbers only (~30 seconds)
.\acs-impact-assessment-tool.ps1
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
├── docs/
│   ├── knowledge/                  ← Reference data for skills (update when dates change)
│   │   ├── acs-retirement-dates.md
│   │   ├── acs-metric-names.md
│   │   ├── acs-severity-thresholds.md
│   │   └── acs-migration-paths.md
│   └── ...                         ← Project documentation
│
├── scripts/powershell/             ← Standalone PowerShell tool (alternative)
│   └── acs-impact-assessment-tool.ps1
│
├── migration-guides/               ← Step-by-step migration documentation
│   └── email/
│       └── email-service-migration.md
│
└── exports/                        ← Assessment reports saved here (gitignored)
```

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
