<#
.SYNOPSIS
    Azure Communication Services Impact Assessment Tool

.DESCRIPTION
    This script scans Azure subscriptions for ACS resources and assesses the impact
    of retiring ACS services (Email, SMS, Chat, Calling, Phone Numbers).

.PARAMETER SubscriptionId
    Optional. Specific subscription ID to scan. If not provided, scans all accessible subscriptions.

.PARAMETER OutputPath
    Optional. Path for the CSV output file. Default: ".\ACS_Impact_Assessment.csv"

.PARAMETER IncludeMetrics
    Optional. If specified, retrieves usage metrics from Azure Monitor (slower but more detailed).

.EXAMPLE
    .\acs-impact-assessment-tool.ps1
    Scans all subscriptions and generates a CSV report

.EXAMPLE
    .\acs-impact-assessment-tool.ps1 -SubscriptionId "12345678-1234-1234-1234-123456789abc" -IncludeMetrics
    Scans a specific subscription with metrics

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
    [string]$OutputPath = ".\exports\ACS_Impact_Assessment.csv",

    [Parameter(Mandatory=$false)]
    [switch]$IncludeMetrics
)

# Check if Az module is installed
if (-not (Get-Module -ListAvailable -Name Az.Accounts)) {
    Write-Error "Az PowerShell module is not installed. Please run: Install-Module -Name Az"
    exit 1
}

# Connect to Azure
Write-Host "`n=== Azure Communication Services Impact Assessment Tool ===" -ForegroundColor Cyan
Write-Host "Connecting to Azure..." -ForegroundColor Yellow

