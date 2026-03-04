---
name: 4-azure-channel-detect
description: Fast, resource-based feature detection for Azure resources. Detects features/channels by examining related child resources (domains, endpoints, configurations). Works with any Azure product where features are exposed as sub-resources.
---

## When to use this skill
Use this skill for fast detection of features or capabilities based on related Azure resources (without querying metrics).

Examples:
  - "Detect which ACS channels are configured (fast mode)"
  - "Check which Storage Account features are enabled"
  - "Find configured endpoints for my API Management service"
  - "Quick scan for enabled features without metrics"

## Preconditions
- Azure authentication completed (use **1-azure-auth-check** skill)
- Subscription(s) selected (use **2-azure-subscription-select** skill)
- Resources discovered (use **3-azure-resource-scan** skill)
- User has **Reader** access to resources

> **Note:** This is a FAST detection method. For complete feature/usage detection including metrics-based analysis, use **5-azure-metrics-collect** skill.

## Workflow

### 1) **Load Resource Inventory**
   - Retrieve resource list from session state (saved by **3-azure-resource-scan**)
   - Confirm resources exist to analyze
   - If no resources: Exit with message "No resources to analyze"

### 2) **Determine Detection Configuration**

   **Interactive Mode:**
   - Display: "Configure feature detection for [Resource Type]"
   - Ask user: "What features/channels do you want to detect?"
   - Present detection methods:
     ```
     Detection Methods:
     1. Use predefined configuration (for common Azure products)
     2. Specify child resource types to check
     3. Specify resource properties/configurations to check
     ```

   **Predefined Configurations (Examples):**
   - **Azure Communication Services:**
     - Email: Check for `Microsoft.Communication/EmailServices/Domains`
     - Phone Numbers: Check for `Microsoft.Communication/CommunicationServices/phoneNumbers`

   - **Storage Accounts:**
     - Blob Storage: Check `properties.primaryEndpoints.blob`
     - File Shares: Check `Microsoft.Storage/storageAccounts/fileServices`
     - Queue Storage: Check `properties.primaryEndpoints.queue`

   - **SQL Server:**
     - Databases: Check for `Microsoft.Sql/servers/databases`
     - Elastic Pools: Check for `Microsoft.Sql/servers/elasticPools`
     - Firewall Rules: Check for `Microsoft.Sql/servers/firewallRules`

### 3) **For Each Resource in Inventory**
   - Display: "🔍 Analyzing: [Resource Name]"
   - Initialize feature detection results:
     ```
     {
       ResourceId: "...",
       ResourceName: "...",
       FeaturesDetected: [],
       DetectionMethod: "Resource-based",
       LimitationsNote: "Usage metrics not checked - for complete detection use azure-metrics-collect"
     }
     ```

### 4) **Detect Features via Child Resources**
   - For each feature/channel to detect:
     - Build query for related child resources:
       ```bash
       az resource list \
         --resource-group <resource-group> \
         --resource-type <child-resource-type> \
         --output json
       ```
     - Filter for resources related to parent resource

   - **If child resources found:**
     - Mark feature as DETECTED
     - Count child resources
     - Display: "✅ [Feature Name] detected ([N] resource(s))"
     - Add to FeaturesDetected array

   - **If no child resources found:**
     - Mark feature as NOT DETECTED
     - Display: "⚪ [Feature Name] not detected"

### 5) **Detect Features via Resource Properties**
   - Alternative detection method: Check resource properties
   - Query resource details:
     ```bash
     az resource show --ids <resource-id> --output json
     ```
   - Check for specific property values indicating feature enablement
   - Example: `properties.enabledFeatures`, `properties.capabilities`

### 6) **Display Detection Limitations**
   - Show important disclaimer:
     ```
     ⚠️ Detection Limitations (Fast Mode):
     - Only features exposed as child resources are detected
     - Features detected via usage metrics may be MISSED
     - This method cannot detect UNUSED features
     - Recommendation: Use azure-metrics-collect for complete analysis
     ```
   - List which features CAN be detected (resource-based)
   - List which features CANNOT be detected (require metrics)

### 7) **Aggregate Results by Resource**
   - For each resource, create summary:
     ```
     Resource: ACSProd
       ✅ Email Service (2 domains)
       ✅ Phone Numbers (3 numbers)
       ⚠️ SMS: Requires metrics (use azure-metrics-collect)
       ⚠️ Chat: Requires metrics (use azure-metrics-collect)
       ⚠️ Calling: Requires metrics (use azure-metrics-collect)
     ```

### 8) **Save Detection Results**
   - Update resource inventory with detection results:
     - Add `FeaturesDetected` array to each resource
     - Add `DetectionMethod` field
     - Add `RequiresMetricsForComplete` flag
   - Store updated inventory in session state

### 9) **Provide Recommendations**
   - Display next steps:
     ```
     💡 Recommendations:
     - ✅ [N] features detected via resources
     - ⚠️ [M] features require metrics analysis
     - To get complete detection, run: 5-azure-metrics-collect
     ```

## Output
- Features detected per resource (resource-based only)
- Count of detectable vs. metrics-required features
- Detection limitations clearly stated
- Updated resource inventory with detection results

## Detection Speed
- **Fast:** ~30 seconds per subscription
- **Trade-off:** Limited detection coverage (only resource-based features)

## When to Use Metrics Instead
Use **5-azure-metrics-collect** if you need:
- Detection of features based on actual usage (not just configuration)
- SMS, Chat, Calling detection for ACS
- Usage-based features for any Azure product
- Complete feature detection (no gaps)

## Related Skills
- Use **1-azure-auth-check**, **2-azure-subscription-select**, **3-azure-resource-scan** before this skill
- Use **5-azure-metrics-collect** after this skill for complete detection
- Use **6-azure-impact-analyze** after detection to assess severity

## Example Invocation
```
User: "Do a quick check for ACS features without metrics"
Agent: [Runs 4-azure-channel-detect skill]
Output:
  🔍 Analyzing: ACSProd
  ✅ Email Service detected (2 domains)
  ✅ Phone Numbers detected (1 number)
  ⚠️ SMS, Chat, Calling require metrics for detection

  💡 For complete detection, run: 5-azure-metrics-collect
```

