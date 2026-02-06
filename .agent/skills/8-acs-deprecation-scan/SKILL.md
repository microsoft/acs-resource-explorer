---
name: 8-acs-deprecation-scan
description: Run the repo’s ACS impact assessment scan (read-only) and produce an impact summary plus migration guidance. Uses the existing PowerShell script and never claims feature usage without evidence.
---

## When to use this skill
Use this skill when the user asks to scan Azure subscriptions for Azure Communication Services (ACS) resources and produce a deprecation/retirement impact summary with links to migration guidance.

Examples:
  - "Scan my subscription for ACS deprecations."
  - "Run an ACS impact assessment and summarize what is potentially affected."
  - "Generate an ACS deprecation impact report with metrics if available."

## Preconditions
- Read-only access (at least **Reader**) to the target subscription(s).
- PowerShell Az module available and authenticated (the script uses `Connect-AzAccount`).
- The canonical scan script lives under: `scripts/powershell/acs-impact-assessment-tool.ps1`.

> Note: On macOS/Linux use `pwsh` (PowerShell 7). On Windows you can use `pwsh` or Windows PowerShell if supported by the script.

## Workflow
1) **Locate the canonical command**
   - Open `scripts/powershell/README.md` and confirm the correct invocation, flags, and expected output files.
   - Do not guess flags.

2) **Run the scan (read-only)**
   - Run the script from `scripts/powershell` (as documented in the script README).
   - Use `-IncludeMetrics` for a complete assessment; without it, only Email + Phone Numbers are detected.

   Example (macOS/Linux):
   - `pwsh ./acs-impact-assessment-tool.ps1 -IncludeMetrics`

   Example (Windows):
   - `pwsh .\acs-impact-assessment-tool.ps1 -IncludeMetrics`

3) **Collect outputs**
   - Identify the output artifacts created by the script (CSV by default).
   - Default output is `exports/ACS_Impact_Assessment.csv` unless `-OutputPath` is used.
   - Save the raw scan output path(s).

4) **Generate a human-readable report**
   - Write `docs/ACS-DEPRECATION-IMPACT-REPORT.md` with:
     - Summary counts (subscriptions scanned if available, ACS resources found)
     - Breakdown by subscription and resource group
     - Potential impact section that references `src/config/retiring-features.ts` (or equivalent catalog) and links to relevant files under `migration-guides/**`
     - Confidence & limitations: clearly state what cannot be inferred (e.g., feature/channel usage may be unknown if telemetry/metrics are missing)
     - Next steps checklist
