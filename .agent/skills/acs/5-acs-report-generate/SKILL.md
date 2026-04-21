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

## ACS CSV Columns (17 total)
Pre-configured CSV structure:
```
SubscriptionName, SubscriptionId,
ResourceGroup, ResourceName, Location,
LookbackPeriodDays,
EmailDetected, EmailUsageCount,
SMSDetected, SMSUsageCount,
ChatDetected, ChatUsageCount,
CallingDetected, CallingUsageCount,
PhoneNumbersDetected, PhoneNumbersUsageCount,
TotalChannelsImpacted
```

## Workflow

### 0) **Load Knowledge References**
   Read the following knowledge files before generating the report:
   - Read `docs/knowledge/acs-retirement-dates.md` — channel status types and effective dates for report headers
   - Read `docs/knowledge/acs-migration-paths.md` — migration paths and guide links for per-resource recommendations

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
     1. CSV (Excel-compatible)
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
   - Use the pre-configured 17-column structure
   - Build CSV content by constructing a header row followed by one data row per resource,
     with all values comma-separated and quoted where necessary
   - Write the CSV content directly to the output file using the Write tool
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

   ## ACS Channel Detection Results

   | Channel | Resources Impacted | Usage (last [N] days) | Status Type |
   |---------|--------------------|-----------------------|-------------|
   | Email   | [N] | [Usage count] messages | 🔴 Retirement |
   | SMS     | [N] | [Usage count] messages | 🔴 Retirement |
   | Chat    | [N] | [Usage count] messages | 🔴 Retirement |
   | Calling | [N] | [Usage count] calls    | 🟡 Breaking Change |
   | Phone Numbers | [N] | [Usage count] operations | 🔴 Retirement |

   ## Resource Impact Summary

   ### [Resource Name]
   - **Subscription:** [Name]
   - **Resource Group:** [Name]
   - **Channels Detected:** Email, Chat, Phone Numbers
   - **Usage:** Email: 1,250 | Chat: 543 | Phone Numbers: 15
   - **Guides:**
     - 📧 [Email Retirement Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email)
     - 💬 [Chat Retirement Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat)
     - 📞 [Calling Breaking Change Guide](https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk) *(if Calling detected)*

   [Repeat for each resource...]

   ## ACS Channel Guides
   - 📧 Email — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email
   - 📱 SMS — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms
   - 💬 Chat — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat
   - 📞 Calling — Breaking Change Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk
   - ☎️ Phone Numbers — Retirement Guide: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer

   ## Next Steps
   1. Review migration guides for each detected channel
   2. Engage ACS support for complex multi-channel migrations
   3. Track progress using the exported CSV

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
     📧 Email:         [N] resource(s) — [Total Usage] messages (Retirement)
     📱 SMS:           [N] resource(s) — [Total Usage] messages (Retirement)
     💬 Chat:          [N] resource(s) — [Total Usage] messages (Retirement)
     📞 Calling:       [N] resource(s) — [Total Usage] calls (Breaking Change — Teams required)
     ☎️ Phone Numbers: [N] resource(s) — [Total Usage] operations (Retirement)

   💡 Next Steps:
   1. Review exported reports in: ./exports/
   2. Read the guide for each detected channel
   3. Visit https://aka.ms/acs-retirement-and-breaking-changes-guide for complete migration guidance
   ```

### 8) **Display Report Access Information**
   ```
   📁 Reports Generated:
   ✅ CSV:      ./exports/2026-02-25_ACS_Impact_Assessment.csv
   ✅ Markdown: ./exports/2026-02-25_ACS_Impact_Assessment.md
   ✅ JSON:     ./exports/2026-02-25_ACS_Impact_Assessment.json
   ```

## Output
- CSV file with complete ACS channel data (17 columns)
- Markdown report with ACS migration guide links
- JSON file for automated processing
- Console summary with channel-level statistics

## Knowledge References

> Authoritative reference data for this skill — update these files when retirement dates or migration paths change:
> - **Retirement dates:** [docs/knowledge/acs-retirement-dates.md](../../../../docs/knowledge/acs-retirement-dates.md)
> - **Migration paths & guide links:** [docs/knowledge/acs-migration-paths.md](../../../../docs/knowledge/acs-migration-paths.md)

## ACS Migration Resources
- 📧 Email: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-email
- 📱 SMS: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-sms
- 💬 Chat: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-chat
- 📞 Calling: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-voicevideo-calling-sdk
- ☎️ Phone Numbers: https://aka.ms/acs-retirement-and-breaking-changes-guide#acs-number-management-direct-offer
- Retirement & Breaking Changes: https://aka.ms/acs-retirement-and-breaking-changes-guide
- Full migration paths reference: [docs/knowledge/acs-migration-paths.md](../../../../docs/knowledge/acs-migration-paths.md)

## Related Skills
- Use **4-acs-impact-analyze** before this skill for complete reports
- This is the final skill in the ACS workflow
