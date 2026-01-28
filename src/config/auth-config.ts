import { Configuration, LogLevel } from '@azure/msal-browser';

// MSAL configuration for Azure AD authentication
export const msalConfig: Configuration = {
  auth: {
    clientId: process.env.AZURE_CLIENT_ID || '',
    authority: `https://login.microsoftonline.com/${process.env.AZURE_TENANT_ID || 'common'}`,
    redirectUri: process.env.NEXT_PUBLIC_REDIRECT_URI || 'http://localhost:3000',
  },
  cache: {
    cacheLocation: 'sessionStorage',
    storeAuthStateInCookie: false,
  },
  system: {
    loggerOptions: {
      loggerCallback: (level, message, containsPii) => {
        if (containsPii) {
          return;
        }
        switch (level) {
          case LogLevel.Error:
            console.error(message);
            return;
          case LogLevel.Info:
            console.info(message);
            return;
          case LogLevel.Verbose:
            console.debug(message);
            return;
          case LogLevel.Warning:
            console.warn(message);
            return;
        }
      },
    },
  },
};

// Scopes required for Azure Resource Manager access
export const loginRequest = {
  scopes: [
    'https://management.azure.com/user_impersonation',
    'User.Read',
  ],
};

// Additional scopes for specific APIs
export const apiScopes = {
  azureManagement: ['https://management.azure.com/user_impersonation'],
  microsoftGraph: ['https://graph.microsoft.com/.default'],
};
