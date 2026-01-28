import { AzureClients } from './client';
import { ACSResource, FeatureUsage } from '@/types';

export class AzureResourceScanner {
  constructor(private clients: AzureClients) {}

  // Get all subscriptions accessible to the user
  async getSubscriptions(): Promise<{ id: string; name: string }[]> {
    const subscriptions: { id: string; name: string }[] = [];

    for await (const subscription of this.clients.subscriptionClient.subscriptions.list()) {
      if (subscription.subscriptionId && subscription.displayName) {
        subscriptions.push({
          id: subscription.subscriptionId,
          name: subscription.displayName,
        });
      }
    }

    return subscriptions;
  }

  // Find all ACS resources in a subscription
  async findACSResources(subscriptionId: string): Promise<ACSResource[]> {
    const resources: ACSResource[] = [];
    const resourceClient = this.clients.getResourceClient(subscriptionId);

    try {
      // Query for Azure Communication Services resources
      const resourceList = resourceClient.resources.list({
        filter: "resourceType eq 'Microsoft.Communication/communicationServices'",
      });

      for await (const resource of resourceList) {
        if (resource.id && resource.name && resource.location) {
          const resourceGroupMatch = resource.id.match(/resourceGroups\/([^\/]+)/);
          const resourceGroup = resourceGroupMatch ? resourceGroupMatch[1] : '';

          resources.push({
            id: resource.id,
            name: resource.name,
            location: resource.location,
            subscriptionId,
            resourceGroup,
            provisioningState: (resource as any).provisioningState || 'Unknown',
          });
        }
      }
    } catch (error) {
      console.error(`Error scanning subscription ${subscriptionId}:`, error);
      throw new Error(`Failed to scan subscription: ${error}`);
    }

    return resources;
  }

  // Get usage metrics for an ACS resource
  async getResourceMetrics(
    subscriptionId: string,
    resourceId: string,
    metricNames: string[],
    startTime: Date,
    endTime: Date
  ): Promise<FeatureUsage[]> {
    const monitorClient = this.clients.getMonitorClient(subscriptionId);
    const usageData: FeatureUsage[] = [];

    try {
      const metrics = await monitorClient.metrics.list(resourceId, {
        timespan: `${startTime.toISOString()}/${endTime.toISOString()}`,
        interval: 'P1D',
        metricnames: metricNames.join(','),
        aggregation: 'Total,Count',
      });

      for (const metric of metrics.value || []) {
        if (!metric.name?.value || !metric.timeseries) continue;

        let totalUsage = 0;
        let lastUsed: Date | undefined;

        for (const timeseries of metric.timeseries) {
          for (const data of timeseries.data || []) {
            if (data.total || data.count) {
              totalUsage += (data.total || data.count || 0);
              if (data.timeStamp && (!lastUsed || data.timeStamp > lastUsed)) {
                lastUsed = data.timeStamp;
              }
            }
          }
        }

        if (totalUsage > 0) {
          usageData.push({
            featureName: metric.name.value,
            resourceId,
            usageCount: totalUsage,
            lastUsed,
          });
        }
      }
    } catch (error) {
      console.error(`Error fetching metrics for ${resourceId}:`, error);
      // Don't throw - return empty array if metrics aren't available
    }

    return usageData;
  }

  // Scan all subscriptions for ACS resources
  async scanAllSubscriptions(): Promise<Map<string, ACSResource[]>> {
    const subscriptions = await this.getSubscriptions();
    const allResources = new Map<string, ACSResource[]>();

    for (const subscription of subscriptions) {
      try {
        const resources = await this.findACSResources(subscription.id);
        if (resources.length > 0) {
          allResources.set(subscription.id, resources);
        }
      } catch (error) {
        console.error(`Error scanning subscription ${subscription.name}:`, error);
        // Continue with other subscriptions even if one fails
      }
    }

    return allResources;
  }
}
