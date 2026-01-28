# ACS Transition Agent - AI-Powered Web Application

**Status:** 🔮 Future Development (Phase 2+)

This folder will contain an AI-powered web application that provides an interactive, user-friendly interface for assessing ACS resource retirement impact and guiding migrations.

---

## Planned Features

### Phase 1 - MVP (Future)
- **Azure AD Authentication** - Secure, delegated access to customer subscriptions
- **Interactive Subscription Scanner** - Web-based UI for resource discovery
- **All Channel Detection** - Email, SMS, Chat, Calling, Phone Numbers
- **Azure Monitor Integration** - Real-time usage metrics (3-month lookback)
- **Severity Ratings** - Critical/Warning/Info classifications
- **Embedded Migration Guides** - In-app step-by-step guidance
- **CSV Export** - Exportable reports for planning

### Phase 2 - Scale (3-6 months after MVP)
- **Multi-Subscription Scanning** - Tenant-wide visibility
- **Batch Processing** - Scan multiple subscriptions in parallel
- **Enhanced Reporting** - Dashboard analytics and trends

### Phase 3 - Intelligence (6-12 months)
- **M365 License Tracking** - Monitor HVE license deployments
- **Revenue Attribution** - Track Email → M365 conversions
- **Partner Portal** - Multi-tenant management for SIs
- **Cost Calculator** - Migration cost estimation

### Phase 4 - AI-Powered (Vision)
- **Code Analysis** - GitHub integration for automated scanning
- **AI Migration Suggestions** - Intelligent code migration recommendations
- **Automated Testing** - Integrated test environments
- **Multi-Service Support** - Expand beyond ACS to other Azure deprecations

---

## Technology Stack (Planned)

### Frontend
- **Next.js 14** - React framework with SSR
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern, responsive UI
- **MSAL.js** - Azure AD authentication library

### Backend
- **Next.js API Routes** - Serverless API endpoints
- **Azure SDKs:**
  - `@azure/arm-communication` - Resource discovery
  - `@azure/arm-monitor` - Metrics collection
  - `@azure/identity` - Authentication

### Deployment
- **Azure Static Web Apps** - Minimal infrastructure (<$1K/year)
- **Global CDN** - Fast worldwide access
- **Automatic scaling** - Handle traffic spikes

---

## Why Not Build Now?

The AI-powered web application is **deferred to Phase 2** for the following reasons:

### Current Priority: PowerShell Script
- **Immediate value** - PowerShell tool provides complete functionality today
- **Multi-subscription support** - Already built into PowerShell tool
- **Enterprise-friendly** - IT pros prefer automation scripts
- **No UI complexity** - Focus on core detection logic first

### Validation First
- **Prove demand** - Validate customer need before investing in web UI
- **Gather feedback** - Learn from PowerShell tool usage
- **Refine detection logic** - Perfect the scanning algorithm
- **Inform UI design** - Understand customer workflows

### Team Constraints
- **Small team** - 3 PMs + 1 engineer focused on guides and scripts
- **12-week MVP** - PowerShell + guides deliverable in timeline
- **Scope management** - Web app = +6-8 weeks of development

---

## Current Alternatives

While the web application is under development, use these tools:

### For Automated Scanning
- **[PowerShell Script](../scripts/powershell/)** - Full-featured multi-subscription scanner
  - Same detection capabilities as planned web app
  - Faster to run (no UI overhead)
  - CSV export for reporting

### For Migration Guidance
- **[Migration Guides](../migration-guides/)** - Step-by-step documentation
  - Complete code examples
  - Testing strategies
  - FAQ and troubleshooting

---

## Development Timeline (Estimated)

| Phase | Timeline | Status |
|-------|----------|--------|
| **PowerShell Tool** | Current | ✅ Complete |
| **Migration Guides** | Current | 🚧 1 of 5 complete |
| **Web App MVP** | +3 months | 📅 Planned |
| **Multi-Sub Scanning** | +6 months | 📅 Planned |
| **M365 Tracking** | +12 months | 📅 Planned |

---

## Why Build This Eventually?

The web application will provide value that scripts cannot:

### User Experience
- **Visual interface** - Intuitive for non-technical users
- **Interactive exploration** - Drill down into resources
- **Real-time progress** - Live scanning status

### Accessibility
- **No PowerShell required** - Broader audience reach
- **Cross-platform** - Works on any device with a browser
- **No local setup** - No modules to install

### Advanced Features
- **Historical tracking** - Compare scans over time
- **Team collaboration** - Share results with stakeholders
- **Integrated guidance** - Migration guides embedded in the flow

---

## Stay Updated

This folder will be populated when Phase 2 development begins. Check back for:
- Architecture documentation
- Setup instructions
- Contribution guidelines
- Deployment guide

---

## Related Resources

- **Current Tools:** [Scripts](../scripts/) | [Migration Guides](../migration-guides/)
- **Project Docs:** [MVP Scope](../docs/MVP-SCOPE.md) | [Roadmap](../docs/PRESENTATION-NOTES.md)

---

**Last Updated:** 2026-01-28
**Status:** Planning Phase
**Maintained By:** ACS Transition Agent Team
