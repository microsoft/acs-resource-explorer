# Azure Communication Services Transition Agent

## Product Vision

### The Problem: Navigating Service Deprecation at Scale

Azure Communication Services (ACS) is evolving from standalone SDKs and APIs toward integrated scenarios with Microsoft Teams. While this transition unlocks powerful new capabilities, it creates a complex migration challenge for customers, partners, and Microsoft teams alike.

**The Challenge:**
- Customers using ACS standalone features need to understand if and how the deprecation affects them
- Many customers don't know which specific features they're using or how heavily they rely on them
- Migration guidance exists but customers must manually assess their eligibility and relevance
- Partners supporting customers need a systematic way to evaluate migration scope across portfolios
- Microsoft support and engineering teams need visibility into customer impact for prioritization

**The Opportunity:**
An intelligent, automated eligibility checker can transform the deprecation experience from reactive and uncertain to proactive and clear, benefiting all personas in the ecosystem.

---

## Solution: Automated Transition Intelligence

The **ACS Transition Agent** is a web-based tool that connects directly to customer Azure subscriptions to automatically:

1. **Discover** all Azure Communication Services resources in a subscription
2. **Detect** usage across all retiring channels (Email, SMS, Chat, Calling, Phone Numbers)
3. **Analyze** actual usage patterns through Azure Monitor metrics (3-month lookback)
4. **Match** detected usage against the catalog of retiring features
5. **Prioritize** migration efforts based on retirement timelines and usage intensity
6. **Guide** customers to appropriate migration paths with detailed step-by-step guides

### How It Works

```
Customer Login (Azure AD)
    ↓
Scan Azure Subscriptions
    ↓
Discover ACS Resources
    ↓
Analyze Usage Metrics (3-month lookback)
    ↓
Match Against Retiring Features
    ↓
Generate Eligibility Report
    ↓
Present Migration Roadmap
```

The tool provides:
- **Complete Channel Detection**: Scans all retiring ACS services (Email, SMS, Chat, Calling, Phone Numbers)
- **Impact Assessment**: Clear visibility into which resources are affected per channel
- **Severity Ratings**: Critical/Warning/Info classifications based on retirement timelines
- **Usage Insights**: Quantified metrics showing actual feature utilization per channel
- **Migration Guides**: Dedicated migration guides for each retiring channel with code examples
- **CSV Export**: Exportable reports for enterprise planning and tracking

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
A healthcare SaaS company built telehealth features using multiple ACS services two years ago. They receive an email about deprecation but aren't sure which features they're using. They log into the Transition Agent, scan their subscription, and discover:
- 3 ACS resources using multiple retiring channels:
  - **Calling SDK**: 45,000 calls in last 3 months (high usage → critical priority)
  - **Chat SDK**: 12,000 chat messages (moderate usage → warning)
  - **SMS**: 3,500 messages (low usage → info)
- Retirement dates vary by service
- Estimated migration effort: High (4-6 sprints for multi-channel migration)
- Direct links to 3 separate migration guides (Calling → Teams, Chat → Teams, SMS → alternatives)

Now they can confidently plan their multi-channel migration roadmap and budget accordingly.

---

### For Microsoft Partners

**Problem**: "We support dozens of customers using ACS. We need a systematic way to assess impact across our entire customer base."

**Value Delivered**:
- **Portfolio Visibility**: Scan multiple customer tenants to understand aggregate exposure
- **Customer Prioritization**: Identify which customers need immediate attention
- **Scoped Engagements**: Present data-driven migration proposals with accurate effort estimates
- **Proactive Service**: Contact customers before they experience service disruption
- **Competitive Advantage**: Demonstrate expertise in Azure migration and modernization

**Example Scenario**:
A Microsoft partner manages ACS implementations for 20 enterprise customers. They run the Transition Agent for each customer subscription and generate portfolio reports showing:
- 12 of 20 customers are impacted across multiple channels
- Email service most widely used (10 customers), followed by SMS (7 customers)
- 4 customers have critical-severity issues (retirement within 6 months)
- Multi-channel migrations increase SOW complexity and value
- Total estimated migration effort: 240 hours across portfolio
- CSV exports for each customer enable detailed scoped SOWs

