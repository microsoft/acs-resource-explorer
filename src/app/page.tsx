'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/auth/useAuth';
import { Scanner } from '@/components/Scanner';
import { Results } from '@/components/Results';
import { ScanResult } from '@/types';

export default function Home() {
  const { isAuthenticated, login, logout, getUserProfile } = useAuth();
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const userProfile = getUserProfile();

  const handleScanComplete = (result: ScanResult) => {
    setScanResult(result);
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="max-w-2xl w-full">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="mb-6">
              <h1 className="text-4xl font-bold text-azure-blue mb-2">
                ACS Transition Agent
              </h1>
              <p className="text-gray-600 text-lg">
                Azure Communication Services Eligibility Checker
              </p>
            </div>

            <div className="mb-8 text-left bg-gray-50 p-6 rounded-md">
              <h2 className="text-xl font-semibold mb-3 text-gray-800">
                What does this tool do?
              </h2>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-azure-blue font-bold">•</span>
                  <span>Scans your Azure subscriptions for Communication Services resources</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-azure-blue font-bold">•</span>
                  <span>Analyzes usage patterns and metrics</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-azure-blue font-bold">•</span>
                  <span>Identifies retiring features that may impact your applications</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-azure-blue font-bold">•</span>
                  <span>Provides migration guidance and recommendations</span>
                </li>
              </ul>
            </div>

            <button
              onClick={login}
              className="bg-azure-blue text-white py-3 px-8 rounded-md font-semibold text-lg hover:bg-azure-dark transition-colors w-full"
            >
              Sign In with Microsoft
            </button>

            <p className="mt-4 text-sm text-gray-500">
              This tool requires read-only access to your Azure subscriptions
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-azure-blue">
                ACS Transition Agent
              </h1>
              <p className="text-gray-600 mt-1">
                Azure Communication Services Eligibility Checker
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">
                Signed in as <span className="font-medium">{userProfile?.name}</span>
              </p>
              <button
                onClick={logout}
                className="mt-2 text-sm text-azure-blue hover:text-azure-dark underline"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>

        {/* Scanner */}
        <Scanner onScanComplete={handleScanComplete} />

        {/* Results */}
        {scanResult && <Results scanResult={scanResult} />}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Need help?{' '}
            <a
              href="https://learn.microsoft.com/azure/communication-services/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-azure-blue hover:underline"
            >
              Visit Azure Communication Services Documentation
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
