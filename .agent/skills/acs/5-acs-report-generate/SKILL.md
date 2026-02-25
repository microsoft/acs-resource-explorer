---
name: 5-acs-report-generate
description: Generate ACS deprecation impact reports in CSV, Markdown, or JSON format. Pre-configured with all 5 ACS channel columns, ACS migration guide links, and ACS-specific report sections.
---

## When to use this skill
Use this skill to export the complete ACS impact assessment to shareable formats.

Examples:
  - "Export the ACS assessment to CSV"
  - "Generate an ACS deprecation report"
  - "Create a summary of ACS migration impact for my team"
  - "Save the ACS scan results"

## Preconditions
- ACS impact analysis complete (use **4-acs-impact-analyze** — recommended)
- OR at minimum: ACS resources scanned + channel detection complete
- Session state contains ACS resource inventory with analysis data

## Default File Naming
```
{Timestamp}_ACS_Impact_Assessment.{extension}

Examples:
  2026-02-25_ACS_Impact_Assessment.csv
  2026-02-25_ACS_Impact_Assessment.md
  2026-02-25_ACS_Impact_Assessment.json
```

Default output location: `./exports/`

## ACS CSV Columns (19 total)
Pre-configured CSV structure matching the PowerShell tool output:
```
SubscriptionName, SubscriptionId,
ResourceGroup, ResourceName, Location,
LookbackPeriodDays,
EmailDetected, EmailUsageCount,
SMSDetected, SMSUsageCount,
ChatDetected, ChatUsageCount,
CallingDetected, CallingUsageCount,
PhoneNumbersDetected, PhoneNumbersUsageCount,
TotalChannelsImpacted,
HighestSeverity,
MigrationEffortEstimate
```

> This matches the output of `scripts/powershell/acs-impact-assessment-tool.ps1` for cross-tool compatibility.

## Workflow

### 1) **Load ACS Resource Inventory**
   - Retrieve complete inventory from session state
   - Display data availability check:
     ```
     📊 Report Data Summary:
     ACS Resources: [N]
     Subscriptions Scanned: [N]
     Detection Method: [Resource-based / Metrics-based]
     Impact Analysis: [Complete / Not run]
     Lookback Period: [N] days (if metrics used)
     ```
   - If impact analysis not run: Warn user, continue with available data

### 2) **Configure Report Options**
   - Ask user: "What report format(s) would you like?"
     ```
     1. CSV (Excel-compatible, matches PowerShell tool output)
     2. Markdown (Human-readable, suitable for sharing)
     3. JSON (Machine-readable, for integration)
     4. All formats
     ```
   - Prompt for output directory (default: `./exports/`)
   - Prompt for custom filename prefix (default: timestamp + `ACS_Impact_Assessment`)

### 3) **Create Output Directory**
   - Check if `./exports/` exists; create if needed
   - Verify write permissions

### 4) **Generate CSV Report (if selected)**
   - Include ALL scanned resources (even those with zero usage — for complete inventory)
   - Use the pre-configured 19-column structure
   - Export:
     ```powershell
     $inventory | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
     ```
   - Display: "✅ CSV saved: [Path] ([N] resources)"

