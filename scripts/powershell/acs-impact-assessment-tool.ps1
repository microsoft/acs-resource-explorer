<#
.SYNOPSIS
    Azure Communication Services Impact Assessment Tool

.DESCRIPTION
    This script scans Azure subscriptions for ACS resources and assesses the impact
    of retiring ACS services (Email, SMS, Chat, Calling, Phone Numbers).

.PARAMETER SubscriptionId
    Optional. Specific subscription ID to scan. If not provided, scans all accessible subscriptions.

.PARAMETER OutputPath
    Optional. Path for the CSV output file.

.PARAMETER IncludeMetrics
    Optional. If specified, retrieves usage metrics from Azure Monitor (slower but more detailed).

.PARAMETER LookbackDays
    Optional. Number of days to look back for usage metrics (1-93 days). Default: 90 days.
    Azure Monitor retention limit is 93 days for 1-hour granularity metrics.

.EXAMPLE
    .\acs-impact-assessment-tool.ps1
    Scans all subscriptions and generates a CSV report

.EXAMPLE
    .\acs-impact-assessment-tool.ps1 -SubscriptionId "12345678-1234-1234-1234-123456789abc" -IncludeMetrics
    Scans a specific subscription with metrics (90-day lookback)

.EXAMPLE
    .\acs-impact-assessment-tool.ps1 -IncludeMetrics -LookbackDays 30
    Scans with metrics using 30-day lookback period

.EXAMPLE
    .\acs-impact-assessment-tool.ps1 -IncludeMetrics -LookbackDays 93
    Scans with metrics using maximum 93-day lookback period

.NOTES
    Requires: Az PowerShell module (Install-Module -Name Az)
    Version: 1.0
    Last Updated: January 2026
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId,

    [Parameter(Mandatory=$false)]
    [string]$OutputPath,

    [Parameter(Mandatory=$false)]
    [switch]$IncludeMetrics,

    [Parameter(Mandatory=$false)]
    [ValidateRange(1, 93)]
    [int]$LookbackDays = 90
)

$toolVersion = "1.0.0"
$scanType = if ($IncludeMetrics) { "Full" } else { "Fast" }
$runTimestampUtc = [DateTime]::UtcNow.ToString("yyyyMMddHHmmss", [Globalization.CultureInfo]::InvariantCulture)

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = ".\exports\ACS_Impact_Assessment.csv"
}

$outputDirectory = Split-Path -Path $OutputPath -Parent
$outputFileName = Split-Path -Path $OutputPath -Leaf
$outputExtension = [System.IO.Path]::GetExtension($outputFileName)
$outputBaseName = if ($outputExtension) {
    [System.IO.Path]::GetFileNameWithoutExtension($outputFileName)
} else {
    $outputFileName
}
$outputBaseName = $outputBaseName -replace '_v\d+(?:\.\d+)*(?:_\d{14})?$', ''
$outputBaseName = $outputBaseName -replace '_(?:Fast|Full)$', ''
$versionedFileName = "${outputBaseName}_${scanType}_v${toolVersion}_${runTimestampUtc}$outputExtension"

$OutputPath = if ($outputDirectory) {
    Join-Path -Path $outputDirectory -ChildPath $versionedFileName
} else {
    $versionedFileName
}

# Check if Az module is installed
if (-not (Get-Module -ListAvailable -Name Az.Accounts)) {
    Write-Error "Az PowerShell module is not installed. Please run: Install-Module -Name Az"
    exit 1
}

# Connect to Azure
Write-Host "`n=== Azure Communication Services Impact Assessment Tool ===" -ForegroundColor Cyan
Write-Host "Tool version: $toolVersion" -ForegroundColor Gray
Write-Host "Checking Azure connection..." -ForegroundColor Yellow

try {
    # Check if already connected
    $currentContext = Get-AzContext
    if (-not $currentContext) {
        Write-Host "Not connected to Azure. Connecting..." -ForegroundColor Yellow
        Connect-AzAccount -ErrorAction Stop | Out-Null
        $currentContext = Get-AzContext
    }

    Write-Host "Successfully connected to Azure" -ForegroundColor Green

    # Display tenant information
    if ($currentContext) {
        $tenantId = $currentContext.Tenant.Id
        $accountName = $currentContext.Account.Id

        Write-Host "`nConnected to:" -ForegroundColor Cyan
        Write-Host "  Account:   $accountName" -ForegroundColor White
        Write-Host "  Tenant ID: $tenantId" -ForegroundColor White

        Write-Host "`nNote: If you need to connect to a different tenant, please rerun:" -ForegroundColor Gray
        Write-Host "  Connect-AzAccount -TenantId '$tenantId'" -ForegroundColor Gray
    }
} catch {
    Write-Error "Failed to connect to Azure: $_"
    exit 1
}

