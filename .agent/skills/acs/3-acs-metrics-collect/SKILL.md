---
name: 3-acs-metrics-collect
description: Comprehensive ACS usage detection via Azure Monitor metrics. All 5 ACS channels pre-configured (Email, SMS, Chat, Calling, Phone Numbers). Configurable lookback period of 1-93 days.
---

## When to use this skill
Use this skill for complete detection of all 5 retiring ACS channels based on actual usage metrics.

Examples:
  - "Collect full ACS usage metrics"
  - "Check all ACS channels with metrics"
  - "Run complete ACS channel detection"
  - "How much are my ACS resources being used?"

## Preconditions
- Azure authentication completed (use **azure/1-azure-auth-check** skill)
- ACS resources discovered (use **1-acs-resource-scan** skill)
- User has **Monitoring Reader** access to ACS resources

> **⏱️ Performance Note:** This skill takes ~3-5 minutes per subscription but provides 100% channel coverage across all 5 retiring ACS services.

## Knowledge References

> Authoritative reference data for this skill — update these files when Microsoft changes metric names or query parameters:
> - **Metric names & query parameters:** [docs/knowledge/acs-metric-names.md](../../../../docs/knowledge/acs-metric-names.md)

## ACS Metrics Configuration

All metrics are pre-configured. No manual setup required. See [acs-metric-names.md](../../../../docs/knowledge/acs-metric-names.md) for the full reference including aggregation types and query parameters.

| Channel | Metrics Collected |
|---------|------------------|
| Email | `EmailMessagesSent`, `EmailDeliveryAttempts`, `EmailOperations` |
| SMS | `SMSMessagesSent`, `SMSMessagesReceived` |
| Chat | `ChatMessageCount`, `ChatThreadCount`, `ActiveChatUsers` |
| Calling | `CallDuration`, `CallCount`, `ParticipantCount` |
| Phone Numbers | `PhoneNumberOperations` |

## Workflow

### 0) **Load Knowledge References**
   Read the following knowledge file before collecting metrics:
   - Read `docs/knowledge/acs-metric-names.md` — metric names, aggregation types, and query parameters for all 5 ACS channels

### 1) **Load ACS Resource Inventory**
   - Retrieve ACS resources from session state (saved by **1-acs-resource-scan**)
   - If no resources: Exit with "No ACS resources to analyze"

### 2) **Configure Lookback Period**
   - Ask user: "How many days of usage history should we analyze? (1-93)"
   - Display recommendation: "💡 Recommended: 90 days for comprehensive analysis"
   - Default: 90 days if not specified
   - Maximum: 93 days (Azure Monitor hourly granularity retention limit)

### 3) **Calculate Time Range**
   - End time: Current date/time (UTC)
   - Start time: End time minus lookback days
   - Display: "📅 Analyzing usage from [Start Date] to [End Date] ([N] days)"

### 4) **For Each ACS Resource**
   - Display: "📊 Collecting metrics: [Resource Name] ([Resource Group])"
   - Set Azure context to resource's subscription
   - Initialize ACS-specific results:
     ```
     {
       ResourceName: "...",
       ResourceId: "...",
       LookbackPeriodDays: N,
       EmailUsageCount: 0,        EmailDetected: false,
       SMSUsageCount: 0,          SMSDetected: false,
       ChatUsageCount: 0,         ChatDetected: false,
       CallingUsageCount: 0,      CallingDetected: false,
       PhoneNumbersUsageCount: 0, PhoneNumbersDetected: false,
       TotalChannelsDetected: 0,
       DetectionMethod: "Azure Monitor Metrics",
       DetectionComplete: true
     }
     ```

