---
name: 7-azure-report-generate
description: Generate comprehensive reports (CSV, Markdown, JSON) for Azure resource impact assessments. Export detailed findings, statistics, and recommendations. Works with any Azure product deprecation analysis.
---

## When to use this skill
Use this skill to export impact assessment results to shareable formats after completing analysis.

Examples:
  - "Export the results to CSV"
  - "Generate a report of my analysis"
  - "Create a summary document for my team"
  - "Save the impact assessment results"

## Preconditions
- Azure authentication completed (use **1-azure-auth-check** skill)
- Resources scanned (use **3-azure-resource-scan** skill)
- Features detected (use **4-azure-channel-detect** or **5-azure-metrics-collect** skill)
- Impact analyzed (use **6-azure-impact-analyze** skill - optional but recommended)
- Session state contains complete resource inventory with analysis data

## Workflow

### 1) **Load Complete Resource Inventory**
   - Retrieve resource inventory from session state
   - Verify data completeness:
     - ✅ Resource details (name, ID, subscription, location)
     - ✅ Feature detection results
     - ✅ Usage metrics (if collected)
     - ✅ Impact analysis (severity, effort, priority)
   - Display data summary:
     ```
     📊 Report Data Summary:
     Resources: 5
     Subscriptions: 2
     Features Detected: 12
     Impact Analysis: Complete
     ```

### 2) **Configure Report Options**

   **Interactive Mode:**
   - Ask user: "What type of report would you like to generate?"
   - Present options:
     ```
     Report Formats:
     1. CSV (Excel-compatible, detailed data)
     2. Markdown (Human-readable, documentation)
     3. JSON (Machine-readable, API integration)
     4. All formats
     ```
   - Prompt for output directory (default: `./exports/`)
   - Prompt for custom filename prefix (default: timestamp-based)

### 3) **Create Output Directory**
   - Check if output directory exists
   - If not exists:
     - Create directory structure
     - Display: "📁 Created output directory: [Path]"
   - Verify write permissions

### 4) **Generate CSV Report (if selected)**

   **CSV Structure:**
   ```csv
   SubscriptionName,SubscriptionId,ResourceGroup,ResourceName,ResourceType,Location,
   Feature1Detected,Feature1Usage,Feature2Detected,Feature2Usage,...,
   TotalFeaturesImpacted,HighestSeverity,SeverityReason,MigrationEffortEstimate,
   EffortReason,RecommendedPriority,LookbackPeriodDays,AnalysisDate
   ```

   **CSV Generation Steps:**
   - For each resource in inventory:
     - Extract all fields
     - Flatten nested objects (features, usage counts)
     - Format dates (ISO 8601)
     - Escape special characters in text fields
     - Add row to CSV

   - Export using:
     ```powershell
     $inventory | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
     ```

   - Display: "✅ CSV report saved: [Path]"
   - Display row count: "[N] resources exported"