The partner proactively reaches out with data-driven migration proposals, turning potential churn into a larger services engagement opportunity.

---

### For Microsoft (Support, Engineering, Product Teams)

**Problem**: "We need to understand customer impact, prioritize support resources, and track migration progress at scale."

**Value Delivered**:
- **Impact Metrics**: Aggregate data on how many customers are affected by each retiring feature
- **Usage Patterns**: Understand which features are most actively used to inform deprecation timelines
- **Early Warning System**: Identify customers at risk of service disruption
- **Resource Allocation**: Direct support resources to customers with critical-severity impacts
- **Migration Tracking**: Monitor adoption of integrated scenarios over time
- **Customer Success**: Reduce support tickets by enabling self-service impact assessment

**Example Scenario**:
The ACS product team wants to understand the impact across all retiring services. Aggregated data from the Transition Agent shows:
- **Email**: 1,200 customers (most widely used), 85% have >1,000 emails/month
- **SMS**: 950 customers, 60% moderate usage
- **Chat**: 870 customers with high message volumes
- **Calling**: 420 customers (mostly telehealth and customer support)
- **Phone Numbers SDK**: 180 customers (least used)
- 35% of customers use multiple retiring services (complex migrations)

This data informs decisions to:
1. Prioritize Email → M365 HVE migration support (highest impact)
2. Track M365 license conversions from Email migrations (revenue attribution)
3. Extend SMS timeline due to high adoption
4. Create combo migration guides for multi-service customers
5. Allocate FastTrack resources based on channel usage patterns

---

## Key Differentiators

### 1. Automated Discovery
Unlike manual checklists or documentation, the tool **actively scans** Azure environments to discover actual resource usage.

### 2. Usage-Based Assessment
Goes beyond "do you use this SDK?" to **"how much do you use it?"** with quantified metrics from Azure Monitor.

### 3. Intelligent Prioritization
Combines retirement timelines, usage intensity, and migration complexity to calculate **severity and effort**.

### 4. Actionable Guidance
Doesn't just identify problems—provides **specific migration paths** and links to documentation for each impacted feature.

### 5. Integrated Scenarios Promotion
Actively showcases the **benefits of Teams integration**, turning deprecation into an opportunity to adopt enhanced capabilities.

---

## Success Metrics

### Customer Success
- **Reduction in support tickets** related to deprecation confusion
- **Faster migration completion** rates
- **Higher satisfaction scores** during deprecation lifecycle

### Business Impact
- **Increased adoption** of integrated Teams scenarios
- **Reduced customer churn** during transition period
- **Higher partner engagement** in migration services

### Operational Efficiency
- **Decreased support burden** through self-service assessment
- **Better resource allocation** based on impact data
- **Improved deprecation communication** with personalized insights

---

## Roadmap Vision

### Phase 1 - MVP (Current - 12 weeks)
**Team:** 3 Product Managers + 1 Engineer

- Azure AD authentication
- Single subscription scanning
- **All channel detection** (Email, SMS, Chat, Calling, Phone Numbers)
- Azure Monitor metrics analysis (3-month lookback)
- Severity calculation and eligibility reporting
- **5 migration guides** (one per channel) with code examples
- CSV export for enterprise planning

### Phase 2: Scale & Multi-Subscription (3-6 months)
- Multi-subscription scanning (most customer-requested)
- Tenant-wide visibility
- Enhanced reporting and analytics
- Batch CSV exports across subscriptions

### Phase 3: M365 Revenue Attribution (6-12 months)
- **M365 license tracking integration** with telemetry team
- Revenue attribution dashboard (track Email → M365 HVE conversions)
- ROI metrics for tool investment
- Cost calculator for migration alternatives
- Partner portal for SI access

### Phase 4: AI-Powered Migration (Vision)
- Automated code analysis (GitHub integration)
- AI-powered code migration suggestions
- Integrated testing environments
- Expanded to other Azure service deprecations (reusable pattern)

