---
name: 5-azure-metrics-collect
description: Comprehensive feature/usage detection via Azure Monitor metrics. Collects usage data over configurable lookback period (1-93 days). Works with any Azure product that emits metrics to Azure Monitor.
---

## When to use this skill
Use this skill for complete feature detection based on actual usage metrics (slower but comprehensive).

Examples:
  - "Collect usage metrics for my ACS resources"
  - "Analyze Storage Account usage over the last 90 days"
  - "Get complete feature detection with metrics"
  - "How much are these resources being used?"

## Preconditions
- Azure authentication completed (use **1-azure-auth-check** skill)
- Subscription(s) selected (use **2-azure-subscription-select** skill)
- Resources discovered (use **3-azure-resource-scan** skill)
- User has **Monitoring Reader** access to resources

> **Note:** This is a COMPREHENSIVE detection method. It takes longer (~3-5 minutes per subscription) but provides complete usage-based detection.

## Workflow

### 1) **Load Resource Inventory**
   - Retrieve resource list from session state (saved by **3-azure-resource-scan**)
   - Confirm resources exist to analyze
   - If no resources: Exit with message "No resources to analyze"

### 2) **Configure Metrics Collection**

   **Interactive Mode:**
   - Ask user: "How far back should we check for usage? (1-93 days)"
   - Display recommendation: "💡 Recommended: 90 days for comprehensive analysis"
   - Prompt for lookback period
   - Validate: Must be between 1-93 days (Azure Monitor retention limit)

   **Non-Interactive Mode:**
   - Accept parameter: `-LookbackDays 90`
   - Default: 90 days if not specified

### 3) **Determine Metrics to Collect**

   **Interactive Mode:**
   - Ask user: "Which features/channels do you want to analyze?"
   - Present options based on resource type

   **Predefined Metric Configurations (Examples):**

   **Azure Communication Services:**
   ```
   Email:
     - EmailMessagesSent
     - EmailDeliveryAttempts
     - EmailOperations

   SMS:
     - SMSMessagesSent
     - SMSMessagesReceived

   Chat:
     - ChatMessageCount
     - ChatThreadCount
     - ActiveChatUsers

   Calling:
     - CallDuration
     - CallCount
     - ParticipantCount

   Phone Numbers:
     - PhoneNumberOperations
   ```

   **Storage Accounts:**
   ```
   Blob Storage:
     - BlobCapacity
     - BlobCount
     - Transactions (filter: API = blob)

   File Shares:
     - FileCapacity
     - FileCount
     - Transactions (filter: API = file)

   Queue Storage:
     - QueueCapacity
     - QueueCount
     - QueueMessageCount
   ```

   **Custom Metrics:**
   - Allow user to specify custom metric names
   - Validate metric availability for resource type

### 4) **Calculate Time Range**
   - Set end time: Current date/time
   - Set start time: Current date/time minus lookback days
   - Display: "📅 Analyzing usage from [Start Date] to [End Date] ([N] days)"

### 5) **For Each Resource in Inventory**
   - Display: "📊 Collecting metrics: [Resource Name]"
   - Set Azure context to resource's subscription
   - Initialize metrics results:
     ```
     {
       ResourceId: "...",
       ResourceName: "...",
       LookbackPeriodDays: N,
       FeatureUsage: {},
       DetectionMethod: "Azure Monitor Metrics",
       Complete: true
     }
     ```

