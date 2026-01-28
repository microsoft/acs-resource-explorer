# Azure Communication Services Transition Agent

**A comprehensive suite of tools to help customers migrate from retiring ACS standalone SDKs to integrated Microsoft 365 solutions.**

---

## Overview

The **ACS Transition Agent** is a collection of assessment tools, migration guides, and future AI-powered applications designed to simplify the transition from retiring Azure Communication Services (ACS) standalone features to integrated Microsoft 365 scenarios.

###  Components

| Component | Status | Description |
|-----------|--------|-------------|
| **[Assessment Scripts](scripts/)** | ✅ Available | PowerShell tools for scanning Azure subscriptions and detecting retiring service usage |
| **[Migration Guides](migration-guides/)** | 🚧 In Progress | Step-by-step documentation for migrating each retiring service (1 of 5 complete) |
| **[AI Agent Application](ai-agent/)** | 📅 Planned | Interactive web application with guided migrations (Phase 2+) |

---

## Quick Start

### Option 1: Automated Assessment (PowerShell)

**Best for:** IT professionals, partners managing multiple customers, bulk assessments

```powershell
# Navigate to the PowerShell script directory
cd scripts/powershell

# Run a quick scan (all subscriptions, no metrics)
.\acs-impact-assessment-tool.ps1

# Run with detailed usage metrics
.\acs-impact-assessment-tool.ps1 -IncludeMetrics
```

**Features:**
- ✅ Multi-subscription scanning
- ✅ Detects all 5 retiring channels (Email, SMS, Chat, Calling, Phone Numbers)
- ✅ Optional Azure Monitor metrics (90-day lookback)
- ✅ Severity calculation (Critical/Warning/Info)
- ✅ CSV export for planning and tracking

[**Full PowerShell Documentation →**](scripts/powershell/README.md)

---

### Option 2: Manual Migration Guides

**Best for:** Developers implementing migrations, understanding migration paths

**Available Now:**
- **[Email Service → Microsoft 365 HVE](migration-guides/email/)** - Complete guide with code examples

**Coming Soon:**
- SMS API migration (alternative providers)
- Chat SDK → Teams integration
- Calling SDK → Teams Calling
- Phone Numbers SDK → Azure Portal management

[**Browse All Migration Guides →**](migration-guides/README.md)

---

### Option 3: AI-Powered Web Application (Future)

**Best for:** Non-technical users, interactive exploration, team collaboration

**Status:** Phase 2 development (planned for Q2 2026)

**Planned Features:**
- Interactive web UI with Azure AD authentication
- Real-time subscription scanning
- Embedded migration guidance
- Multi-subscription dashboard
- M365 license tracking

[**Learn More About the AI Agent →**](ai-agent/README.md)

---

## The Problem We're Solving

### Navigating Service Deprecation at Scale

Azure Communication Services (ACS) is evolving from standalone SDKs and APIs toward integrated scenarios with Microsoft Teams. While this transition unlocks powerful new capabilities, it creates a complex migration challenge:

**Customer Challenges:**
- "Which retiring services am I using?"
- "How heavily do I rely on each service?"
- "What's my migration timeline and effort?"
- "Where do I start?"

**Partner Challenges:**
- "Which of my customers are impacted?"
- "How do I scope migration projects across my portfolio?"
- "What's my service opportunity pipeline?"

**Microsoft Team Challenges:**
- "How many customers are affected by each retirement?"
- "Which services have the highest usage?"
- "How do we track migration progress?"

---

## The Solution: Multi-Tool Approach

The ACS Transition Agent provides **three complementary tools** that work together:

### 1. Assessment Scripts → Discovery
**Purpose:** Find out what's retiring in your Azure subscriptions

**Tools:**
- PowerShell impact assessment tool (multi-subscription scanning)
- Python scripts (planned - cross-platform support)
- Azure CLI scripts (planned - alternative method)

**Output:** CSV reports with detected resources, usage metrics, and severity ratings

---

### 2. Migration Guides → Implementation
**Purpose:** Step-by-step instructions for migrating each service