### 5) **Generate Markdown Report (if selected)**

   **ACS-Specific Markdown Structure:**
   ```markdown
   # ACS Deprecation Impact Assessment Report

   **Analysis Date:** [Date]
   **Detection Method:** [Resource-based / Azure Monitor Metrics]
   **Lookback Period:** [N] days (if metrics used)

   ## Executive Summary
   - Total ACS Resources Scanned: [N]
   - Resources Using Retiring Services: [M]
   - Subscriptions Analyzed: [X]

   ## Retiring ACS Services Detected

   | Channel | Resources Impacted | Usage (last [N] days) |
   |---------|--------------------|----------------------|
   | Email   | [N] | [Usage count] messages |
   | SMS     | [N] | [Usage count] messages |
   | Chat    | [N] | [Usage count] messages |
   | Calling | [N] | [Usage count] calls |
   | Phone Numbers | [N] | [Usage count] operations |

   ## Severity Breakdown
   - 🔴 Critical: [N] resource(s) — Immediate action required
   - 🟡 Warning:  [N] resource(s) — Plan migration soon
   - ℹ️ Info:     [N] resource(s) — Low priority
   - ✅ None:     [N] resource(s) — No migration needed

   ## Priority Migration Plan

   ### Priority 1: [Resource Name] 🔴 Critical
   - **Subscription:** [Name]
   - **Resource Group:** [Name]
   - **Channels Impacted:** Email, Chat, Phone Numbers
   - **Usage:** Email: 1,250 | Chat: 543 | Phone Numbers: 15
   - **Migration Effort:** High
   - **Migration Guides:**
     - 📧 [Email Service Migration](migration-guides/email/email-service-migration.md)
     - 💬 [Chat SDK Migration](https://aka.ms/acs-chat-migration) *(coming soon)*
   - **Next Steps:**
     1. Schedule migration planning meeting
     2. Review Email migration guide
     3. Plan Chat SDK migration

   [Repeat for each resource...]

   ## ACS Migration Resources
   - 📧 Email Service: [migration-guides/email/email-service-migration.md](../migration-guides/email/email-service-migration.md)
   - 💬 Chat SDK: https://aka.ms/acs-chat-migration
   - 📞 Calling SDK: https://aka.ms/acs-calling-migration
   - 📱 SMS API: https://aka.ms/acs-sms-migration
   - ☎️ Phone Numbers: https://aka.ms/acs-phone-migration

   ## Next Steps
   1. Prioritize Critical resources for immediate migration planning
   2. Review migration guides for each impacted channel
   3. Engage ACS support for complex multi-channel migrations
   4. Track progress using the exported CSV

   ## Confidence & Limitations
   - **High confidence:** Channels detected via Azure Monitor metrics
   - **Limited confidence:** Channels detected via resource existence only (actual usage unknown)
   - **Not assessed:** Channels with zero metrics may still be in use if outside lookback period
   ```

### 6) **Generate JSON Report (if selected)**
   - ACS-specific JSON structure:
     ```json
     {
       "metadata": {
         "analysisDate": "2026-02-25",
         "analysisType": "ACS Deprecation Impact Assessment",
         "detectionMethod": "Azure Monitor Metrics",
         "lookbackPeriodDays": 90,
         "toolVersion": "1.0"
       },
       "summary": {
         "totalACSResources": 2,
         "resourcesWithImpact": 1,
         "subscriptionsScanned": 1,
         "channelBreakdown": {
           "email": { "resourcesDetected": 1, "totalUsage": 1250 },
           "sms": { "resourcesDetected": 0, "totalUsage": 0 },
           "chat": { "resourcesDetected": 1, "totalUsage": 543 },
           "calling": { "resourcesDetected": 0, "totalUsage": 0 },
           "phoneNumbers": { "resourcesDetected": 1, "totalUsage": 15 }
         }
       },
       "resources": [...]
     }
     ```

### 7) **Display Console Summary**
   Always display regardless of file export:
   ```
   === ACS Impact Assessment Report ===
   Analysis Date: [Date]

   📊 Scan Summary:
   Total ACS Resources: [N]
   Resources with Retiring Services in Use: [M]
   Subscriptions Scanned: [N]

   📡 Channel Detection Results:
     Email:         [N] resource(s) — [Total Usage] messages
     SMS:           [N] resource(s) — [Total Usage] messages
     Chat:          [N] resource(s) — [Total Usage] messages
     Calling:       [N] resource(s) — [Total Usage] calls
     Phone Numbers: [N] resource(s) — [Total Usage] operations

   🎯 Migration Priority:
     🔴 Critical: [N] resource(s) — Immediate action required
     🟡 Warning:  [N] resource(s) — Plan within 30 days
     ℹ️ Info:     [N] resource(s) — Low priority

   💡 Next Steps:
   1. Review exported reports in: ./exports/
   2. Read migration guides for impacted channels
   3. Visit https://aka.ms/acs-transition-guides for additional resources
   ```

### 8) **Display Report Access Information**
   ```
   📁 Reports Generated:
   ✅ CSV:      ./exports/2026-02-25_ACS_Impact_Assessment.csv
   ✅ Markdown: ./exports/2026-02-25_ACS_Impact_Assessment.md
   ✅ JSON:     ./exports/2026-02-25_ACS_Impact_Assessment.json
   ```

## Output
- CSV file compatible with `acs-impact-assessment-tool.ps1` output format
- Markdown report with ACS migration guide links
- JSON file for automated processing
- Console summary with channel-level statistics

## ACS Migration Resources
- Email: [migration-guides/email/email-service-migration.md](../../../migration-guides/email/email-service-migration.md)
- All channels: https://aka.ms/acs-transition-guides

## Related Skills
- Use **4-acs-impact-analyze** before this skill for complete reports
- This is the final skill in the ACS workflow

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 395-469 for example implementation.