# Get subscriptions to scan
if ($SubscriptionId) {
    Write-Host "`nFiltering to specific subscription: $SubscriptionId" -ForegroundColor Cyan
    try {
        $subscriptions = @(Get-AzSubscription -SubscriptionId $SubscriptionId -ErrorAction Stop)
        Write-Host "Found subscription: $($subscriptions[0].Name)" -ForegroundColor Green
    } catch {
        Write-Error "Could not find subscription with ID: $SubscriptionId"
        Write-Host "`nAvailable subscriptions:" -ForegroundColor Yellow
        Get-AzSubscription | Format-Table Name, Id, State -AutoSize
        exit 1
    }
} else {
    # Check if there's a default subscription in the current context
    $defaultSubscription = (Get-AzContext).Subscription

    if ($defaultSubscription) {
        Write-Host "`nDefault subscription detected: $($defaultSubscription.Name) ($($defaultSubscription.Id))" -ForegroundColor Cyan
        Write-Host "Options:" -ForegroundColor Yellow
        Write-Host "  1. Scan only the default subscription (recommended)" -ForegroundColor White
        Write-Host "  2. Scan all accessible subscriptions ($((Get-AzSubscription).Count) subscriptions)" -ForegroundColor White

        if ([Environment]::UserInteractive -and -not [System.Console]::IsInputRedirected) {
            $choice = Read-Host "`nEnter your choice (1 or 2, default is 1)"
        } else {
            $choice = "1"
            Write-Host "`nNon-interactive mode: defaulting to option 1 (default subscription only)" -ForegroundColor Gray
        }

        if ($choice -eq "2") {
            Write-Host "`nScanning all accessible subscriptions..." -ForegroundColor Cyan
            $subscriptions = Get-AzSubscription
        } else {
            Write-Host "`nScanning only default subscription: $($defaultSubscription.Name)" -ForegroundColor Green
            $subscriptions = @(Get-AzSubscription -SubscriptionId $defaultSubscription.Id)
        }
    } else {
        Write-Host "`nNo default subscription found - scanning all accessible subscriptions" -ForegroundColor Cyan
        $subscriptions = Get-AzSubscription
    }
}

Write-Host "`nScanning $($subscriptions.Count) subscription(s)..." -ForegroundColor Yellow

# Detection mode information
if ($IncludeMetrics) {
    Write-Host "`nDetection Mode: FULL (with metrics)" -ForegroundColor Green
    Write-Host "  - All channels will be detected via Azure Monitor usage metrics" -ForegroundColor White
    Write-Host "  - Lookback period: Last $LookbackDays days" -ForegroundColor White
    Write-Host "  - This will take longer but provides complete detection + usage counts" -ForegroundColor White
    if ($LookbackDays -lt 93) {
        Write-Host "  - Note: You can extend lookback up to 93 days with '-LookbackDays 93'" -ForegroundColor Gray
    }
} else {
    Write-Host "`nDetection Mode: FAST (resource-only)" -ForegroundColor Yellow
    Write-Host "  - Only Email and Phone Numbers can be detected (via resources)" -ForegroundColor White
    Write-Host "  - SMS, Chat, Call Automation, Job Router, Advance Messaging, and Rooms require '-IncludeMetrics' flag for detection" -ForegroundColor White
    Write-Host "  - Recommendation: Re-run with '-IncludeMetrics' for complete results" -ForegroundColor DarkYellow
}

# List subscriptions that will be scanned
if ($subscriptions.Count -le 5) {
    Write-Host "Subscriptions to scan:" -ForegroundColor Cyan
    foreach ($sub in $subscriptions) {
        Write-Host "  - $($sub.Name) ($($sub.Id))" -ForegroundColor White
    }
} else {
    Write-Host "First 5 subscriptions to scan:" -ForegroundColor Cyan
    $subscriptions | Select-Object -First 5 | ForEach-Object {
        Write-Host "  - $($_.Name) ($($_.Id))" -ForegroundColor White
    }
    Write-Host "  ... and $($subscriptions.Count - 5) more" -ForegroundColor Gray
}

