# ACS Transition Agent - Migration Guides

This folder contains step-by-step migration guides for transitioning from retiring Azure Communication Services (ACS) standalone SDKs and APIs to integrated Microsoft 365 solutions.

---

## Available Guides

### Email Service

- **[Email Service Migration Guide](email/email-service-migration.md)** - Complete guide for migrating from ACS Email Service to Microsoft 365 High-Volume Email (HVE)
  - Executive summary and prerequisites
  - Step-by-step migration instructions
  - Code examples (TypeScript, C#)
  - Testing strategy and validation
  - FAQ and troubleshooting
  - **[Azure DevOps Wiki Format](email/email-service-migration.wiki.md)**

**Status:** ✅ Complete | **Effort:** High | **Retirement Date:** 2027-12-31

---

## Guides in Development

The following migration guides are planned and will use the Email guide as a template:

### SMS API
- **Status:** 📝 Planned
- **Effort:** Medium
- **Target Service:** Alternative SMS providers (to be determined)

### Chat SDK
- **Status:** 📝 Planned
- **Effort:** Medium
- **Target Service:** Microsoft Teams Chat integration

### Calling SDK
- **Status:** 📝 Planned
- **Effort:** High
- **Target Service:** Microsoft Teams Calling integration

### Phone Numbers SDK
- **Status:** 📝 Planned
- **Effort:** Low
- **Target Service:** Azure Portal management

---

## How to Use These Guides

1. **Run an assessment** - Use the [PowerShell script](../scripts/powershell/) to identify which services you're using
2. **Review the appropriate guide** - Each guide is specific to one retiring service
3. **Follow the step-by-step instructions** - Guides include prerequisites, code examples, and testing strategies
4. **Test thoroughly** - Each guide includes a testing checklist
5. **Track your progress** - Use the CSV export from the assessment tool to track migrations

---

## Migration Guide Template

Each guide follows a consistent structure:

1. **Executive Summary** - Overview and migration path
2. **Prerequisites** - Required access, tools, and knowledge
3. **Migration Path Overview** - High-level steps
4. **Step-by-Step Instructions** - Detailed implementation guide
5. **Code Examples** - TypeScript and C# samples
6. **Testing Strategy** - Validation and rollback procedures
7. **FAQ** - Common questions and troubleshooting

---

## Policy Compliance

All migration guides follow Microsoft's policy compliance requirements:

- ✅ **Microsoft first-party solutions only** - No third-party Azure Marketplace partners
- ✅ **M365 integration preferred** - Leverage existing Microsoft 365 investments
- ✅ **Validated by product teams** - Guides reviewed by M365 and ACS teams

---

## Related Resources

- [Assessment Scripts](../scripts/) - Automated tools to identify retiring service usage
- [AI Agent](../ai-agent/) - Interactive web application for guided migrations (future)
- [Project Documentation](../docs/) - Full project details and MVP scope

---

## Contributing

If you have feedback on these guides or suggestions for improvements:
1. Test the migration guide with your resources
2. Document any issues or missing steps
3. Open an issue in the repository with details
4. Include your environment and configuration

---

## Support

For questions about these migration guides:
- **Technical questions:** Open an issue in the repository
- **Migration assistance:** Contact the ACS team or Microsoft FastTrack
- **Partner support:** Reach out to your Microsoft account team

---

**Last Updated:** 2026-01-28
**Maintained By:** ACS Transition Agent Team
