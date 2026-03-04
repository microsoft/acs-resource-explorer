---
name: 1-acs-resource-scan
description: Scan Azure subscriptions for Azure Communication Services (ACS) resources (Microsoft.Communication/CommunicationServices). ACS-specific version of azure/3-azure-resource-scan with resource type pre-filled.
---

## When to use this skill
Use this skill to discover all ACS Communication Services resources across selected subscription(s).

Examples:
  - "Find all my ACS resources"
  - "Scan for Azure Communication Services"
  - "Discover ACS Communication Services across my subscriptions"
  - "How many ACS resources do I have?"

## Preconditions
- Azure authentication completed (use **azure/1-azure-auth-check** skill)
- Subscription(s) selected (use **azure/2-azure-subscription-select** skill)
- User has **Reader** access to target subscription(s)

## ACS Resource Type
This skill scans for: `Microsoft.Communication/CommunicationServices`

No interactive product selection is needed — this is pre-configured for ACS.

## Workflow

### 1) **Scan Each Selected Subscription**
   - For each subscription in selection (from **azure/2-azure-subscription-select**):
     - Set Azure subscription context:
       ```bash
       az account set --subscription <subscription-id>
       ```
     - Display: "📋 Scanning subscription: [Subscription Name]"

### 2) **Query ACS Resources**
   ```bash
   az resource list \
     --resource-type "Microsoft.Communication/CommunicationServices" \
     --output json
   ```

### 3) **Optional: Filter Resources**
   - Ask user: "Do you want to filter by resource name, location, or tags? (Y/N)"
   - If YES:
     - Prompt for filter criteria (name pattern, location, tags)
     - Apply using `--query` JMESPath filters or `--tag` flags

### 4) **Process Results**
   - **If NO resources found:**
     - Display: "ℹ️ No ACS resources found in [Subscription Name]"
     - Continue to next subscription

   - **If resources found:**
     - Display: "✅ Found [N] ACS resource(s) in [Subscription Name]"
     - For each resource, collect:
       - Resource Name, Resource ID, Resource Group
       - Location, Tags, Connection String endpoint

### 5) **Build ACS Resource Inventory**
   - Create structured inventory:
     ```
     {
       SubscriptionId: "...",
       SubscriptionName: "...",
       ResourceType: "Microsoft.Communication/CommunicationServices",
       ResourceName: "...",
       ResourceId: "...",
       ResourceGroup: "...",
       Location: "...",
       Tags: {...},
       Endpoint: "https://[resource].communication.azure.com"
     }
     ```

### 6) **Display Summary**
   ```
   === ACS Resource Scan Summary ===
   Resource Type: Microsoft.Communication/CommunicationServices
   Subscriptions Scanned: [N]
   Total ACS Resources Found: [M]

   By Subscription:
     - [Sub Name]: [N] ACS resource(s)
       • [Resource Name] ([Resource Group], [Location])
   ```

### 7) **Save Inventory to Session State**
   - Store ACS resource inventory for use by downstream skills:
     - `2-acs-channel-detect`
     - `3-acs-metrics-collect`
     - `4-acs-impact-analyze`
     - `5-acs-report-generate`

### 8) **Provide Next Steps**
   - If resources found:
     - Suggest: "Use **2-acs-channel-detect** for fast detection or **3-acs-metrics-collect** for complete usage analysis"
   - If no resources found:
     - Display: "✅ No ACS resources found. No migration action required."

## Output
- Total ACS resource count across all subscriptions
- Resource inventory (name, ID, subscription, resource group, location)
- Session state saved for downstream ACS skills

## Error Handling
- Permission errors: Log warning, continue to next subscription
- Subscription access errors: Display error, skip subscription

## Related Skills
- Requires **azure/1-azure-auth-check** and **azure/2-azure-subscription-select**
- Use **2-acs-channel-detect** after this (fast detection)
- Use **3-acs-metrics-collect** after this (complete detection)