# Initialize results array
$impactAssessment = @()
$totalACSResourcesFound = 0

# Metrics to check for each channel
$metricsConfig = @{
    Email = @('ApiRequests', 'DeliveryStatusUpdate', 'UserEngagement')
    SMS = @('APIRequestSMS')
    Chat = @('APIRequestChat')
    CallAutomation = @('APIRequestCallAutomation', 'APIRequestCallRecording', 'AcsCallAutomationCallbackEvent')
    JobRouter = @('ApiRequestRouter')
    AdvanceMessaging = @('APIRequestsAdvancedMessaging')
    Rooms = @('ApiRequestRooms')
}

# Scan each subscription
foreach ($subscription in $subscriptions) {
    Write-Host "`nScanning subscription: $($subscription.Name) ($($subscription.Id))" -ForegroundColor Cyan

    try {
        Set-AzContext -SubscriptionId $subscription.Id -ErrorAction Stop | Out-Null

        # Find all ACS resources
        $acsResources = Get-AzResource -ResourceType "Microsoft.Communication/CommunicationServices" -ErrorAction SilentlyContinue

        if (-not $acsResources) {
            Write-Host "  No ACS resources found" -ForegroundColor Gray
            continue
        }

        Write-Host "  Found $($acsResources.Count) ACS resource(s)" -ForegroundColor Green
        $totalACSResourcesFound += $acsResources.Count

        foreach ($resource in $acsResources) {
            Write-Host "    Analyzing: $($resource.Name)" -ForegroundColor White

            # Warn about detection limitations without metrics
            if (-not $IncludeMetrics) {
                Write-Host "      Note: Running without -IncludeMetrics. Only Email and Phone Numbers can be detected via resources." -ForegroundColor Gray
                Write-Host "            SMS, Chat, Call Automation, Job Router, Advance Messaging, and Rooms require -IncludeMetrics flag for detection via usage metrics." -ForegroundColor Gray
            }

            # Initialize resource impact data
            $resourceImpact = [PSCustomObject]@{
                SubscriptionName = $subscription.Name
                SubscriptionId = $subscription.Id
                ResourceGroup = $resource.ResourceGroupName
                ResourceName = $resource.Name
                Location = $resource.Location
                LookbackPeriodDays = $(if ($IncludeMetrics) { $LookbackDays } else { "N/A" })

                # Channel detection flags
                EmailDetected = $false
                EmailUsageCount = 0
                SMSDetected = $false
                SMSUsageCount = 0
                ChatDetected = $false
                ChatUsageCount = 0
                CallAutomationDetected = $false
                CallAutomationUsageCount = 0
                JobRouterDetected = $false
                JobRouterUsageCount = 0
                AdvanceMessagingDetected = $false
                AdvanceMessagingUsageCount = 0
                RoomsDetected = $false
                RoomsUsageCount = 0
                PhoneNumbersDetected = $false
                PhoneNumbersUsageCount = 0
                AccessKeysAuthDisabled = $false

                # Overall impact
                TotalChannelsImpacted = 0
            }

            # Check for Email domains (resource-based detection)
            $emailDomains = Get-AzResource -ResourceGroupName $resource.ResourceGroupName `
                                          -ResourceType "Microsoft.Communication/EmailServices/Domains" `
                                          -ErrorAction SilentlyContinue

            if ($emailDomains) {
                $resourceImpact.EmailDetected = $true
                $resourceImpact.TotalChannelsImpacted++
                $resourceImpact.EmailUsageCount = [int]$emailDomains.Count
                Write-Host "      [+] Email service detected ($($emailDomains.Count) domain(s))" -ForegroundColor Yellow
            }

            # Read expanded properties to detect whether key-based auth is disabled.
            $resourceDetails = Get-AzResource -ResourceId $resource.ResourceId -ExpandProperties -ErrorAction SilentlyContinue
            $resourceImpact.AccessKeysAuthDisabled = [bool]$resourceDetails.Properties.disableLocalAuth

            # Check for Phone Numbers via connection-string data-plane API.
            if ($resourceImpact.AccessKeysAuthDisabled) {
                Write-Host "      [!] Access key auth disabled — skipping phone number detection." -ForegroundColor DarkYellow
            } else {
                $connectionString = az communication list-key `
                    -g $resource.ResourceGroupName -n $resource.Name `
                    --query primaryConnectionString -o tsv --only-show-errors 2>$null

                if ($connectionString) {
                    $phoneNumberRaw = az communication phonenumber list `
                        --connection-string $connectionString -o json --only-show-errors 2>$null
                    $phoneNumberCount = if ($phoneNumberRaw) { @($phoneNumberRaw | ConvertFrom-Json).Count } else { 0 }

                    if ($phoneNumberCount -gt 0) {
                        $resourceImpact.PhoneNumbersDetected = $true
                        $resourceImpact.PhoneNumbersUsageCount = $phoneNumberCount
                        $resourceImpact.TotalChannelsImpacted++
                        Write-Host "      [+] Phone Numbers detected ($phoneNumberCount number(s))" -ForegroundColor Yellow
                    }
                }
            }

            # If IncludeMetrics is specified, get usage metrics for all channels
            if ($IncludeMetrics) {
                Write-Host "      Retrieving usage metrics (last $LookbackDays days)..." -ForegroundColor Gray

                $endTime = Get-Date
                $startTime = $endTime.AddDays(-$LookbackDays)

                # Check each channel's metrics
                foreach ($channel in $metricsConfig.Keys) {
                    $metricNames = $metricsConfig[$channel]
                    $totalUsage = 0

                    foreach ($metricName in $metricNames) {
                        try {
                            $metrics = Get-AzMetric -ResourceId $resource.ResourceId `
                                                   -MetricName $metricName `
                                                   -StartTime $startTime `
                                                   -EndTime $endTime `
                                                   -TimeGrain 01:00:00 `
                                                   -AggregationType Total `
                                                   -ErrorAction SilentlyContinue `
                                                   -WarningAction SilentlyContinue

                            if ($metrics -and $metrics.Data) {
                                $sum = ($metrics.Data | Measure-Object -Property Total -Sum).Sum
                                if ($sum -gt 0) {
                                    $totalUsage += $sum
                                }
                            }
                        } catch {
                            # Metric not available, skip
                        }
                    }

                    # Update resource impact based on channel usage
                    if ($totalUsage -gt 0) {
                        switch ($channel) {
                            'Email' {
                                $resourceImpact.EmailDetected = $true
                                $resourceImpact.EmailUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Email usage: $totalUsage messages" -ForegroundColor Yellow
                            }
                            'SMS' {
                                $resourceImpact.SMSDetected = $true
                                $resourceImpact.SMSUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] SMS usage: $totalUsage messages" -ForegroundColor Yellow
                            }
                            'Chat' {
                                $resourceImpact.ChatDetected = $true
                                $resourceImpact.ChatUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Chat usage: $totalUsage messages" -ForegroundColor Yellow
                            }
                            'CallAutomation' {
                                $resourceImpact.CallAutomationDetected = $true
                                $resourceImpact.CallAutomationUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Call Automation usage: $totalUsage operations" -ForegroundColor Yellow
                            }
                            'JobRouter' {
                                $resourceImpact.JobRouterDetected = $true
                                $resourceImpact.JobRouterUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Job Router usage: $totalUsage operations" -ForegroundColor Yellow
                            }
                            'AdvanceMessaging' {
                                $resourceImpact.AdvanceMessagingDetected = $true
                                $resourceImpact.AdvanceMessagingUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Advance Messaging usage: $totalUsage operations" -ForegroundColor Yellow
                            }
                            'Rooms' {
                                $resourceImpact.RoomsDetected = $true
                                $resourceImpact.RoomsUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Rooms usage: $totalUsage operations" -ForegroundColor Yellow
                            }
                        }
                    }
                }
            }

            # Display usage breakdown for this resource
            if ($IncludeMetrics) {
                Write-Host "`n      Channel Usage Summary (last $LookbackDays days):" -ForegroundColor Cyan
                Write-Host "        Email:         $($resourceImpact.EmailUsageCount) messages $(if ($resourceImpact.EmailUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.EmailDetected) { "Yellow" } else { "Gray" })
                Write-Host "        SMS:           $($resourceImpact.SMSUsageCount) messages $(if ($resourceImpact.SMSUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.SMSDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Chat:          $($resourceImpact.ChatUsageCount) messages $(if ($resourceImpact.ChatUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.ChatDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Call Automation: $($resourceImpact.CallAutomationUsageCount) operations $(if ($resourceImpact.CallAutomationUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.CallAutomationDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Job Router:    $($resourceImpact.JobRouterUsageCount) operations $(if ($resourceImpact.JobRouterUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.JobRouterDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Advance Msg:   $($resourceImpact.AdvanceMessagingUsageCount) operations $(if ($resourceImpact.AdvanceMessagingUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.AdvanceMessagingDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Rooms:         $($resourceImpact.RoomsUsageCount) operations $(if ($resourceImpact.RoomsUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.RoomsDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Phone Numbers: $($resourceImpact.PhoneNumbersUsageCount) operations $(if ($resourceImpact.PhoneNumbersUsageCount -eq 0) { '(zero usage in last ' + $LookbackDays + ' days)' } else { '' })" -ForegroundColor $(if ($resourceImpact.PhoneNumbersDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Access Key Auth: $(if ($resourceImpact.AccessKeysAuthDisabled) { 'Disabled' } else { 'Enabled' })" -ForegroundColor $(if ($resourceImpact.AccessKeysAuthDisabled) { "DarkYellow" } else { "Gray" })

                if ($LookbackDays -lt 93) {
                    Write-Host "`n      Want to check further back? Re-run with '-LookbackDays 93' (max: 93 days)" -ForegroundColor DarkYellow
                } else {
                    Write-Host "`n      Note: 93 days is the maximum lookback period for Azure Monitor metrics" -ForegroundColor Gray
                }
            } else {
                Write-Host "`n      Channel Usage Summary:" -ForegroundColor Cyan
                Write-Host "        Email:         $(if ($resourceImpact.EmailDetected) { 'Detected' } else { 'Not detected' })" -ForegroundColor $(if ($resourceImpact.EmailDetected) { "Yellow" } else { "Gray" })
                Write-Host "        SMS:           Requires -IncludeMetrics flag" -ForegroundColor Gray
                Write-Host "        Chat:          Requires -IncludeMetrics flag" -ForegroundColor Gray
                Write-Host "        Call Automation: Requires -IncludeMetrics flag" -ForegroundColor Gray
                Write-Host "        Job Router:    Requires -IncludeMetrics flag" -ForegroundColor Gray
                Write-Host "        Advance Msg:   Requires -IncludeMetrics flag" -ForegroundColor Gray
                Write-Host "        Rooms:         Requires -IncludeMetrics flag" -ForegroundColor Gray
                Write-Host "        Phone Numbers: $(if ($resourceImpact.PhoneNumbersDetected) { 'Detected' } else { 'Not detected' })" -ForegroundColor $(if ($resourceImpact.PhoneNumbersDetected) { "Yellow" } else { "Gray" })
                Write-Host "        Access Key Auth: $(if ($resourceImpact.AccessKeysAuthDisabled) { 'Disabled' } else { 'Enabled' })" -ForegroundColor $(if ($resourceImpact.AccessKeysAuthDisabled) { "DarkYellow" } else { "Gray" })
            }

            # Always add resource to assessment (even with 0 usage)
            $impactAssessment += $resourceImpact
        }

    } catch {
        Write-Warning "Error scanning subscription $($subscription.Name): $_"
    }
}

