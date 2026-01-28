import { ScanResult, EligibilityResult } from '@/types';
import { format } from 'date-fns';

export class ReportGenerator {
  // Generate a markdown report
  generateMarkdown(scanResult: ScanResult): string {
    const { subscriptionId, scanDate, totalResources, impactedResources, summary, results } = scanResult;

    let markdown = `# Azure Communication Services Transition Report\n\n`;
    markdown += `**Generated:** ${format(new Date(scanDate), 'MMMM d, yyyy \'at\' h:mm a')}\n`;
    markdown += `**Subscription:** ${subscriptionId}\n\n`;

    // Executive Summary
    markdown += `## Executive Summary\n\n`;
    markdown += `- **Total ACS Resources Scanned:** ${totalResources}\n`;
    markdown += `- **Impacted Resources:** ${impactedResources}\n`;
    markdown += `- **Critical Issues:** ${summary.critical}\n`;
    markdown += `- **Warnings:** ${summary.warnings}\n`;
    markdown += `- **Informational:** ${summary.info}\n\n`;

    if (impactedResources === 0) {
      markdown += `### Status: ✅ No Action Required\n\n`;
      markdown += `Your Azure Communication Services resources are not using any retiring features. No migration is required at this time.\n\n`;
      return markdown;
    }

    markdown += `### Status: ⚠️ Action Required\n\n`;
    markdown += `Your Azure Communication Services resources are using retiring features that require migration.\n\n`;

    // Detailed Findings
    markdown += `## Detailed Findings\n\n`;

    const impactedResults = results.filter(r => r.isImpacted);

    impactedResults.forEach((result, idx) => {
      markdown += `### ${idx + 1}. ${result.resourceName}\n\n`;
      markdown += `**Resource ID:** \`${result.resourceId}\`\n`;
      markdown += `**Migration Effort:** ${result.estimatedMigrationEffort.toUpperCase()}\n\n`;

      result.impactedFeatures.forEach((impact) => {
        const severityEmoji = impact.severity === 'critical' ? '🔴' : impact.severity === 'warning' ? '🟡' : '🔵';
        markdown += `#### ${severityEmoji} ${impact.feature.name}\n\n`;
        markdown += `**Severity:** ${impact.severity.toUpperCase()}\n`;
        markdown += `**Retirement Date:** ${format(new Date(impact.feature.retirementDate), 'MMMM d, yyyy')}\n\n`;
        markdown += `${impact.feature.description}\n\n`;

        // Usage Metrics
        if (impact.detectedUsage.length > 0) {
          markdown += `**Detected Usage:**\n\n`;
          impact.detectedUsage.forEach(usage => {
            markdown += `- ${usage.featureName}: ${usage.usageCount.toLocaleString()} operations`;
            if (usage.lastUsed) {
              markdown += ` (last used: ${format(new Date(usage.lastUsed), 'MMM d, yyyy')})`;
            }
            markdown += `\n`;
          });
          markdown += `\n`;
        }

        // Migration Path
        markdown += `**Migration Path: ${impact.feature.migrationPath.title}**\n\n`;
        markdown += `${impact.feature.migrationPath.description}\n\n`;
        markdown += `**Alternative Solution:** ${impact.feature.migrationPath.alternativeSolution}\n\n`;
        markdown += `**Estimated Effort:** ${impact.feature.migrationPath.estimatedEffort.toUpperCase()}\n\n`;

        markdown += `**Migration Steps:**\n\n`;
        impact.feature.migrationPath.steps.forEach((step, stepIdx) => {
          markdown += `${stepIdx + 1}. ${step}\n`;
        });
        markdown += `\n`;

        markdown += `**Documentation:** [View Migration Guide](${impact.feature.migrationPath.documentationUrl})\n\n`;

        // Integrated Scenarios
        if (impact.feature.integratedScenarios && impact.feature.integratedScenarios.length > 0) {
          markdown += `**Integrated Scenarios Available:**\n\n`;
          impact.feature.integratedScenarios.forEach(scenario => {
            markdown += `- **${scenario.name}:** ${scenario.description}\n`;
            markdown += `  - Benefits:\n`;
            scenario.benefitsOverStandalone.forEach(benefit => {
              markdown += `    - ${benefit}\n`;
            });
            markdown += `  - [Learn More](${scenario.documentationUrl})\n`;
          });
          markdown += `\n`;
        }
      });

      // Recommendations
      if (result.recommendations.length > 0) {
        markdown += `**Recommendations:**\n\n`;
        result.recommendations.forEach(rec => {
          markdown += `- ${rec}\n`;
        });
        markdown += `\n`;
      }

      markdown += `---\n\n`;
    });

    // Next Steps
    markdown += `## Next Steps\n\n`;
    markdown += `1. Review the detailed findings above for each impacted resource\n`;
    markdown += `2. Prioritize migration efforts based on severity and retirement dates\n`;
    markdown += `3. Follow the migration steps provided for each retiring feature\n`;
    markdown += `4. Test your application with the new integrated scenarios\n`;
    markdown += `5. Monitor for any issues and refer to documentation as needed\n\n`;

    markdown += `## Resources\n\n`;
    markdown += `- [Azure Communication Services Documentation](https://learn.microsoft.com/azure/communication-services/)\n`;
    markdown += `- [Teams Interoperability Guide](https://learn.microsoft.com/azure/communication-services/concepts/teams-interop)\n`;
    markdown += `- [Migration Support](https://azure.microsoft.com/support/)\n\n`;

    return markdown;
  }

  // Generate CSV report
  generateCSV(scanResult: ScanResult): string {
    const headers = [
      'Resource Name',
      'Resource ID',
      'Is Impacted',
      'Migration Effort',
      'Feature Name',
      'Severity',
      'Retirement Date',
      'Usage Metric',
      'Usage Count',
      'Documentation URL',
    ];

    let csv = headers.join(',') + '\n';

    for (const result of scanResult.results) {
      if (result.impactedFeatures.length === 0) {
        // Resource with no impacts
        csv += [
          this.escapeCSV(result.resourceName),
          this.escapeCSV(result.resourceId),
          'No',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
          'N/A',
        ].join(',') + '\n';
      } else {
        // Resource with impacts
        for (const impact of result.impactedFeatures) {
          for (const usage of impact.detectedUsage) {
            csv += [
              this.escapeCSV(result.resourceName),
              this.escapeCSV(result.resourceId),
              'Yes',
              result.estimatedMigrationEffort,
              this.escapeCSV(impact.feature.name),
              impact.severity,
              impact.feature.retirementDate,
              this.escapeCSV(usage.featureName),
              usage.usageCount,
              this.escapeCSV(impact.feature.migrationPath.documentationUrl),
            ].join(',') + '\n';
          }

          // If no usage detected but feature is impacted
          if (impact.detectedUsage.length === 0) {
            csv += [
              this.escapeCSV(result.resourceName),
              this.escapeCSV(result.resourceId),
              'Yes',
              result.estimatedMigrationEffort,
              this.escapeCSV(impact.feature.name),
              impact.severity,
              impact.feature.retirementDate,
              'N/A',
              '0',
              this.escapeCSV(impact.feature.migrationPath.documentationUrl),
            ].join(',') + '\n';
          }
        }
      }
    }

    return csv;
  }

  // Escape CSV values
  private escapeCSV(value: string): string {
    if (value.includes(',') || value.includes('"') || value.includes('\n')) {
      return `"${value.replace(/"/g, '""')}"`;
    }
    return value;
  }

  // Download report as file
  downloadReport(content: string, filename: string, type: 'text/markdown' | 'text/csv') {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}
