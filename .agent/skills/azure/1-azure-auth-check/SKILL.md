---
name: 1-azure-auth-check
description: Verify Azure authentication status and display connection information (tenant, account, subscription context). Works with any Azure product or service.
---

## When to use this skill
Use this skill when you need to verify Azure authentication before performing Azure operations, or when troubleshooting authentication issues.

Examples:
  - "Check if I'm authenticated to Azure"
  - "Show my current Azure connection info"
  - "Verify my Azure tenant and subscription context"
  - "Am I connected to the right Azure account?"

## Preconditions
- PowerShell Az module installed (`Install-Module -Name Az`)
- User has Azure credentials (will prompt for authentication if needed)

> Note: On macOS/Linux use `pwsh` (PowerShell 7). On Windows you can use `pwsh` or Windows PowerShell.

## Workflow

### 1) **Check Az Module Installation**
   - Verify `Az.Accounts` module is available
   - If not installed, provide installation instructions:
     ```powershell
     Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
     ```
   - Exit with clear error if module unavailable

### 2) **Check Existing Azure Context**
   - Run `Get-AzContext` to check for existing authenticated session
   - If context exists:
     - Extract tenant ID, account ID, and current subscription
     - Display connection status: ✅ "Already authenticated"
   - If no context exists:
     - Display: ⚠️ "Not authenticated to Azure"

### 3) **Authenticate if Needed**
   - If no existing context:
     - Prompt user: "Would you like to connect now? (Y/N)"
     - If Yes: Run `Connect-AzAccount`
     - If No: Exit with message "Authentication required to continue"
   - Handle authentication errors gracefully

### 4) **Display Connection Information**
   - Show authenticated user details:
     ```
     ✅ Connected to Azure

     Account:   user@domain.com
     Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     Current Subscription: Subscription Name (sub-id)
     ```

### 5) **Provide Multi-Tenant Guidance (if applicable)**
   - If user has access to multiple tenants, inform them:
     ```
     Note: To connect to a different tenant, use:
     Connect-AzAccount -TenantId 'your-tenant-id'
     ```

### 6) **Save Context for Subsequent Skills**
   - Store authentication context in session variable or state file:
     - Tenant ID
     - Account ID
     - Current subscription (if any)
   - This allows downstream skills to skip re-authentication

## Output
- Authentication status (authenticated/not authenticated)
- Tenant information
- Account details
- Current subscription context
- Session state saved for use by subsequent skills

## Related Skills
- Use **2-azure-subscription-select** after this skill to choose subscriptions to scan
- Required before any Azure resource scanning or metrics collection skills

## Example Invocation
```
User: "Check my Azure authentication"
Agent: [Runs 1-1-azure-auth-check skill]
Output:
  ✅ Connected to Azure
  Account: john.doe@contoso.com
  Tenant ID: abc123...
  Current Subscription: Production (sub-123...)
```

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 60-96 for example implementation of this workflow.