### 5) **Collect Metrics for Each Channel**

   For each channel, query Azure Monitor via the Azure CLI:
   ```bash
   az monitor metrics list \
     --resource <resource-id> \
     --metric <metric-name> \
     --start-time <start-time-UTC> \
     --end-time <end-time-UTC> \
     --interval PT1H \
     --aggregation Total \
     --output json
   ```

   Sum returned values by iterating `value[0].timeseries[].data[].total` and summing all non-null entries.

   **Email (3 metrics):**
   - Query: `EmailMessagesSent`, `EmailDeliveryAttempts`, `EmailOperations`
   - Display progress: "  ⏳ Checking Email metrics..."
   - If total > 0: Set EmailDetected = true, store EmailUsageCount

   **SMS (2 metrics):**
   - Query: `SMSMessagesSent`, `SMSMessagesReceived`
   - Display progress: "  ⏳ Checking SMS metrics..."
   - If total > 0: Set SMSDetected = true, store SMSUsageCount

   **Chat (3 metrics):**
   - Query: `ChatMessageCount`, `ChatThreadCount`, `ActiveChatUsers`
   - Display progress: "  ⏳ Checking Chat metrics..."
   - If total > 0: Set ChatDetected = true, store ChatUsageCount

   **Calling (3 metrics):**
   - Query: `CallDuration`, `CallCount`, `ParticipantCount`
   - Display progress: "  ⏳ Checking Calling metrics..."
   - If total > 0: Set CallingDetected = true, store CallingUsageCount

   **Phone Numbers (1 metric):**
   - Query: `PhoneNumberOperations`
   - Display progress: "  ⏳ Checking Phone Numbers metrics..."
   - If total > 0: Set PhoneNumbersDetected = true, store PhoneNumbersUsageCount

### 6) **Display Resource Usage Summary**
   ```
   📊 Usage Summary: [Resource Name] (Last [N] days)
   ┌─────────────────┬───────────────┬────────────────┐
   │ Channel         │ Usage Count   │ Status         │
   ├─────────────────┼───────────────┼────────────────┤
   │ Email           │ 1,250         │ ✅ Detected     │
   │ SMS             │ 0             │ ⚪ Zero usage   │
   │ Chat            │ 543           │ ✅ Detected     │
   │ Calling         │ 0             │ ⚪ Zero usage   │
   │ Phone Numbers   │ 15            │ ✅ Detected     │
   └─────────────────┴───────────────┴────────────────┘

   Channels with usage: 3 out of 5
   ```

### 7) **Provide Lookback Guidance**
   - If lookback < 93 days:
     - Display: "💡 Want more coverage? Re-run with -LookbackDays 93 (maximum)"
   - If lookback = 93 days:
     - Display: "ℹ️ 93 days is the maximum Azure Monitor retention for hourly granularity"

### 8) **Save Metrics Results to Session State**
   - Update ACS resource inventory with complete channel usage data
   - All 5 channel fields populated (detected flag + usage count)
   - Include lookback period for downstream reference

### 9) **Display Collection Summary**
   ```
   === ACS Metrics Collection Complete ===
   Resources Analyzed: [N]
   Lookback Period: [N] days

   Channel Detection Summary (across all resources):
     ✅ Email:          [N] resource(s) with usage
     ✅ SMS:            [N] resource(s) with usage
     ⚪ Chat:           0 resource(s) with usage
     ⚪ Calling:        0 resource(s) with usage
     ✅ Phone Numbers:  [N] resource(s) with usage

   💡 Next: Run 4-acs-impact-analyze to map detected channels to migration guides
   ```

## Output
- Usage counts for all 5 ACS channels per resource
- Detection flags (true/false) for each channel
- Lookback period used
- Updated session state with complete ACS metrics data

## Performance
- **Speed:** ~3-5 minutes per subscription
- **Coverage:** 100% — all 5 retiring ACS channels detected
- **Data range:** 1-93 days of hourly usage data

## Error Handling
- Metric unavailable: Silent (metric may not apply to resource), continue
- API throttling: Retry with exponential backoff
- Permission denied: Display error, skip resource

## Related Skills
- Requires **azure/1-azure-auth-check**, **azure/2-azure-subscription-select**, **1-acs-resource-scan**
- Can be combined with **2-acs-channel-detect** for fast pre-check
- Use **4-acs-impact-analyze** after this skill

