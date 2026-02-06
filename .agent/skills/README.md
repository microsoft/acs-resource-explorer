# Azure Deprecation Analysis Skills

This directory contains **Level 2 Agent Skills** for Claude Code CLI that provide generic, reusable workflows for analyzing Azure resource deprecation impact across any Azure product or service.

## Skills Overview

These skills work together as a composable workflow pipeline. Each skill performs a specific task and passes state to the next skill in the sequence.

### 🔐 1. 1-azure-auth-check
**Purpose:** Verify Azure authentication and display connection information.

**When to use:**
- "Check my Azure authentication"
- "Show my current Azure connection"

**Outputs:** Authentication status, tenant info, account details, subscription context

---

### 📋 2. 2-azure-subscription-select
**Purpose:** Interactive subscription selection (single or multiple subscriptions).

**When to use:**
- "Select subscriptions to scan"
- "I want to scan all my subscriptions"

**Preconditions:** Requires **1-azure-auth-check** first

**Outputs:** List of selected subscription(s) saved to session state

---

### 🔍 3. 3-azure-resource-scan
**Purpose:** Scan subscriptions for specific resource types (ACS, Storage, SQL, VMs, etc).

**When to use:**
- "Scan for Azure Communication Services resources"
- "Find all Storage Accounts in my subscription"

**Preconditions:** Requires **1-azure-auth-check** and **2-azure-subscription-select**

**Interactive prompts:**
- Which Azure product to scan? (presents common options + custom)
- Optional filtering by name, location, or tags

**Outputs:** Resource inventory saved to session state

---

### ⚡ 4. 4-azure-channel-detect
**Purpose:** Fast, resource-based feature detection (no metrics).

**When to use:**
- "Quick scan for enabled features"
- "Detect which ACS channels are configured (fast mode)"

**Preconditions:** Requires **3-azure-resource-scan** first

**Detection method:** Examines child resources and resource properties

**Trade-offs:**
- ✅ Fast (~30 seconds per subscription)
- ⚠️ Limited coverage (only resource-based features)

**Outputs:** Features detected per resource (partial detection)

---

### 📊 5. 5-azure-metrics-collect
**Purpose:** Comprehensive, metrics-based feature detection (1-93 day lookback).

**When to use:**
- "Collect usage metrics for my resources over 90 days"
- "Get complete feature detection with metrics"

**Preconditions:** Requires **3-azure-resource-scan** first

**Detection method:** Queries Azure Monitor metrics for actual usage

**Interactive prompts:**
- Lookback period (1-93 days, default: 90)
- Which features/channels to analyze

**Trade-offs:**
- ✅ Complete detection (100% coverage)
- ⚠️ Slower (~3-5 minutes per subscription)

**Outputs:** Complete feature usage data per resource

---

### 🎯 6. 6-azure-impact-analyze
**Purpose:** Calculate severity and migration effort based on usage patterns.

**When to use:**
- "Analyze the impact of detected features"
- "Which resources should I prioritize for migration?"

**Preconditions:** Requires **4-azure-channel-detect** OR **5-azure-metrics-collect**

**Interactive prompts:**
- Use predefined severity rules or define custom thresholds

**Severity levels:**
- 🔴 Critical: High usage or business-critical resources
- 🟡 Warning: Moderate usage
- ℹ️ Info: Low usage or minimal impact

**Migration effort:**
- High: 3+ features, >10k operations
- Medium: 2 features, >1k operations
- Low: 1 feature, <1k operations

**Outputs:**
- Severity per resource
- Migration effort estimates
- Prioritized resource list
- Recommended next steps

---

### 📝 7. 7-azure-report-generate
**Purpose:** Export results to CSV, Markdown, JSON formats.

**When to use:**
- "Generate a report with all analysis results"
- "Export the results to CSV"

**Preconditions:** Requires all previous skills (complete analysis)

**Interactive prompts:**
- Report format (CSV, Markdown, JSON, or all)
- Output directory (default: `./exports/`)

**Outputs:**
- CSV: Excel-compatible detailed data
- Markdown: Human-readable documentation
- JSON: Machine-readable for API integration
- Console: Summary statistics and recommendations

---

### 🚀 8. 8-acs-deprecation-scan (EXISTING)
**Purpose:** ACS-specific orchestrator that runs the full workflow automatically.

**When to use:**
- "Scan my subscription for ACS deprecations"
- "Run an ACS impact assessment"

**What it does:** Orchestrates skills 1-7 with ACS-specific configurations

---

## Workflow Sequences

### Full Workflow (Complete Analysis)
```
1-azure-auth-check
  ↓
2-azure-subscription-select
  ↓
3-azure-resource-scan (interactive: choose product)
  ↓
5-azure-metrics-collect (comprehensive, 90 days)
  ↓
6-azure-impact-analyze (severity + effort)
  ↓
7-azure-report-generate (CSV + Markdown + JSON)
```

### Fast Workflow (Resource-Only Detection)
```
1-azure-auth-check
  ↓
2-azure-subscription-select
  ↓
3-azure-resource-scan
  ↓
4-azure-channel-detect (fast, resource-based)
  ↓
7-azure-report-generate (limited data)
```

### ACS-Specific Workflow (Automated)
```
8-acs-deprecation-scan (orchestrates all steps automatically)
```

## Usage Examples

