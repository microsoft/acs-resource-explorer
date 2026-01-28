# ACS Transition Agent - MVP Scope
## Realistic Delivery for Small Team (3 PMs + 1 Engineer)

---

## Executive Summary

**Goal:** Launch a basic but functional ACS Transition Agent that delivers immediate value with minimal complexity.

**Team:** 3 Product Managers + 1 Engineer
**Timeline:** 8-12 weeks to production
**Approach:** Start simple, validate with customers, iterate based on feedback

---

## What We're Building (MVP)

### Core Functionality Only

**1. Basic Resource Scanner**
- Scan a single Azure subscription at a time (no multi-subscription initially)
- Detect ACS Communication Services resources using Azure Resource Manager API
- Simple web interface with Azure AD sign-in
- **Complexity:** Low - Use existing Azure SDKs

**2. All ACS Channel Detection (Email, SMS, Chat, Calling, Phone Numbers)**
- Detect usage across ALL retiring ACS services
- Check for metrics across all channels:
  - **Email:** EmailMessagesSent, EmailDeliveryAttempts, EmailOperations
  - **SMS:** SMSMessagesSent, SMSMessagesReceived
  - **Chat:** ChatMessageCount, ChatThreadCount, ActiveChatUsers
  - **Calling:** CallDuration, CallCount, ParticipantCount
  - **Phone Numbers:** PhoneNumberOperations
- Display all impacted channels per resource with retirement dates
- **Why all channels:** Customers often use multiple ACS services - need complete picture

**3. Simple Results Display**
- Show list of impacted resources grouped by retiring service
- Display basic info per channel:
  - Resource name
  - Usage count per channel (Email: 1,500 emails, SMS: 200 messages, etc.)
  - Retirement date
  - Severity (Critical/Warning/Info based on timeline)
- Migration recommendation per channel with links to guides
- **No fancy dashboards** - Just a clear, organized table with key information

**4. Static Migration Guides (One per Channel)**
- **Email Service:** Comprehensive guide for Email → M365 HVE migration (already created)
- **SMS API:** Basic migration guide with alternative providers
- **Chat SDK:** Guide to Teams integration or alternatives
- **Calling SDK:** Guide to Teams Calling integration
- **Phone Numbers SDK:** Guide to Azure Portal management
- Hosted as simple documentation pages
- Code examples for TypeScript/C# (most common languages)
- **No dynamic content** - Keep it simple, reusable templates

**5. Basic Export**
- Export results to CSV only (simpler than Markdown reports)
- Contains: Resource name, Subscription, Channel (Email/SMS/Chat/Calling/Phone), Usage count, Retirement date, Severity, Migration recommendation
- One row per resource per impacted channel
- **No custom formatting** - Just raw data customers can open in Excel

---

## Why All Channels? (Complexity vs. Value)

**Isn't this too much for 1 engineer?**
No - here's why detecting all channels is not significantly more work:

### Technical Reality
- **Same Azure APIs:** All channels use the same Azure Monitor metrics API - just different metric names
- **Already built:** The codebase already has the infrastructure for multi-channel detection
- **Configuration-driven:** Adding a new channel is just adding entries to the retiring-features config file
- **Pattern reuse:** Detection logic is identical across channels (check metric > 0, calculate severity, display result)

### Work Breakdown
**For Email only:**
- Engineer: 3 weeks to build metrics collection + detection + display
- PMs: 1 week to write Email migration guide

**For All 5 channels:**
- Engineer: +1 week to add 4 more metric names and config entries (NOT 3x work)
- PMs: +2 weeks to write 4 more migration guides (can use template)

**Total additional cost:** 3 weeks of team time to get 5x the value

### Customer Reality
- **Multi-service usage is common:** Most ACS customers use 2-3 services (Email + SMS, or Chat + Calling)
- **Incomplete picture is frustrating:** Scanning only Email means customers need to manually check other services
- **Single scan expectation:** Customers expect "scan my ACS resources" to mean ALL ACS resources

### Business Value
- **Complete visibility:** Know which retiring services are most used across customer base
- **Better prioritization:** Data-driven decision on which migration guides to enhance first
- **Higher adoption:** Tool provides complete value, not partial value

**Bottom Line:** The incremental engineering cost is small, but the customer value is 5x higher.

---

## What We're NOT Building (Post-MVP)

### Features Deferred to Later Phases

❌ **Multi-subscription scanning** - Add in Phase 2 (single subscription is enough for MVP)
❌ **M365 license tracking** - Great idea but requires integration with M365 telemetry team (Phase 3)
❌ **Advanced channel-specific analytics** - Just basic usage counts for MVP
❌ **Automated migration tools** - Just guidance for now
❌ **Partner portal** - Focus on direct customers first
❌ **Advanced reporting** - CSV export is enough for MVP
❌ **Custom dashboards** - Simple table view is sufficient
❌ **Usage trend analysis** - Just current state, no historical trends
❌ **Cost calculators** - Too complex for MVP
❌ **Integration with Azure Advisor** - Future enhancement

