# Claude Context - ACS Transition Agent

This file provides context for Claude (AI assistant) about the ACS Transition Agent project, including current state, key decisions, and what to know when continuing work.

---

## Project Overview

**Name:** Azure Communication Services (ACS) Transition Agent
**Purpose:** Automated eligibility checker for retiring ACS standalone SDKs and APIs
**Current Phase:** MVP Development Planning
**Team Size:** 3 Product Managers + 1 Engineer
**Timeline:** 12 weeks to production

---

## What This Tool Does

The ACS Transition Agent is a Next.js web application that:
1. Connects to customer Azure subscriptions via Azure AD authentication
2. Scans for Azure Communication Services resources
3. Detects usage across **all retiring channels** (Email, SMS, Chat, Calling, Phone Numbers)
4. Analyzes 3 months of Azure Monitor metrics
5. Calculates severity (Critical/Warning/Info) based on retirement dates and usage
6. Provides migration guides for each channel
7. Exports results to CSV for planning

**Key Differentiator:** Complete multi-channel detection in a single scan, not just one service.

---

## Current State (as of 2026-01-28)

### ✅ What's Complete
- Full application architecture (Next.js + Azure SDKs)
- Azure AD authentication with delegated permissions
- Resource discovery using Azure Resource Manager SDK
- Metrics collection using Azure Monitor SDK
- Detection logic for all 5 retiring channels
- Eligibility checker with severity calculation
- Results display UI component
- CSV and Markdown export functionality
- **Email Service migration guide** (comprehensive, M365 HVE only - policy compliant)
- **PowerShell impact assessment tool** (acs-impact-assessment-tool.ps1)
  - Multi-subscription scanning support
  - Optional metrics retrieval
  - Comprehensive README documentation
- API endpoint for serving migration guides
- Complete documentation:
  - README.md (product vision)
  - PRESENTATION-NOTES.md (v-team talking points)
  - MVP-SCOPE.md (12-week plan)
  - INTEGRATION-SUMMARY.md (technical integration details)
  - CONVERSATION-NOTES.md (full project history with change log)
  - claude.md (this file)
  - ACS-IMPACT-ASSESSMENT-README.md (PowerShell tool docs)
- **All code committed and pushed to GitHub**

### ⏳ What's Pending (MVP Work)
- **4 more migration guides** (SMS, Chat, Calling, Phone Numbers) - Use Email guide as template
- UI polish and refinements
- Internal testing with sample subscriptions
- Customer pilot (5-10 friendly customers)
- Production deployment

### ⚠️ Known Technical Debt
**SendGrid Cleanup Required** in `src/config/retiring-features.ts` (lines 231-260):
- Remove SendGrid references from Email service configuration
- Update to Microsoft 365 HVE only (policy compliance)
- Affects: title, description, alternativeSolution, steps, integratedScenarios

---

## Key Architecture Decisions

### 1. All Channels in MVP (Not Just Email)
**Why:**
- Same detection infrastructure (just different metric names)
- Configuration-driven (adding channels = config entries)
- Only +1 week engineering effort for 4 additional channels
- 60%+ of customers use multiple ACS services
- Complete picture = 5x more value than partial scan

**Trade-off:** Single subscription scanning (not multi-sub) to keep scope manageable

### 2. No Database/Persistent Storage
**Why:**
- Reduces complexity and security concerns
- Runtime analysis only (fetch metrics on-demand)
- No customer data stored
- Simplifies MVP delivery

### 3. Policy Compliance: Microsoft First-Party Only
**Critical:** Cannot recommend third-party Azure Marketplace partners (e.g., SendGrid)
- Only Microsoft 365 solutions in migration guides
- SendGrid references must be removed from code

### 4. CSV Export Only (Not Markdown) for MVP
**Why:** Customers know Excel, simpler than formatted reports

### 5. Static Migration Guides (5 Guides)
**Why:** Content changes slowly, no need for dynamic generation

---

## Technology Stack

### Frontend
- Next.js 14 with React 18
- TypeScript
- Tailwind CSS
- MSAL.js for Azure AD authentication

### Backend
- Next.js API Routes (serverless)
- Azure SDKs:
  - `@azure/arm-communication` (resource discovery)
  - `@azure/arm-monitor` (metrics collection)
  - `@azure/identity` (authentication)

