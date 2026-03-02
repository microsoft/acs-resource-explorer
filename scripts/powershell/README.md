# ACS Impact Assessment Tool - PowerShell Script

## Overview

The **ACS Impact Assessment Tool** is a PowerShell script that automatically scans your Azure subscriptions to identify resources using retiring Azure Communication Services (ACS) channels. It helps you quickly assess the impact of ACS service retirements across your entire Azure environment.

---

## Key Features

✅ **Multi-Subscription Scanning** - Scan all accessible subscriptions or target specific ones
✅ **All Channel Detection** - Detects Email, SMS, Chat, Calling, and Phone Numbers usage
✅ **Usage Metrics** - Optionally retrieves 90-day usage data from Azure Monitor
✅ **Severity Calculation** - Automatic Critical/Warning/Info classification
✅ **Migration Effort Estimation** - Calculates Low/Medium/High effort based on impacted channels
✅ **CSV Export** - Generates detailed CSV report for planning and tracking
✅ **Color-Coded Console Output** - Easy-to-read results with visual indicators

---

## Quick Reference - How to Run

**Navigate to the script directory first:**
```powershell
cd C:\Users\YourName\ACS-Transition-Agent-v0\scripts\powershell
```

**Then choose your scan type:**

```powershell
# Quick scan (FAST mode - only detects Email + Phone Numbers)
.\acs-impact-assessment-tool.ps1

# Recommended: Full scan with metrics (detects ALL channels)
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# Scan a specific subscription only (no prompt)
.\acs-impact-assessment-tool.ps1 -SubscriptionId "your-subscription-id" -IncludeMetrics

# Custom output location
.\acs-impact-assessment-tool.ps1 -OutputPath "C:\Reports\ACS_Scan.csv" -IncludeMetrics

# Full detailed scan with everything
.\acs-impact-assessment-tool.ps1 -SubscriptionId "your-sub-id" -IncludeMetrics -OutputPath "C:\Reports\Detailed_Scan.csv"
```

**Important - Detection Modes:**

| Flag | Channels Detected | Speed | Use Case |
|------|------------------|-------|----------|
| **No flags** (FAST) | Email, Phone Numbers only | ~30 seconds | Quick check for Email domains |
| **`-IncludeMetrics`** (FULL) | All 5 channels (Email, SMS, Chat, Calling, Phone Numbers) | ~3-5 minutes | Complete assessment (recommended) |

⚠️ **Without `-IncludeMetrics`, SMS, Chat, and Calling are NOT detected.** Always use `-IncludeMetrics` for accurate results.

**Subscription Selection:**
- Without `-SubscriptionId`: Prompts to scan default subscription or all subscriptions
- With `-SubscriptionId`: Scans specified subscription only (no prompt)