# Display summary
Write-Host "`n=== Impact Assessment Summary ===" -ForegroundColor Cyan
Write-Host "Total ACS resources found: $totalACSResourcesFound" -ForegroundColor White

if ($impactAssessment.Count -gt 0) {
    $resourcesWithRetiringServices = ($impactAssessment | Where-Object { $_.TotalChannelsImpacted -gt 0 }).Count
    Write-Host "Resources using retiring services: $resourcesWithRetiringServices" -ForegroundColor White

    $emailCount = ($impactAssessment | Where-Object { $_.EmailDetected }).Count
    $smsCount = ($impactAssessment | Where-Object { $_.SMSDetected }).Count
    $chatCount = ($impactAssessment | Where-Object { $_.ChatDetected }).Count
    $callAutomationCount = ($impactAssessment | Where-Object { $_.CallAutomationDetected }).Count
    $jobRouterCount = ($impactAssessment | Where-Object { $_.JobRouterDetected }).Count
    $advanceMessagingCount = ($impactAssessment | Where-Object { $_.AdvanceMessagingDetected }).Count
    $roomsCount = ($impactAssessment | Where-Object { $_.RoomsDetected }).Count
    $phoneCount = ($impactAssessment | Where-Object { $_.PhoneNumbersDetected }).Count
    $accessKeyAuthDisabledCount = ($impactAssessment | Where-Object { $_.AccessKeysAuthDisabled }).Count

    Write-Host "Access key auth disabled: $accessKeyAuthDisabledCount resource(s)" -ForegroundColor White

    if ($resourcesWithRetiringServices -gt 0) {
        Write-Host "`nRetiring Services Detected:" -ForegroundColor Yellow
        if ($emailCount -gt 0) { Write-Host "  - Email Service: $emailCount resource(s)" -ForegroundColor White }
        if ($smsCount -gt 0) { Write-Host "  - SMS API: $smsCount resource(s)" -ForegroundColor White }
        if ($chatCount -gt 0) { Write-Host "  - Chat SDK: $chatCount resource(s)" -ForegroundColor White }
        if ($callAutomationCount -gt 0) { Write-Host "  - Call Automation API: $callAutomationCount resource(s)" -ForegroundColor White }
        if ($jobRouterCount -gt 0) { Write-Host "  - Job Router API: $jobRouterCount resource(s)" -ForegroundColor White }
        if ($advanceMessagingCount -gt 0) { Write-Host "  - Advance Messaging API: $advanceMessagingCount resource(s)" -ForegroundColor White }
        if ($roomsCount -gt 0) { Write-Host "  - Rooms API: $roomsCount resource(s)" -ForegroundColor White }
        if ($phoneCount -gt 0) { Write-Host "  - Phone Numbers SDK: $phoneCount resource(s)" -ForegroundColor White }

    } else {
        Write-Host "`nGood news! Your ACS resources are not using any retiring services." -ForegroundColor Green
        Write-Host "All resources analyzed - no migration action required." -ForegroundColor Green
    }

    # Export to CSV (always export all resources)
    Write-Host "`nExporting results to: $OutputPath" -ForegroundColor Yellow

    # Create exports directory if it doesn't exist
    $outputDir = Split-Path -Path $OutputPath -Parent
    if ($outputDir -and -not (Test-Path -Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        Write-Host "  Created output directory: $outputDir" -ForegroundColor Gray
    }

    $impactAssessment | Export-Csv -Path $OutputPath -NoTypeInformation
    if ($IncludeMetrics) {
        Write-Host "Export complete! All $($impactAssessment.Count) ACS resource(s) included with $LookbackDays-day usage data." -ForegroundColor Green
    } else {
        Write-Host "Export complete! All $($impactAssessment.Count) ACS resource(s) included (resource detection only)." -ForegroundColor Green
    }

    # Display results table
    Write-Host "`n=== Detailed Results ===" -ForegroundColor Cyan
    $impactAssessment | Format-Table -Property ResourceName, ResourceGroup, AccessKeysAuthDisabled, TotalChannelsImpacted, EmailUsageCount, SMSUsageCount, ChatUsageCount, CallAutomationUsageCount, JobRouterUsageCount, AdvanceMessagingUsageCount, RoomsUsageCount, PhoneNumbersUsageCount -AutoSize

} else {
    Write-Host "`nNo ACS resources found in the scanned subscription(s)." -ForegroundColor Green
}

Write-Host "`n=== Assessment Complete ===" -ForegroundColor Cyan

if ($IncludeMetrics) {
    Write-Host "`nUsage data covers: Last $LookbackDays days" -ForegroundColor Cyan
    if ($LookbackDays -lt 93) {
        Write-Host "To check further back, re-run with: -IncludeMetrics -LookbackDays 93 (maximum)" -ForegroundColor Yellow
    }
}

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Review the CSV report: $OutputPath" -ForegroundColor White
Write-Host "  2. Prioritize resources with 'Critical' severity" -ForegroundColor White
Write-Host "  3. Review migration guides for each detected channel" -ForegroundColor White
Write-Host "  4. Plan migration timeline based on retirement dates" -ForegroundColor White
Write-Host "`nFor migration guides, visit: https://aka.ms/acs-retirement-and-breaking-changes-guide" -ForegroundColor Cyan