### Deployment
- Azure Static Web Apps (recommended for MVP)
- Minimal infrastructure (<$1K/year)

---

## File Structure (Key Files)

```
src/
├── types/index.ts                    # TypeScript type definitions
├── config/retiring-features.ts       # Retiring features catalog (⚠️ SendGrid cleanup needed)
├── lib/
│   ├── azure/
│   │   ├── client.ts                # Azure client initialization
│   │   └── scanner.ts               # Resource & metrics scanning
│   ├── eligibility/checker.ts       # Eligibility matching logic
│   └── report/generator.ts          # CSV/Markdown export
├── app/
│   ├── api/
│   │   ├── scan/route.ts           # Scan API endpoint
│   │   └── migration-guide/[featureId]/route.ts  # Migration guide API
│   └── components/
│       ├── Scanner.tsx              # Scan UI
│       └── Results.tsx              # Results display
└── auth/
    ├── auth-config.ts               # Azure AD config
    ├── AuthProvider.tsx             # Auth context provider
    └── useAuth.ts                   # Auth React hook

migration-guides/
├── email-service-migration.md       # Standard markdown
└── email-service-migration.wiki.md  # Azure DevOps wiki format

Documentation:
├── README.md                        # Product vision, setup instructions
├── PRESENTATION-NOTES.md            # V-team 1-pager
├── MVP-SCOPE.md                     # 12-week plan with 3 PMs + 1 engineer
├── INTEGRATION-SUMMARY.md           # Technical integration details
├── CONVERSATION-NOTES.md            # Full project history
└── claude.md                        # This file
```

---

## Retiring Features Configuration

**File:** `src/config/retiring-features.ts`

### Structure:
```typescript
interface RetiringFeature {
  id: string;
  name: string;
  category: 'sdk' | 'api' | 'service';
  description: string;
  retirementDate: string;
  detectionCriteria: {
    metricNames?: string[];
    sdkPatterns?: string[];
    apiEndpoints?: string[];
  };
  migrationPath: {
    title: string;
    description: string;
    documentationUrl: string;
    alternativeSolution: string;
    estimatedEffort: 'low' | 'medium' | 'high';
    steps: string[];
  };
  integratedScenarios?: Array<{
    name: string;
    description: string;
    benefitsOverStandalone: string[];
    documentationUrl: string;
  }>;
}
```

### Current Retiring Features:
1. **Email Service** (`acs-email-service`) - Retirement: 2027-12-31, Effort: HIGH
2. **Calling SDK** (`acs-calling-sdk-standalone`) - Retirement: TBD, Effort: HIGH
3. **Chat SDK** (`acs-chat-sdk-standalone`) - Retirement: TBD, Effort: MEDIUM
4. **SMS API** (`acs-sms-api`) - Retirement: TBD, Effort: MEDIUM
5. **Phone Numbers SDK** (`acs-phone-numbers-sdk`) - Retirement: TBD, Effort: LOW

---

## Azure Monitor Metrics

**File:** `src/app/api/scan/route.ts`

All metrics collected during scan:
```javascript
const allMetricNames = [
  // Calling
  'CallDuration',
  'CallCount',
  'ParticipantCount',
  // Chat
  'ChatMessageCount',
  'ChatThreadCount',
  'ActiveChatUsers',
  // SMS
  'SMSMessagesSent',
  'SMSMessagesReceived',
  // Phone Numbers
  'PhoneNumberOperations',
  // Email
  'EmailMessagesSent',
  'EmailDeliveryAttempts',
  'EmailOperations',
];
```

---

## Severity Classification Algorithm

**File:** `src/lib/eligibility/checker.ts`

Logic per channel:
```
CRITICAL if:
  - Retirement date < 6 months AND high usage
  - OR retirement date < 3 months

WARNING if:
  - Retirement date < 9 months
  - OR moderate usage

INFO otherwise
```

**Usage Thresholds:**
- Email: High = >1000, Moderate = >100
- SMS: High = >500, Moderate = >50
- Chat: High = >10000, Moderate = >1000
- Calling: High = >500, Moderate = >50
- Phone Numbers: Any usage = INFO

---

## Migration Guide Template

**Reference:** Use `migration-guides/email-service-migration.md` as template