See [Usage](#usage) section below for detailed explanations and scenarios.

---

## Prerequisites

### 1. PowerShell 5.1 or Later
Check your version:
```powershell
$PSVersionTable.PSVersion
```

### 2. Azure PowerShell Module (Az)
Install if not already installed:
```powershell
Install-Module -Name Az -Repository PSGallery -Force -AllowClobber
```

Update to latest version:
```powershell
Update-Module -Name Az
```

### 3. Azure Permissions
Your Azure account needs at least **Reader** role on the subscriptions you want to scan.

---

## Installation

1. Download the script:
   ```powershell
   # Clone the repository or download directly
   cd C:\Your\Preferred\Directory
   ```

2. Verify the script is present:
   ```powershell
   Test-Path .\acs-impact-assessment-tool.ps1
   ```

3. (Optional) Unblock the script if downloaded from the internet:
   ```powershell
   Unblock-File -Path .\acs-impact-assessment-tool.ps1
   ```

---

## Usage

### Quick Start

The simplest way to run the script:

```powershell
.\acs-impact-assessment-tool.ps1
```

**Behavior:**
- Connects to Azure (login prompt if needed)
- Shows your default subscription (the one you selected during login)
- **Prompts you to choose:**
  - Option 1: Scan only the default subscription (recommended)
  - Option 2: Scan all accessible subscriptions

**Output:** Console summary + `exports/ACS_Impact_Assessment.csv` (folder created automatically)

⚠️ **IMPORTANT:** This basic scan only detects **Email** and **Phone Numbers**. For complete detection of all channels, use `-IncludeMetrics` flag.

---

### Understanding Channel Detection

The script has two detection modes:

#### FAST Mode (Default - No `-IncludeMetrics`)
**Detects via Resource Checking:**
- ✅ **Email Service** - Checks for email domain resources
- ✅ **Phone Numbers** - Checks for purchased phone numbers
- ❌ **SMS** - Cannot detect (no separate resources)
- ❌ **Chat** - Cannot detect (no separate resources)
- ❌ **Calling** - Cannot detect (no separate resources)

**Speed:** ~30 seconds per subscription
**Use Case:** Quick Email domain check only

#### FULL Mode (With `-IncludeMetrics`)
**Detects via Azure Monitor Usage Metrics:**
- ✅ **Email Service** - Checks message sending metrics
- ✅ **SMS** - Checks SMS send/receive metrics
- ✅ **Chat** - Checks message and thread metrics
- ✅ **Calling** - Checks call duration and count metrics
- ✅ **Phone Numbers** - Checks phone number operations

**Speed:** ~3-5 minutes per subscription
**Use Case:** Complete assessment with usage counts (recommended)

**Why Metrics Are Needed:**
SMS, Chat, and Calling are capabilities enabled on the main ACS resource, not separate resources. The only way to detect if you're using them is by checking usage metrics from Azure Monitor.

**Recommendation:** Always use `-IncludeMetrics` unless you only care about Email domains.

---

### Common Usage Scenarios

Choose the command that best fits your needs:

| Scenario | Command | Detects | When to Use |
|----------|---------|---------|-------------|
| **Email domains only** | `.\acs-impact-assessment-tool.ps1` | Email, Phone Numbers | Quick check (NOT recommended - incomplete) |
| **Complete assessment** ⭐ | `.\acs-impact-assessment-tool.ps1 -IncludeMetrics` | All 5 channels + usage counts | Recommended for accurate results |
| **Single subscription** | `.\acs-impact-assessment-tool.ps1 -SubscriptionId "xxx" -IncludeMetrics` | All 5 channels | Focus on one specific subscription |
| **Custom output location** | `.\acs-impact-assessment-tool.ps1 -IncludeMetrics -OutputPath "C:\Reports\scan.csv"` | All 5 channels | Save results to a specific location |
| **Full detailed analysis** | `.\acs-impact-assessment-tool.ps1 -SubscriptionId "xxx" -IncludeMetrics -OutputPath "C:\Reports\detailed.csv"` | All 5 channels with full details | Complete scan with all options |

---

### Advanced Usage Examples

#### 1. Scan Specific Subscription

```powershell
.\acs-impact-assessment-tool.ps1 -SubscriptionId "12345678-1234-1234-1234-123456789abc"
```

#### 2. Include Usage Metrics (Detailed Analysis)

```powershell
.\acs-impact-assessment-tool.ps1 -IncludeMetrics
```

⚠️ **Note:** This retrieves 90 days of Azure Monitor metrics. It's slower but provides accurate usage counts per channel.

#### 3. Custom Output Path

```powershell
.\acs-impact-assessment-tool.ps1 -OutputPath "C:\Reports\ACS_Assessment_2026-01-28.csv"
```

#### 4. Full Detailed Scan (Specific Sub + Metrics + Custom Path)

```powershell
.\acs-impact-assessment-tool.ps1 `
    -SubscriptionId "12345678-1234-1234-1234-123456789abc" `
    -IncludeMetrics `
    -OutputPath "C:\ACS\Reports\DetailedAssessment.csv"
```

---

## Understanding the Output

### Console Output

The script provides color-coded output:
- 🟢 **Green** - Successful operations, connection status
- 🟡 **Yellow** - Detection of retiring services, warnings
- 🔴 **Red** - Critical severity items
- ⚪ **Gray** - Informational messages

### CSV Report Columns

| Column | Description |
|--------|-------------|
| `SubscriptionName` | Name of the Azure subscription |
| `SubscriptionId` | Subscription GUID |
| `ResourceGroup` | Resource group containing the ACS resource |
| `ResourceName` | Name of the ACS resource |
| `Location` | Azure region |
| `EmailDetected` | True/False - Email service usage detected |
| `EmailUsageCount` | Number of emails sent (if `-IncludeMetrics` used) |
| `SMSDetected` | True/False - SMS API usage detected |
| `SMSUsageCount` | Number of SMS messages (if `-IncludeMetrics` used) |
| `ChatDetected` | True/False - Chat SDK usage detected |
| `ChatUsageCount` | Number of chat messages (if `-IncludeMetrics` used) |
| `CallingDetected` | True/False - Calling SDK usage detected |
| `CallingUsageCount` | Number of calls (if `-IncludeMetrics` used) |
| `PhoneNumbersDetected` | True/False - Phone Numbers SDK usage detected |
| `PhoneNumbersUsageCount` | Usage count (if `-IncludeMetrics` used) |
| `TotalChannelsImpacted` | Count of retiring channels used by this resource |
| `HighestSeverity` | Critical/Warning/Info |
| `MigrationEffortEstimate` | Low/Medium/High |

---

## Severity Classification

The script automatically calculates severity based on usage patterns:

### Critical
- Email usage > 1,000 messages in 90 days
- Calling usage > 500 calls in 90 days
- Multiple high-usage channels

### Warning
- Email usage > 100 messages in 90 days
- SMS usage > 50 messages in 90 days
- Moderate usage detected

### Info
- Low usage detected
- Resource exists but minimal activity

---

## Migration Effort Estimation

Based on the number of impacted channels:

- **Low** - 1 channel impacted (e.g., only Phone Numbers SDK)
- **Medium** - 2 channels impacted (e.g., Email + SMS)
- **High** - 3+ channels impacted (complex multi-channel migration)

---

## Example Output

### Console Summary Example

```
=== Azure Communication Services Impact Assessment Tool ===
Connecting to Azure...
Successfully connected to Azure

Connected to:
  Account:   user@example.com
  Tenant ID: 12345678-abcd-1234-abcd-123456789abc

Note: If you need to connect to a different tenant, please rerun:
  Connect-AzAccount -TenantId '12345678-abcd-1234-abcd-123456789abc'

Default subscription detected: Production (12345678-1234-1234-1234-123456789abc)
Options:
  1. Scan only the default subscription (recommended)
  2. Scan all accessible subscriptions (132 subscriptions)

Enter your choice (1 or 2, default is 1): 1

Scanning only default subscription: Production

Scanning 1 subscription(s)...
Subscriptions to scan:
  - Production (12345678-1234-1234-1234-123456789abc)

Scanning subscription: Production (12345678-1234-1234-1234-123456789abc)
  Found 2 ACS resource(s)
    Analyzing: acs-prod-eastus
      ✓ Email service detected (2 domain(s))
      ✓ SMS usage: 1500 messages
    Analyzing: acs-prod-westus
      ✓ Calling usage: 350 calls

=== Impact Assessment Summary ===
Total ACS resources scanned: 2

Retiring Services Detected:
  - Email Service: 1 resource(s)
  - SMS API: 1 resource(s)
  - Calling SDK: 1 resource(s)

Severity Breakdown:
  - Critical: 1 resource(s)
  - Warning: 1 resource(s)

Exporting results to: .\exports\ACS_Impact_Assessment.csv
  Created output directory: .\exports
Export complete!

=== Assessment Complete ===
```

---

## Troubleshooting

### Issue: "Az module is not installed"

**Solution:**
```powershell
Install-Module -Name Az -Repository PSGallery -Force
```

### Issue: "Connect-AzAccount failed"

**Possible causes:**
1. Not logged into Azure
2. Expired authentication token
3. Network connectivity issues

**Solution:**
```powershell
# Clear cached credentials and reconnect
Disconnect-AzAccount
Connect-AzAccount
```

### Issue: Need to scan resources in a different tenant

**Scenario:** You have access to multiple Azure tenants and need to scan resources in a specific tenant.

**Solution:**

The script displays your current tenant ID after connecting. To connect to a different tenant:

```powershell
# Option 1: Reconnect with specific tenant ID
Disconnect-AzAccount
Connect-AzAccount -TenantId "your-tenant-id-here"

# Then run the script
.\acs-impact-assessment-tool.ps1

# Option 2: Check available tenants first
Get-AzTenant

# Then connect to the desired tenant
Connect-AzAccount -TenantId "your-target-tenant-id"
```

**Tip:** The script shows your current tenant ID in the connection output, making it easy to verify you're connected to the correct tenant before scanning.

### Issue: "No ACS resources found" (but you know they exist)

**Possible causes:**
1. Insufficient permissions (need Reader role minimum)
2. Wrong subscription selected
3. Resources in different subscription

**Solution:**
```powershell
# List all subscriptions you have access to
Get-AzSubscription | Format-Table Name, Id, State

# Verify your current context
Get-AzContext
```

### Issue: Metrics retrieval is very slow

**Explanation:** The `-IncludeMetrics` flag retrieves 90 days of data from Azure Monitor for each metric (15+ metrics per resource). This is network-intensive.

**Solution:**
- Run without `-IncludeMetrics` for quick resource discovery
- Use `-IncludeMetrics` only when you need accurate usage counts
- Run during off-peak hours for large environments

### Issue: Script execution is blocked

**Error:** One of the following errors may appear:
- "cannot be loaded because running scripts is disabled on this system"
- "File C:\...\acs-impact-assessment-tool.ps1 cannot be loaded. The file is not digitally signed. You cannot run this script on the current system."

**Explanation:** By default, Windows restricts running unsigned PowerShell scripts for security. This is a common issue when running scripts downloaded from the internet or not digitally signed.

**Solution Option 1 (Recommended - Permanent Fix):**
```powershell
# Check current execution policy
Get-ExecutionPolicy

# Set execution policy to allow scripts (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Solution Option 2 (Bypass - One-Time Run):**
```powershell
# Run the script with execution policy bypass (doesn't change system settings)
powershell -ExecutionPolicy Bypass -File .\acs-impact-assessment-tool.ps1

# Or with parameters
powershell -ExecutionPolicy Bypass -File .\acs-impact-assessment-tool.ps1 -IncludeMetrics
```

### Issue: Azure PowerShell Module Compatibility Error

**Error:** "Method 'get_SerializationSettings' in type 'Microsoft.Azure.Management.Internal.Resources.ResourceManagementClient' from assembly 'Microsoft.Azure.PowerShell.Clients.ResourceManager' does not have an implementation."

**Possible causes:**
1. Conflicting Azure PowerShell modules (old AzureRM and new Az modules installed together)
2. Corrupted or incompatible Az module versions
3. Missing assembly dependencies

**Solution:**
```powershell
# 1. Check what Azure modules you have installed
Get-Module -ListAvailable -Name Az*, Azure*

# 2. Uninstall all old AzureRM modules (if any exist)
Uninstall-Module -Name AzureRM -AllVersions -Force

# 3. Uninstall all Az modules
Uninstall-Module -Name Az -AllVersions -Force

# 4. Reinstall the latest Az module
Install-Module -Name Az -Repository PSGallery -Force -AllowClobber -Scope CurrentUser

# 5. Import the module
Import-Module Az

# 6. Verify installation
Get-Module -ListAvailable -Name Az

# 7. Re-run the script
.\acs-impact-assessment-tool.ps1
```

**Alternative Quick Fix:**
```powershell
# Update all Az modules to latest version
Update-Module -Name Az -Force
```

**Important Note:** The old AzureRM modules are deprecated and incompatible with the current Az modules. Microsoft recommends uninstalling all AzureRM modules before installing Az modules to avoid conflicts.

---

## Performance Considerations

| Environment | Without -IncludeMetrics | With -IncludeMetrics |
|-------------|------------------------|----------------------|
| 1 subscription, 5 resources | ~30 seconds | ~3-5 minutes |
| 5 subscriptions, 20 resources | ~2 minutes | ~10-15 minutes |
| 10+ subscriptions, 50+ resources | ~5 minutes | ~30+ minutes |

**Recommendation:** Run without `-IncludeMetrics` first to get a quick inventory, then re-run with `-IncludeMetrics` for resources that need detailed analysis.

---

## Integration with ACS Transition Agent

This PowerShell script provides an alternative assessment method that complements the web-based ACS Transition Agent:

| Feature | PowerShell Script | Web Application |
|---------|------------------|-----------------|
| **Multi-subscription scanning** | ✅ Built-in | 🔄 Phase 2 |
| **Batch processing** | ✅ Yes | ❌ Manual per sub |
| **User interface** | ❌ CLI only | ✅ Web UI |
| **Real-time metrics** | ✅ Yes (with flag) | ✅ Yes |
| **Migration guides** | ❌ Not included | ✅ Built-in |
| **CSV export** | ✅ Yes | ✅ Yes |

**Use Case:**
- Use the **PowerShell script** for bulk assessment across many subscriptions
- Use the **Web Application** for interactive exploration and migration guidance

---

## Next Steps After Running Assessment

1. **Review the CSV Report**
   - Open in Excel or Power BI
   - Filter by `HighestSeverity = Critical`
   - Group by `SubscriptionName` for organizational planning

2. **Prioritize Resources**
   - Focus on Critical severity first
   - Address resources with high usage counts
   - Plan multi-channel migrations (High effort) early

3. **Access Migration Guides**
   - Email Service → Microsoft 365 HVE: https://aka.ms/acs-email-migration
   - SMS API: https://aka.ms/acs-sms-migration
   - Chat SDK: https://aka.ms/acs-chat-migration
   - Calling SDK: https://aka.ms/acs-calling-migration
   - Phone Numbers SDK: https://aka.ms/acs-phone-migration
   - Retirement & Breaking Changes (comprehensive): https://aka.ms/acs-retirement-and-breaking-changes-guide

4. **Create Migration Timeline**
   - Check retirement dates for each service
   - Allow 3-6 months for High effort migrations
   - Schedule testing and validation time

5. **Monitor Progress**
   - Re-run assessment monthly
   - Track migration completion
   - Update CSV with migration status

---

## Getting Help

### Built-in Help
```powershell
Get-Help .\acs-impact-assessment-tool.ps1 -Full
```

### Examples
```powershell
Get-Help .\acs-impact-assessment-tool.ps1 -Examples
```

### Parameter Details
```powershell
Get-Help .\acs-impact-assessment-tool.ps1 -Parameter IncludeMetrics
```

---

## Contributing

If you find issues or have suggestions for improvements:
1. Document the issue with script output
2. Include your PowerShell version: `$PSVersionTable.PSVersion`
3. Include your Az module version: `Get-Module -Name Az -ListAvailable`

---

## Version History

### Version 1.0 (2026-01-26)
- Initial release
- Multi-subscription scanning
- All 5 ACS channel detection
- Optional metrics retrieval
- Severity and effort calculation
- CSV export

---

## License

MIT License - See LICENSE file for details

---

## Related Resources

- **ACS Transition Agent:** See `README.md` in project root
- **Email Migration Guide:** https://aka.ms/acs-email-migration
- **SMS Migration Guide:** https://aka.ms/acs-sms-migration
- **Chat Migration Guide:** https://aka.ms/acs-chat-migration
- **Calling Migration Guide:** https://aka.ms/acs-calling-migration
- **Phone Numbers Migration Guide:** https://aka.ms/acs-phone-migration
- **Retirement & Breaking Changes:** https://aka.ms/acs-retirement-and-breaking-changes-guide
- **Azure Monitor Metrics:** [Microsoft Docs](https://docs.microsoft.com/azure/communication-services/concepts/metrics)

---

**Last Updated:** 2026-01-26
**Maintained By:** ACS Transition Agent Team
