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

1. **Navigate to the script folder:**
   ```powershell
   cd [path-to-ACS-Transition-Agent-v0]\scripts\powershell
   ```

2. **Run the script:**
   ```powershell
   .\acs-impact-assessment-tool.ps1 -IncludeMetrics -LookbackDays 90
   ```

3. **Follow the prompts:**
   - Login to Azure when prompted
   - Select subscription option:
     - `1` = Scan only default subscription (recommended)
     - `2` = Scan all accessible subscriptions

4. **Wait for completion:** 3-5 minutes per subscription

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

- [ ] **Location:** `.\exports\ACS_Impact_Assessment.csv`
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

- Check troubleshooting section in [PowerShell README](powershell/README.md)
- Contact: [Your support contact]