---

## Technical Architecture (Simplified)

### Frontend
- **Next.js** - Single web application
- **Azure AD (MSAL)** - Sign-in only, minimal config
- **Simple UI** - No complex state management, basic forms and tables
- **Tailwind CSS** - Pre-built components, minimal custom styling

### Backend
- **Next.js API Routes** - No separate backend service needed
- **Azure SDK** - Resource Manager for resource discovery
- **Azure Monitor SDK** - Metrics collection
- **No database** - Everything runtime/session-based

### Deployment
- **Azure Static Web Apps** - Simplest deployment, includes Azure AD integration
- **No complex infrastructure** - Single service, auto-scaling handled by platform

### Data Storage
- **None required** - No persistent storage for MVP
- All data fetched on-demand and discarded after session
- Reduces security/compliance concerns significantly

---

## Team Roles & Responsibilities

### Product Managers (3)
**PM 1 - Product Owner/Lead**
- Define MVP requirements and priorities
- Customer validation and feedback
- Stakeholder communication (Azure/M365 teams)
- Success metrics definition

**PM 2 - Technical PM**
- Work with engineer on technical feasibility
- API/SDK selection and architecture review
- Migration guide content creation
- Documentation and user guides

**PM 3 - Go-to-Market PM**
- Customer communication strategy
- Partner enablement planning (post-MVP)
- Launch planning and rollout strategy
- M365 team collaboration for HVE guidance

### Engineer (1)
- Build entire MVP application (realistic for 8-12 weeks)
- Azure integration (ARM SDK, Monitor SDK, AD auth)
- Simple UI implementation
- Deployment and basic testing
- **Focus on working code over perfect code**

---

## Delivery Timeline (12 Weeks)

### Weeks 1-2: Setup & Planning
- [ ] Finalize MVP requirements
- [ ] Set up development environment
- [ ] Create Azure AD app registration
- [ ] Set up Next.js project structure
- [ ] **PM deliverable:** Requirements document

### Weeks 3-5: Core Scanning (Engineer Focus)
- [ ] Implement Azure AD authentication
- [ ] Build subscription scanner
- [ ] Integrate Azure Resource Manager SDK for ACS resource discovery
- [ ] Integrate Azure Monitor SDK for metrics collection
- [ ] Build basic UI for scan input
- [ ] **PM deliverable:** Start migration guide content for all channels

### Weeks 6-8: Detection & Results (Engineer Focus)
- [ ] Build detection logic for all channels (Email, SMS, Chat, Calling, Phone Numbers)
- [ ] Implement severity calculation based on retirement dates and usage
- [ ] Create results display page with channel grouping
- [ ] Implement CSV export with all channel data
- [ ] **PM deliverable:** Complete all 5 migration guides (Email, SMS, Chat, Calling, Phone Numbers)

### Weeks 9-10: Testing & Polish
- [ ] Internal testing with sample subscriptions
- [ ] Bug fixes and UI refinements
- [ ] Documentation (how to use the tool)
- [ ] Security review (basic)
- [ ] **PM deliverable:** User documentation

### Weeks 11-12: Launch Prep
- [ ] Deploy to staging environment
- [ ] Customer pilot (5-10 friendly customers)
- [ ] Gather feedback and make adjustments
- [ ] Deploy to production
- [ ] **PM deliverable:** Launch communication plan

---

## Success Criteria (MVP)

### Must Have (Launch Blockers)
✅ Successfully scan Azure subscription and find ACS resources
✅ Detect usage for ALL channels (Email, SMS, Chat, Calling, Phone Numbers)
✅ Display clear results with retirement dates and severity
✅ Provide links to migration guides for each channel
✅ Export results to CSV with all channel data
✅ Azure AD authentication works
✅ Handle resources with multiple retiring channels correctly

### Nice to Have (Can defer)
⚠️ Beautiful UI design - Functional is enough
⚠️ Advanced error handling - Basic errors only
⚠️ Comprehensive test coverage - Manual testing OK for MVP
⚠️ Performance optimization - Works for 1 subscription at a time is fine

---

## Metrics to Track (Simple)

### Launch Metrics (First 3 Months)
- **Adoption:** Number of unique users/tenants
- **Usage:** Number of scans performed
- **Detection:** Number of impacted resources found per channel
- **Channel breakdown:** Email usage, SMS usage, Chat usage, Calling usage, Phone Numbers usage
- **Engagement:** Number of CSV exports downloaded
- **Documentation:** Number of migration guide views per channel

### Success Indicators
- 100+ scans in first month
- 50+ customers discover retiring service usage they didn't know about
- Visibility into which channels are most used (informs prioritization)
- 20+ customers begin migration planning
- Low support ticket volume (<10 tickets/month)

