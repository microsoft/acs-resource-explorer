[[_TOC_]]

# Azure Communication Services Email - Migration Guide

**Document Version:** 1.0
**Last Updated:** January 2026
**Target Audience:** Third-party developers, ISVs, and Partners
**Wiki Path:** SPOOL/_wiki/wikis/SPOOL.wiki/9164/SPOOL

---

## Executive Summary

Azure Communication Services (ACS) Email will be **retired 36 months after official notification** (target: December 31, 2027). This guide provides comprehensive instructions for migrating to Microsoft 365 High-Volume Email (HVE).

### Key Points

:warning: **No new features** will be added to ACS Email
:no_entry_sign: **No new deployments** are allowed
:calendar: **36-month timeline** for complete migration
:white_check_mark: **Microsoft 365 HVE supported migration path** available
:arrows_counterclockwise: **Backward compatibility** maintained until sunset

### Quick Decision Matrix

| Your Scenario | Recommended Path | Estimated Effort |
|:--------------|:-----------------|:-----------------|
| High-volume transactional email (>10k/day) | Microsoft 365 HVE (multiple users) | Medium-High |
| Marketing emails with analytics | Microsoft 365 HVE | Medium |
| Low-volume transactional (<1k/day) | Microsoft 365 HVE | Medium |
| Internal notifications only | Microsoft 365 HVE | Low-Medium |
| Complex email workflows | Microsoft 365 HVE | Medium-High |

---

## Retirement Overview

### Timeline

```
┌─────────────────────────────────────────────────────────────┐
│                    36-Month Timeline                         │
├─────────────────────────────────────────────────────────────┤
│ Month 0:  Official retirement announcement                   │
│ Month 3:  Assessment and planning phase                      │
│ Month 6:  Begin migration to new platform                    │
│ Month 12: First wave migrations complete                     │
│ Month 24: All migrations should be underway                  │
│ Month 33: Final migration deadline reminder                  │
│ Month 36: ACS Email fully sunset                             │
└─────────────────────────────────────────────────────────────┘
```

### What's Changing

| Feature | Current Status | Post-Retirement |
|:--------|:--------------|:----------------|
| ACS Email API | :white_check_mark: Available | :x: Decommissioned |
| ACS Email SDK | :white_check_mark: Available | :x: Decommissioned |
| Email domains | :white_check_mark: Active | :x: Removed |
| Existing emails in flight | :white_check_mark: Processed | :warning: May be rejected |
| Technical support | :white_check_mark: Full support | :warning: Deprecation support only |

### Applicability

| Audience | Applies | Action Required |
|:---------|:--------|:----------------|
| Third-party application developers | :white_check_mark: Yes | Migrate to Microsoft 365 HVE |
| ISVs and Partners | :white_check_mark: Yes | Migrate customer workloads |
| First-party (Microsoft) workloads | :x: No | Separate 1P migration path |
| New ACS Email deployments | :x: No | Use Microsoft 365 HVE from day 1 |

---

## Impact Assessment

### Step 1: Identify Current Usage

Run this PowerShell script to assess your ACS Email usage:

```powershell
# ACS Email Usage Assessment Script
# Requires: Az PowerShell module

Connect-AzAccount

$subscriptions = Get-AzSubscription
$acsEmailResources = @()

foreach ($subscription in $subscriptions) {
    Set-AzContext -SubscriptionId $subscription.Id

    # Find ACS resources
    $acsResources = Get-AzResource -ResourceType "Microsoft.Communication/CommunicationServices"

    foreach ($resource in $acsResources) {
        # Check for email domains
        $emailDomains = Get-AzResource -ResourceGroupName $resource.ResourceGroupName `
                                       -ResourceType "Microsoft.Communication/EmailServices/Domains"

        if ($emailDomains) {
            $acsEmailResources += [PSCustomObject]@{
                SubscriptionName = $subscription.Name
                SubscriptionId = $subscription.Id
                ResourceGroup = $resource.ResourceGroupName
                ResourceName = $resource.Name
                Location = $resource.Location
                EmailDomains = $emailDomains.Count
            }
        }
    }
}

# Display results
$acsEmailResources | Format-Table -AutoSize

# Export to CSV
$acsEmailResources | Export-Csv -Path "ACS_Email_Resources.csv" -NoTypeInformation

Write-Host "`nTotal ACS Email resources found: $($acsEmailResources.Count)" -ForegroundColor Cyan
```

### Step 2: Analyze Email Metrics

Use Azure Monitor to gather usage metrics:

```bash
# Azure CLI command to get email metrics (last 30 days)
az monitor metrics list \
  --resource /subscriptions/{subscription-id}/resourceGroups/{rg-name}/providers/Microsoft.Communication/CommunicationServices/{resource-name} \
  --metric "EmailMessagesSent" \
  --start-time 2024-12-01T00:00:00Z \
  --end-time 2024-12-31T23:59:59Z \
  --interval PT1H \
  --aggregation Total \
  --output table
