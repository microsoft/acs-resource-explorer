# ACS Deprecation Impact Report

**Report Generated:** 2026-02-02
**Assessment Tool:** ACS Impact Assessment PowerShell Script v1.0
**Detection Mode:** FULL (with Azure Monitor metrics)
**Lookback Period:** 90 days

---

## Executive Summary

This report summarizes the impact assessment of Azure Communication Services (ACS) resources in your Azure environment. The scan was performed to identify usage of ACS services that are scheduled for retirement.

### Key Findings

- **Subscriptions Scanned:** 1
- **ACS Resources Found:** 2
- **Resources Using Retiring Services:** 0
- **Migration Action Required:** None

**Good news!** Your ACS resources are not currently using any retiring services based on 90-day usage metrics.

---

## Scan Coverage

### Subscriptions Scanned

| Subscription Name | Subscription ID | Resources Found |
|------------------|-----------------|-----------------|
| JameelaPayAsYouGo | a89e7234-d3e0-4956-aee2-934220095a4e | 2 |

### Resources Analyzed

| Resource Name | Resource Group | Location | Status |
|--------------|---------------|----------|---------|
| ACSProd | JameelaACS_RG | global | No retiring services detected |
| ACSDevAndTest | JameelaACS_RG | global | No retiring services detected |

---

## Channel Usage Analysis (90-Day Period)

The following channels were analyzed for each resource:

### ACSProd
- **Email Service:** 0 messages (not in use)
- **SMS API:** 0 messages (not in use)
- **Chat SDK:** 0 messages (not in use)
- **Calling SDK:** 0 calls (not in use)
- **Phone Numbers SDK:** 0 operations (not in use)

**Severity:** None
**Migration Effort:** None

### ACSDevAndTest
- **Email Service:** 0 messages (not in use)
- **SMS API:** 0 messages (not in use)
- **Chat SDK:** 0 messages (not in use)
- **Calling SDK:** 0 calls (not in use)
- **Phone Numbers SDK:** 0 operations (not in use)

**Severity:** None
**Migration Effort:** None

---

## Retiring Services Reference

For detailed information about each retiring service and retirement dates, see:
- Configuration file: [src/config/retiring-features.ts](../src/config/retiring-features.ts)

### Retiring Services Include:

1. **Email Service** - Custom email domain functionality
2. **SMS API** - SMS sending and receiving capabilities
3. **Chat SDK** - Real-time chat messaging
4. **Calling SDK** - Voice and video calling features
5. **Phone Numbers SDK** - Phone number management and operations

---

## Migration Guidance

Although no active usage was detected, migration guides are available for reference:

- **Email Service Migration:** [migration-guides/email/email-service-migration.md](../migration-guides/email/email-service-migration.md)
- **All Migration Guides:** [migration-guides/README.md](../migration-guides/README.md)

---

## Confidence & Limitations

### Detection Method
This assessment used Azure Monitor metrics to detect channel usage over the last **90 days**. This is the recommended method as it provides accurate usage data based on actual API calls and operations.

### What Was Detected
- All five retiring service channels (Email, SMS, Chat, Calling, Phone Numbers)
- Usage counts based on Azure Monitor metrics
- Resource configurations and deployments

### Limitations
1. **Historical Usage:** Only the last 90 days of usage were analyzed. Usage beyond this period is not included.
2. **Maximum Lookback:** Azure Monitor metrics are retained for a maximum of 93 days at 1-hour granularity.
3. **Inactive Resources:** Resources that have been dormant for more than 90 days would show as "not in use" even if they were previously active.
4. **Configuration vs Usage:** The presence of ACS resources doesn't necessarily mean features are actively used. This scan detected actual usage through metrics.

### Confidence Level
**High Confidence** - The full metrics scan provides accurate detection of all retiring channels based on actual usage patterns.

---

## Next Steps Checklist

Even though no active usage was detected, consider the following actions:

- [ ] Review the detailed CSV report at: `scripts/powershell/exports/ACS_Impact_Assessment.csv`
- [ ] Verify that the ACS resources (ACSProd and ACSDevAndTest) are still needed
- [ ] If resources are unused, consider decommissioning them to reduce costs
- [ ] Document the purpose of each ACS resource for future reference
- [ ] Set up Azure Monitor alerts if you plan to start using ACS features in the future
- [ ] Bookmark migration guides in case you activate any retiring features
- [ ] Re-run this assessment if you begin using ACS services (use `-IncludeMetrics` flag)
- [ ] Consider extending the lookback period to 93 days if needed: `-LookbackDays 93`

---

## Re-running the Assessment

To re-run this assessment in the future:

```powershell
# From the scripts/powershell directory
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# For maximum lookback period (93 days)
.\acs-impact-assessment-tool.ps1 -IncludeMetrics -LookbackDays 93

# For a specific subscription
.\acs-impact-assessment-tool.ps1 -SubscriptionId "your-subscription-id" -IncludeMetrics
```

---

## Additional Resources

- **ACS Impact Assessment Tool:** [scripts/powershell/README.md](../scripts/powershell/README.md)
- **Migration Guides:** [migration-guides/](../migration-guides/)
- **Retiring Features Config:** [src/config/retiring-features.ts](../src/config/retiring-features.ts)
- **Azure Monitor Metrics:** [Microsoft Docs](https://docs.microsoft.com/azure/communication-services/concepts/metrics)

---

## Raw Data

The complete assessment results are available in CSV format:
- **Location:** `scripts/powershell/exports/ACS_Impact_Assessment.csv`
- **Format:** CSV with 19 columns including subscription info, usage counts, severity, and migration effort
- **Use Case:** Import into Excel or Power BI for advanced analysis and reporting

---

**Report Status:** Complete
**Assessment Result:** No migration action required at this time
**Recommendation:** Monitor resources and re-assess if usage patterns change
