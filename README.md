# Azure Transition Agent — ACS Edition

**An AI agent-powered tool that automates the full retirement impact workflow for Azure Communication Services (ACS). It scans Azure subscriptions, detects ACS resources, identifies channels with active usage, reports the last 90 days of usage data, and produces a prioritized migration report with per-channel guidance.**

---

## The Solution

A set of composable **AI Agent Skills** that automate the full assessment workflow:

1. **Scan** — discover all ACS resources across your subscriptions
2. **Detect** — identify which impacted channels are in use (4 retiring + 1 breaking change)
3. **Analyze** — map detected channels to migration guides based on actual usage
4. **Report** — export results to CSV, Markdown, and JSON with links to migration guides

The `azure/` skills are a **reusable open pattern** for any Azure service retirement. The `acs/` skills are the first implementation, pre-configured for ACS.

---

## Getting Started

### Choose Your Path

| Path | Cost | Best for |
|------|------|----------|
| [Option A — GitHub Copilot Free](#option-a-github-copilot-free) | Free | Users with a GitHub account who want no cost |
| [Option B — Claude Code](#option-b-claude-code) | ~$20/month (Claude Pro) | Most seamless, fully guided experience |

**Prerequisites:**
- **Git** — to clone this repository ([Step 1](#1-install-git))
- **Azure CLI** (`az`) — to connect to Azure and run scans ([Step 2](#2-install-the-azure-cli))
- **An AI agent** — GitHub Copilot (free) or Claude Code ([Step 3](#3-choose-your-ai-agent))

> **Already have all three?** Jump to [Clone the Repository](#4-clone-the-repository).

---

### 1. Install Git

Git is used to download (clone) this project to your computer.

**Windows:**
1. Go to https://git-scm.com/download/win
2. Download and run the installer
3. Accept all default options
4. Open a new Command Prompt or terminal and verify: `git --version`

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

### 2. Install the Azure CLI

The Azure CLI (`az`) is used to connect to your Azure subscriptions and collect resource and usage data. It works on Windows, macOS, and Linux — no additional modules required.

**Windows:**
1. Go to https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
2. Download and run the MSI installer
3. Open a new terminal window and verify: `az version`

**macOS:**
```bash
brew update && brew install azure-cli
```

**Linux (Ubuntu/Debian):**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

For other Linux distributions and package managers, see: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

---

### 3. Choose Your AI Agent

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
# After cloning the repo (Step 4 below), open it in VS Code:
code ACS-Transition-Agent-v0
```

**Step 5 — Install required VS Code extensions:**

To run the tool in VS Code, install the **PowerShell** and **Rainbow CSV** extensions. To install the extensions repeat the following steps for each one:
1. Open VS Code
2. Click the Extensions icon in the left sidebar (looks like four squares)
3. Search for **PowerShell** or **Rainbow CSV**
4. Click **Install**

**Step 5 — Install Python:**

Python is required to run the tool. Download and install Python from the official website: [Python Downloads](https://www.python.org/downloads/)

> **Note:** GitHub Copilot Free includes 50 chat messages per month. A full ACS scan typically uses 5–10 messages. If you run scans frequently, consider upgrading to GitHub Copilot Pro ($10/month).


---

#### Option B: Claude Code

**Cost:** Requires a Claude Pro subscription (~$20/month) or Anthropic API credits.

Claude Code is the most seamless option — it fully understands the Agent Skills format and guides you interactively through each step.

**Step 1 — Install Node.js** (if you don't already have it):
1. Go to https://nodejs.org
2. Download and install the **LTS** version (labeled "Recommended for most users")
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

### 4. Clone the Repository

Open a terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
git clone https://github.com/jameelaesa/ACS-Transition-Agent-v0.git
cd ACS-Transition-Agent-v0
```

---

### 5. Connect to Azure

Before running the assessment, sign in with the Azure CLI.

```bash
az login
```

A browser window will open asking you to sign in with your Azure credentials. Sign in with the account that has access to the subscriptions you want to scan.

**Verify you're connected:**
```bash
az account show
```

You should see your account email, subscription name, and tenant ID.

> **Permissions required:** You need at least **Reader** access on the subscriptions you want to scan. For usage metrics, you also need **Monitoring Reader** access.

---

### 6. Run the ACS Assessment

#### Option A: GitHub Copilot

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

#### Option B: Claude Code

Open Claude Code in the project directory:

```bash
cd ACS-Transition-Agent-v0
claude
```

Then start the assessment:

```
Run an ACS deprecation scan
```

Claude guides you through the complete workflow interactively:

```
Step 1: Verify Azure authentication         ← checks you're logged in
Step 2: Select subscription(s) to scan     ← choose default, all, or specific
Step 3: Discover ACS resources             ← finds all CommunicationServices resources
Step 4: Choose detection mode              ← fast (30 sec) or full (3-5 min with metrics)
Step 5: Analyze impact                     ← map channels to migration guides
Step 6: Generate reports                   ← saves CSV, Markdown, JSON to ./exports/
```

---

### Example Output

```
Step 1: Checking Azure authentication...
✅ Authenticated — user@contoso.com (Contoso Corp)

Step 2: Subscription selection...
✅ Scanning 2 subscription(s): Contoso-Prod, Contoso-Dev

Step 3: Discovering ACS resources...
✅ Found 3 ACS resource(s) across 2 subscription(s)
   • ContosoComms       (rg-communications, Contoso-Prod)
   • ContosoSupportBot  (rg-support, Contoso-Prod)
   • ContosoDevTest     (rg-dev, Contoso-Dev)

Step 4: Collecting usage metrics (90-day lookback)...
   ⏳ Analyzing ContosoComms...
   ⏳ Analyzing ContosoSupportBot...
   ⏳ Analyzing ContosoDevTest...
✅ Metrics collected

Step 5: Analyzing impact...
Step 6: Generating reports...
✅ Reports saved to ./exports/
```

```
╔══════════════════════════════════════════════════╗
║        ACS Impact Assessment Complete            ║
╠══════════════════════════════════════════════════╣
║ Subscriptions Scanned:  2                        ║
║ ACS Resources Found:    3                        ║
║ Detection Mode: Full (90-day lookback)           ║
╠══════════════════════════════════════════════════╣
║ Retiring Services Detected:                      ║
║   📧 Email:         2 resource(s) — 48,201 msgs  ║
║   📱 SMS:           1 resource(s) — 3,847 msgs   ║
║   💬 Chat:          1 resource(s) — 12,093 msgs  ║
║   📞 Calling:       2 resource(s) — 9,412 calls  ║
║   ☎️  Phone Numbers: 1 resource(s) — 204 ops     ║
╠══════════════════════════════════════════════════╣
║ Reports saved to: ./exports/                     ║
╚══════════════════════════════════════════════════╝

💡 Next Steps:
   📧 Email (2 resources) — Retirement Guide:
      https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email
   📱 SMS (1 resource) — Retirement Guide:
      https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms
   💬 Chat (1 resource) — Retirement Guide:
      https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat
   📞 Calling (2 resources) — Breaking Change Guide:
      https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk
   ☎️  Phone Numbers (1 resource) — Retirement Guide:
      https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer

   Full Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide
```

---

### 7. Find Your Results

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
| Claude Code | `Run an ACS deprecation scan` |

---

### Individual Steps

Run steps one at a time when you want to re-run a specific part, pick a different detection mode, or customize the workflow.

#### Step 1 — Verify Azure Authentication

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Check my Azure authentication` |
| Claude Code | `Check my Azure auth` |

#### Step 2 — Select Subscriptions

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Select subscriptions to scan` |
| Claude Code | `Select subscriptions to scan` |

#### Step 3 — Find ACS Resources

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Find my ACS resources` |
| Claude Code | `Find my ACS resources` |

#### Step 4a — Fast Channel Detection *(Email + Phone Numbers only, ~30 sec)*

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Quick ACS channel check` |
| Claude Code | `Quick ACS channel check` |

#### Step 4b — Full Metrics Collection *(all 5 channels, ~3–5 min)*

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Collect ACS usage metrics` |
| Claude Code | `Collect ACS metrics` |

#### Step 5 — Analyze Impact

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Analyze ACS impact` |
| Claude Code | `Analyze ACS impact` |

#### Step 6 — Generate Report

| Agent | Command |
|-------|---------|
| GitHub Copilot | `Generate ACS report` |
| Claude Code | `Generate ACS report` |

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

## What the Assessment Detects

The full scan checks for active usage of all 5 impacted ACS channels over the past 90 days:

| Channel | Status Type | Detection |
|---------|------------|-----------|
| Email Service | 🔴 Retirement | ✅ Full (metrics) |
| SMS API | 🔴 Retirement | ✅ Full (metrics) |
| Chat SDK | 🔴 Retirement | ✅ Full (metrics) |
| Calling SDK | 🟡 Breaking Change — must integrate with Teams | ✅ Full (metrics) |
| Phone Numbers SDK | 🔴 Retirement | ✅ Full (metrics) |

---

## Channel Guides

After your assessment, use these guides to plan your next steps:

| Channel | Status Type | Guide |
|---------|------------|-------|
| Email Service | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email) |
| SMS API | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms) |
| Chat SDK | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat) |
| Calling SDK | 🟡 Breaking Change | [Breaking Change Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk) — must integrate with Teams |
| Phone Numbers SDK | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer) |

All channels effective **July 31, 2028**. Full guide: https://aka.ms/acs-retirement-and-breaking-changes-guide

---

## Troubleshooting

### "az: command not found" or Azure CLI not recognized
Install the Azure CLI from https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest, then restart your terminal.

### "az login" fails or browser doesn't open
Try the device code login method:
```bash
az login --use-device-code
```
Copy the code shown, go to https://microsoft.com/devicelogin, and enter the code.

### "No ACS resources found" but I know I have some
- Make sure you selected the correct subscription
- Verify your account has Reader access: check in the Azure Portal under **Subscriptions → Access control (IAM)**
- Try specifying the subscription directly when prompted, or run:
  ```bash
  az account set --subscription "your-subscription-id"
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

### GitHub Copilot doesn't trigger the skill automatically
Point it directly to the skill file:
```
Follow the instructions in .agent/skills/acs/0-acs-full-scan/SKILL.md and run the ACS assessment
```

### Can't use an AI agent at all?
As an alternative, a standalone PowerShell script is available at `scripts/powershell/acs-impact-assessment-tool.ps1`. It requires the PowerShell Az module (`Install-Module -Name Az`) and runs the assessment without an AI agent. See the script header for usage instructions.

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
│   ├── azure/                      ← Generic skills (reusable for any Azure product)
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
├── docs/knowledge/                 ← Reference data for skills
│   ├── acs-retirement-dates.md     ← Channel retirement dates and urgency tiers
│   ├── acs-metric-names.md         ← Azure Monitor metric names per channel
│   ├── acs-channel-status.md       ← Full channel status breakdown
│   └── acs-migration-paths.md      ← Migration paths and guide links
│
├── migration-guides/               ← Migration guide links
│
└── exports/                        ← Assessment reports saved here (gitignored)
```

---

## Support

- **Questions or issues:** Open an issue in this repository
- **ACS migration guidance:** https://aka.ms/acs-retirement-and-breaking-changes-guide
- **Channel guides:** https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk | https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer

---

**Last Updated:** 2026-03-04