```

### Step 3: Document Your Email Workflow

Complete this assessment checklist:

- [ ] Email volume per day/month
- [ ] Email types (transactional, marketing, notifications)
- [ ] Custom email templates in use
- [ ] Email tracking and analytics requirements
- [ ] Compliance requirements (GDPR, HIPAA, etc.)
- [ ] Sender domains and authentication (SPF, DKIM, DMARC)
- [ ] Integration points (applications, services, APIs)
- [ ] Retry logic and error handling
- [ ] Email scheduling requirements
- [ ] Attachment handling

---

## Migration Path: Microsoft 365 High-Volume Email

### Overview

Microsoft 365 High-Volume Email (HVE) provides email capabilities within the Microsoft 365 ecosystem, offering seamless integration with your organization's existing Microsoft services.

**Best for:**
- Organizations already using Microsoft 365
- All volume ranges (scale with multiple licensed users)
- Transactional and marketing emails
- Internal and external notifications
- Enterprise compliance requirements

### Feature Comparison

| Feature | Microsoft 365 HVE | ACS Email (Current) |
|:--------|:------------------|:--------------------|
| **Max Daily Volume** | 5,000/user/day (scale with users) | 10,000/day |
| **Email Analytics** | Basic (via admin center) | Basic |
| **Template Engine** | Limited (HTML support) | No |
| **API Access** | Graph API | REST API |
| **Webhook Support** | Limited (via subscriptions) | Yes |
| **Custom Domains** | Yes | Yes |
| **Pricing Model** | Per-user license (E3/E5) | Pay-as-you-go |
| **SLA** | 99.9% | 99.9% |
| **Global Infrastructure** | Yes | Yes |
| **Migration Effort** | Medium | N/A |
| **Microsoft Support** | Full enterprise support | Limited |

---

## Pre-Migration Planning

### 1. Create Migration Team

Assign roles and responsibilities:

| Role | Responsibilities |
|:-----|:----------------|
| **Project Manager** | Overall migration coordination |
| **Technical Lead** | Architecture and implementation |
| **DevOps Engineer** | Infrastructure and deployment |
| **QA Engineer** | Testing and validation |
| **Security Engineer** | Security and compliance review |

### 2. Create Migration Timeline

Sample 12-week migration timeline:

| Week | Activities |
|:-----|:-----------|
| Week 1-2 | Assessment and planning |
| Week 3-4 | Microsoft 365 setup and configuration |
| Week 5-6 | Development environment migration |
| Week 7-8 | Code migration and testing |
| Week 9-10 | Staging environment deployment |
| Week 11 | Production pilot (10% traffic) |
| Week 12 | Full production migration |
| Week 13+ | Monitoring and optimization |

### 3. Set Up Parallel Environment

:clipboard: **Best Practices:**
- Keep ACS Email running during migration
- Route subset of traffic to Microsoft 365 HVE for testing
- Monitor both systems for comparison
- Plan rollback procedure

### 4. Compliance & Security Review

- [ ] Review data residency requirements
- [ ] Verify Microsoft 365 meets compliance standards
- [ ] Update privacy policies and terms of service
- [ ] Conduct security assessment
- [ ] Update vendor risk management documents

---

## Migration Steps

### Step 1: Prerequisites

**Requirements:**
- Active Microsoft 365 subscription (E3/E5 or Business Premium)
- Global Administrator or Exchange Administrator role
- Azure AD application registration
- Sufficient licensed users for email volume (5,000 emails/day per user)

#### Calculate Required Users

```typescript
// Calculate number of licensed users needed
function calculateRequiredUsers(dailyEmailVolume: number): number {
  const emailsPerUserPerDay = 5000;
  return Math.ceil(dailyEmailVolume / emailsPerUserPerDay);
}

// Example: 15,000 emails per day requires 3 licensed users
const requiredUsers = calculateRequiredUsers(15000);
console.log(`Required licensed users: ${requiredUsers}`);
```

### Step 2: Set Up Azure AD Application

#### 2.1 Register Azure AD Application

```bash
# Using Azure CLI
az ad app create \
  --display-name "Email Service Application" \
  --sign-in-audience AzureADMyOrg

# Note the Application (client) ID
```

#### 2.2 Configure API Permissions

Required Microsoft Graph permissions:
- `Mail.Send` (Application permission)
- `User.Read.All` (Application permission)

```bash
# Add Microsoft Graph permissions
az ad app permission add \
  --id <app-id> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Role

# Add User.Read.All permission
az ad app permission add \
  --id <app-id> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions df021288-bdef-4463-88db-98f22de89214=Role
```

#### 2.3 Grant Admin Consent

```bash
az ad app permission admin-consent --id <app-id>
```

#### 2.4 Create Client Secret

```bash
az ad app credential reset \
  --id <app-id> \
  --append

# Save the client secret securely - it's shown only once
```

### Step 3: Configure Sender Mailboxes

Create dedicated mailboxes for sending (e.g., noreply@contoso.com, notifications@contoso.com):

```powershell
# Connect to Exchange Online
Connect-ExchangeOnline

# Create shared mailbox for sending
New-Mailbox -Shared -Name "Notifications" -DisplayName "Notifications" `
  -Alias notifications -PrimarySmtpAddress notifications@contoso.com

# Grant SendAs permission to the application
Add-MailboxPermission -Identity notifications@contoso.com `
  -User <app-name> -AccessRights SendAs
```

### Step 4: Code Migration

# [TypeScript](#tab/typescript)

**Before (ACS Email):**

```typescript
// ACS Email - OLD CODE
import { EmailClient } from "@azure/communication-email";

const connectionString = process.env.ACS_CONNECTION_STRING;
const client = new EmailClient(connectionString);

async function sendEmail() {
  const emailMessage = {
    senderAddress: "noreply@contoso.com",
    content: {
      subject: "Welcome to Contoso",
      plainText: "Hello! Welcome to our service.",
      html: "<html><h1>Welcome!</h1><p>Hello! Welcome to our service.</p></html>"
    },
    recipients: {
      to: [{ address: "customer@example.com" }]
    }
  };

  const poller = await client.beginSend(emailMessage);
  const response = await poller.pollUntilDone();
  console.log("Email sent:", response);
}
```

**After (Microsoft 365 HVE):**

```typescript
// Microsoft 365 HVE - NEW CODE
import { Client } from "@microsoft/microsoft-graph-client";
import { ClientSecretCredential } from "@azure/identity";

const credential = new ClientSecretCredential(
  process.env.TENANT_ID!,
  process.env.CLIENT_ID!,
  process.env.CLIENT_SECRET!
);

