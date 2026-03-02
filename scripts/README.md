# ACS Transition Agent - Assessment Scripts

This folder contains automated scripts for scanning Azure subscriptions and assessing the impact of retiring ACS services.

---

## Available Scripts

### PowerShell

- **[acs-impact-assessment-tool.ps1](powershell/acs-impact-assessment-tool.ps1)** - Multi-subscription scanner for ACS resources
  - Detects all retiring channels (Email, SMS, Chat, Calling, Phone Numbers)
  - Optional metrics retrieval from Azure Monitor
  - Severity and migration effort calculation
  - CSV export for planning and tracking
  - **[Full Documentation](powershell/README.md)**

---

## Quick Start

### PowerShell Script

```powershell
# Navigate to the PowerShell script directory
cd scripts/powershell

# Run a basic scan (fast, all subscriptions)
.\acs-impact-assessment-tool.ps1

# Run with detailed usage metrics
.\acs-impact-assessment-tool.ps1 -IncludeMetrics

# Scan a specific subscription
.\acs-impact-assessment-tool.ps1 -SubscriptionId "your-subscription-id"
```

See [PowerShell README](powershell/README.md) for detailed usage instructions.

---

## Future Scripts

Additional scripts will be added to this folder as the ACS Transition Agent suite expands:

- **Python scripts** (planned) - Cross-platform assessment tools
- **Bash scripts** (planned) - Linux/macOS automation
- **Azure CLI scripts** (planned) - Alternative scanning methods

---

## Related Resources

- [Migration Guides](../migration-guides/) - Migration guide references
- [Project Documentation](../docs/) - Full project details

---

## Support

For questions or issues with these scripts, please open an issue in the repository or contact the ACS team.
