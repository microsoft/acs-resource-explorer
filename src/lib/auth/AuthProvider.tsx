'use client';

import { MsalProvider } from '@azure/msal-react';
import { PublicClientApplication } from '@azure/msal-browser';
import { msalConfig } from '@/config/auth-config';
import { ReactNode, useMemo } from 'react';

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const msalInstance = useMemo(() => {
    return new PublicClientApplication(msalConfig);
  }, []);

  return <MsalProvider instance={msalInstance}>{children}</MsalProvider>;
}
