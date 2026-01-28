// Azure Communication Services resource types
export interface ACSResource {
  id: string;
  name: string;
  location: string;
  subscriptionId: string;
  resourceGroup: string;
  provisioningState: string;
}

// Feature usage data from Azure Monitor
export interface FeatureUsage {
  featureName: string;
  resourceId: string;
  usageCount: number;
  lastUsed?: Date;
  sdkVersion?: string;
}

// Retiring feature definition
export interface RetiringFeature {
  id: string;
  name: string;
  category: 'sdk' | 'api' | 'service';
  description: string;
  retirementDate: string;
  affectedSDKs?: string[];
  affectedAPIs?: string[];
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
  integratedScenarios?: {
    name: string;
    description: string;
    benefitsOverStandalone: string[];
    documentationUrl: string;
  }[];
}

// Eligibility check result
export interface EligibilityResult {
  resourceId: string;
  resourceName: string;
  isImpacted: boolean;
  impactedFeatures: {
    feature: RetiringFeature;
    detectedUsage: FeatureUsage[];
    severity: 'critical' | 'warning' | 'info';
  }[];
  recommendations: string[];
  estimatedMigrationEffort: 'low' | 'medium' | 'high';
}

// Scan result summary
export interface ScanResult {
  subscriptionId: string;
  scanDate: Date;
  totalResources: number;
  impactedResources: number;
  results: EligibilityResult[];
  summary: {
    critical: number;
    warnings: number;
    info: number;
  };
}

// User authentication state
export interface UserProfile {
  name: string;
  email: string;
  tenantId: string;
}