### 5) **Generate Markdown Report (if selected)**

   **Markdown Structure:**
   ```markdown
   # Azure Impact Assessment Report

   **Analysis Date:** [Date]
   **Analysis Type:** [Product Name] Deprecation Impact

   ## Executive Summary
   - Total Resources Scanned: N
   - Resources with Impacted Features: M
   - Subscriptions Analyzed: X
   - Lookback Period: Y days

   ## Severity Breakdown
   - 🔴 Critical: N resources
   - 🟡 Warning: M resources
   - ℹ️ Info: X resources

   ## Migration Effort
   - High: N resources (3-4 weeks each)
   - Medium: M resources (1-2 weeks each)
   - Low: X resources (<1 week each)

   ## Detailed Findings

   ### Priority 1: [Resource Name]
   - **Subscription:** [Name]
   - **Resource Group:** [Name]
   - **Severity:** Critical
   - **Features Impacted:** Feature1, Feature2, Feature3
   - **Usage Summary:**
     - Feature1: [Usage] operations
     - Feature2: [Usage] operations
   - **Migration Effort:** High
   - **Recommended Next Steps:**
     1. [Action 1]
     2. [Action 2]

   [Repeat for each resource...]

   ## Migration Timeline Recommendations

   | Priority | Resource | Target Completion | Effort |
   |----------|----------|-------------------|--------|
   | 1 | Resource1 | [Date] | High |
   | 2 | Resource2 | [Date] | Medium |

   ## Migration Guides

   - [Feature1 Migration Guide](link)
   - [Feature2 Migration Guide](link)

   ## Appendix: Methodology

   ### Data Collection
   - Detection Method: [Resource-based / Metrics-based]
   - Metrics Lookback: [N] days
   - Scan Date: [Date]

   ### Severity Calculation
   [Details of severity thresholds used]

   ### Effort Estimation
   [Details of effort calculation methodology]
   ```

   **Markdown Generation Steps:**
   - Build report sections programmatically
   - Include summary statistics
   - Add detailed resource breakdowns (sorted by priority)
   - Include charts/tables using Markdown syntax
   - Add links to migration guides
   - Include methodology appendix

   - Write to file:
     ```powershell
     $markdownContent | Out-File -FilePath $mdPath -Encoding UTF8
     ```

   - Display: "✅ Markdown report saved: [Path]"

### 6) **Generate JSON Report (if selected)**

   **JSON Structure:**
   ```json
   {
     "metadata": {
       "analysisDate": "2026-02-06T10:30:00Z",
       "analysisType": "ACS Deprecation Impact",
       "toolVersion": "1.0",
       "lookbackPeriodDays": 90,
       "detectionMethod": "Metrics-based"
     },
     "summary": {
       "totalResources": 5,
       "resourcesWithImpact": 3,
       "subscriptionsScanned": 2,
       "totalFeaturesDetected": 12,
       "severityCounts": {
         "critical": 1,
         "warning": 1,
         "info": 1
       },
       "effortCounts": {
         "high": 1,
         "medium": 1,
         "low": 1
       }
     },
     "resources": [
       {
         "subscriptionId": "...",
         "subscriptionName": "...",
         "resourceGroup": "...",
         "resourceName": "...",
         "resourceType": "...",
         "location": "...",
         "features": [
           {
             "name": "Email",
             "detected": true,
             "usage": 1250,
             "severity": "critical"
           }
         ],
         "impact": {
           "totalFeaturesImpacted": 3,
           "highestSeverity": "Critical",
           "severityReason": "...",
           "migrationEffort": "High",
           "effortReason": "...",
           "recommendedPriority": 1
         },
         "recommendations": [
           "Action 1",
           "Action 2"
         ]
       }
     ]
   }
   ```

   **JSON Generation Steps:**
   - Build structured object with metadata, summary, and resource details
   - Ensure proper data types (numbers, booleans, strings)
   - Format dates as ISO 8601
   - Convert inventory to JSON:
     ```powershell
     $jsonData | ConvertTo-Json -Depth 10 | Out-File -FilePath $jsonPath -Encoding UTF8
     ```

   - Display: "✅ JSON report saved: [Path]"

### 7) **Generate Console Summary Report**

   **Always display regardless of file export options:**
   ```
   === Azure Impact Assessment Report ===
   Analysis Date: 2026-02-06

   📊 Scan Summary:
   Total Resources: 5
   Resources with Impacted Features: 3
   Subscriptions Scanned: 2
   Lookback Period: 90 days

   🎯 Severity Breakdown:
   🔴 Critical: 1 resource(s) - IMMEDIATE ACTION REQUIRED
   🟡 Warning:  1 resource(s) - Plan migration within 30 days
   ℹ️ Info:     1 resource(s) - Low priority

   📋 Migration Effort:
   High:   1 resource(s) - Allocate 3-4 weeks per resource
   Medium: 1 resource(s) - Allocate 1-2 weeks per resource
   Low:    1 resource(s) - Allocate <1 week per resource

   📈 Detailed Results:

   [Formatted table with key columns]

   === Recommendations ===

   Immediate Actions (Critical):
   • 1 resource requires immediate attention
   • Start with: ACSProd (Priority 1)

   Upcoming Actions (Warning):
   • 1 resource should be migrated within 30 days

   💡 Next Steps:
   1. Review exported reports in: [Output Directory]
   2. Read migration guides for impacted features
   3. Schedule planning meetings for Critical resources
   4. Track migration progress using exported CSV
   ```

