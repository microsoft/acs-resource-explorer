'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/auth/useAuth';
import { ScanResult } from '@/types';

interface ScannerProps {
  onScanComplete: (result: ScanResult) => void;
}

export function Scanner({ onScanComplete }: ScannerProps) {
  const { getAccessToken } = useAuth();
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [subscriptionId, setSubscriptionId] = useState<string>('');

  const handleScan = async () => {
    setIsScanning(true);
    setError(null);

    try {
      // Get access token
      const token = await getAccessToken();

      // Call scan API
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          accessToken: token,
          subscriptionId: subscriptionId || undefined,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Scan failed');
      }

      const result: ScanResult = await response.json();
      onScanComplete(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Scan error:', err);
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4 text-azure-blue">Scan Azure Resources</h2>

      <div className="mb-4">
        <label htmlFor="subscriptionId" className="block text-sm font-medium text-gray-700 mb-2">
          Subscription ID (optional - leave blank to scan all)
        </label>
        <input
          id="subscriptionId"
          type="text"
          value={subscriptionId}
          onChange={(e) => setSubscriptionId(e.target.value)}
          placeholder="Enter subscription ID or leave blank"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-azure-blue focus:border-azure-blue"
          disabled={isScanning}
        />
      </div>

      <button
        onClick={handleScan}
        disabled={isScanning}
        className="w-full bg-azure-blue text-white py-3 px-6 rounded-md font-semibold hover:bg-azure-dark disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isScanning ? 'Scanning...' : 'Start Scan'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      {isScanning && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-blue-800 text-sm">
            Scanning your Azure subscriptions for Communication Services resources...
            This may take a few minutes.
          </p>
        </div>
      )}
    </div>
  );
}
