import { RetiringFeature } from '@/types';

// Configuration for all retiring ACS standalone features
// Update this file with actual retiring features and migration guidance
export const RETIRING_FEATURES: RetiringFeature[] = [
  {
    id: 'standalone-calling-sdk',
    name: 'Standalone Calling SDK',
    category: 'sdk',
    description: 'Azure Communication Services standalone Calling SDK is being retired. Customers should migrate to integrated calling scenarios with Microsoft Teams.',
    retirementDate: '2025-12-31',
    affectedSDKs: [
      '@azure/communication-calling@1.x',
      'azure-communication-calling (Python)',
      'com.azure.android.communication.calling',
      'AzureCommunicationCalling (iOS)',
    ],
    affectedAPIs: [
      '/calling/call',
      '/calling/participants',
    ],
    detectionCriteria: {
      metricNames: [
        'CallDuration',
        'CallCount',
        'ParticipantCount',
      ],
      sdkPatterns: [
        '@azure/communication-calling',
        'azure.communication.calling',
        'com.azure.android.communication.calling',
        'AzureCommunicationCalling',
      ],
      apiEndpoints: [
        '/calling/',
      ],
    },
    migrationPath: {
      title: 'Migrate to Microsoft Teams Integrated Calling',
      description: 'Move from standalone ACS calling to Microsoft Teams integrated scenarios for enhanced collaboration features.',
      documentationUrl: 'https://learn.microsoft.com/azure/communication-services/concepts/teams-endpoint',
      alternativeSolution: 'Use Azure Communication Services with Teams interoperability for calling scenarios',
      estimatedEffort: 'medium',
      steps: [
        'Review your current calling implementation and identify dependencies',
        'Set up Teams interoperability in your Azure Communication Services resource',
        'Update SDK dependencies to Teams-compatible versions',
        'Migrate calling logic to use Teams calling SDK',
        'Test calling scenarios with Teams endpoints',
        'Update authentication to support Teams identity',
        'Deploy and monitor the new implementation',
      ],
    },
    integratedScenarios: [
      {
        name: 'Teams Interoperability',
        description: 'Enable calling between ACS users and Microsoft Teams users',
        benefitsOverStandalone: [
          'Seamless integration with Microsoft 365 ecosystem',
          'Access to Teams features like chat, screen sharing, and recording',
          'Better enterprise compliance and governance',
          'Unified identity and access management',
        ],
        documentationUrl: 'https://learn.microsoft.com/azure/communication-services/concepts/teams-interop',
      },
    ],
  },
  {
    id: 'standalone-chat-sdk',
    name: 'Standalone Chat SDK',
    category: 'sdk',
    description: 'Azure Communication Services standalone Chat SDK is being retired. Migrate to Teams-integrated chat for unified messaging.',
    retirementDate: '2025-12-31',
    affectedSDKs: [
      '@azure/communication-chat@1.x',
      'azure-communication-chat (Python)',
      'com.azure.android.communication.chat',
      'AzureCommunicationChat (iOS)',
    ],
    affectedAPIs: [
      '/chat/threads',
      '/chat/messages',
    ],
    detectionCriteria: {
      metricNames: [
        'ChatMessageCount',
        'ChatThreadCount',
        'ActiveChatUsers',
      ],
      sdkPatterns: [
        '@azure/communication-chat',
        'azure.communication.chat',
        'com.azure.android.communication.chat',
        'AzureCommunicationChat',
      ],
      apiEndpoints: [
        '/chat/',
      ],
    },
    migrationPath: {
      title: 'Migrate to Teams Chat Integration',
      description: 'Transition from standalone chat to Teams-integrated chat for enterprise messaging.',
      documentationUrl: 'https://learn.microsoft.com/azure/communication-services/quickstarts/chat/get-started-teams-interop',
      alternativeSolution: 'Use Microsoft Teams chat with ACS integration',
      estimatedEffort: 'medium',
      steps: [
        'Audit existing chat threads and message storage requirements',
        'Plan data migration strategy for chat history',
        'Configure Teams chat integration in ACS resource',
        'Update client SDKs to Teams-compatible versions',
        'Migrate user identities to support Teams authentication',
        'Test chat functionality with Teams endpoints',
        'Migrate chat data if required',
        'Deploy and validate the new chat implementation',
      ],
    },
    integratedScenarios: [
      {
        name: 'Teams Chat Interoperability',
        description: 'Enable chat between ACS applications and Microsoft Teams',
        benefitsOverStandalone: [
          'Unified chat experience across platforms',
          'Rich formatting and file sharing capabilities',
          'Enterprise-grade security and compliance',
          'Integration with Teams channels and groups',
        ],
        documentationUrl: 'https://learn.microsoft.com/azure/communication-services/concepts/interop/guest/teams-administration',
      },
    ],
  },
  {
    id: 'standalone-sms-api',
    name: 'Standalone SMS API (Legacy)',
    category: 'api',
    description: 'Legacy SMS API endpoints are being deprecated in favor of the unified messaging API.',
    retirementDate: '2026-06-30',
    affectedAPIs: [
      '/sms/send',
      '/sms/messages',
    ],
    detectionCriteria: {
      metricNames: [
        'SMSMessagesSent',
        'SMSMessagesReceived',
      ],
      apiEndpoints: [
        '/sms/',
      ],
    },
    migrationPath: {
      title: 'Migrate to Unified Messaging API',
      description: 'Move to the new unified messaging API that supports SMS, MMS, and future messaging channels.',
      documentationUrl: 'https://learn.microsoft.com/azure/communication-services/concepts/sms/concepts',
      alternativeSolution: 'Use the unified Messaging API for SMS capabilities',
      estimatedEffort: 'low',
      steps: [
        'Review current SMS integration points',
        'Update API endpoints to new unified messaging API',
        'Update request/response handling for new API format',
        'Test SMS delivery and receipt',
        'Monitor for any delivery issues',
      ],
    },
  },
  {
    id: 'standalone-phone-numbers-sdk',
    name: 'Standalone Phone Numbers SDK',
    category: 'sdk',
    description: 'Phone number management SDK is consolidating into unified resource management.',
    retirementDate: '2026-03-31',
    affectedSDKs: [
      '@azure/communication-phone-numbers@1.x',
      'azure-communication-phonenumbers (Python)',
    ],
    detectionCriteria: {
      metricNames: [
        'PhoneNumberOperations',
      ],
      sdkPatterns: [
        '@azure/communication-phone-numbers',
        'azure.communication.phonenumbers',
      ],
    },
    migrationPath: {
      title: 'Migrate to Unified Resource Management',
      description: 'Use Azure Resource Manager for phone number provisioning and management.',
      documentationUrl: 'https://learn.microsoft.com/azure/communication-services/quickstarts/telephony/get-phone-number',
      alternativeSolution: 'Use Azure ARM APIs or Portal for phone number management',
      estimatedEffort: 'low',
      steps: [
        'Identify phone number management operations in code',
        'Move to Azure Portal or ARM templates for provisioning',
        'Update automation scripts to use ARM APIs',
        'Test phone number acquisition and release',
      ],
    },
  },
  {
    id: 'acs-email-service',
    name: 'Azure Communication Services Email',
    category: 'service',
    description: 'Azure Communication Services Email will be retired 36 months after official notification. No new ACS Email capabilities or feature investments will be introduced. All Azure-based email services under ACS will be fully sunset.',
    retirementDate: '2027-12-31',
    affectedSDKs: [
      '@azure/communication-email',
      'azure-communication-email (Python)',
      'com.azure.android.communication.email',
      'AzureCommunicationEmail (iOS)',
    ],
    affectedAPIs: [
      '/emails',
      '/emails/send',
    ],
    detectionCriteria: {
      metricNames: [
        'EmailMessagesSent',
        'EmailDeliveryAttempts',
        'EmailOperations',
      ],
      sdkPatterns: [
        '@azure/communication-email',
        'azure.communication.email',
        'com.azure.android.communication.email',
        'AzureCommunicationEmail',
      ],
      apiEndpoints: [
        '/emails/',
      ],
    },
    migrationPath: {
      title: 'Migrate to External Email Providers or Microsoft 365 HVE',
      description: 'Customers using ACS Email must migrate email workloads to supported alternatives such as external third-party email delivery providers (e.g., SendGrid) or Microsoft 365 High-Volume Email (HVE) for entry-level external email scenarios.',
      documentationUrl: '/migration-guides/email-service-migration.md',
      alternativeSolution: 'Use external email service providers like SendGrid, or Microsoft 365 High-Volume Email (HVE) for entry-level scenarios',
      estimatedEffort: 'high',
      steps: [
        'Audit current email sending patterns and volume',
        'Evaluate migration options: External providers (SendGrid) vs Microsoft 365 HVE',
        'Choose appropriate email service provider based on requirements',
        'Set up account and configure DNS records with new provider',
        'Update application code to use new email API/SDK',
        'Migrate email templates and assets',
        'Test email delivery, rendering, and tracking',
        'Update monitoring and alerting for new email service',
        'Perform gradual rollout to minimize disruption',
        'Monitor deliverability and engagement metrics',
      ],
    },
    integratedScenarios: [
      {
        name: 'External Email Service Providers (Recommended)',
        description: 'Migrate to established external email providers like SendGrid or other commercial SMTP-based or API-based email services',
        benefitsOverStandalone: [
          'Advanced deliverability controls and analytics',
          'High-volume and fully customizable email delivery',
          'Marketing and transactional email support',
          'Proven infrastructure with established SLAs',
          'Rich feature set for email campaigns',
        ],
        documentationUrl: 'https://sendgrid.com/solutions/email-api/',
      },
      {
        name: 'Microsoft 365 High-Volume Email (HVE)',
        description: 'Use Microsoft 365 HVE as an alternative for entry-level external email scenarios',
        benefitsOverStandalone: [
          'Integration with Microsoft 365 ecosystem',
          'Entry-level solution for external email',
          'Suitable for basic transactional emails',
          'Microsoft support and compliance',
        ],
        documentationUrl: 'https://learn.microsoft.com/microsoft-365/compliance/high-volume-email',
      },
    ],
  },
];

// Helper function to get feature by ID
export function getFeatureById(id: string): RetiringFeature | undefined {
  return RETIRING_FEATURES.find(f => f.id === id);
}

// Helper function to get features by category
export function getFeaturesByCategory(category: 'sdk' | 'api' | 'service'): RetiringFeature[] {
  return RETIRING_FEATURES.filter(f => f.category === category);
}

// Helper function to check if a retirement date is approaching (within 6 months)
export function isRetirementApproaching(retirementDate: string): boolean {
  const sixMonthsFromNow = new Date();
  sixMonthsFromNow.setMonth(sixMonthsFromNow.getMonth() + 6);
  return new Date(retirementDate) <= sixMonthsFromNow;
}