### 8) **Generate Statistics Summary**
   - Calculate and display additional insights:
     ```
     📊 Additional Statistics:

     By Subscription:
       - Production:   3 resources (2 impacted)
       - Development:  2 resources (1 impacted)

     By Feature:
       - Email:        2 resources detected
       - SMS:          1 resource detected
       - Chat:         1 resource detected
       - Calling:      0 resources detected
       - Phone Numbers: 2 resources detected

     Usage Volume (90 days):
       - Total Email Messages:     1,250
       - Total SMS Messages:       0
       - Total Chat Messages:      543
       - Total Calls:              0
       - Total Phone Operations:   15
     ```

### 9) **Provide Report Access Information**
   - Display file locations:
     ```
     📁 Reports Generated:

     ✅ CSV:      [Full Path] ([File Size])
     ✅ Markdown: [Full Path] ([File Size])
     ✅ JSON:     [Full Path] ([File Size])

     💡 Tips:
     - Open CSV in Excel for filtering and sorting
     - Share Markdown with your team for human-readable summary
     - Use JSON for automated processing or integration
     ```

### 10) **Optional: Send Report via Email**
   - Ask user: "Would you like to email this report? (Y/N)"
   - If YES:
     - Prompt for recipient email(s)
     - Prompt for subject line
     - Attach generated files
     - Send using configured email service
     - Display: "📧 Report sent to [Recipients]"

### 11) **Optional: Upload to Azure Storage**
   - Ask user: "Would you like to upload reports to Azure Storage? (Y/N)"
   - If YES:
     - Prompt for storage account and container
     - Upload reports to blob storage
     - Generate SAS URL for sharing
     - Display: "☁️ Reports uploaded: [Blob URL]"

## Output Files

### Default Naming Convention
```
{Timestamp}_{ProductName}_Impact_Assessment.{extension}

Examples:
- 2026-02-06_ACS_Impact_Assessment.csv
- 2026-02-06_Storage_Impact_Assessment.md
- 2026-02-06_SQL_Impact_Assessment.json
```

### File Locations
- Default: `./exports/`
- Custom: User-specified directory
- Cloud: Azure Blob Storage (optional)

## Report Sections (Markdown/PDF)

1. **Executive Summary** - High-level overview
2. **Severity Breakdown** - Distribution of impact levels
3. **Migration Effort** - Estimated work required
4. **Detailed Findings** - Resource-by-resource analysis
5. **Priority Recommendations** - Ordered migration plan
6. **Migration Timeline** - Suggested schedule
7. **Migration Guides** - Links to documentation
8. **Methodology** - How analysis was performed
9. **Appendix** - Raw data tables

## Customization Options
- Custom report templates
- Company branding/logo
- Additional calculated fields
- Custom sorting/grouping
- Filter by severity, subscription, or resource type

## Related Skills
- Use **6-azure-impact-analyze** before this skill (for complete reports)
- This is typically the FINAL skill in the workflow sequence

## Example Invocation
```
User: "Generate a report with all the analysis results"
Agent: [Runs 7-azure-report-generate skill]
Output:
  📊 Report Data Summary:
  Resources: 2
  Features Detected: 3
  Impact Analysis: Complete

  What format would you like?
  1. CSV
  2. Markdown
  3. JSON
  4. All formats

  User selects: 4

  📁 Created output directory: ./exports/
  ✅ CSV report saved: ./exports/2026-02-06_ACS_Impact_Assessment.csv (2 resources)
  ✅ Markdown report saved: ./exports/2026-02-06_ACS_Impact_Assessment.md
  ✅ JSON report saved: ./exports/2026-02-06_ACS_Impact_Assessment.json

  [Displays console summary...]
```

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 395-469 for example implementation of this workflow.
