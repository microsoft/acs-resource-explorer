import { NextRequest, NextResponse } from 'next/server';
import { createAzureClients } from '@/lib/azure/client';
import { AzureResourceScanner } from '@/lib/azure/scanner';
import { EligibilityChecker } from '@/lib/eligibility/checker';
import { ScanResult } from '@/types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { accessToken, subscriptionId } = body;

    if (!accessToken) {
      return NextResponse.json(
        { error: 'Access token is required' },
        { status: 401 }
      );
    }

    // Create Azure clients
    const clients = createAzureClients(accessToken);
    const scanner = new AzureResourceScanner(clients);
    const checker = new EligibilityChecker();

    // Scan for resources
    let resources;
    if (subscriptionId) {
      // Scan specific subscription
      resources = await scanner.findACSResources(subscriptionId);
    } else {
      // Scan all subscriptions
      const allResources = await scanner.scanAllSubscriptions();
      resources = Array.from(allResources.values()).flat();
    }

    if (resources.length === 0) {
      return NextResponse.json({
        message: 'No Azure Communication Services resources found',
        results: [],
      });
    }

    // Check eligibility for each resource
    const eligibilityResults = [];
    const endTime = new Date();
    const startTime = new Date();
    startTime.setMonth(startTime.getMonth() - 3); // Look back 3 months

    for (const resource of resources) {
      // Get metrics for the resource
      const allMetricNames = [
        'CallDuration',
        'CallCount',
        'ParticipantCount',
        'ChatMessageCount',
        'ChatThreadCount',
        'ActiveChatUsers',
        'SMSMessagesSent',
        'SMSMessagesReceived',
        'PhoneNumberOperations',
        'EmailMessagesSent',
        'EmailDeliveryAttempts',
        'EmailOperations',
      ];

      const metrics = await scanner.getResourceMetrics(
        resource.subscriptionId,
        resource.id,
        allMetricNames,
        startTime,
        endTime
      );

      // Check eligibility
      const result = checker.checkResource(resource, metrics);
      eligibilityResults.push(result);
    }

    // Create scan result summary
    const scanResult: ScanResult = checker.createScanResult(
      subscriptionId || 'all',
      eligibilityResults
    );

    return NextResponse.json(scanResult);
  } catch (error) {
    console.error('Scan error:', error);
    return NextResponse.json(
      { error: 'Failed to scan resources', details: String(error) },
      { status: 500 }
    );
  }
}