### Example 1: Full ACS Analysis with Metrics
```
User: "Check my Azure authentication"
Claude: [Runs 1-azure-auth-check]

User: "Select my Production subscription"
Claude: [Runs 2-azure-subscription-select]

User: "Scan for Azure Communication Services resources"
Claude: [Runs 3-azure-resource-scan]

User: "Collect usage metrics over 90 days"
Claude: [Runs 5-azure-metrics-collect]

User: "Analyze the impact and prioritize"
Claude: [Runs 6-azure-impact-analyze]

User: "Generate a report with all formats"
Claude: [Runs 7-azure-report-generate]
```

### Example 2: Quick Storage Account Check
```
User: "Check my auth and scan for Storage Accounts"
Claude: [Runs 1-azure-auth-check, then 3-azure-resource-scan]

User: "Do a quick feature detection"
Claude: [Runs 4-azure-channel-detect]

User: "Export to CSV"
Claude: [Runs 7-azure-report-generate]
```

### Example 3: Automated ACS Scan
```
User: "Scan my subscription for ACS deprecations"
Claude: [Runs 8-acs-deprecation-scan - orchestrates entire workflow]
```

## Invoking Skills

### Automatic Invocation
Claude will automatically use relevant skills when you ask questions that match their descriptions:
- "Check my Azure authentication" → Triggers **1-azure-auth-check**
- "Scan for Storage Accounts" → Triggers **3-azure-resource-scan**

### Manual Invocation
Use slash commands to invoke skills directly:
```
/1-azure-auth-check
/2-azure-subscription-select
/3-azure-resource-scan
/5-azure-metrics-collect
/6-azure-impact-analyze
/7-azure-report-generate
/8-acs-deprecation-scan
```

### With Arguments
Some skills accept arguments:
```
/3-azure-resource-scan Microsoft.Communication/CommunicationServices
/5-azure-metrics-collect --lookback 93
```

## Generic Design

All skills (except `8-acs-deprecation-scan`) are **product-agnostic** and work with any Azure service:

✅ **Supported Azure Products:**
- Azure Communication Services
- Storage Accounts
- SQL Databases
- Virtual Machines
- App Services
- API Management
- Cosmos DB
- Any Azure resource type

**How it works:**
1. **3-azure-resource-scan** prompts you to select the Azure product
2. Subsequent skills adapt based on resource type
3. Predefined configurations for common products (ACS, Storage, SQL)
4. Custom configurations for any Azure resource type

## Key Features

### 🔄 State Management
Skills pass state between each other via session variables:
- **1-azure-auth-check** saves authentication context
- **2-azure-subscription-select** saves selected subscriptions
- **3-azure-resource-scan** saves resource inventory
- **4-azure-channel-detect/metrics-collect** enriches inventory with detection results
- **6-azure-impact-analyze** adds severity and priority
- **7-azure-report-generate** exports complete dataset

### 📊 Interactive Prompts
Skills ask clarifying questions to customize behavior:
- Product selection (3-azure-resource-scan)
- Filtering options (3-azure-resource-scan)
- Lookback period (5-azure-metrics-collect)
- Severity rules (6-azure-impact-analyze)
- Report format (7-azure-report-generate)

### ⚙️ Predefined Configurations
Common Azure products have built-in detection rules:
- **ACS:** Email, SMS, Chat, Calling, Phone Numbers
- **Storage:** Blob, File, Queue, Table
- **SQL:** Databases, Elastic Pools, Firewall Rules

### 🎛️ Customization
Advanced users can define:
- Custom resource types
- Custom metrics to collect
- Custom severity thresholds
- Custom effort estimation rules

## File Locations

These skills are stored in the **project-level** skills directory:
```
.agent/skills/
├── 1-azure-auth-check/SKILL.md
├── 2-azure-subscription-select/SKILL.md
├── 3-azure-resource-scan/SKILL.md
├── 4-azure-channel-detect/SKILL.md
├── 5-azure-metrics-collect/SKILL.md
├── 6-azure-impact-analyze/SKILL.md
├── 7-azure-report-generate/SKILL.md
└── 8-acs-deprecation-scan/SKILL.md
```

**Scope:** These skills are available only in this project (ACS-Transition-Agent-v0).

To make them available across all projects, move them to:
```
~/.agent/skills/
```

## Migration from .claude/skills/ and .claude/skills/ and .github/skills/

The original `8-acs-deprecation-scan` skill was in `.claude/skills/ and .github/skills/` (incorrect location). It has been copied to `.agent/skills/` (correct location).

**Action Required:**
You can safely delete the old `.claude/skills/ and .github/skills/` directory:
```bash
rm -rf .github/skills
```

## Next Steps

1. **Test the skills:** Try invoking each skill manually to verify they work
2. **Create custom configurations:** Add predefined rules for your specific Azure products
3. **Automate workflows:** Create orchestrator skills (like `8-acs-deprecation-scan`) for your most common scenarios
4. **Share skills:** Move to `~/.agent/skills/` to use across all projects

## Reference Implementation

All skills reference the PowerShell script implementation:
```
scripts/powershell/acs-impact-assessment-tool.ps1
```

Each skill's SKILL.md file includes line number references to the relevant workflow implementation.

## Support

For questions or issues with these skills:
- Review the individual SKILL.md files for detailed workflow documentation
- Check the PowerShell script for reference implementation
- See the Claude Code documentation: https://code.claude.com/docs/en/skills

---

**Created:** 2026-02-06
**Skills Version:** 1.0
**Compatible with:** Claude Code CLI, Claude API, Claude.ai
