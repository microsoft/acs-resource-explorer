---
name: 0-acs-full-scan
description: Full ACS deprecation impact assessment orchestrator. Runs the complete workflow — auth check, subscription selection, ACS resource scan, channel detection (fast or full), impact analysis, and report generation. ACS-specific, no PowerShell script required.
---

## When to use this skill
Use this skill to run a complete end-to-end ACS deprecation impact assessment in one guided workflow.

Examples:
  - "Run an ACS deprecation scan"
  - "Do a full ACS impact assessment"
  - "Check my subscriptions for retiring ACS services"
  - "Generate an ACS deprecation impact report"
  - "Scan my subscription for ACS deprecations"
  - "Run an ACS impact assessment and summarize what is potentially affected"

## What This Skill Does
Orchestrates all ACS-specific skills in sequence to deliver a complete impact assessment:

```
azure/1-azure-auth-check           → Verify Azure authentication
azure/2-azure-subscription-select  → Choose subscription(s) to scan
acs/1-acs-resource-scan            → Discover all ACS resources
acs/2-acs-channel-detect           → Fast: Email + Phone Numbers (optional)
acs/3-acs-metrics-collect          → Full: All 5 channels via Azure Monitor
acs/4-acs-impact-analyze           → Map channels to migration guides
acs/5-acs-report-generate          → Export CSV, Markdown, and/or JSON
```

## Preconditions
- Azure CLI installed (`az` command available) — https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
- Reader access (minimum) to target Azure subscription(s)
- Monitoring Reader access for metrics collection

## Workflow

### Step 1: Azure Authentication
   - Run **azure/1-azure-auth-check**
   - Verify existing session or prompt for login
   - Display connected account and tenant
   - **Exit if authentication fails**

### Step 2: Subscription Selection
   - Run **azure/2-azure-subscription-select**
   - Default: Use current default subscription (recommended)
   - Options: All subscriptions, or enter a specific subscription ID
   - **Exit if no valid subscription selected**

### Step 3: ACS Resource Discovery
   - Run **1-acs-resource-scan**
   - Scans for `Microsoft.Communication/CommunicationServices` resources
   - Displays count per subscription
   - **If no ACS resources found:**
     - Display: "✅ Good news! No ACS resources found. No migration action required."
     - **Exit workflow**

### Step 4: Choose Detection Mode
   - Ask user:
     ```
     Detection Mode:
     1. Fast scan — Email + Phone Numbers only (~30 seconds per subscription)
        (Use if you only need to check Email and Phone Numbers)

     2. Full scan — All 5 channels via Azure Monitor metrics (~3-5 min per subscription)
        (Recommended — detects Email, SMS, Chat, Calling, and Phone Numbers)

     Choose [1/2] (default: 2):
     ```

   **If Mode 1 (Fast):**
   - Run **2-acs-channel-detect**
   - Note: SMS, Chat, Calling cannot be detected in fast mode

   **If Mode 2 (Full):**
   - Run **3-acs-metrics-collect**
   - Ask for lookback period (default: 90 days, max: 93 days)
   - Collects usage data for all 5 channels

### Step 5: Channel Analysis
   - Run **4-acs-impact-analyze**
   - Map each detected channel to its migration guide
   - Link to Retirement Guide or Breaking Change Guide per channel

### Step 6: Report Generation
   - Run **5-acs-report-generate**
   - Default: Generate all formats (CSV + Markdown + JSON)
   - Output to `./exports/` directory

## Quick Summary Display
After all steps complete:
```
╔══════════════════════════════════════════════════╗
║        ACS Impact Assessment Complete            ║
╠══════════════════════════════════════════════════╣
║ Subscriptions Scanned: [N]                       ║
║ ACS Resources Found:   [N]                       ║
║ Detection Mode: [Fast / Full ([N]-day lookback)] ║
╠══════════════════════════════════════════════════╣
║ Retiring Services Detected:                      ║
║   Email:         [N] resources ([Usage])         ║
║   SMS:           [N] resources ([Usage])         ║
║   Chat:          [N] resources ([Usage])         ║
║   Calling:       [N] resources ([Usage])         ║
║   Phone Numbers: [N] resources ([Usage])         ║
╠══════════════════════════════════════════════════╣
║ Reports saved to: ./exports/                     ║
╚══════════════════════════════════════════════════╝

💡 Next Steps:
1. Review migration guides for each detected channel
2. Visit https://aka.ms/acs-retirement-and-breaking-changes-guide
```

## Output
- CSV report (Excel-compatible, 17 columns)
- Markdown report (human-readable with migration guide links)
- JSON report (machine-readable)
- Console summary with channel detection breakdown

## Knowledge Base

Reference data used by this workflow lives in `docs/knowledge/`. Update these files when Microsoft publishes new retirement dates or migration guidance:

| File | Used By |
|------|---------|
| [acs-retirement-dates.md](../../../../docs/knowledge/acs-retirement-dates.md) | Channel status types and effective dates |
| [acs-metric-names.md](../../../../docs/knowledge/acs-metric-names.md) | Metrics collection |
| [acs-migration-paths.md](../../../../docs/knowledge/acs-migration-paths.md) | Migration paths and guide links |
| [acs-channel-status.md](../../../../docs/knowledge/acs-channel-status.md) | Full Breaking Change vs Retirement detail |

## ACS Channel Guides
- 📧 Email — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email
- 📱 SMS — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms
- 💬 Chat — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat
- 📞 Calling — Breaking Change Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk
- ☎️ Phone Numbers — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer
- All channels — Full Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide

## Related Skills (Individual Steps)
Run these individually if you need to re-run a specific step:
- **azure/1-azure-auth-check** — Re-authenticate
- **azure/2-azure-subscription-select** — Change subscription scope
- **1-acs-resource-scan** — Re-run resource discovery
- **2-acs-channel-detect** — Fast channel check
- **3-acs-metrics-collect** — Collect usage metrics
- **4-acs-impact-analyze** — Re-map channels to guides
- **5-acs-report-generate** — Re-export in different format
