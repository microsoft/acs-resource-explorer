---
name: 6-azure-impact-analyze
description: Calculate severity and migration effort for Azure resources with detected features. Configurable severity thresholds based on usage patterns and business impact. Works with any Azure product deprecation scenario.
---

## When to use this skill
Use this skill after feature detection to assess business impact and prioritize migration efforts.

Examples:
  - "Analyze the impact of these detected features"
  - "Calculate severity for resources with retiring services"
  - "Estimate migration effort for these resources"
  - "Which resources should I prioritize for migration?"

## Preconditions
- Azure authentication completed (use **1-azure-auth-check** skill)
- Resources discovered (use **3-azure-resource-scan** skill)
- Features detected (use **4-azure-channel-detect** or **5-azure-metrics-collect** skill)
- Session state contains resource inventory with feature detection results

## Workflow

### 1) **Load Resource Inventory with Detection Results**
   - Retrieve resource inventory from session state
   - Verify each resource has feature detection data:
     - `FeaturesDetected` array
     - `FeatureUsage` object (if metrics collected)
     - `TotalFeaturesDetected` count
   - If no detection data: Exit with message "Run azure-channel-detect or azure-metrics-collect first"

### 2) **Configure Severity Thresholds**

   **Interactive Mode:**
   - Ask user: "Do you want to use predefined severity rules or define custom thresholds?"
   - Present options:
     ```
     Severity Configuration:
     1. Use predefined rules (recommended for common Azure products)
     2. Define custom usage thresholds
     3. Define custom business impact rules
     ```

   **Predefined Severity Rules (Examples):**

   **Azure Communication Services:**
   ```
   Critical Severity:
     - Email usage > 1,000 messages/day average
     - Calling usage > 500 calls/day average
     - Any feature with >10,000 operations in period

   Warning Severity:
     - Email usage > 100 messages/day average
     - SMS usage > 50 messages/day average
     - Any feature with >1,000 operations in period

   Info Severity:
     - Any feature detected with usage below Warning threshold
     - Resources with features detected but low usage
   ```

   **Storage Accounts:**
   ```
   Critical Severity:
     - Total transactions > 1,000,000 in period
     - Data stored > 10 TB
     - Business-critical tag present

   Warning Severity:
     - Total transactions > 100,000 in period
     - Data stored > 1 TB

   Info Severity:
     - Feature detected with minimal usage
   ```

   **Custom Threshold Configuration:**
   - Allow user to specify:
     - Usage thresholds per feature
     - Retirement timeline urgency (days until retirement)
     - Business criticality tags
     - Custom severity rules

### 3) **For Each Resource in Inventory**
   - Display: "🔍 Analyzing impact: [Resource Name]"
   - Initialize impact assessment:
     ```
     {
       ResourceId: "...",
       ResourceName: "...",
       SubscriptionName: "...",
       ResourceGroup: "...",
       Location: "...",

       TotalFeaturesImpacted: 0,
       FeaturesWithUsage: [],

       HighestSeverity: "None",
       SeverityReason: "",

       MigrationEffortEstimate: "None",
       EffortReason: "",

       RecommendedPriority: 0,
       NextSteps: []
     }
     ```

### 4) **Calculate Severity for Each Feature**
   - For each detected feature:
     - Get usage count (if metrics available)
     - Get lookback period (to calculate average)
     - Apply severity rules:

       **Usage-Based Severity:**
       - Calculate daily average: `usageCount / lookbackDays`
       - Compare against thresholds
       - Assign severity: Critical / Warning / Info

       **Timeline-Based Severity:**
       - If retirement date known:
         - Days until retirement < 30: Increase severity
         - Days until retirement < 90: Add urgency flag

       **Business Impact:**
       - Check resource tags (e.g., "Environment=Production")
       - Increase severity for production resources

   - Select highest severity across all features
   - Store severity reason:
     ```
     Example: "Critical: Email usage (1,250 messages over 90 days = 14/day average) exceeds threshold (10/day)"
     ```

### 5) **Estimate Migration Effort**
   - Calculate based on multiple factors:

     **Factor 1: Number of Impacted Features**
     ```
     High Effort:   3+ features with usage
     Medium Effort: 2 features with usage
     Low Effort:    1 feature with usage
     ```

     **Factor 2: Usage Volume**
     ```
     High Effort:   Any feature with >10,000 operations
     Medium Effort: Any feature with >1,000 operations
     Low Effort:    All features with <1,000 operations
     ```

     **Factor 3: Feature Complexity**
     ```
     High Effort:   Features requiring code changes + testing
     Medium Effort: Features requiring configuration changes
     Low Effort:    Features with direct drop-in replacements
     ```

     **Factor 4: Integration Depth**
     ```
     High Effort:   Deeply integrated (multiple callsites, custom logic)
     Medium Effort: Moderately integrated (few callsites, standard patterns)
     Low Effort:    Lightly integrated (single callsite, simple usage)
     ```

   - Combine factors using weighted scoring
   - Assign final effort estimate: High / Medium / Low
   - Store effort reason

### 6) **Calculate Recommended Priority**
   - Priority scoring formula:
     ```
     Priority Score =
       (Severity Weight) +
       (Effort Weight) +
       (Usage Volume Weight) +
       (Timeline Urgency Weight)

     Weights:
       Critical Severity: +100 points
       Warning Severity:  +50 points
       Info Severity:     +10 points

       High Effort:       +30 points (needs more time)
       Medium Effort:     +20 points
       Low Effort:        +10 points

       High Usage:        +20 points (high business impact)
       Timeline < 30 days: +50 points (urgent)
       Timeline < 90 days: +25 points
     ```

   - Sort resources by priority score (highest first)
   - Assign priority ranks: 1 (highest), 2, 3, ...