---

## Risks & Mitigations

### Risk 1: Single Engineer Bandwidth
**Mitigation:** Keep scope extremely focused. PMs handle all non-coding work (content, testing, documentation, comms)

### Risk 2: Azure API Complexity
**Mitigation:** Use existing Azure SDK libraries. Don't build custom integrations. Start with read-only operations only.

### Risk 3: Customer Adoption
**Mitigation:** PMs run pilot with 5-10 friendly customers before broad launch. Get feedback early.

### Risk 4: M365 HVE Guidance Accuracy
**Mitigation:** PM3 works directly with M365 team to validate migration guide content before launch.

### Risk 5: Scope Creep
**Mitigation:** Ruthlessly defer everything not in "Must Have" list. Create backlog for Phase 2.

---

## Phase 2 Roadmap (Post-MVP, 3-6 Months Later)

Once MVP proves value, expand with:
1. **Multi-subscription scanning** - Scan entire tenant at once
2. **SMS API retirement detection** - Add second retiring service
3. **M365 license tracking** - Partner with M365 telemetry team
4. **Partner portal** - Enable partners to scan customer tenants
5. **Advanced reporting** - Markdown reports, trend analysis
6. **Additional retiring features** - Chat SDK, Calling SDK, Phone Numbers

**Prioritize based on MVP feedback** - Let customers tell you what's most valuable

---

## Budget Estimate (Minimal)

### Personnel (12 weeks)
- 1 Engineer: 12 weeks
- 3 PMs: 25% time each = ~9 PM-weeks total

### Infrastructure (Annual)
- Azure Static Web Apps: ~$50/month = $600/year
- Azure AD: Free tier (sufficient for MVP)
- Domain/SSL: Included with Static Web Apps
- **Total:** <$1K/year

### Tools & Services
- GitHub/DevOps: Existing Microsoft tools
- VS Code: Free
- Azure subscription: Use existing test subscription

**Total MVP Investment:** Primarily personnel time, minimal infrastructure cost

---

## Key Decisions

### Decision 1: All ACS Channels for MVP
**Rationale:** Customers use multiple ACS services - need complete visibility. Detection logic is similar across channels (just different metrics). The code architecture already supports it.

### Decision 2: No Database/Storage
**Rationale:** Reduces complexity, security concerns, infrastructure cost

### Decision 3: Single Subscription Scanning
**Rationale:** 80% of customers need to scan 1-3 subscriptions max. Multi-sub can wait.

### Decision 4: CSV Export Only
**Rationale:** Customers know Excel. Markdown reports are nice-to-have.

### Decision 5: Static Migration Guides (5 Guides)
**Rationale:** Content changes slowly. One guide per channel is manageable for 3 PMs. Use template approach to speed up creation.

---

## Launch Checklist

### Technical
- [ ] Azure AD app registered and configured
- [ ] Application deployed to production
- [ ] SSL certificate configured
- [ ] Basic monitoring/logging enabled
- [ ] Tested with 3+ different Azure subscriptions

### Content
- [ ] All 5 migration guides completed (Email, SMS, Chat, Calling, Phone Numbers)
- [ ] Email guide reviewed by M365 team
- [ ] User documentation written
- [ ] FAQ document created
- [ ] Known limitations documented

### Communication
- [ ] Internal announcement (Azure/ACS team)
- [ ] Customer pilot completed (5-10 customers)
- [ ] Launch email drafted
- [ ] Support process defined (who handles questions?)

### Legal/Compliance
- [ ] Privacy review (minimal - no data storage)
- [ ] Terms of use (simple - read-only tool)
- [ ] Security basic review completed

---

## Success Story (What Good Looks Like)

**3 Months Post-Launch:**

*"We launched the ACS Transition Agent MVP with a team of 3 PMs and 1 engineer in 12 weeks. In the first 3 months, 200+ customers scanned their subscriptions and discovered impacted services: 85 using Email, 120 using SMS, 45 using Chat, 30 using Calling, and 15 using Phone Numbers SDK. Many customers had multiple retiring services - the comprehensive scan gave them complete visibility.*

*The data showed Email and SMS are the most widely used retiring services, helping us prioritize migration support. 30+ customers have begun migrations using our guides, and we've received only 8 support tickets (all resolved quickly with FAQ additions).*

*Based on customer feedback, our Phase 2 priorities are clear: multi-subscription scanning (most requested) and M365 license tracking (to measure migration success). The MVP proved the concept works, customers love the proactive guidance, and we're ready to scale."*

---

## Bottom Line

**Start Simple. Deliver Value. Iterate Fast.**

This MVP scope is realistic for a 3 PM + 1 engineer team, delivers immediate value to customers, and proves the concept works before investing in complex features. Focus on Email service retirement first, get it right, then expand.

**The goal isn't perfection - it's getting customers actionable guidance before their services retire.**
