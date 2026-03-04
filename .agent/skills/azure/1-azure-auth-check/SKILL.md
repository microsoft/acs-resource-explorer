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
- Azure CLI installed (`az` command available)
- Installation: https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest (Windows, macOS, Linux)

## Workflow

### 1) **Check Azure CLI Installation**
   - Verify `az` is available:
     ```bash
     az version
     ```
   - If not installed, provide installation instructions:
     ```
     Install Azure CLI: https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
     ```
   - Exit with clear error if CLI unavailable

### 2) **Check Existing Azure Context**
   - Run `az account show` to check for an existing authenticated session
   - If context exists:
     - Extract tenant ID, account ID, and current subscription
     - Display connection status: ✅ "Already authenticated"
   - If no context exists (error or "Please run 'az login'"):
     - Display: ⚠️ "Not authenticated to Azure"

### 3) **Authenticate if Needed**
   - If no existing context:
     - Prompt user: "Would you like to connect now? (Y/N)"
     - If Yes: Run `az login`
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
   - If the user needs to connect to a different tenant, inform them:
     ```
     Note: To connect to a different tenant, use:
     az login --tenant 'your-tenant-id'
     ```

### 6) **Save Context for Subsequent Skills**
   - Store authentication context in session state:
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
Agent: [Runs 1-azure-auth-check skill]
Output:
  ✅ Connected to Azure
  Account: john.doe@contoso.com
  Tenant ID: abc123...
  Current Subscription: Production (sub-123...)
```