**Content:**
- Executive summaries and prerequisites
- Detailed migration paths
- Code examples (TypeScript, C#, Python)
- Testing strategies
- FAQ and troubleshooting

**Coverage:** All 5 retiring services (Email, SMS, Chat, Calling, Phone Numbers)

---

### 3. AI Agent Application → Guided Experience
**Purpose:** Interactive, user-friendly interface for non-technical users

**Capabilities:**
- Visual subscription scanning
- Real-time progress tracking
- Embedded migration guidance
- Team collaboration features
- Historical tracking and reporting

**Status:** Phase 2 (planned after validating scripts and guides)

---

## Value Proposition by Persona

### For Customers

**Problem**: "I'm not sure if my application uses any retiring features, or how urgently I need to migrate."

**Value Delivered**:
- **Zero Manual Audit**: Automated discovery eliminates guesswork and manual code reviews
- **Risk Clarity**: Understand exactly which features are at risk and when
- **Effort Estimation**: Get realistic migration effort estimates before starting
- **Prioritization**: Focus on critical items first with severity-based rankings
- **Confidence**: Make informed decisions about migration timing and resource allocation

**Example Scenario**:
A healthcare SaaS company scans their Azure subscription with the PowerShell tool and discovers:
- 3 ACS resources using multiple retiring channels:
  - **Calling SDK**: 45,000 calls in last 3 months → Critical priority
  - **Chat SDK**: 12,000 chat messages → Warning
  - **SMS**: 3,500 messages → Info
- They download 3 migration guides (Calling, Chat, SMS) and create a phased migration plan

---

### For Microsoft Partners

**Problem**: "We support dozens of customers using ACS. We need a systematic way to assess impact across our entire customer base."

**Value Delivered**:
- **Portfolio Visibility**: Run PowerShell script across all customer tenants
- **Customer Prioritization**: Identify which customers need immediate attention
- **Scoped Engagements**: Present data-driven migration proposals with accurate effort estimates
- **Proactive Service**: Contact customers before they experience service disruption
- **Competitive Advantage**: Demonstrate expertise in Azure migration and modernization

**Example Scenario**:
A Microsoft partner runs the assessment tool for 20 enterprise customers and generates portfolio reports showing:
- 12 of 20 customers are impacted across multiple channels
- Email service most widely used (10 customers), followed by SMS (7 customers)
- 4 customers have critical-severity issues (retirement within 6 months)
- Total estimated migration effort: 240 hours across portfolio
- They proactively reach out with scoped SOWs for each customer

---

### For Microsoft (Support, Engineering, Product Teams)

**Problem**: "We need to understand customer impact, prioritize support resources, and track migration progress at scale."

**Value Delivered**:
- **Impact Metrics**: Aggregate data on how many customers are affected by each retiring feature
- **Usage Patterns**: Understand which features are most actively used to inform deprecation timelines
- **Early Warning System**: Identify customers at risk of service disruption
- **Resource Allocation**: Direct support resources to customers with critical-severity impacts
- **Migration Tracking**: Monitor adoption of integrated scenarios over time

**Example Scenario**:
The ACS product team aggregates assessment data across customers and discovers:
- **Email**: 1,200 customers (most widely used), 85% have >1,000 emails/month
- **SMS**: 950 customers, 60% moderate usage
- **Calling**: 420 customers (mostly telehealth and customer support)
- This data informs decisions to prioritize Email → M365 HVE migration support

---

## Key Differentiators

### 1. Multi-Channel Detection
Unlike single-service scanners, the ACS Transition Agent detects **all 5 retiring channels** in a single scan:
- Email Service
- SMS API
- Chat SDK
- Calling SDK
- Phone Numbers SDK

### 2. Complete Tool Suite
Provides multiple ways to assess and migrate:
- **Scripts** for automation and bulk operations
- **Guides** for implementation details
- **AI Agent** (future) for interactive guidance

### 3. Usage-Based Prioritization
Not just "yes/no" detection - quantifies actual usage:
- 90-day metrics from Azure Monitor
- Severity ratings based on retirement timelines
- Migration effort estimates (Low/Medium/High)

### 4. Microsoft First-Party Only
All migration paths use Microsoft solutions:
- Email → Microsoft 365 High-Volume Email (HVE)
- Chat/Calling → Teams integration
- Policy compliant (no third-party marketplace partners)

---

## Roadmap

### Phase 1 - Current (Available Now)
✅ **PowerShell assessment tool** with multi-subscription scanning
✅ **Email migration guide** (comprehensive, M365 HVE only)
🚧 **4 additional migration guides** (SMS, Chat, Calling, Phone Numbers) - In development

### Phase 2 - Scale (3-6 months)
📅 **AI-powered web application** with interactive UI
📅 **Enhanced reporting** and analytics
📅 **Multi-subscription dashboard**

### Phase 3 - Intelligence (6-12 months)
📅 **M365 license tracking** integration
📅 **Revenue attribution** (Email → M365 HVE conversions)
📅 **Partner portal** for multi-tenant management
📅 **Cost calculator** for migration alternatives

### Phase 4 - AI-Powered (Vision)
📅 **Automated code analysis** (GitHub integration)
📅 **AI migration suggestions**
📅 **Integrated testing environments**
📅 **Expand to other Azure service deprecations** (reusable pattern)

---

## Project Structure

```
ACS-Transition-Agent-v0/
├── README.md                      # This file - project overview
├── .gitignore
│
├── docs/                          # Project documentation
│   ├── PRESENTATION-NOTES.md      # V-team talking points
│   ├── MVP-SCOPE.md               # 12-week development plan
│   ├── INTEGRATION-SUMMARY.md     # Technical integration details
│   ├── CONVERSATION-NOTES.md      # Full project history
│   └── claude.md                  # AI assistant context
│
├── scripts/                       # Assessment & automation scripts
│   ├── README.md                  # Scripts index
│   └── powershell/
│       ├── README.md              # PowerShell tool documentation
│       └── acs-impact-assessment-tool.ps1
│
├── migration-guides/              # Step-by-step migration documentation
│   ├── README.md                  # Guides index
│   └── email/
│       ├── email-service-migration.md
│       └── email-service-migration.wiki.md
│
└── ai-agent/                      # AI-powered web application (future)
    └── README.md                  # AI agent roadmap and features
```

---

## Getting Started

### Prerequisites

**For PowerShell Scripts:**
- PowerShell 5.1 or later
- Azure PowerShell module (`Az`)
- Azure account with Reader permissions on subscriptions

**For Migration Guides:**
- Access to Azure subscription
- Understanding of current ACS implementation
- Development environment for your language (TypeScript, C#, etc.)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/ACS-Transition-Agent-v0.git
   cd ACS-Transition-Agent-v0
   ```

2. **Choose your starting point:**
   - **Assessment:** [scripts/powershell/README.md](scripts/powershell/README.md)
   - **Migration:** [migration-guides/README.md](migration-guides/README.md)

---

## Documentation

- **[Project Vision & Scope](docs/MVP-SCOPE.md)** - Detailed 12-week plan and rationale
- **[Presentation Notes](docs/PRESENTATION-NOTES.md)** - V-team talking points
- **[Technical Integration](docs/INTEGRATION-SUMMARY.md)** - Azure SDK integration details
- **[Full Project History](docs/CONVERSATION-NOTES.md)** - Development decisions and change log

---

## Success Metrics (Target: First 3 Months)

- 100+ PowerShell scans performed
- 50+ customers discover retiring service usage
- Channel usage data collected (which services are most used?)
- 20+ customers begin migration planning
- <10 support tickets/month

---

## Contributing

We welcome feedback and contributions!

1. Test the tools with your Azure subscriptions
2. Review the migration guides
3. Document any issues or missing steps
4. Open an issue with details about your environment

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Technical questions:** Open an issue in this repository
- **Migration assistance:** Contact the ACS team or Microsoft FastTrack
- **Partner support:** Reach out to your Microsoft account team

---

**Last Updated:** 2026-01-28
**Maintained By:** ACS Transition Agent Team
**Current Phase:** Phase 1 - Scripts & Guides
