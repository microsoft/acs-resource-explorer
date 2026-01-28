import { ACSResource, FeatureUsage, RetiringFeature, EligibilityResult, ScanResult } from '@/types';
import { RETIRING_FEATURES } from '@/config/retiring-features';

export class EligibilityChecker {
  // Check if a resource is impacted by retiring features
  checkResource(
    resource: ACSResource,
    usageMetrics: FeatureUsage[]
  ): EligibilityResult {
    const impactedFeatures: EligibilityResult['impactedFeatures'] = [];
    const recommendations: string[] = [];

    for (const feature of RETIRING_FEATURES) {
      const detectedUsage = this.detectFeatureUsage(feature, usageMetrics);

      if (detectedUsage.length > 0) {
        const severity = this.calculateSeverity(feature, detectedUsage);
        impactedFeatures.push({
          feature,
          detectedUsage,
          severity,
        });

        // Add recommendations
        recommendations.push(
          `${feature.name}: ${feature.migrationPath.alternativeSolution}`
        );
      }
    }

    const isImpacted = impactedFeatures.length > 0;
    const estimatedMigrationEffort = this.calculateOverallEffort(impactedFeatures);

    return {
      resourceId: resource.id,
      resourceName: resource.name,
      isImpacted,
      impactedFeatures,
      recommendations,
      estimatedMigrationEffort,
    };
  }

  // Detect if a retiring feature is being used based on metrics
  private detectFeatureUsage(
    feature: RetiringFeature,
    usageMetrics: FeatureUsage[]
  ): FeatureUsage[] {
    const detected: FeatureUsage[] = [];

    for (const usage of usageMetrics) {
      // Check if metric name matches any of the feature's detection criteria
      const matchesMetric = feature.detectionCriteria.metricNames?.some(
        metricName => usage.featureName.toLowerCase().includes(metricName.toLowerCase())
      );

      // Check SDK patterns if version information is available
      const matchesSdk = feature.detectionCriteria.sdkPatterns?.some(
        pattern => usage.sdkVersion?.toLowerCase().includes(pattern.toLowerCase())
      );

      if (matchesMetric || matchesSdk) {
        detected.push(usage);
      }
    }

    return detected;
  }

  // Calculate severity based on usage patterns and retirement date
  private calculateSeverity(
    feature: RetiringFeature,
    usage: FeatureUsage[]
  ): 'critical' | 'warning' | 'info' {
    const retirementDate = new Date(feature.retirementDate);
    const now = new Date();
    const monthsUntilRetirement =
      (retirementDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24 * 30);

    // Calculate total usage
    const totalUsage = usage.reduce((sum, u) => sum + u.usageCount, 0);

    // Critical if retirement is soon and high usage
    if (monthsUntilRetirement < 6 && totalUsage > 1000) {
      return 'critical';
    }

    // Critical if retirement is very soon
    if (monthsUntilRetirement < 3) {
      return 'critical';
    }

    // Warning if moderate usage or moderate time
    if (monthsUntilRetirement < 9 || totalUsage > 100) {
      return 'warning';
    }

    return 'info';
  }

  // Calculate overall migration effort
  private calculateOverallEffort(
    impactedFeatures: EligibilityResult['impactedFeatures']
  ): 'low' | 'medium' | 'high' {
    if (impactedFeatures.length === 0) return 'low';

    const efforts = impactedFeatures.map(f => f.feature.migrationPath.estimatedEffort);

    // If any feature has high effort, overall is high
    if (efforts.includes('high')) return 'high';

    // If multiple medium or any medium + others, overall is high
    const mediumCount = efforts.filter(e => e === 'medium').length;
    if (mediumCount > 1 || (mediumCount === 1 && efforts.length > 2)) return 'high';

    // If any medium, overall is medium
    if (mediumCount === 1) return 'medium';

    // Multiple low effort features
    if (efforts.length > 2) return 'medium';

    return 'low';
  }

  // Create a summary scan result
  createScanResult(
    subscriptionId: string,
    eligibilityResults: EligibilityResult[]
  ): ScanResult {
    const summary = {
      critical: 0,
      warnings: 0,
      info: 0,
    };

    let impactedResources = 0;

    for (const result of eligibilityResults) {
      if (result.isImpacted) {
        impactedResources++;
      }

      for (const impact of result.impactedFeatures) {
        switch (impact.severity) {
          case 'critical':
            summary.critical++;
            break;
          case 'warning':
            summary.warnings++;
            break;
          case 'info':
            summary.info++;
            break;
        }
      }
    }

    return {
      subscriptionId,
      scanDate: new Date(),
      totalResources: eligibilityResults.length,
      impactedResources,
      results: eligibilityResults,
      summary,
    };
  }
}
