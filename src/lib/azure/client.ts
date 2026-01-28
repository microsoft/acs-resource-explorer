import { ClientSecretCredential, TokenCredential } from '@azure/identity';
import { CommunicationServiceManagementClient } from '@azure/arm-communication';
import { SubscriptionClient } from '@azure/arm-subscriptions';
import { ResourceManagementClient } from '@azure/arm-resources';
import { MonitorClient } from '@azure/arm-monitor';

// Custom credential that uses the access token from MSAL
export class BrowserTokenCredential implements TokenCredential {
  constructor(private accessToken: string) {}

  async getToken(): Promise<{ token: string; expiresOnTimestamp: number }> {
    return {
      token: this.accessToken,
      expiresOnTimestamp: Date.now() + 3600000, // 1 hour from now
    };
  }
}

export interface AzureClients {
  subscriptionClient: SubscriptionClient;
  getResourceClient: (subscriptionId: string) => ResourceManagementClient;
  getCommunicationClient: (subscriptionId: string) => CommunicationServiceManagementClient;
  getMonitorClient: (subscriptionId: string) => MonitorClient;
}

// Create Azure clients using the access token
export function createAzureClients(accessToken: string): AzureClients {
  const credential = new BrowserTokenCredential(accessToken);

  return {
    subscriptionClient: new SubscriptionClient(credential),
    getResourceClient: (subscriptionId: string) =>
      new ResourceManagementClient(credential, subscriptionId),
    getCommunicationClient: (subscriptionId: string) =>
      new CommunicationServiceManagementClient(credential, subscriptionId),
    getMonitorClient: (subscriptionId: string) =>
      new MonitorClient(credential, subscriptionId),
  };
}
