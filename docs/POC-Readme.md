# QA Testing Guide - ACS Impact Assessment Tool

## Prerequisites

- Azure account with Reader access to subscriptions
- Azure PowerShell module: `Install-Module -Name Az`

## One-Time Setup

Run this command **once** in PowerShell (as Administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## How to Test

1. **Save the script file** (`acs-impact-assessment-tool.ps1`) to a location of your choice (e.g., Documents folder)

2. **Open PowerShell** and navigate to where you saved the script:
   ```powershell
   cd "C:\Users\[YourName]\Documents"
   ```
   (Replace with your actual folder path)

3. **Run the script:**
   ```powershell
   .\acs-impact-assessment-tool.ps1 -IncludeMetrics -LookbackDays 90
   ```

4. **Follow the prompts:**
   - Login to Azure when prompted
   - Select subscription option:
     - `1` = Scan only default subscription (recommended)
     - `2` = Scan all accessible subscriptions

5. **Wait for completion:** 3-5 minutes per subscription

## What to Verify

### Console Output ✓

- [ ] Shows **"Detection Mode: FULL (with metrics)"**
- [ ] Shows **"Lookback period: Last 90 days"**
- [ ] Displays your tenant ID and account
- [ ] Lists ACS resources found (or "No ACS resources found")
- [ ] Shows per-resource channel breakdown with usage counts:
  ```
  Channel Usage Summary (last 90 days):
    Email:         0 messages (zero usage in last 90 days)
    SMS:           0 messages (zero usage in last 90 days)
    Chat:          0 messages (zero usage in last 90 days)
    Calling:       0 calls (zero usage in last 90 days)
    Phone Numbers: 0 operations (zero usage in last 90 days)
  ```
- [ ] Summary shows:
  - Total ACS resources found: X
  - Resources using retiring services: X
- [ ] Shows CSV export path

### CSV File ✓

- [ ] **Location:** `.\exports\ACS_Impact_Assessment.csv` (in the same folder where you ran the script)
- [ ] Opens in Excel without errors
- [ ] Contains these columns:
  - `SubscriptionName`
  - `ResourceName`
  - `LookbackPeriodDays` (should show "90")
  - `EmailUsageCount`
  - `SMSUsageCount`
  - `ChatUsageCount`
  - `CallingUsageCount`
  - `PhoneNumbersUsageCount`
  - `HighestSeverity`
  - `MigrationEffortEstimate`
- [ ] All ACS resources are included (even with 0 usage)

## Common Issues

| Issue | Solution |
|-------|----------|
| **"Unable to acquire token"** or **"Authentication failed"** with MFA warning | Your organization requires multi-factor authentication. Run: `Connect-AzAccount -TenantId "your-tenant-id"` (use the Tenant ID from the error message) and complete MFA prompts, then run the script again |
| **"User interaction is required"** | Complete interactive authentication with your tenant: `Connect-AzAccount -TenantId "your-tenant-id"`, then run the script again |
| "Script cannot be loaded" | Run the setup command above |
| "Az module not installed" | Run: `Install-Module -Name Az` |
| "No ACS resources found" | This is normal if no ACS resources exist in your subscription |
| Slow performance | Expected - metrics retrieval takes 3-5 minutes per subscription |

## Test Report Template

Copy and fill out:

```
Test Date: [Date]
Tester: [Your Name]
Subscription: [Subscription Name]

Console Output: ✅ PASS / ❌ FAIL
CSV Generated: ✅ PASS / ❌ FAIL
CSV Opens in Excel: ✅ PASS / ❌ FAIL
LookbackPeriodDays = 90: ✅ PASS / ❌ FAIL
Zero usage explicitly shown: ✅ PASS / ❌ FAIL

Issues Found:
[Describe any issues or write "None"]

CSV Location:
[Full path to generated CSV file]

Screenshots:
[Attach console output and CSV file if issues found]
```

## Expected Results

### If ACS Resources Exist:
- Console shows resource analysis with channel breakdown
- CSV contains all resources with usage data
- Zero values clearly marked as "(zero usage in last 90 days)"

### If No ACS Resources:
- Console shows: "No ACS resources found in the scanned subscription(s)"
- No CSV file generated

## Need Help?

- Review the Common Issues section above
- If Azure PowerShell module is missing: Run `Install-Module -Name Az`
- For execution policy errors: Run the One-Time Setup command
- Contact your test coordinator with questions
