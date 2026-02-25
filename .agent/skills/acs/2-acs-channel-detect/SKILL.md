---
name: 2-acs-channel-detect
description: Fast, resource-based detection of ACS channels (Email, Phone Numbers). Detects Email via EmailServices/Domains child resources and Phone Numbers via phoneNumbers child resources. Note: SMS, Chat, and Calling require metrics — use 3-acs-metrics-collect for complete detection.
---

## When to use this skill
Use this skill for a fast (~30 seconds) check of which ACS channels are configured via child resources.

Examples:
  - "Quick check for ACS channels (no metrics)"
  - "Detect which ACS services are configured"
  - "Fast scan for ACS Email and Phone Numbers"
  - "Do I have ACS Email domains set up?"

## Preconditions
- Azure authentication completed (use **azure/1-azure-auth-check** skill)
- ACS resources discovered (use **1-acs-resource-scan** skill)
- User has **Reader** access to resources

> **⚠️ Coverage Limitation:** This skill detects Email and Phone Numbers only.
> SMS, Chat, and Calling usage cannot be detected without metrics.
> For complete 5-channel detection, use **3-acs-metrics-collect**.

## ACS Channel Detection Configuration

| Channel | Detection Method | Child Resource Type |
|---------|-----------------|---------------------|
| Email | Child resources | `Microsoft.Communication/EmailServices/Domains` |
| Phone Numbers | Child resources | `Microsoft.Communication/CommunicationServices/phoneNumbers` |
| SMS | ❌ Requires metrics | Use `3-acs-metrics-collect` |
| Chat | ❌ Requires metrics | Use `3-acs-metrics-collect` |
| Calling | ❌ Requires metrics | Use `3-acs-metrics-collect` |

## Workflow

### 1) **Load ACS Resource Inventory**
   - Retrieve ACS resources from session state (saved by **1-acs-resource-scan**)
   - If no resources: Exit with "No ACS resources to analyze"

### 2) **For Each ACS Resource**
   - Display: "🔍 Analyzing: [Resource Name] ([Resource Group])"
   - Initialize detection results:
     ```
     {
       ResourceName: "...",
       EmailDetected: false,
       EmailDomainCount: 0,
       PhoneNumbersDetected: false,
       PhoneNumberCount: 0,
       SMSDetected: "Requires metrics",
       ChatDetected: "Requires metrics",
       CallingDetected: "Requires metrics",
       DetectionMethod: "Resource-based (fast mode)"
     }
     ```

### 3) **Detect Email Service**
   - Query for Email domain resources in the resource group:
     ```powershell
     Get-AzResource -ResourceGroupName $rgName `
                    -ResourceType "Microsoft.Communication/EmailServices/Domains" `
                    -ErrorAction SilentlyContinue
     ```
   - **If domains found:**
     - Set EmailDetected = true
     - Count domains
     - Display: "  ✅ Email Service detected ([N] domain(s))"

   - **If no domains:**
     - Display: "  ⚪ Email Service not detected (no domains found)"

### 4) **Detect Phone Numbers**
   - Query for phone number resources:
     ```powershell
     Get-AzResource -ResourceGroupName $rgName `
                    -ResourceType "Microsoft.Communication/CommunicationServices/phoneNumbers" `
                    -ErrorAction SilentlyContinue
     ```
   - **If found:**
     - Set PhoneNumbersDetected = true
     - Count phone numbers
     - Display: "  ✅ Phone Numbers detected ([N] number(s))"

   - **If none found:**
     - Display: "  ⚪ Phone Numbers not detected"

### 5) **Display Channel Summary**
   ```
   === ACS Channel Detection Summary: [Resource Name] ===

   ✅ Email Service:   Detected (2 domains)
   ⚪ Phone Numbers:   Not detected
   ⚠️ SMS:             Requires -IncludeMetrics (use 3-acs-metrics-collect)
   ⚠️ Chat:            Requires -IncludeMetrics (use 3-acs-metrics-collect)
   ⚠️ Calling:         Requires -IncludeMetrics (use 3-acs-metrics-collect)

   Channels detected via resources: 1 out of 2 detectable (Email, Phone Numbers)
   Channels requiring metrics: 3 (SMS, Chat, Calling)
   ```

### 6) **Save Detection Results to Session State**
   - Update ACS resource inventory with detection results
   - Flag `RequiresMetricsForComplete = true` for all resources (always true for ACS)

### 7) **Recommend Next Steps**
   ```
   💡 Recommendations:
   - For Email/Phone Numbers only: Proceed to 4-acs-impact-analyze
   - For complete 5-channel detection: Run 3-acs-metrics-collect
   ```

## Output
- Email Service detection status (detected / not detected) + domain count
- Phone Numbers detection status + count
- Clear note that SMS, Chat, Calling require metrics
- Updated session state with detection results

## Detection Speed
- **~30 seconds per subscription**
- Suitable for quick checks or when metrics access is unavailable

## When to Use Metrics Instead
Use **3-acs-metrics-collect** if you need:
- SMS usage detection
- Chat usage detection
- Calling usage detection
- Usage-based detection (actual volume, not just configuration)
- Complete 5-channel coverage

## Related Skills
- Requires **azure/1-azure-auth-check**, **azure/2-azure-subscription-select**, **1-acs-resource-scan**
- Use **3-acs-metrics-collect** for complete detection
- Use **4-acs-impact-analyze** after detection

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 234-266 for example implementation.
