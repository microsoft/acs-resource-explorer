---
name: 3-azure-resource-scan
description: Scan Azure subscriptions for specific resource types. Interactive prompts allow scanning any Azure product (ACS, Storage, Compute, Databases, etc). Returns resource inventory across selected subscriptions.
---

## When to use this skill
Use this skill to discover Azure resources of a specific type across selected subscription(s).

Examples:
  - "Scan for Azure Communication Services resources"
  - "Find all Storage Accounts in my subscription"
  - "List all SQL databases across my subscriptions"
  - "Discover resources of type X"

## Preconditions
- Azure authentication completed (use **1-azure-auth-check** skill)
- Subscription(s) selected (use **2-azure-subscription-select** skill)
- User has **Reader** access to target subscription(s)

## Workflow

### 1) **Determine Resource Type to Scan**

   **Interactive Mode:**
   - Ask user: "Which Azure product or service do you want to scan?"
   - Present common options:
     ```
     Common Azure Products:
     1. Azure Communication Services (Microsoft.Communication/CommunicationServices)
     2. Storage Accounts (Microsoft.Storage/storageAccounts)
     3. SQL Databases (Microsoft.Sql/servers/databases)
     4. Virtual Machines (Microsoft.Compute/virtualMachines)
     5. App Services (Microsoft.Web/sites)
     6. Enter custom resource type
     ```
   - If option 6: Prompt for full resource type string
   - Validate resource type format: `Microsoft.Provider/ResourceType`

   **Non-Interactive Mode:**
   - Accept resource type as parameter: `-ResourceType "Microsoft.Communication/CommunicationServices"`

### 2) **Optional: Resource Filtering**
   - Ask user: "Do you want to filter by resource name, location, or tags? (Y/N)"
   - If YES:
     - Prompt for filter criteria:
       - Name pattern (wildcards supported)
       - Location (e.g., "eastus", "westeurope")
       - Tags (key=value pairs)
   - Store filter criteria for use in query

### 3) **Scan Each Selected Subscription**
   - For each subscription in selection (from **2-azure-subscription-select**):
     - Set Azure context: `Set-AzContext -SubscriptionId $subId`
     - Display: "📋 Scanning subscription: [Subscription Name]"

### 4) **Query Resources**
   - Build query:
     ```powershell
     Get-AzResource -ResourceType $resourceType -ErrorAction SilentlyContinue
     ```
   - Apply filters if specified:
     - Name filter: `-Name $namePattern`
     - Location filter: Where-Object filtering
     - Tag filter: Where-Object filtering

### 5) **Process Query Results**
   - **If NO resources found:**
     - Display: "ℹ️ No resources found in [Subscription Name]"
     - Continue to next subscription

   - **If resources found:**
     - Display: "✅ Found [N] resource(s) in [Subscription Name]"
     - For each resource, collect:
       - Resource Name
       - Resource ID
       - Resource Group
       - Location
       - Tags (if any)
       - Creation date (if available)

### 6) **Build Resource Inventory**
   - Create structured inventory for each resource:
     ```
     {
       SubscriptionId: "...",
       SubscriptionName: "...",
       ResourceType: "...",
       ResourceName: "...",
       ResourceId: "...",
       ResourceGroup: "...",
       Location: "...",
       Tags: {...},
       CreatedDate: "..."
     }
     ```
   - Add to inventory collection

### 7) **Display Summary**
   - Show scan results:
     ```
     === Resource Scan Summary ===
     Resource Type: Microsoft.Communication/CommunicationServices
     Subscriptions Scanned: 3
     Total Resources Found: 12

     By Subscription:
       - Production: 5 resources
       - Staging: 4 resources
       - Development: 3 resources
     ```

### 8) **Save Inventory for Subsequent Skills**
   - Store resource inventory in session state:
     - Resource collection (array of resource objects)
     - Resource count by subscription
     - Resource type scanned
   - This allows downstream skills to analyze these specific resources

### 9) **Provide Next Steps**
   - If resources found:
     - Suggest: "Use **4-azure-channel-detect** or **5-azure-metrics-collect** to analyze these resources"
   - If no resources found:
     - Display: "✅ No [Product] resources found. No further analysis needed."

## Output
- Resource count per subscription
- Total resource count
- Detailed resource inventory (saved to session state)
- Resource type scanned
- Filter criteria used (if any)

## Interactive Prompts
1. "Which Azure product or service do you want to scan?"
2. "Do you want to filter by name, location, or tags?"
3. (If filtering) "Enter filter criteria:"

## Error Handling
- Permission errors: Log warning, continue to next subscription
- Invalid resource type: Prompt user to re-enter
- Subscription access errors: Display error, skip subscription

## Related Skills
- Use **1-azure-auth-check** before this skill
- Use **2-azure-subscription-select** before this skill
- Use **4-azure-channel-detect** after this skill (for feature detection)
- Use **5-azure-metrics-collect** after this skill (for usage metrics)

## Example Invocation
```
User: "Scan for Azure Communication Services resources"
Agent: [Runs 3-azure-resource-scan skill]
Output:
  📋 Scanning subscription: Production
  ✅ Found 2 resource(s)

  📋 Scanning subscription: Development
  ℹ️ No resources found

  === Resource Scan Summary ===
  Resource Type: Microsoft.Communication/CommunicationServices
  Total Resources Found: 2
  - Production: 2 resources (ACSProd, ACSDevAndTest)
```

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 180-196 for example implementation of this workflow.
