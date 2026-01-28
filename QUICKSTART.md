# Quick Start Guide

Get the ACS Transition Agent running in 5 minutes!

## Step 1: Install Dependencies

```bash
npm install
```

## Step 2: Set Up Azure AD App

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in:
   - Name: `ACS Transition Agent`
   - Redirect URI: `http://localhost:3000`
5. Click **Register**
6. Note your **Application (client) ID** and **Directory (tenant) ID**

## Step 3: Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Azure Service Management**
4. Check **user_impersonation**
5. Click **Add permissions**
6. Click **Grant admin consent** (requires admin)

## Step 4: Create Environment File

Copy the example environment file:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and add your values:

```
AZURE_CLIENT_ID=your-client-id-from-step-2
AZURE_TENANT_ID=your-tenant-id-from-step-2
NEXT_PUBLIC_REDIRECT_URI=http://localhost:3000
```

## Step 5: Run the App

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Step 6: Use the Tool

1. Click **Sign In with Microsoft**
2. Grant permissions when prompted
3. Click **Start Scan** to scan your subscriptions
4. View the results and export reports

## Troubleshooting

### "Access token is required" error
- Make sure you've granted API permissions and admin consent in Step 3

### "No resources found"
- Ensure you have Azure Communication Services resources in your subscription
- Check that you have at least Reader access to the subscription

### Authentication popup blocked
- Allow popups for localhost:3000 in your browser

### CORS errors
- Make sure you're running on localhost:3000 (not 127.0.0.1)
- Update your Azure AD app redirect URI if needed

## Next Steps

- Customize retiring features in [src/config/retiring-features.ts](src/config/retiring-features.ts)
- Deploy to Azure Static Web Apps or App Service
- Add more metrics or SDK detection criteria
- Integrate with your CI/CD pipeline

## Need Help?

See the full [README.md](README.md) for detailed documentation and architecture information.