---

## Getting Started

See the [Setup Instructions](#setup-instructions) below to deploy the ACS Transition Agent in your environment.

---

## Technical Architecture

### Frontend
- **Framework**: Next.js 14 with React 18
- **Authentication**: Azure AD (MSAL.js)
- **Styling**: Tailwind CSS
- **Deployment**: Azure Static Web Apps or App Service

### Backend
- **API**: Next.js API Routes (serverless functions)
- **Azure SDK**: @azure/arm-communication, @azure/arm-monitor
- **Authentication**: Azure AD token-based (delegated permissions)

### Data Flow
1. User authenticates with Azure AD
2. Frontend acquires access token with Azure Management API scope
3. API routes use token to query Azure Resource Manager
4. Scanner discovers ACS resources and queries Azure Monitor metrics
5. Eligibility checker matches usage against retiring features configuration
6. Results returned to frontend for display

### Security
- **Zero credential storage**: Uses user's Azure AD identity (no service principals stored)
- **Least privilege**: Requests only read-only permissions to Azure subscriptions
- **Token-based**: All Azure API calls use short-lived OAuth tokens
- **Client-side auth**: MSAL handles token acquisition and refresh

---

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm/yarn
- Azure subscription
- Azure AD app registration

### 1. Create Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click "New registration"
3. Name: "ACS Transition Agent"
4. Supported account types: "Accounts in this organizational directory only" (or multi-tenant if needed)
5. Redirect URI: `http://localhost:3000` (for local development)
6. Click "Register"

### 2. Configure API Permissions

1. In your app registration, go to "API permissions"
2. Click "Add a permission"
3. Select "Azure Service Management"
4. Check "user_impersonation"
5. Click "Add permissions"
6. Click "Grant admin consent" (requires Azure AD admin)

### 3. Note Your Configuration

Copy these values from your app registration:
- **Application (client) ID**
- **Directory (tenant) ID**

### 4. Install Dependencies

```bash
npm install
```

### 5. Configure Environment

Copy `.env.local.example` to `.env.local` and fill in your values:

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```
AZURE_CLIENT_ID=your-client-id-here
AZURE_TENANT_ID=your-tenant-id-here
NEXT_PUBLIC_REDIRECT_URI=http://localhost:3000
```

### 6. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 7. Usage

1. Click "Sign In with Microsoft"
2. Grant permissions when prompted
3. Click "Scan My Subscriptions"
4. Review the eligibility report
5. Follow migration guidance for impacted resources

---

## Deployment

### Deploy to Azure Static Web Apps

```bash
# Install Azure CLI
az login

# Create resource group
az group create --name acs-transition-agent --location eastus

# Create static web app
az staticwebapp create \
  --name acs-transition-agent \
  --resource-group acs-transition-agent \
  --source https://github.com/yourusername/acs-transition-agent \
  --location eastus \
  --branch main \
  --app-location "/" \
  --output-location ".next"
```

Update your Azure AD app registration redirect URI to include your production URL.

---

## Configuration

### Adding New Retiring Features

Edit `src/config/retiring-features.ts` to add new features to the retirement catalog:

```typescript
{
  id: 'feature-id',
  name: 'Feature Name',
  category: 'sdk' | 'api' | 'service',
  description: 'Description of what is retiring',
  retirementDate: '2025-12-31',
  detectionCriteria: {
    metricNames: ['MetricName1', 'MetricName2'],
    sdkPatterns: ['@azure/package-name'],
  },
  migrationPath: {
    title: 'Migration Title',
    description: 'How to migrate',
    documentationUrl: 'https://docs.microsoft.com/...',
    alternativeSolution: 'What to use instead',
    estimatedEffort: 'low' | 'medium' | 'high',
    steps: ['Step 1', 'Step 2', '...'],
  },
}
```

---

## Contributing

This is a POC (Proof of Concept) for the ACS Transition Agent. Contributions and feedback are welcome!

---

## License

MIT License - See LICENSE file for details

---

## Support

For questions or issues, please contact the ACS team or open an issue in this repository.