const client = Client.initWithMiddleware({
  authProvider: {
    getAccessToken: async () => {
      const token = await credential.getToken("https://graph.microsoft.com/.default");
      return token.token;
    }
  }
});

async function sendEmail() {
  const sendMail = {
    message: {
      subject: "Welcome to Contoso",
      body: {
        contentType: "HTML",
        content: "<html><h1>Welcome!</h1><p>Hello! Welcome to our service.</p></html>"
      },
      toRecipients: [
        {
          emailAddress: {
            address: "customer@example.com"
          }
        }
      ]
    },
    saveToSentItems: "false"
  };

  try {
    await client
      .api('/users/noreply@contoso.com/sendMail')
      .post(sendMail);

    console.log('Email sent successfully');
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}
```

# [C#](#tab/csharp)

**Before (ACS Email):**

```csharp
using Azure.Communication.Email;

var client = new EmailClient(connectionString);
var emailContent = new EmailContent("Order Confirmation")
{
    PlainText = "Your order has been confirmed.",
    Html = "<p>Your order has been confirmed.</p>"
};

var recipients = new EmailRecipients(new List<EmailAddress>
{
    new EmailAddress("customer@example.com")
});

var message = new EmailMessage("noreply@contoso.com", recipients, emailContent);
var result = await client.SendAsync(WaitUntil.Started, message);
```

**After (Microsoft 365 HVE):**

```csharp
using Microsoft.Graph;
using Azure.Identity;

var credential = new ClientSecretCredential(
    tenantId, clientId, clientSecret);

var graphClient = new GraphServiceClient(credential);

var message = new Message
{
    Subject = "Order Confirmation",
    Body = new ItemBody
    {
        ContentType = BodyType.Html,
        Content = "<p>Your order has been confirmed.</p>"
    },
    ToRecipients = new List<Recipient>
    {
        new Recipient
        {
            EmailAddress = new EmailAddress
            {
                Address = "customer@example.com"
            }
        }
    }
};

await graphClient.Users["noreply@contoso.com"]
    .SendMail(message, false)
    .Request()
    .PostAsync();
```

# [Python](#tab/python)

**Before (ACS Email):**

```python
from azure.communication.email import EmailClient

client = EmailClient.from_connection_string(connection_string)

message = {
    "content": {
        "subject": "Invoice",
        "plainText": "Your invoice is attached.",
    },
    "recipients": {
        "to": [{"address": "customer@example.com"}]
    },
    "senderAddress": "billing@contoso.com",
}

poller = client.begin_send(message)
result = poller.result()
```

**After (Microsoft 365 HVE):**

```python
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress

credential = ClientSecretCredential(
    tenant_id=os.getenv('TENANT_ID'),
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET')
)

client = GraphServiceClient(credential)

async def send_email():
    message = Message()
    message.subject = "Invoice"
    message.body = ItemBody()
    message.body.content_type = BodyType.Html
    message.body.content = "<p>Your invoice is attached.</p>"

    to_recipient = Recipient()
    to_recipient.email_address = EmailAddress()
    to_recipient.email_address.address = "customer@example.com"
    message.to_recipients = [to_recipient]

    await client.users.by_user_id('billing@contoso.com').send_mail.post(
        body={'message': message, 'save_to_sent_items': False}
    )

    print('Email sent successfully')
```

# [Java](#tab/java)

**Before (ACS Email):**

```java
import com.azure.communication.email.*;
import com.azure.communication.email.models.*;

EmailClient emailClient = new EmailClientBuilder()
    .connectionString(connectionString)
    .buildClient();

EmailMessage message = new EmailMessage()
    .setSenderAddress("noreply@contoso.com")
    .setToRecipients("customer@example.com")
    .setSubject("Welcome")
    .setBodyPlainText("Hello! Welcome to our service.");

SyncPoller<EmailSendResult, EmailSendResult> poller =
    emailClient.beginSend(message);
poller.waitForCompletion();
```

**After (Microsoft 365 HVE):**

```java
import com.microsoft.graph.authentication.TokenCredentialAuthProvider;
import com.microsoft.graph.models.*;
import com.microsoft.graph.requests.GraphServiceClient;
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;

ClientSecretCredential credential = new ClientSecretCredentialBuilder()
    .clientId(clientId)
    .clientSecret(clientSecret)
    .tenantId(tenantId)
    .build();

GraphServiceClient graphClient = GraphServiceClient.builder()
    .authenticationProvider(new TokenCredentialAuthProvider(
        Arrays.asList("https://graph.microsoft.com/.default"),
        credential))
    .buildClient();

Message message = new Message();
message.subject = "Welcome";
ItemBody body = new ItemBody();
body.contentType = BodyType.HTML;
body.content = "<p>Hello! Welcome to our service.</p>";
message.body = body;

Recipient recipient = new Recipient();
EmailAddress emailAddress = new EmailAddress();
emailAddress.address = "customer@example.com";
recipient.emailAddress = emailAddress;
message.toRecipients = Arrays.asList(recipient);

graphClient.users("noreply@contoso.com")
    .sendMail(UserSendMailParameterSet.newBuilder()
        .withMessage(message)
        .withSaveToSentItems(false)
        .build())
    .buildRequest()
    .post();
```

---

### Step 5: Advanced Features

#### A. Email Templates

Create HTML templates and store them in your application:

```typescript
// Template with placeholders
const emailTemplate = `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #0078D4; color: white; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome {{firstName}}!</h1>
    </div>
    <div class="content">
        <p>Your order #{{orderNumber}} has been confirmed.</p>
        <p>Total: {{orderTotal}}</p>
    </div>
</body>
</html>
`;

// Function to populate template
function populateTemplate(template: string, data: Record<string, string>): string {
  let result = template;
  for (const [key, value] of Object.entries(data)) {
    result = result.replace(new RegExp(`{{${key}}}`, 'g'), value);
  }
  return result;
}

// Send email with template
const htmlContent = populateTemplate(emailTemplate, {
  firstName: 'John',
  orderNumber: '12345',
  orderTotal: '$99.99'
});

await client.api('/users/noreply@contoso.com/sendMail').post({
  message: {
    subject: 'Order Confirmation',
    body: {
      contentType: 'HTML',
      content: htmlContent
    },
    toRecipients: [{ emailAddress: { address: 'customer@example.com' } }]
  },
  saveToSentItems: false
});
```

#### B. Batch Sending

```typescript
// Send multiple emails efficiently using Microsoft Graph batch requests
async function sendBatchEmails(recipients: string[]) {
  const batch = client.createBatch();

  recipients.forEach((email, index) => {
    const sendMail = {
      message: {
        subject: "Batch Notification",
        body: {
          contentType: "HTML",
          content: `<p>Hello ${email}</p>`
        },
        toRecipients: [{ emailAddress: { address: email } }]
      },
      saveToSentItems: "false"
    };

    batch.post(
      `${index}`,
      `/users/noreply@contoso.com/sendMail`,
      sendMail
    );
  });

  const response = await batch.execute();
  console.log('Batch emails sent:', response);
}
```

#### C. Attachments

```typescript
const message = {
  subject: "Invoice Attached",
  body: {
    contentType: "HTML",
    content: "<p>Please find your invoice attached.</p>"
  },
  toRecipients: [
    { emailAddress: { address: "customer@example.com" } }
  ],
  attachments: [
    {
      "@odata.type": "#microsoft.graph.fileAttachment",
      name: "invoice.pdf",
      contentType: "application/pdf",
      contentBytes: base64Content
    }
  ]
};

await client
  .api('/users/billing@contoso.com/sendMail')
  .post({ message, saveToSentItems: false });
```

#### D. Load Balancing Across Multiple Sender Mailboxes

For high-volume scenarios, distribute load across multiple licensed users:

```typescript
// Load balancer for email sending
class EmailLoadBalancer {
  private senderMailboxes = [
    'sender1@contoso.com',
    'sender2@contoso.com',
    'sender3@contoso.com'
  ];
  private currentIndex = 0;

  getNextSender(): string {
    const sender = this.senderMailboxes[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % this.senderMailboxes.length;
    return sender;
  }

  async sendEmail(to: string, subject: string, body: string) {
    const sender = this.getNextSender();

    await client.api(`/users/${sender}/sendMail`).post({
      message: {
        subject,
        body: { contentType: 'HTML', content: body },
        toRecipients: [{ emailAddress: { address: to } }]
      },
      saveToSentItems: false
    });
  }
}

const loadBalancer = new EmailLoadBalancer();
await loadBalancer.sendEmail('customer@example.com', 'Subject', '<p>Body</p>');
```

### Step 6: Environment Configuration

#### Azure Key Vault Integration

```typescript
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();
const secretClient = new SecretClient(
  "https://your-keyvault.vault.azure.net/",
  credential
);

// Retrieve secrets
const tenantId = await secretClient.getSecret("TenantId");
const clientId = await secretClient.getSecret("ClientId");
const clientSecret = await secretClient.getSecret("ClientSecret");

// Use for Graph client authentication
const graphCredential = new ClientSecretCredential(
  tenantId.value,
  clientId.value,
  clientSecret.value
);
```

#### Docker Environment Variables

```dockerfile
# Dockerfile
ENV TENANT_ID=${TENANT_ID}
ENV CLIENT_ID=${CLIENT_ID}
ENV CLIENT_SECRET=${CLIENT_SECRET}
ENV EMAIL_FROM_ADDRESS=noreply@contoso.com
ENV EMAIL_FROM_NAME="Contoso Notifications"
```

### Step 7: Implement Rate Limiting & Retry Logic

#### Rate Limits
- **5,000 messages per day per user**
- **30 messages per minute**

#### Retry Logic with Exponential Backoff

```typescript
async function sendEmailWithRetry(
  emailData: any,
  maxRetries = 3,
  sender = 'noreply@contoso.com'
) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      await client.api(`/users/${sender}/sendMail`).post(emailData);
      return { success: true, attempt: attempt + 1 };
    } catch (error: any) {
      if (error.statusCode === 429) {
        // Rate limit exceeded
        const retryAfter = parseInt(error.headers?.['retry-after']) || Math.pow(2, attempt);
        console.log(`Rate limited. Retrying after ${retryAfter}s (attempt ${attempt + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      } else if (error.statusCode >= 500) {
        // Server error - retry
        const backoff = Math.pow(2, attempt) * 1000;
        console.log(`Server error. Retrying after ${backoff}ms (attempt ${attempt + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, backoff));
      } else {
        // Client error - don't retry
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Step 8: Monitoring & Analytics

#### Application Insights Integration

```typescript
import { TelemetryClient } from "applicationinsights";

const appInsights = new TelemetryClient();

async function sendEmailWithTracking(
  to: string,
  subject: string,
  body: string,
  sender = 'noreply@contoso.com'
) {
  const startTime = Date.now();
  const emailId = crypto.randomUUID();

  try {
    await sendEmailWithRetry({
      message: {
        subject,
        body: { contentType: 'HTML', content: body },
        toRecipients: [{ emailAddress: { address: to } }]
      },
      saveToSentItems: false
    }, 3, sender);

    // Track success
    appInsights.trackEvent({
      name: 'EmailSent',
      properties: {
        to,
        subject,
        provider: 'Microsoft365HVE',
        sender,
        emailId
      }
    });

    appInsights.trackMetric({
      name: 'EmailSendDuration',
      value: Date.now() - startTime
    });

    return { success: true, emailId };
  } catch (error) {
    // Track failure
    appInsights.trackException({
      exception: error as Error,
      properties: { to, subject, sender, emailId }
    });

    throw error;
  }
}
```

### Step 9: Cost Optimization

#### Microsoft 365 Licensing

| License | Email Capability | Price/User/Month | Best For |
|:--------|:----------------|:-----------------|:---------|
| Microsoft 365 E3 | 5,000 emails/day | ~$36 | Enterprise |
| Microsoft 365 E5 | 5,000 emails/day | ~$57 | Enterprise + Security |
| Microsoft 365 Business Premium | 5,000 emails/day | ~$22 | SMB |

#### Cost Calculation

```typescript
function calculateMonthlyCost(
  dailyEmailVolume: number,
  licenseType: 'E3' | 'E5' | 'Business' = 'E3'
): number {
  const emailsPerUserPerDay = 5000;
  const usersNeeded = Math.ceil(dailyEmailVolume / emailsPerUserPerDay);

  const pricePerUser = {
    'E3': 36,
    'E5': 57,
    'Business': 22
  };

  return usersNeeded * pricePerUser[licenseType];
}

// Example: 15,000 emails per day with E3 license
const monthlyCost = calculateMonthlyCost(15000, 'E3');
console.log(`Estimated monthly cost: $${monthlyCost}`);
// Output: Estimated monthly cost: $108 (3 users × $36)
```

---

## Testing & Validation

### Test Strategy

#### Phase 1: Unit Testing

```typescript
// Jest test example
import { sendEmail } from './emailService';
import { Client } from '@microsoft/microsoft-graph-client';

jest.mock('@microsoft/microsoft-graph-client');

describe('Email Service', () => {
  let mockClient: jest.Mocked<Client>;

  beforeEach(() => {
    jest.clearAllMocks();
    mockClient = {
      api: jest.fn().mockReturnThis(),
      post: jest.fn().mockResolvedValue({ statusCode: 202 })
    } as any;
  });

  test('should send email successfully', async () => {
    await sendEmail('test@example.com', 'Test Subject', '<p>Test Body</p>');

    expect(mockClient.api).toHaveBeenCalledWith(
      '/users/noreply@contoso.com/sendMail'
    );
    expect(mockClient.post).toHaveBeenCalled();
  });

  test('should handle rate limiting with retry', async () => {
    mockClient.post
      .mockRejectedValueOnce({ statusCode: 429, headers: { 'retry-after': '1' } })
      .mockResolvedValueOnce({ statusCode: 202 });

    const result = await sendEmailWithRetry(
      { message: { subject: 'Test' } }
    );

    expect(result.success).toBe(true);
    expect(result.attempt).toBe(2);
  });
});
```

#### Phase 2: Integration Testing

```typescript
// Integration test with actual Microsoft Graph API
describe('Microsoft 365 HVE Integration', () => {
  test('should send real email to test account', async () => {
    const result = await client
      .api('/users/test@yourdomain.com/sendMail')
      .post({
        message: {
          subject: 'Integration Test',
          body: {
            contentType: 'Text',
            content: 'This is a test email'
          },
          toRecipients: [
            { emailAddress: { address: 'recipient@yourdomain.com' } }
          ]
        },
        saveToSentItems: false
      });

    expect(result).toBeDefined();
  });
});
```

#### Phase 3: Load Testing

```javascript
// k6 load testing script for Microsoft Graph
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '5m', target: 50 },   // Ramp up to 50 VUs
    { duration: '10m', target: 50 },  // Stay at 50 VUs
    { duration: '5m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'], // 95% of requests under 5s
    http_req_failed: ['rate<0.05'],    // Less than 5% failure rate
  },
};

const TENANT_ID = __ENV.TENANT_ID;
const CLIENT_ID = __ENV.CLIENT_ID;
const CLIENT_SECRET = __ENV.CLIENT_SECRET;

let accessToken = null;

function getAccessToken() {
  if (accessToken) return accessToken;

  const tokenUrl = `https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token`;
  const tokenPayload = {
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    scope: 'https://graph.microsoft.com/.default',
    grant_type: 'client_credentials'
  };

  const response = http.post(tokenUrl, tokenPayload);
  accessToken = JSON.parse(response.body).access_token;
  return accessToken;
}

export default function() {
  const token = getAccessToken();

  const payload = JSON.stringify({
    message: {
      subject: 'Load Test',
      body: {
        contentType: 'Text',
        content: 'Load testing email delivery'
      },
      toRecipients: [
        { emailAddress: { address: 'loadtest@example.com' } }
      ]
    },
    saveToSentItems: false
  });

  const params = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };

  let res = http.post(
    'https://graph.microsoft.com/v1.0/users/sender@contoso.com/sendMail',
    payload,
    params
  );

  check(res, {
    'status is 202': (r) => r.status === 202,
    'no errors': (r) => !r.body.includes('error'),
  });

  sleep(1); // Respect rate limits (30/min = ~2 per second)
}
```

### Validation Checklist

- [ ] All email types tested (transactional, notifications, marketing)
- [ ] Template rendering verified across email clients
- [ ] Attachments working correctly
- [ ] Personalization data populating
- [ ] Rate limiting and retry logic working
- [ ] Load balancing across sender mailboxes
- [ ] SPF/DKIM/DMARC records validated
- [ ] Delivery rates meet baseline requirements
- [ ] Error handling working correctly
- [ ] Monitoring and alerting configured
- [ ] Cost tracking in place
- [ ] Compliance requirements met

### Email Deliverability Testing

```bash
# Test SPF record
nslookup -type=txt yourdomain.com

# Test DKIM
nslookup -type=txt selector1._domainkey.yourdomain.onmicrosoft.com

# Test DMARC
nslookup -type=txt _dmarc.yourdomain.com
```

**Test with these services:**
- [mail-tester.com](https://www.mail-tester.com)
- [mxtoolbox.com/deliverability](https://mxtoolbox.com/deliverability)
- [Google Postmaster Tools](https://postmaster.google.com/)

---

## Rollback Plan

### Preparation

#### 1. Keep ACS Email Active
- Maintain existing ACS resources during migration
- Don't delete domains or resources until fully validated

#### 2. Feature Flags

```typescript
// Use feature flags for gradual rollout
const useM365Email = await featureFlagClient.getFlag('use-m365-email');

if (useM365Email) {
  await sendViaM365(emailData);
} else {
  await sendViaACS(emailData);
}
```

#### 3. Traffic Splitting

```typescript
// Route percentage of traffic to new provider
const rolloutPercentage = 10; // Start with 10%
const useM365 = Math.random() * 100 < rolloutPercentage;

if (useM365) {
  await sendViaM365(emailData);
  telemetry.trackEvent('M365Email', { success: true });
} else {
  await sendViaACS(emailData);
  telemetry.trackEvent('ACSEmail', { success: true });
}
```

### Rollback Triggers

Execute rollback if:
- Email delivery rate drops below 95%
- Error rate exceeds 5%
- Cost exceeds budget by 20%
- Critical compliance issue discovered
- Severe bug in production
- Rate limits consistently exceeded

### Rollback Procedure

#### Immediate Actions (0-15 minutes)

```bash
# Update feature flag to disable Microsoft 365 HVE
az appconfig kv set \
  --name myAppConfig \
  --key use-m365-email \
  --value false \
  --yes

# Restart services to pick up configuration
kubectl rollout restart deployment/email-service
```

#### Communication (15-30 minutes)
- Notify stakeholders of rollback
- Update status page
- Document issues encountered

#### Investigation (30+ minutes)
- Review logs and metrics
- Identify root cause
- Create action plan for re-attempt

---

## Post-Migration

### Week 1: Monitoring

#### Key Metrics to Track

```typescript
// Application Insights custom metrics
const metrics = {
  emailsSent: 0,
  emailsDelivered: 0,
  emailsBounced: 0,
  emailsFailed: 0,
  rateLimitHits: 0,
  averageDeliveryTime: 0,
  costPerEmail: 0
};

// Track daily
appInsights.trackMetric({ name: 'DailyEmailsSent', value: metrics.emailsSent });
appInsights.trackMetric({ name: 'DeliveryRate', value: (metrics.emailsDelivered / metrics.emailsSent) * 100 });
appInsights.trackMetric({ name: 'BounceRate', value: (metrics.emailsBounced / metrics.emailsSent) * 100 });
appInsights.trackMetric({ name: 'RateLimitHitRate', value: (metrics.rateLimitHits / metrics.emailsSent) * 100 });
```

#### Alert Configuration

```yaml
# Azure Monitor alert rules
- name: High Email Bounce Rate
  condition: bounceRate > 5%
  window: 15 minutes
  action: Send notification to ops team

- name: Email Delivery Failure
  condition: failureRate > 10%
  window: 5 minutes
  action: Page on-call engineer

- name: Rate Limit Threshold
  condition: rateLimitHitRate > 20%
  window: 1 hour
  action: Scale up licensed users

- name: High Cost Alert
  condition: monthlyCost > $500
  window: 1 day
  action: Send notification to finance team
```

### Month 1: Optimization

#### 1. Review Delivery Metrics
- Compare against ACS baseline
- Identify and fix deliverability issues
- Optimize send times
- Adjust sender mailbox distribution

#### 2. Cost Analysis

```sql
-- Query to analyze email costs
SELECT
  DATE(timestamp) as date,
  sender_mailbox,
  COUNT(*) as emails_sent,
  COUNT(*) / 5000.0 as user_days_consumed,
  (COUNT(*) / 5000.0) * 36 as estimated_daily_cost
FROM email_logs
WHERE provider = 'Microsoft365HVE'
GROUP BY DATE(timestamp), sender_mailbox
ORDER BY date DESC;
```

#### 3. Performance Tuning
- Optimize batch sizes (max 20 requests per batch)
- Implement connection pooling
- Cache Microsoft Graph access tokens (valid for 1 hour)
- Distribute load across sender mailboxes

#### 4. License Optimization

```typescript
// Monitor usage and adjust licensed users
async function optimizeLicenses() {
  const last30DaysAvg = await getAverageDailyVolume(30);
  const currentUsers = 5; // Current licensed sender mailboxes
  const requiredUsers = Math.ceil(last30DaysAvg / 5000);

  if (requiredUsers < currentUsers) {
    console.log(`Can reduce by ${currentUsers - requiredUsers} licenses`);
  } else if (requiredUsers > currentUsers) {
    console.log(`Need ${requiredUsers - currentUsers} additional licenses`);
  }
}
```

### Decommissioning ACS Email

**Only after:**
- [ ] 30+ days of stable operation on Microsoft 365 HVE
- [ ] All metrics meeting or exceeding targets
- [ ] Stakeholder sign-off obtained
- [ ] Documentation updated
- [ ] Team trained on new platform
- [ ] Cost analysis approved

**Decommission Steps:**

```bash
# 1. Stop sending via ACS (already done)

# 2. Export historical data if needed
az communication email-domain export \
  --resource-group myResourceGroup \
  --email-service-name myEmailService \
  --output-file email-history.json

# 3. Remove domains
az communication email-domain delete \
  --resource-group myResourceGroup \
  --email-service-name myEmailService \
  --domain-name AzureManagedDomain

# 4. Delete ACS Email resources
az communication email-service delete \
  --resource-group myResourceGroup \
  --name myEmailService \
  --yes

# 5. Update documentation and runbooks
# 6. Remove ACS connection strings from Key Vault
# 7. Notify team of decommission completion
```

---

## Frequently Asked Questions

### General Questions

> **Q: Do I have to migrate immediately?**

A: No, you have 36 months from the retirement announcement. However, starting early reduces risk and allows for thorough testing.

> **Q: Will Microsoft help with migration costs?**

A: Migration tooling and documentation are provided at no cost. Some customers may qualify for Azure migration credits - contact your Microsoft account team.

> **Q: Can I continue using ACS Email after the deadline?**

A: No, the service will be completely decommissioned. Plan to complete your migration before the deadline.

> **Q: What if I already have Microsoft 365 licenses?**

A: You can use your existing Microsoft 365 E3/E5 or Business Premium licenses. Each licensed user can send up to 5,000 emails per day.

### Technical Questions

> **Q: How do I migrate email templates?**

A: Microsoft 365 HVE supports HTML email templates. Store templates in your application code and use placeholder replacement before sending. See the Advanced Features section for examples.

> **Q: What about email tracking and analytics?**

A: Microsoft 365 HVE provides basic reporting through the Microsoft 365 Admin Center. For advanced analytics, integrate with Application Insights or your existing analytics platform using custom tracking.

> **Q: How do I handle GDPR compliance?**

A: Microsoft 365 is GDPR compliant. Ensure you:
- Configure data residency in your tenant settings
- Update privacy policies
- Implement unsubscribe mechanisms
- Review Microsoft's Data Processing Agreement

> **Q: What if I have custom email domains?**

A: Microsoft 365 supports custom domains. You'll need to:
1. Add your domain to Microsoft 365
2. Verify domain ownership
3. Configure MX, SPF, DKIM, and DMARC records
4. Create sender mailboxes with your custom domain

> **Q: How do I handle high email volumes (>5,000/day)?**

A: Scale horizontally by:
1. Creating multiple licensed sender mailboxes
2. Implementing load balancing across mailboxes
3. Monitoring usage per mailbox to stay within limits
4. Each user can send 5,000 emails/day

### Cost Questions

> **Q: Will my costs increase?**

A: It depends on your volume:
- Low volume (<5k/day): $36-57/month (1 E3/E5 license)
- Medium volume (5k-15k/day): $72-171/month (2-3 licenses)
- High volume (15k-50k/day): $216-570/month (6-10 licenses)

Compare to your current ACS Email costs to determine ROI.

> **Q: Are there free tiers?**

A: No free tier for Microsoft 365 HVE. You need an active Microsoft 365 E3, E5, or Business Premium subscription.

> **Q: Can I use existing Microsoft 365 licenses?**

A: Yes! If you already have Microsoft 365 licenses, you can use those for email sending at no additional cost (within the 5,000 emails/day/user limit).

> **Q: What about overage charges?**

A: Microsoft 365 HVE uses rate limiting (5,000/day/user) rather than overage charges. If you exceed limits, emails will be throttled. Scale by adding more licensed users.

---

## Support Resources

### Documentation

#### Microsoft 365
- [Graph API - Send Mail](https://learn.microsoft.com/graph/api/user-sendmail)
- [Microsoft Graph Best Practices](https://learn.microsoft.com/graph/best-practices-concept)
- [High-Volume Email Documentation](https://learn.microsoft.com/microsoft-365/compliance/high-volume-email)
- [Microsoft Graph SDK](https://learn.microsoft.com/graph/sdks/sdks-overview)

#### Azure Communication Services
- [Retirement Announcement](https://azure.microsoft.com/updates/)
- [Support Timeline](https://portal.azure.com)

### Community Support

#### Microsoft Q&A
- [Microsoft Graph](https://learn.microsoft.com/answers/tags/158/ms-graph)
- [Microsoft 365](https://learn.microsoft.com/answers/products/m365)

#### Stack Overflow
- [Microsoft Graph Questions](https://stackoverflow.com/questions/tagged/microsoft-graph)
- [Microsoft Graph API](https://stackoverflow.com/questions/tagged/microsoft-graph-api)

#### GitHub
- [Microsoft Graph SDK](https://github.com/microsoftgraph)
- [Microsoft Graph Toolkit](https://github.com/microsoftgraph/microsoft-graph-toolkit)

### Microsoft Support

| Support Type | Details |
|:-------------|:--------|
| **Azure Support** | Open ticket via Azure Portal |
| **Account Team** | Contact your Microsoft account manager |
| **FastTrack** | Available for Enterprise customers with eligible licenses |
| **Premier Support** | Dedicated support for Premier customers |

### Migration Assistance

For complex migrations or enterprise support:
- **Microsoft Consulting Services (MCS)** - Professional migration services
- **Certified Microsoft Partners** - Find partners specializing in Microsoft 365
- **FastTrack Center** - Free deployment assistance for eligible customers

**Contact Links:**
- [Find a Microsoft Partner](https://appsource.microsoft.com/marketplace/partner-dir)
- [FastTrack for Microsoft 365](https://www.microsoft.com/fasttrack/microsoft-365)
- [Microsoft Consulting Services](https://www.microsoft.com/en-us/msservices)

---

## Appendix

### A. DNS Configuration Examples

#### SPF Record
```
v=spf1 include:spf.protection.outlook.com -all
```

#### DKIM Records (Microsoft 365)
Microsoft 365 automatically configures DKIM for your domain. To enable:

```powershell
# Connect to Exchange Online
Connect-ExchangeOnline

# Enable DKIM for your domain
New-DkimSigningConfig -DomainName yourdomain.com -Enabled $true
```

#### DMARC Record
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc@yourdomain.com; fo=1; pct=100
```

### B. Cost Calculator

```typescript
interface CostEstimate {
  dailyVolume: number;
  usersNeeded: number;
  monthlyCost: number;
  costPerEmail: number;
  licenseType: 'E3' | 'E5' | 'Business';
}

function calculateDetailedCost(
  dailyEmailVolume: number,
  licenseType: 'E3' | 'E5' | 'Business' = 'E3'
): CostEstimate {
  const emailsPerUserPerDay = 5000;
  const usersNeeded = Math.ceil(dailyEmailVolume / emailsPerUserPerDay);

  const pricePerUser = {
    'E3': 36,
    'E5': 57,
    'Business': 22
  };

  const monthlyCost = usersNeeded * pricePerUser[licenseType];
  const monthlyEmails = dailyEmailVolume * 30;
  const costPerEmail = monthlyCost / monthlyEmails;

  return {
    dailyVolume: dailyEmailVolume,
    usersNeeded,
    monthlyCost,
    costPerEmail,
    licenseType
  };
}

// Example usage
console.log('Cost Analysis:');
console.log('Low Volume (2k/day):', calculateDetailedCost(2000, 'E3'));
console.log('Medium Volume (10k/day):', calculateDetailedCost(10000, 'E3'));
console.log('High Volume (25k/day):', calculateDetailedCost(25000, 'E3'));

/* Output:
Low Volume (2k/day): {
  dailyVolume: 2000,
  usersNeeded: 1,
  monthlyCost: 36,
  costPerEmail: 0.0006,
  licenseType: 'E3'
}
Medium Volume (10k/day): {
  dailyVolume: 10000,
  usersNeeded: 2,
  monthlyCost: 72,
  costPerEmail: 0.00024,
  licenseType: 'E3'
}
High Volume (25k/day): {
  dailyVolume: 25000,
  usersNeeded: 5,
  monthlyCost: 180,
  costPerEmail: 0.00024,
  licenseType: 'E3'
}
*/
```

### C. Sample Migration Runbook

```yaml
title: ACS Email to Microsoft 365 HVE Migration Runbook
version: 1.0
owner: Platform Team
last_updated: January 2026

pre-migration:
  - task: Inventory current email usage
    command: "node scripts/inventory-acs-email.js"
    duration: 2 hours

  - task: Calculate required Microsoft 365 licenses
    steps:
      - Review average daily email volume
      - Calculate users needed (volume / 5000)
      - Purchase additional licenses if needed
    duration: 1 week (procurement)

  - task: Set up Azure AD application
    steps:
      - Register application
      - Configure Graph API permissions
      - Grant admin consent
      - Create client secret
    duration: 1 hour

  - task: Create sender mailboxes
    steps:
      - Create shared mailboxes
      - Configure SendAs permissions
      - Verify mailbox configuration
    duration: 2 hours

  - task: Configure custom domains
    steps:
      - Add domain to Microsoft 365
      - Configure DNS records
      - Verify domain ownership
      - Wait for DNS propagation
    duration: 2-3 days

migration:
  - task: Deploy code changes
    steps:
      - Update dependencies (Microsoft Graph SDK)
      - Implement new email service
      - Update configuration
      - Deploy to dev environment
      - Run unit tests
      - Deploy to staging
      - Run integration tests
      - Deploy to production
    rollback: "Revert to previous deployment"
    duration: 2 weeks

  - task: Enable feature flag
    command: "az appconfig kv set --key use-m365-email --value true"
    validation: "Check metrics dashboard for delivery rates"
    duration: 30 minutes

  - task: Monitor initial traffic (10%)
    duration: 3 days
    success_criteria:
      - Delivery rate > 95%
      - Error rate < 5%
      - No rate limiting issues

  - task: Increase traffic gradually
    steps:
      - Increase to 25%
      - Monitor for 2 days
      - Increase to 50%
      - Monitor for 2 days
      - Increase to 100%
    duration: 1 week

post-migration:
  - task: Monitor for 30 days
    alerts:
      - Delivery rate
      - Error rate
      - Rate limit hits
      - Cost tracking

  - task: Optimize and tune
    activities:
      - Adjust load balancing
      - Optimize batch sizes
      - Review license utilization
    duration: 2 weeks

  - task: Decommission ACS resources
    when: "After 30 days of stable operation"
    steps:
      - Export historical data
      - Delete ACS Email domains
      - Delete ACS Email resources
      - Update documentation
      - Notify team
    duration: 1 day
```

### D. Compliance Checklist

- [ ] Data Processing Agreement reviewed (Microsoft 365)
- [ ] Data residency configured in tenant settings
- [ ] GDPR compliance verified
- [ ] HIPAA compliance reviewed (if applicable)
- [ ] SOC 2/ISO certifications verified
- [ ] Privacy policy updated
- [ ] Terms of service updated
- [ ] Customer notification sent
- [ ] Opt-out mechanism implemented
- [ ] Data retention policy aligned
- [ ] Security assessment completed
- [ ] Vendor risk assessment updated
- [ ] Microsoft 365 security baseline applied

### E. Microsoft Graph API Scopes Reference

| Permission | Type | Description | Required For |
|:-----------|:-----|:------------|:-------------|
| Mail.Send | Application | Send mail as any user | Sending emails |
| User.Read.All | Application | Read all users | Accessing sender mailboxes |
| Mail.ReadWrite | Delegated | Read and write user mail | User context sending |

---

## Related Wiki Pages

:link: [SPOOL Main Wiki](https://skype.visualstudio.com/SPOOL/_wiki/wikis/SPOOL.wiki/9164/SPOOL)
:link: [Azure Communication Services Overview](#)
:link: [Email Service Architecture](#)
:link: [Migration Best Practices](#)
:link: [Microsoft 365 Administration](#)
:link: [Microsoft Graph API Documentation](#)

---

**Document End**

:email: **For questions or support, contact:** acs-migration-support@microsoft.com

:calendar: **Last Updated:** January 2026
:page_facing_up: **Document Version:** 1.0
:globe_with_meridians: **Wiki Path:** SPOOL/_wiki/wikis/SPOOL.wiki/9164/SPOOL
