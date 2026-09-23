# ACS Resource Explorer
 
**An AI agent-powered tool that scans Azure subscriptions, detects ACS resources, identifies channels with active usage, reports the last 90 days of usage data, and produces a prioritized migration report with per-channel guidance.**
 
---
 
## The Solution
 
A set of composable **AI Agent Skills** that automate the full assessment workflow:
 
1. **Scan** — discover all ACS resources across your subscriptions
2. **Detect** — identify which impacted channels are in use (4 retiring + 1 breaking change)
3. **Analyze** — map detected channels to migration guides based on actual usage
4. **Report** — export results to CSV, Markdown, and JSON with links to migration guides
 
---
 
## Getting Started
**Prerequisites:**
- **Git** — to clone this repository ([Step 1](#1-install-git))
- **Azure CLI** (`az`) — to connect to Azure and run scans ([Step 2](#2-install-the-azure-cli))
- **An AI agent** — GitHub Copilot ([Step 3](#3-choose-your-ai-agent))
 
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
 
The Azure CLI (`az`) is used to connect to your Azure subscriptions and collect resource and usage data. It works on Windows, macOS, and Linux.
 
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
 
### 3. Install the Azure Communication extension 
The `az communication` extension is required to detect purchased phone numbers. Taking into consideration that `Disable Access Keys Authentication` option under `Settings` should be unchecked:
 
```bash
az extension add --name communication
```
 
If already installed, update it:
 
```bash
az extension update --name communication
```
 
Verify the extension commands are available:
 
```bash
az communication -h
```
 
---
 
### 3. Install GitHub Copilot
 
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
code acs-transition-agent
```
 
**Step 5 — Install required VS Code extensions:**
 
To run the tool in VS Code, install the **PowerShell** and **Rainbow CSV** extensions. To install the extensions, repeat the following steps for each extension:
1. Open VS Code
2. Click the Extensions icon in the left sidebar (looks like four squares)
3. Search for the extension name (e.g., **PowerShell** or **Rainbow CSV**)
4. Click **Install**
 
**Step 5 — Install Python:**
 
Python is required to run the tool. Download and install Python from the official website: [Python Downloads](https://www.python.org/downloads/)
 
> **Note:** GitHub Copilot Free includes 50 chat messages per month. A full ACS scan typically uses 5–10 messages. If you run scans frequently, consider upgrading to GitHub Copilot Pro ($10/month).
 
### 4. Clone the Repository
 
Open a terminal (Command Prompt, PowerShell, or Terminal) and run:
 
```bash
git clone https://github.com/microsoft/acs-transition-agent.git
cd acs-transition-agent
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
 
Make sure you've opened the project folder in VS Code (`code acs-transition-agent`), then:
 
1. Open the **Chat** panel: press `Ctrl+Alt+I` (Windows/Linux) or `Ctrl+Cmd+I` (macOS)
2. The following are some example prompts you can use in the input:
   |Prompt|Description|
   |------|-----------|
   | `Run full scan  ` | Will run full scan including Email, Phone numbers, and metrics|
   | `Run fast scan `| Will run fast scan including Email and Phone numbers only|
   | `Scan my usage`| Will be asking you if you want to run full or fast scan|
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
| `ACS_ResourceExplorer_Full_v{ToolVersion}_yyyyMMddHHmmss.csv` | CSV | Opening in Excel, filtering and sorting |
| `ACS_ResourceExplorer_Full_v{ToolVersion}_yyyyMMddHHmmss.md` | Markdown | Sharing with your team |
| `ACS_ResourceExplorer_Full_v{ToolVersion}_yyyyMMddHHmmss.json` | JSON | Automated processing |
 
**To open the CSV in Excel:**
1. Open File Explorer and navigate to the `exports/` folder
2. Double-click the `.csv` file
3. Excel will open it automatically
 
---
 
## What the Assessment Detects

**Fast Scan**

The fast scan performs a resource-only check and skips usage analysis:

| Channel | Detection |
|---------|-----------|
| Email Service | Email Communication Services domains |
| Phone Numbers | Purchased phone numbers |


**Full Scan**

The full scan includes all fast scan checks and analyzes active usage across all impacted ACS channels over the last 90 days.

| Channel | Metric(s) |
|---------|-----------|
| Email Service | `ApiRequests`, `DeliveryStatusUpdate`, `UserEngagement` |
| SMS | `APIRequestSMS` |
| Chat | `APIRequestChat` |
| Call Automation | `APIRequestCallAutomation`, `APIRequestCallRecording`, `AcsCallAutomationCallbackEvent` |
| Job Router | `ApiRequestRouter` |
| Advance Messaging | `APIRequestsAdvancedMessaging` |
| Rooms | `ApiRequestRooms` |
 
---
 
## Channel Guides
 
After your assessment, use these guides to plan your next steps:
 
| Channel | Status Type | Guide |
|---------|------------|-------|
| Email Service | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement#acs-email) |
| SMS | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement#acs-sms) |
| Chat | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement#acs-chat) |
| Call Automation | 🟡 Breaking Change | [Breaking Change Guide](https://aka.ms/acs-retirement#acs-call-automation) |
| Job Router | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement#acs-job-router) |
| Advance Messaging | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement#acs-advanced-messaging-whatsapp) |
| Rooms | 🔴 Retirement | [Retirement Guide](https://aka.ms/acs-retirement#acs-rooms) |
 
Full guidance: [Retirement and breaking changes guide for Azure Communication Services](https://aka.ms/acs-retirement)
 
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
 
### GitHub Copilot doesn't trigger the skill automatically
Point it directly to the skill file:
```
Follow the instructions in .agent/skills/acs/0-acs-full-scan/SKILL.md and run the ACS assessment
```

### Running script result in a timeout after few minutes?
The agent may automatically apply a timeout of approximately 2 minutes, especially when running a fast scan. If the scan does not complete within that time, it may fail with a timeout error. To avoid this, you can modify your prompt to explicitly allow a longer execution time or instruct the agent to use a persistent PowerShell session. This gives the scan additional time to complete and helps prevent timeout-related failures. Examples:
```
run fast scan and allow it to run for more than 2 minutes
```
```
run fast scan in a persistent PowerShell process
```

### Can't use an AI agent at all?
As an alternative, a standalone PowerShell script is available at `scripts/powershell/acs-impact-assessment-tool.ps1`. It requires the PowerShell Az module (`Install-Module -Name Az`) and runs the assessment without an AI agent. See the script header for usage instructions.
Run fast scan command
```
.\scripts\powershell\acs-impact-assessment-tool.ps1 -SubscriptionId REPLACE_WITH_SUBSCRIPTION_ID
 ```
Run full scan command
```
.\scripts\powershell\acs-impact-assessment-tool.ps1 -SubscriptionId REPLACE_WITH_SUBSCRIPTION_ID -IncludeMetrics -LookbackDays 90
 ```
---
 
## Support
 
- **Questions or issues:** Open an issue in this repository
- **ACS migration guidance:** [Retirement and breaking changes guide for Azure Communication Services](https://aka.ms/acs-retirement)
 
---
 
**Last Updated:** 2026-09-22
 