**Required Sections:**
1. Executive Summary
2. Prerequisites
3. Migration Path Overview
4. Step-by-Step Instructions
5. Code Examples (TypeScript, C#)
6. Testing Strategy
7. FAQ

**Policy Requirement:** Microsoft first-party solutions only (no third-party marketplace partners)

---

## MVP Roadmap (12 Weeks)

| Weeks | Phase | Key Deliverables |
|-------|-------|-----------------|
| 1-2 | Setup | Requirements doc, dev environment, Azure AD, Next.js |
| 3-5 | Core Scanning | Auth, scanner, ARM/Monitor SDKs, basic UI |
| 6-8 | Detection & Results | All channels, severity calc, results UI, CSV export, **5 migration guides** |
| 9-10 | Testing | Internal testing, bug fixes, docs, security review |
| 11-12 | Launch | Staging deploy, customer pilot, production launch |

**Team:**
- **PM 1 (Lead):** Requirements, customer validation, stakeholder comms
- **PM 2 (Technical):** Migration guide content, documentation
- **PM 3 (GTM):** Launch planning, M365 collaboration
- **Engineer:** Full MVP implementation

---

## Phase 2 & 3 Roadmap

### Phase 2 (3-6 months):
- Multi-subscription scanning (most customer-requested)
- Tenant-wide visibility
- Enhanced reporting

### Phase 3 (6-12 months):
- **M365 license tracking** integration (requires M365 telemetry team)
- Revenue attribution dashboard (track Email → M365 HVE conversions)
- Partner portal
- Cost calculator

---

## Important Context for Claude

### When Working on This Project:

1. **Policy Compliance is Critical:**
   - Never suggest third-party marketplace partners
   - Only recommend Microsoft first-party solutions
   - SendGrid references must be removed

2. **All Channels Matter:**
   - Don't suggest "just do Email first"
   - The architecture is configuration-driven
   - Adding channels is minimal work

3. **Keep MVP Simple:**
   - No database
   - Single subscription only
   - CSV export only (not complex reports)
   - Static migration guides

4. **Team Constraints:**
   - Only 1 engineer - keep implementation realistic
   - 3 PMs can handle content, testing, docs
   - 12 weeks total - no scope creep

5. **M365 Revenue Attribution:**
   - Phase 3 feature (not MVP)
   - Requires M365 team integration
   - Key ROI metric for tool

### Common Questions to Expect:

**Q: "Why not start with just Email?"**
A: 60%+ of customers use multiple services. Same detection infrastructure. Only +1 week engineering for 4 more channels. Complete picture = 5x more valuable.

**Q: "Why not multi-subscription in MVP?"**
A: Keep scope manageable for 1 engineer. 80% of customers scan 1-3 subs. Validate single-sub first, add multi-sub in Phase 2 based on demand.

**Q: "Why CSV only?"**
A: Customers know Excel. Markdown reports are nice-to-have. Simpler for MVP.

---

## Testing Instructions

```bash
# Run development server
npm run dev

# Open http://localhost:3000

# Test flow:
1. Sign in with Azure AD
2. Select subscription
3. Scan for ACS resources
4. Verify all channels detected
5. Check severity calculations
6. Export to CSV
7. View migration guides
```

---

## Success Metrics (First 3 Months)

- 100+ scans performed
- 50+ customers discover retiring services
- Channel usage data (which services most used?)
- 20+ customers begin migration planning
- <10 support tickets/month

---

## Quick Reference Commands

```bash
# Install dependencies
npm install

# Run development
npm run dev

# Build for production
npm run build

# Deploy to Azure Static Web Apps
az staticwebapp create --name acs-transition-agent ...
```

---

## Key Contacts & Resources

- **Product Vision:** See README.md
- **V-Team Presentation:** See PRESENTATION-NOTES.md
- **MVP Plan:** See MVP-SCOPE.md
- **Full History:** See CONVERSATION-NOTES.md
- **Technical Integration:** See INTEGRATION-SUMMARY.md

---

## Last Updated

**Date:** 2026-01-28
**Updated By:** Claude (AI Assistant)
**Changes:**
- Added PowerShell impact assessment tool and documentation
- Fixed Unicode parse errors in PowerShell script (commit: 5b41a12)
- Added Azure PowerShell module compatibility troubleshooting to README
- Updated current state with latest completions
- All changes committed and pushed to GitHub

---

**Note to Claude:** When continuing work on this project, always check this file first for current context, then review CONVERSATION-NOTES.md for detailed history. Keep this file updated as the project evolves.
