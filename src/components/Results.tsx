'use client';

import { ScanResult, EligibilityResult } from '@/types';
import { format } from 'date-fns';
import { ReportGenerator } from '@/lib/report/generator';

interface ResultsProps {
  scanResult: ScanResult;
}

export function Results({ scanResult }: ResultsProps) {
  const { totalResources, impactedResources, summary, results, scanDate, subscriptionId } = scanResult;
  const reportGenerator = new ReportGenerator();

  const handleExportMarkdown = () => {
    const markdown = reportGenerator.generateMarkdown(scanResult);
    const filename = `acs-transition-report-${subscriptionId}-${format(new Date(scanDate), 'yyyy-MM-dd')}.md`;
    reportGenerator.downloadReport(markdown, filename, 'text/markdown');
  };

  const handleExportCSV = () => {
    const csv = reportGenerator.generateCSV(scanResult);
    const filename = `acs-transition-report-${subscriptionId}-${format(new Date(scanDate), 'yyyy-MM-dd')}.csv`;
    reportGenerator.downloadReport(csv, filename, 'text/csv');
  };

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-azure-blue">Scan Summary</h2>
          <div className="flex gap-2">
            <button
              onClick={handleExportMarkdown}
              className="bg-azure-blue text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-azure-dark transition-colors"
            >
              Export Markdown
            </button>
            <button
              onClick={handleExportCSV}
              className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
            >
              Export CSV
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div className="bg-blue-50 p-4 rounded-md">
            <p className="text-sm text-gray-600">Total Resources</p>
            <p className="text-3xl font-bold text-azure-blue">{totalResources}</p>
          </div>
          <div className="bg-red-50 p-4 rounded-md">
            <p className="text-sm text-gray-600">Critical Issues</p>
            <p className="text-3xl font-bold text-red-600">{summary.critical}</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-md">
            <p className="text-sm text-gray-600">Warnings</p>
            <p className="text-3xl font-bold text-yellow-600">{summary.warnings}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-md">
            <p className="text-sm text-gray-600">Impacted Resources</p>
            <p className="text-3xl font-bold text-green-600">{impactedResources}</p>
          </div>
        </div>

        <p className="text-sm text-gray-500">
          Scanned on {format(new Date(scanDate), 'MMMM d, yyyy')} at {format(new Date(scanDate), 'h:mm a')}
        </p>
      </div>

      {/* No Impact Message */}
      {impactedResources === 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-green-800 mb-2">
            Great news! No impacted resources found.
          </h3>
          <p className="text-green-700">
            Your Azure Communication Services resources are not using any retiring features.
            No action is required at this time.
          </p>
        </div>
      )}

      {/* Impacted Resources */}
      {results.map((result) => (
        result.isImpacted && <ResourceCard key={result.resourceId} result={result} />
      ))}
    </div>
  );
}

