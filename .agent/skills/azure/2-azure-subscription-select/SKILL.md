---
name: 2-azure-subscription-select
description: Interactive subscription selection workflow. Choose specific subscription(s) or scan all accessible subscriptions. Works with any Azure product or service.
---

## When to use this skill
Use this skill after authentication to select which Azure subscription(s) to scan for resources.

Examples:
  - "Select subscriptions to scan"
  - "Choose which subscription to analyze"
  - "I want to scan all my subscriptions"
  - "Let me pick a specific subscription"

## Preconditions
- Azure authentication completed (use **1-azure-auth-check** skill first)
- User has read access to at least one Azure subscription

## Workflow

### 1) **Check for Specific Subscription Request**
   - Ask user: "Do you have a specific subscription ID to scan?"
   - If YES:
     - Prompt for subscription ID
     - Validate subscription exists and is accessible
     - If invalid: Show list of available subscriptions
     - If valid: Use that subscription only
   - If NO: Continue to step 2

### 2) **Detect Default Subscription**
   - Get current Azure context: `(Get-AzContext).Subscription`
   - If default subscription exists:
     - Display default subscription name and ID
     - Show count of all accessible subscriptions
   - If no default: Continue to step 3

### 3) **Present Selection Options**
   - Display interactive menu:
     ```
     Options:
     1. Scan only the default subscription: [Name] (recommended)
     2. Scan all accessible subscriptions ([N] subscriptions)
     3. Enter a specific subscription ID
     ```
   - Prompt user for choice (default: Option 1)

### 4) **Process User Selection**
   - **Option 1 (Default subscription):**
     - Use default subscription from context
     - Display: ✅ "Scanning: [Subscription Name]"

   - **Option 2 (All subscriptions):**
     - Get all accessible subscriptions: `Get-AzSubscription`
     - Display count
     - Confirm: "This will scan [N] subscriptions. Continue? (Y/N)"
     - If confirmed: Use all subscriptions

   - **Option 3 (Specific ID):**
     - Prompt for subscription ID
     - Validate with `Get-AzSubscription -SubscriptionId $id`
     - If valid: Use that subscription
     - If invalid: Return to step 3

### 5) **Display Subscription List**
   - If ≤5 subscriptions selected:
     - Show full list with names and IDs
   - If >5 subscriptions selected:
     - Show first 5 subscriptions
     - Display: "... and [N] more subscriptions"

### 6) **Save Selection for Subsequent Skills**
   - Store selected subscription(s) in session state:
     - Subscription IDs (array)
     - Subscription names (array)
     - Selection mode (single/multiple)
   - This allows downstream skills to iterate over selections

## Output
- Count of subscriptions selected
- List of subscription names and IDs (displayed and saved)
- Session state updated with selection

## Interactive Behavior
- **Non-interactive mode:** If `-SubscriptionId` parameter provided, skip prompts
- **Interactive mode:** Guide user through selection process with clear options
- **Validation:** Always verify subscription access before proceeding

## Related Skills
- Use **1-azure-auth-check** before this skill
- Use **3-azure-resource-scan** after this skill to scan selected subscriptions

## Example Invocation
```
User: "Let me select which subscriptions to scan"
Agent: [Runs 2-2-azure-subscription-select skill]
Output:
  Default subscription detected: Production (abc-123...)
  Options:
    1. Scan only default subscription (recommended)
    2. Scan all accessible subscriptions (5 subscriptions)

  User selects: 1

  ✅ Selected: Production (abc-123...)
```

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 98-165 for example implementation of this workflow.
