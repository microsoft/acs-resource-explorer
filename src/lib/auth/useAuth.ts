'use client';

import { useMsal } from '@azure/msal-react';
import { AccountInfo } from '@azure/msal-browser';
import { loginRequest } from '@/config/auth-config';
import { UserProfile } from '@/types';

export function useAuth() {
  const { instance, accounts } = useMsal();

  const login = async () => {
    try {
      await instance.loginPopup(loginRequest);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await instance.logoutPopup();
    } catch (error) {
      console.error('Logout failed:', error);
      throw error;
    }
  };

  const getAccessToken = async (scopes: string[] = loginRequest.scopes) => {
    const account = accounts[0];
    if (!account) {
      throw new Error('No account found. Please login first.');
    }

    try {
      const response = await instance.acquireTokenSilent({
        scopes,
        account,
      });
      return response.accessToken;
    } catch (error) {
      // If silent token acquisition fails, try interactive
      const response = await instance.acquireTokenPopup({
        scopes,
        account,
      });
      return response.accessToken;
    }
  };

  const getUserProfile = (): UserProfile | null => {
    const account = accounts[0];
    if (!account) return null;

    return {
      name: account.name || '',
      email: account.username || '',
      tenantId: account.tenantId || '',
    };
  };

  return {
    login,
    logout,
    getAccessToken,
    getUserProfile,
    isAuthenticated: accounts.length > 0,
    account: accounts[0] as AccountInfo | undefined,
  };
}