### 6) **For Each Feature/Channel**
   - Display progress: "  ⏳ Checking [Feature Name] metrics..."
   - Initialize usage counter = 0

   **For each metric in feature's metric list:**
   - Query Azure Monitor:
     ```powershell
     Get-AzMetric -ResourceId $resourceId `
                  -MetricName $metricName `
                  -StartTime $startTime `
                  -EndTime $endTime `
                  -TimeGrain 01:00:00 `
                  -AggregationType Total `
                  -ErrorAction SilentlyContinue `
                  -WarningAction SilentlyContinue
     ```

   - If metrics returned with data:
     - Sum all metric values: `($metrics.Data | Measure-Object -Property Total -Sum).Sum`
     - Add to feature usage counter

   - If metrics unavailable:
     - Log: "Metric not available (may not be applicable)"
     - Continue to next metric

### 7) **Update Feature Detection Results**
   - If total usage > 0:
     - Mark feature as DETECTED
     - Store usage count
     - Display: "  ✅ [Feature Name]: [Usage Count] (messages/calls/operations)"

   - If total usage = 0:
     - Mark feature as NOT DETECTED (zero usage)
     - Display: "  ⚪ [Feature Name]: 0 usage in last [N] days"

### 8) **Display Resource Usage Summary**
   - For each resource, show comprehensive breakdown:
     ```
     📊 Usage Summary: ACSProd (Last 90 days)
     ┌─────────────────┬──────────────┬────────────────┐
     │ Feature         │ Usage Count  │ Status         │
     ├─────────────────┼──────────────┼────────────────┤
     │ Email           │ 1,250        │ ✅ Detected     │
     │ SMS             │ 0            │ ⚪ Zero usage   │
     │ Chat            │ 543          │ ✅ Detected     │
     │ Calling         │ 0            │ ⚪ Zero usage   │
     │ Phone Numbers   │ 15           │ ✅ Detected     │
     └─────────────────┴──────────────┴────────────────┘

     Total Features with Usage: 3 out of 5
     ```

### 9) **Provide Lookback Period Guidance**
   - If lookback < 93 days:
     - Display: "💡 Want more historical data? Re-run with -LookbackDays 93 (maximum)"

   - If lookback = 93 days:
     - Display: "ℹ️ 93 days is the maximum Azure Monitor retention period for 1-hour granularity"

### 10) **Save Metrics Results**
   - Update resource inventory with metrics data:
     - Add `FeatureUsage` object (feature → usage count)
     - Add `LookbackPeriodDays` field
     - Add `DetectionComplete` flag = true
     - Add `TotalFeaturesDetected` count
   - Store updated inventory in session state

### 11) **Display Collection Summary**
   - Show aggregate statistics:
     ```
     === Metrics Collection Complete ===
     Resources Analyzed: 5
     Lookback Period: 90 days
     Total Features Detected: 12

     Next Steps:
     💡 Use azure-impact-analyze to calculate severity and migration effort
     ```

## Output
- Complete feature usage data per resource
- Usage counts for each feature/channel
- Lookback period used
- Features detected vs. zero usage
- Updated resource inventory with comprehensive metrics

## Performance Characteristics
- **Speed:** ~3-5 minutes per subscription (slower than **4-azure-channel-detect**)
- **Completeness:** 100% feature detection (includes usage-based features)
- **Data Volume:** Queries up to 93 days of hourly metrics per resource

## Error Handling
- Metric not available: Log silently, continue (metric may not apply)
- API throttling: Implement retry logic with exponential backoff
- Permission errors: Display clear error, skip resource

## Cost Considerations
- Azure Monitor API calls are metered
- High resource counts may incur costs
- Recommend batching or limiting scope for large environments

## Related Skills
- Use **1-azure-auth-check**, **2-azure-subscription-select**, **3-azure-resource-scan** before this skill
- Use **4-azure-channel-detect** before this skill (optional - for fast pre-check)
- Use **6-azure-impact-analyze** after this skill to assess severity and effort

## Example Invocation
```
User: "Collect full usage metrics for my ACS resources over 90 days"
Agent: [Runs 5-azure-metrics-collect skill]
Output:
  📅 Analyzing usage from 2025-11-08 to 2026-02-06 (90 days)

  📊 Collecting metrics: ACSProd
    ✅ Email: 1,250 messages
    ⚪ SMS: 0 messages
    ✅ Chat: 543 messages
    ⚪ Calling: 0 calls
    ✅ Phone Numbers: 15 operations

  📊 Collecting metrics: ACSDevAndTest
    ⚪ Email: 0 messages (zero usage in last 90 days)
    ⚪ SMS: 0 messages (zero usage in last 90 days)
    ...

  === Metrics Collection Complete ===
  Resources Analyzed: 2
  Features with Usage: 3 out of 5
```

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 268-363 for example implementation of this workflow.
