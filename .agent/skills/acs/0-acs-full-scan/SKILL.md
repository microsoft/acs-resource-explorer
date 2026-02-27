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
acs/4-acs-impact-analyze           → Severity, effort, priority ranking
acs/5-acs-report-generate          → Export CSV, Markdown, and/or JSON
```

## Preconditions
- PowerShell Az module installed (`Install-Module -Name Az`)
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

### Step 5: Impact Analysis
   - Run **4-acs-impact-analyze**
   - Apply ACS-specific severity thresholds
   - Calculate migration effort per channel
   - Generate priority ranking
   - Link to ACS migration guides

### Step 6: Report Generation
   - Run **5-acs-report-generate**
   - Default: Generate all formats (CSV + Markdown + JSON)
   - Output to `./exports/` directory
   - CSV format is compatible with `acs-impact-assessment-tool.ps1` output

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
║ 🔴 Critical: [N] resource(s)                    ║
║ 🟡 Warning:  [N] resource(s)                    ║
║ ℹ️  Info:     [N] resource(s)                    ║
║ ✅ None:      [N] resource(s)                    ║
╠══════════════════════════════════════════════════╣
║ Reports saved to: ./exports/                     ║
╚══════════════════════════════════════════════════╝

💡 Next Steps:
1. Prioritize 🔴 Critical resources first
2. Review migration guides for each detected channel
3. Visit https://aka.ms/acs-transition-guides
```

## Output
- CSV report (Excel-compatible, 19 columns)
- Markdown report (human-readable with migration guide links)
- JSON report (machine-readable)
- Console summary with severity and channel breakdown

## Knowledge Base

Reference data used by this workflow lives in `docs/knowledge/`. Update these files when Microsoft publishes new retirement dates or migration guidance:

| File | Used By |
|------|---------|
| [acs-retirement-dates.md](../../../../docs/knowledge/acs-retirement-dates.md) | Impact analysis urgency |
| [acs-metric-names.md](../../../../docs/knowledge/acs-metric-names.md) | Metrics collection |
| [acs-severity-thresholds.md](../../../../docs/knowledge/acs-severity-thresholds.md) | Severity + effort calculation |
| [acs-migration-paths.md](../../../../docs/knowledge/acs-migration-paths.md) | Report links + next steps |

## ACS Migration Guides
- 📧 Email: [migration-guides/email/email-service-migration.md](../../../migration-guides/email/email-service-migration.md)
- All channels: https://aka.ms/acs-transition-guides

## Related Skills (Individual Steps)
Run these individually if you need to re-run a specific step:
- **azure/1-azure-auth-check** — Re-authenticate
- **azure/2-azure-subscription-select** — Change subscription scope
- **1-acs-resource-scan** — Re-run resource discovery
- **2-acs-channel-detect** — Fast channel check
- **3-acs-metrics-collect** — Collect usage metrics
- **4-acs-impact-analyze** — Re-analyze with different thresholds
- **5-acs-report-generate** — Re-export in different format