function ResourceCard({ result }: { result: EligibilityResult }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="bg-azure-blue text-white p-4">
        <h3 className="text-xl font-semibold">{result.resourceName}</h3>
        <p className="text-sm opacity-90 mt-1 font-mono text-xs">{result.resourceId}</p>
        <div className="mt-2 flex items-center gap-2">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
            result.estimatedMigrationEffort === 'high'
              ? 'bg-red-500'
              : result.estimatedMigrationEffort === 'medium'
              ? 'bg-yellow-500'
              : 'bg-green-500'
          }`}>
            {result.estimatedMigrationEffort.toUpperCase()} EFFORT
          </span>
        </div>
      </div>

      <div className="p-6">
        {/* Impacted Features */}
        <div className="space-y-4">
          {result.impactedFeatures.map((impact, idx) => (
            <div
              key={idx}
              className={`border-l-4 pl-4 py-2 ${
                impact.severity === 'critical'
                  ? 'border-red-500 bg-red-50'
                  : impact.severity === 'warning'
                  ? 'border-yellow-500 bg-yellow-50'
                  : 'border-blue-500 bg-blue-50'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-semibold text-lg mb-1">{impact.feature.name}</h4>
                  <p className="text-sm text-gray-600 mb-2">{impact.feature.description}</p>

                  <div className="text-sm mb-3">
                    <span className="font-medium">Retirement Date:</span>{' '}
                    <span className="text-red-600 font-semibold">
                      {format(new Date(impact.feature.retirementDate), 'MMMM d, yyyy')}
                    </span>
                  </div>

                  {/* Usage Metrics */}
                  {impact.detectedUsage.length > 0 && (
                    <div className="mb-3">
                      <p className="text-sm font-medium mb-1">Detected Usage:</p>
                      <ul className="text-sm space-y-1">
                        {impact.detectedUsage.map((usage, usageIdx) => (
                          <li key={usageIdx} className="flex items-center gap-2">
                            <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                            <span>
                              {usage.featureName}: {usage.usageCount.toLocaleString()} operations
                              {usage.lastUsed && (
                                <span className="text-gray-500 ml-1">
                                  (last used {format(new Date(usage.lastUsed), 'MMM d, yyyy')})
                                </span>
                              )}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Migration Path */}
                  <div className="bg-white p-4 rounded-md border border-gray-200 mt-3">
                    <h5 className="font-semibold text-azure-blue mb-2">
                      {impact.feature.migrationPath.title}
                    </h5>
                    <p className="text-sm text-gray-700 mb-3">
                      {impact.feature.migrationPath.description}
                    </p>

                    <div className="mb-3">
                      <p className="text-sm font-medium mb-1">Alternative Solution:</p>
                      <p className="text-sm text-gray-600">
                        {impact.feature.migrationPath.alternativeSolution}
                      </p>
                    </div>

                    <div className="mb-3">
                      <p className="text-sm font-medium mb-2">Migration Steps:</p>
                      <ol className="text-sm space-y-1 list-decimal list-inside">
                        {impact.feature.migrationPath.steps.map((step, stepIdx) => (
                          <li key={stepIdx} className="text-gray-600">{step}</li>
                        ))}
                      </ol>
                    </div>

                    <div className="flex gap-2">
                      <a
                        href={impact.feature.migrationPath.documentationUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block bg-azure-blue text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-azure-dark transition-colors"
                      >
                        View Documentation →
                      </a>
                      {impact.feature.migrationPath.documentationUrl.startsWith('/migration-guides/') && (
                        <a
                          href={`/api/migration-guide/${impact.feature.id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-block bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
                        >
                          View Full Migration Guide →
                        </a>
                      )}
                    </div>
                  </div>

                  {/* Integrated Scenarios */}
                  {impact.feature.integratedScenarios && impact.feature.integratedScenarios.length > 0 && (
                    <div className="mt-4 bg-green-50 p-4 rounded-md border border-green-200">
                      <h5 className="font-semibold text-green-800 mb-2">
                        Integrated Scenarios Available
                      </h5>
                      {impact.feature.integratedScenarios.map((scenario, scenarioIdx) => (
                        <div key={scenarioIdx} className="mb-3 last:mb-0">
                          <p className="text-sm font-medium text-green-900">{scenario.name}</p>
                          <p className="text-sm text-green-700 mb-2">{scenario.description}</p>
                          <p className="text-sm font-medium text-green-900 mb-1">Benefits:</p>
                          <ul className="text-sm space-y-1">
                            {scenario.benefitsOverStandalone.map((benefit, benefitIdx) => (
                              <li key={benefitIdx} className="flex items-start gap-2">
                                <span className="text-green-600 mt-1">✓</span>
                                <span className="text-green-700">{benefit}</span>
                              </li>
                            ))}
                          </ul>
                          <a
                            href={scenario.documentationUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-green-700 underline hover:text-green-900 mt-2 inline-block"
                          >
                            Learn more →
                          </a>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Recommendations */}
        {result.recommendations.length > 0 && (
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
            <h4 className="font-semibold text-blue-900 mb-2">Recommendations</h4>
            <ul className="text-sm space-y-1">
              {result.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-blue-600 mt-1">→</span>
                  <span className="text-blue-800">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