try {
    Connect-AzAccount -ErrorAction Stop | Out-Null
    Write-Host "Successfully connected to Azure" -ForegroundColor Green

    # Get current Azure context and display tenant information
    $currentContext = Get-AzContext
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

        $choice = Read-Host "`nEnter your choice (1 or 2, default is 1)"

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
    Write-Host "  - This will take longer but provides complete detection + usage counts" -ForegroundColor White
} else {
    Write-Host "`nDetection Mode: FAST (resource-only)" -ForegroundColor Yellow
    Write-Host "  - Only Email and Phone Numbers can be detected (via resources)" -ForegroundColor White
    Write-Host "  - SMS, Chat, and Calling require '-IncludeMetrics' flag for detection" -ForegroundColor White
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
    Email = @('EmailMessagesSent', 'EmailDeliveryAttempts', 'EmailOperations')
    SMS = @('SMSMessagesSent', 'SMSMessagesReceived')
    Chat = @('ChatMessageCount', 'ChatThreadCount', 'ActiveChatUsers')
    Calling = @('CallDuration', 'CallCount', 'ParticipantCount')
    PhoneNumbers = @('PhoneNumberOperations')
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
                Write-Host "            SMS, Chat, and Calling require -IncludeMetrics flag for detection via usage metrics." -ForegroundColor Gray
            }

            # Initialize resource impact data
            $resourceImpact = [PSCustomObject]@{
                SubscriptionName = $subscription.Name
                SubscriptionId = $subscription.Id
                ResourceGroup = $resource.ResourceGroupName
                ResourceName = $resource.Name
                Location = $resource.Location

                # Channel detection flags
                EmailDetected = $false
                EmailUsageCount = 0
                SMSDetected = $false
                SMSUsageCount = 0
                ChatDetected = $false
                ChatUsageCount = 0
                CallingDetected = $false
                CallingUsageCount = 0
                PhoneNumbersDetected = $false
                PhoneNumbersUsageCount = 0

                # Overall impact
                TotalChannelsImpacted = 0
                HighestSeverity = "None"
                MigrationEffortEstimate = "None"
            }

            # Check for Email domains (resource-based detection)
            $emailDomains = Get-AzResource -ResourceGroupName $resource.ResourceGroupName `
                                          -ResourceType "Microsoft.Communication/EmailServices/Domains" `
                                          -ErrorAction SilentlyContinue

            if ($emailDomains) {
                $resourceImpact.EmailDetected = $true
                $resourceImpact.TotalChannelsImpacted++
                Write-Host "      [+] Email service detected ($($emailDomains.Count) domain(s))" -ForegroundColor Yellow
            }

            # Check for Phone Numbers (resource-based detection)
            try {
                $phoneNumbers = Get-AzResource -ResourceGroupName $resource.ResourceGroupName `
                                               -ResourceType "Microsoft.Communication/CommunicationServices/phoneNumbers" `
                                               -ErrorAction SilentlyContinue

                if (-not $phoneNumbers) {
                    # Try alternate resource type
                    $phoneNumbers = Get-AzResource | Where-Object {
                        $_.ResourceGroupName -eq $resource.ResourceGroupName -and
                        $_.Name -match "^\+\d+"
                    }
                }

                if ($phoneNumbers) {
                    $resourceImpact.PhoneNumbersDetected = $true
                    $resourceImpact.TotalChannelsImpacted++
                    Write-Host "      [+] Phone Numbers detected ($($phoneNumbers.Count) number(s))" -ForegroundColor Yellow
                }
            } catch {
                # Phone number detection failed, will rely on metrics if available
            }

            # If IncludeMetrics is specified, get usage metrics for all channels
            if ($IncludeMetrics) {
                Write-Host "      Retrieving usage metrics (last 90 days)..." -ForegroundColor Gray

                $endTime = Get-Date
                $startTime = $endTime.AddDays(-90)

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
                                if (-not $resourceImpact.TotalChannelsImpacted -or $resourceImpact.TotalChannelsImpacted -eq 0) {
                                    $resourceImpact.TotalChannelsImpacted++
                                }
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
                            'Calling' {
                                $resourceImpact.CallingDetected = $true
                                $resourceImpact.CallingUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Calling usage: $totalUsage calls" -ForegroundColor Yellow
                            }
                            'PhoneNumbers' {
                                $resourceImpact.PhoneNumbersDetected = $true
                                $resourceImpact.PhoneNumbersUsageCount = [int]$totalUsage
                                $resourceImpact.TotalChannelsImpacted++
                                Write-Host "      [+] Phone Numbers usage detected" -ForegroundColor Yellow
                            }
                        }
                    }
                }
            }

            # Display usage breakdown for this resource
            Write-Host "`n      Channel Usage Summary (last 90 days):" -ForegroundColor Cyan
            Write-Host "        Email:        $($resourceImpact.EmailUsageCount) messages" -ForegroundColor $(if ($resourceImpact.EmailDetected) { "Yellow" } else { "Gray" })
            Write-Host "        SMS:          $($resourceImpact.SMSUsageCount) messages" -ForegroundColor $(if ($resourceImpact.SMSDetected) { "Yellow" } else { "Gray" })
            Write-Host "        Chat:         $($resourceImpact.ChatUsageCount) messages" -ForegroundColor $(if ($resourceImpact.ChatDetected) { "Yellow" } else { "Gray" })
            Write-Host "        Calling:      $($resourceImpact.CallingUsageCount) calls" -ForegroundColor $(if ($resourceImpact.CallingDetected) { "Yellow" } else { "Gray" })
            Write-Host "        Phone Numbers: $($resourceImpact.PhoneNumbersUsageCount) operations" -ForegroundColor $(if ($resourceImpact.PhoneNumbersDetected) { "Yellow" } else { "Gray" })

            # Calculate severity and migration effort
            if ($resourceImpact.TotalChannelsImpacted -gt 0) {
                # Determine highest severity
                if ($resourceImpact.EmailUsageCount -gt 1000 -or $resourceImpact.CallingUsageCount -gt 500) {
                    $resourceImpact.HighestSeverity = "Critical"
                } elseif ($resourceImpact.EmailUsageCount -gt 100 -or $resourceImpact.SMSUsageCount -gt 50) {
                    $resourceImpact.HighestSeverity = "Warning"
                } else {
                    $resourceImpact.HighestSeverity = "Info"
                }

                # Estimate migration effort based on number of channels
                if ($resourceImpact.TotalChannelsImpacted -ge 3) {
                    $resourceImpact.MigrationEffortEstimate = "High"
                } elseif ($resourceImpact.TotalChannelsImpacted -eq 2) {
                    $resourceImpact.MigrationEffortEstimate = "Medium"
                } else {
                    $resourceImpact.MigrationEffortEstimate = "Low"
                }
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
    $callingCount = ($impactAssessment | Where-Object { $_.CallingDetected }).Count
    $phoneCount = ($impactAssessment | Where-Object { $_.PhoneNumbersDetected }).Count

    if ($resourcesWithRetiringServices -gt 0) {
        Write-Host "`nRetiring Services Detected:" -ForegroundColor Yellow
        if ($emailCount -gt 0) { Write-Host "  - Email Service: $emailCount resource(s)" -ForegroundColor White }
        if ($smsCount -gt 0) { Write-Host "  - SMS API: $smsCount resource(s)" -ForegroundColor White }
        if ($chatCount -gt 0) { Write-Host "  - Chat SDK: $chatCount resource(s)" -ForegroundColor White }
        if ($callingCount -gt 0) { Write-Host "  - Calling SDK: $callingCount resource(s)" -ForegroundColor White }
        if ($phoneCount -gt 0) { Write-Host "  - Phone Numbers SDK: $phoneCount resource(s)" -ForegroundColor White }

        $criticalCount = ($impactAssessment | Where-Object { $_.HighestSeverity -eq "Critical" }).Count
        $warningCount = ($impactAssessment | Where-Object { $_.HighestSeverity -eq "Warning" }).Count
        $infoCount = ($impactAssessment | Where-Object { $_.HighestSeverity -eq "Info" }).Count

        Write-Host "`nSeverity Breakdown:" -ForegroundColor Yellow
        if ($criticalCount -gt 0) { Write-Host "  - Critical: $criticalCount resource(s)" -ForegroundColor Red }
        if ($warningCount -gt 0) { Write-Host "  - Warning: $warningCount resource(s)" -ForegroundColor DarkYellow }
        if ($infoCount -gt 0) { Write-Host "  - Info: $infoCount resource(s)" -ForegroundColor Gray }
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
    Write-Host "Export complete! All $($impactAssessment.Count) ACS resource(s) included in report." -ForegroundColor Green

    # Display results table
    Write-Host "`n=== Detailed Results ===" -ForegroundColor Cyan
    $impactAssessment | Format-Table -Property ResourceName, ResourceGroup, TotalChannelsImpacted, EmailUsageCount, SMSUsageCount, ChatUsageCount, CallingUsageCount, HighestSeverity, MigrationEffortEstimate -AutoSize

} else {
    Write-Host "`nNo ACS resources found in the scanned subscription(s)." -ForegroundColor Green
}

Write-Host "`n=== Assessment Complete ===" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review the CSV report: $OutputPath" -ForegroundColor White
Write-Host "  2. Prioritize resources with 'Critical' severity" -ForegroundColor White
Write-Host "  3. Review migration guides for each detected channel" -ForegroundColor White
Write-Host "  4. Plan migration timeline based on retirement dates" -ForegroundColor White
Write-Host "`nFor migration guides, visit: https://aka.ms/acs-transition-guides" -ForegroundColor Cyan