### 7) **Generate Recommended Next Steps**
   - Based on severity, effort, and priority, generate actionable recommendations:

     **Critical Severity + High Priority:**
     ```
     1. ⚠️ URGENT: Schedule migration planning meeting immediately
     2. Review migration guide for [Feature Name]
     3. Allocate engineering resources (estimated [Effort] effort)
     4. Plan for testing and rollback strategy
     5. Set migration completion target: [Date based on retirement timeline]
     ```

     **Warning Severity + Medium Priority:**
     ```
     1. Review usage patterns to confirm feature necessity
     2. Read migration guide: [Link]
     3. Plan migration for [Timeframe]
     4. Consider using migration grace period if available
     ```

     **Info Severity + Low Priority:**
     ```
     1. Monitor usage trends
     2. Review migration guide: [Link]
     3. Plan migration for [Timeframe]
     4. Consider if feature is still needed (low usage detected)
     ```

### 8) **Display Impact Analysis Results**
   - Show comprehensive table:
     ```
     === Impact Analysis Results ===

     ┌─────────────────┬────────────┬──────────────┬──────────────┬──────────┐
     │ Resource        │ Features   │ Severity     │ Effort       │ Priority │
     ├─────────────────┼────────────┼──────────────┼──────────────┼──────────┤
     │ ACSProd         │ 3          │ Critical     │ High         │ 1        │
     │ StorageMain     │ 2          │ Warning      │ Medium       │ 2        │
     │ ACSDevAndTest   │ 1          │ Info         │ Low          │ 3        │
     └─────────────────┴────────────┴──────────────┴──────────────┴──────────┘

     Severity Breakdown:
       🔴 Critical: 1 resource(s) - IMMEDIATE ACTION REQUIRED
       🟡 Warning:  1 resource(s) - Plan migration soon
       ℹ️ Info:     1 resource(s) - Low priority

     Migration Effort:
       High:   1 resource(s) - Allocate 3-4 weeks per resource
       Medium: 1 resource(s) - Allocate 1-2 weeks per resource
       Low:    1 resource(s) - Allocate <1 week per resource
     ```

### 9) **Display Priority List**
   - Show resources in priority order:
     ```
     🎯 Recommended Migration Order:

     1. [Priority 1] ACSProd
        Severity: Critical | Effort: High | Features: Email, Chat, Phone Numbers
        Reason: High usage (1,250 emails, 543 chats) + Production environment
        Next Step: Schedule migration planning immediately

     2. [Priority 2] StorageMain
        Severity: Warning | Effort: Medium | Features: Blob Storage, File Shares
        Reason: Moderate usage (50k transactions) + Approaching retirement date
        Next Step: Review migration guide and plan timeline

     3. [Priority 3] ACSDevAndTest
        Severity: Info | Effort: Low | Features: Email
        Reason: Zero usage detected in last 90 days
        Next Step: Consider decommissioning if no longer needed
     ```

### 10) **Save Impact Analysis**
   - Update resource inventory with impact data:
     - Add severity, effort, priority fields
     - Add next steps recommendations
     - Add analysis metadata (thresholds used, date analyzed)
   - Store updated inventory in session state

### 11) **Provide Summary Recommendations**
   - Display overall guidance:
     ```
     💡 Summary Recommendations:

     Immediate Actions (Critical):
       • 1 resource requires immediate attention
       • Estimated total effort: High (3-4 weeks)
       • Start with: ACSProd

     Upcoming Actions (Warning):
       • 1 resource should be migrated within 30 days
       • Estimated total effort: Medium (1-2 weeks)

     Low Priority (Info):
       • 1 resource with low usage - review necessity
       • Consider decommissioning unused resources

     Next Steps:
       1. Use azure-report-generate to export detailed report
       2. Review migration guides for each impacted feature
       3. Schedule planning meetings for Critical resources
       4. Set up project tracking for migration efforts
     ```

## Output
- Severity assessment per resource
- Migration effort estimates
- Prioritized resource list (highest priority first)
- Recommended next steps for each resource
- Summary statistics and recommendations
- Updated resource inventory with impact analysis

## Customization Options
- Custom severity thresholds
- Custom effort estimation rules
- Business-specific priority weighting
- Timeline urgency adjustments
- Tag-based impact rules

## Related Skills
- Use **3-azure-resource-scan**, **4-azure-channel-detect**, or **5-azure-metrics-collect** before this skill
- Use **7-azure-report-generate** after this skill to export results

## Example Invocation
```
User: "Analyze the impact and prioritize my resources for migration"
Agent: [Runs 6-azure-impact-analyze skill]
Output:
  🔍 Analyzing impact: ACSProd
  🔴 Critical Severity: Email usage (1,250 messages) exceeds threshold
  📊 Migration Effort: High (3 features impacted)

  🔍 Analyzing impact: ACSDevAndTest
  ℹ️ Info Severity: Zero usage detected
  📊 Migration Effort: Low (0 features with usage)

  === Impact Analysis Results ===
  Critical Resources: 1
  Warning Resources:  0
  Info Resources:     1

  🎯 Priority 1: ACSProd - Immediate action required
```

