# Azure Communication Services Email - Migration Guide

**Document Version:** 1.0
**Last Updated:** January 2026
**Target Audience:** Third-party developers, ISVs, and Partners

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Retirement Overview](#retirement-overview)
3. [Impact Assessment](#impact-assessment)
4. [Migration Paths](#migration-paths)
5. [Pre-Migration Planning](#pre-migration-planning)
6. [Migration Path 1: SendGrid](#migration-path-1-sendgrid-recommended)
7. [Migration Path 2: Microsoft 365 HVE](#migration-path-2-microsoft-365-high-volume-email)
8. [Code Migration Examples](#code-migration-examples)
9. [Testing & Validation](#testing--validation)
10. [Rollback Plan](#rollback-plan)
11. [Post-Migration](#post-migration)
12. [FAQ](#frequently-asked-questions)
13. [Support Resources](#support-resources)

---

## Executive Summary

Azure Communication Services (ACS) Email will be **retired 36 months after official notification** (target: December 31, 2027). This guide provides comprehensive instructions for migrating to supported alternatives.

### Key Points

- ⚠️ **No new features** will be added to ACS Email
- ⛔ **No new deployments** are allowed
- 📅 **36-month timeline** for complete migration
- ✅ **Two supported migration paths** available
- 🔄 **Backward compatibility** maintained until sunset

### Quick Decision Matrix

| Your Scenario | Recommended Path | Estimated Effort |
|--------------|------------------|------------------|
| High-volume transactional email (>10k/day) | SendGrid or external provider | Medium-High |
| Marketing emails with analytics | SendGrid or external provider | Medium-High |
| Low-volume transactional (<1k/day) | Microsoft 365 HVE | Medium |
| Internal notifications only | Microsoft 365 HVE | Low-Medium |
| Complex email workflows | SendGrid or external provider | High |

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
|---------|---------------|-----------------|
| ACS Email API | ✅ Available | ❌ Decommissioned |
| ACS Email SDK | ✅ Available | ❌ Decommissioned |
| Email domains | ✅ Active | ❌ Removed |
| Existing emails in flight | ✅ Processed | ⚠️ May be rejected |
| Technical support | ✅ Full support | ⚠️ Deprecation support only |

### Applicability

| Audience | Applies | Action Required |
|----------|---------|-----------------|
| Third-party application developers | ✅ Yes | Migrate to alternative |
| ISVs and Partners | ✅ Yes | Migrate customer workloads |
| First-party (Microsoft) workloads | ❌ No | Separate 1P migration path |
| New ACS Email deployments | ❌ No | Use alternatives from day 1 |

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

## Migration Paths

### Path Comparison

| Feature | SendGrid | Microsoft 365 HVE | ACS Email (Current) |
|---------|----------|-------------------|---------------------|
| **Max Daily Volume** | Unlimited (tiered) | 5,000/user/day | 10,000/day |
| **Email Analytics** | Advanced | Basic | Basic |
| **Template Engine** | Yes | Limited | No |
| **API Access** | REST API | Graph API | REST API |
| **Webhook Support** | Yes | Limited | Yes |
| **Custom Domains** | Yes | Yes | Yes |
| **Pricing Model** | Pay-as-you-go | Per-user license | Pay-as-you-go |
| **SLA** | 99.95% | 99.9% | 99.9% |
| **Global Infrastructure** | Yes | Yes | Yes |
| **Migration Effort** | Medium-High | Medium | N/A |

---

## Pre-Migration Planning

### 1. Create Migration Team

Assign roles and responsibilities:

- **Project Manager:** Overall migration coordination
- **Technical Lead:** Architecture and implementation
- **DevOps Engineer:** Infrastructure and deployment
- **QA Engineer:** Testing and validation
- **Security Engineer:** Security and compliance review

### 2. Create Migration Timeline

Sample 12-week migration timeline:

```
Week 1-2:   Assessment and planning
Week 3-4:   Provider selection and account setup
Week 5-6:   Development environment migration
Week 7-8:   Code migration and testing
Week 9-10:  Staging environment deployment
Week 11:    Production pilot (10% traffic)
Week 12:    Full production migration
Week 13+:   Monitoring and optimization
```

### 3. Set Up Parallel Environment

- Keep ACS Email running during migration
- Route subset of traffic to new provider for testing
- Monitor both systems for comparison
- Plan rollback procedure

### 4. Compliance & Security Review

- Review data residency requirements
- Verify new provider meets compliance standards
- Update privacy policies and terms of service
- Conduct security assessment
- Update vendor risk management documents

---

## Migration Path 1: SendGrid (Recommended)

### Overview

SendGrid is a cloud-based email delivery platform with advanced features for transactional and marketing emails.

**Best for:**
- High-volume email (>10,000 emails/day)
- Advanced analytics and reporting
- Marketing campaigns
- Complex email workflows

### Step 1: Account Setup

1. **Create SendGrid Account**
   ```bash
   # Sign up at https://sendgrid.com
   # Choose appropriate plan based on volume
   ```

2. **Verify Sender Identity**
   - Navigate to Settings → Sender Authentication
   - Add and verify your domain
   - Configure SPF and DKIM records

   **DNS Records to Add:**
   ```
   # SPF Record
   TXT @ "v=spf1 include:sendgrid.net ~all"

   # DKIM Records (provided by SendGrid)
   CNAME s1._domainkey.yourdomain.com → s1.domainkey.u12345.wl.sendgrid.net
   CNAME s2._domainkey.yourdomain.com → s2.domainkey.u12345.wl.sendgrid.net
   ```

3. **Create API Key**
   - Navigate to Settings → API Keys
   - Click "Create API Key"
   - Select "Full Access" or customize permissions
   - **Save the API key securely** (shown only once)

### Step 2: Install SDK

**Node.js:**
```bash
npm install @sendgrid/mail
```

**Python:**
```bash
pip install sendgrid
```

**.NET:**
```bash
dotnet add package SendGrid
```

**Java:**
```xml
<dependency>
    <groupId>com.sendgrid</groupId>
    <artifactId>sendgrid-java</artifactId>
    <version>4.9.3</version>
</dependency>
```

### Step 3: Code Migration

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

**After (SendGrid):**

```typescript
// SendGrid - NEW CODE
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendEmail() {
  const msg = {
    to: 'customer@example.com',
    from: 'noreply@contoso.com',
    subject: 'Welcome to Contoso',
    text: 'Hello! Welcome to our service.',
    html: '<html><h1>Welcome!</h1><p>Hello! Welcome to our service.</p></html>',
  };

  try {
    const response = await sgMail.send(msg);
    console.log('Email sent:', response[0].statusCode);
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}
```

### Step 4: Advanced Features

**A. Using Email Templates**

```typescript
// SendGrid Dynamic Templates
const msg = {
  to: 'customer@example.com',
  from: 'noreply@contoso.com',
  templateId: 'd-xyz123abc456def789',
  dynamicTemplateData: {
    firstName: 'John',
    orderNumber: '12345',
    orderTotal: '$99.99'
  }
};

await sgMail.send(msg);
```

**B. Batch Sending**

```typescript
// Send to multiple recipients
const msg = {
  to: ['user1@example.com', 'user2@example.com', 'user3@example.com'],
  from: 'noreply@contoso.com',
  subject: 'Batch Email',
  html: '<p>This is a batch email</p>'
};

await sgMail.send(msg);
```

**C. Attachments**

```typescript
const msg = {
  to: 'customer@example.com',
  from: 'noreply@contoso.com',
  subject: 'Invoice Attached',
  html: '<p>Please find your invoice attached.</p>',
  attachments: [
    {
      content: Buffer.from('Invoice data...').toString('base64'),
      filename: 'invoice.pdf',
      type: 'application/pdf',
      disposition: 'attachment'
    }
  ]
};

await sgMail.send(msg);
```

**D. Webhook Configuration**

Set up webhooks to receive delivery events:

```typescript
// Express.js webhook handler
import express from 'express';

const app = express();
app.use(express.json());

app.post('/sendgrid/webhook', (req, res) => {
  const events = req.body;

  events.forEach(event => {
    console.log(`Email ${event.email}: ${event.event}`);

    switch(event.event) {
      case 'delivered':
        // Update database: email delivered
        break;
      case 'bounce':
        // Handle bounce
        break;
      case 'open':
        // Track email open
        break;
      case 'click':
        // Track link click
        break;
    }
  });

  res.status(200).send('OK');
});
```

### Step 5: Environment Configuration

**Azure Key Vault Integration:**

```typescript
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();
const client = new SecretClient(
  "https://your-keyvault.vault.azure.net/",
  credential
);

const sendGridKey = await client.getSecret("SendGridApiKey");
sgMail.setApiKey(sendGridKey.value);
```

**Docker Environment Variables:**

```dockerfile
# Dockerfile
ENV SENDGRID_API_KEY=${SENDGRID_API_KEY}
ENV EMAIL_FROM_ADDRESS=noreply@contoso.com
ENV EMAIL_FROM_NAME="Contoso Notifications"
```

### Step 6: Monitoring & Analytics

**Application Insights Integration:**

```typescript
import { TelemetryClient } from "applicationinsights";

const appInsights = new TelemetryClient();

async function sendEmailWithTracking(to: string, subject: string) {
  const startTime = Date.now();

  try {
    await sgMail.send({ to, from: 'noreply@contoso.com', subject, html: '...' });

    appInsights.trackEvent({
      name: 'EmailSent',
      properties: { to, subject, provider: 'SendGrid' }
    });

    appInsights.trackMetric({
      name: 'EmailSendDuration',
      value: Date.now() - startTime
    });
  } catch (error) {
    appInsights.trackException({ exception: error as Error });
    throw error;
  }
}
```

### Step 7: Cost Optimization

**SendGrid Pricing Tiers:**

| Plan | Volume | Price/Month | Best For |
|------|--------|-------------|----------|
| Free | 100/day | $0 | Testing |
| Essentials | 50,000/month | $19.95 | Small apps |
| Pro | 100,000/month | $89.95 | Growing businesses |
| Premier | Custom | Custom | Enterprise |

**Cost Comparison Script:**

```typescript
// Calculate monthly costs based on volume
function calculateSendGridCost(monthlyVolume: number): number {
  if (monthlyVolume <= 3000) return 0; // Free tier
  if (monthlyVolume <= 50000) return 19.95;
  if (monthlyVolume <= 100000) return 89.95;

  // Premier pricing (example)
  const additionalEmails = monthlyVolume - 100000;
  const additionalCost = (additionalEmails / 1000) * 0.85;
  return 89.95 + additionalCost;
}

const currentVolume = 75000;
console.log(`Estimated monthly cost: $${calculateSendGridCost(currentVolume)}`);
```

---

## Migration Path 2: Microsoft 365 High-Volume Email

### Overview

Microsoft 365 High-Volume Email (HVE) provides email capabilities within the Microsoft 365 ecosystem.

**Best for:**
- Organizations already using Microsoft 365
- Low to moderate volume (<5,000 emails/day per user)
- Basic transactional emails
- Internal notifications

### Step 1: Prerequisites

**Requirements:**
- Active Microsoft 365 subscription (E3/E5 or Business Premium)
- Global Administrator or Exchange Administrator role
- Azure AD application registration

### Step 2: Set Up Application

1. **Register Azure AD Application**

```bash
# Using Azure CLI
az ad app create \
  --display-name "Email Service Application" \
  --sign-in-audience AzureADMyOrg

# Note the Application (client) ID
```

2. **Configure API Permissions**

Required permissions:
- `Mail.Send` (Application permission)
- `User.Read.All` (Application permission)

```bash
# Add Microsoft Graph permissions
az ad app permission add \
  --id <app-id> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Role
```

3. **Grant Admin Consent**

```bash
az ad app permission admin-consent --id <app-id>
```

4. **Create Client Secret**

```bash
az ad app credential reset \
  --id <app-id> \
  --append
```

### Step 3: Code Migration

**Node.js with Microsoft Graph:**

```typescript
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

  await client
    .api('/users/noreply@contoso.com/sendMail')
    .post(sendMail);

  console.log('Email sent successfully');
}
```

**Python with Microsoft Graph:**

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
    message.subject = "Welcome to Contoso"
    message.body = ItemBody()
    message.body.content_type = BodyType.Html
    message.body.content = "<html><h1>Welcome!</h1></html>"

    to_recipient = Recipient()
    to_recipient.email_address = EmailAddress()
    to_recipient.email_address.address = "customer@example.com"
    message.to_recipients = [to_recipient]

    await client.users.by_user_id('noreply@contoso.com').send_mail.post(
        body={'message': message, 'save_to_sent_items': False}
    )

    print('Email sent successfully')
```

### Step 4: Batch Operations

```typescript
// Send multiple emails efficiently
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

### Step 5: Limitations & Considerations

**Rate Limits:**
- 5,000 messages per day per user
- 30 messages per minute

**Best Practices:**
```typescript
// Implement retry logic with exponential backoff
async function sendEmailWithRetry(emailData: any, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      await client.api('/users/sender@contoso.com/sendMail').post(emailData);
      return;
    } catch (error: any) {
      if (error.statusCode === 429) {
        const retryAfter = parseInt(error.headers['retry-after']) || Math.pow(2, attempt);
        console.log(`Rate limited. Retrying after ${retryAfter}s`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## Code Migration Examples

### Pattern 1: Simple Transactional Email

**Before (ACS):**
```csharp
// C# with ACS Email
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

**After (SendGrid):**
```csharp
using SendGrid;
using SendGrid.Helpers.Mail;

var client = new SendGridClient(apiKey);
var from = new EmailAddress("noreply@contoso.com", "Contoso");
var to = new EmailAddress("customer@example.com");
var subject = "Order Confirmation";
var plainText = "Your order has been confirmed.";
var htmlContent = "<p>Your order has been confirmed.</p>";

var msg = MailHelper.CreateSingleEmail(from, to, subject, plainText, htmlContent);
var response = await client.SendEmailAsync(msg);
```

### Pattern 2: Email with Attachments

**Before (ACS):**
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
    "attachments": [
        {
            "name": "invoice.pdf",
            "attachmentType": "pdf",
            "contentBytesBase64": base64_content
        }
    ]
}

poller = client.begin_send(message)
result = poller.result()
```

**After (SendGrid):**
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

message = Mail(
    from_email='billing@contoso.com',
    to_emails='customer@example.com',
    subject='Invoice',
    plain_text_content='Your invoice is attached.'
)

attachment = Attachment(
    FileContent(base64_content),
    FileName('invoice.pdf'),
    FileType('application/pdf'),
    Disposition('attachment')
)
message.attachment = attachment

sg = SendGridAPIClient(api_key)
response = sg.send(message)
```

### Pattern 3: Template-Based Emails

**Before (ACS - Manual templating):**
```javascript
// Manual template replacement
const template = `
  <html>
    <body>
      <h1>Hello {{firstName}}!</h1>
      <p>Your order #{{orderNumber}} has been shipped.</p>
    </body>
  </html>
`;

const html = template
  .replace('{{firstName}}', customer.firstName)
  .replace('{{orderNumber}}', order.number);

await emailClient.beginSend({
  senderAddress: "orders@contoso.com",
  content: { subject: "Order Shipped", html },
  recipients: { to: [{ address: customer.email }] }
});
```

**After (SendGrid - Dynamic templates):**
```javascript
// Use SendGrid dynamic templates
await sgMail.send({
  to: customer.email,
  from: 'orders@contoso.com',
  templateId: 'd-123abc456def',
  dynamicTemplateData: {
    firstName: customer.firstName,
    orderNumber: order.number
  }
});
```

### Pattern 4: Bulk Email with Personalization

**SendGrid Personalization:**
```typescript
const personalizationsList = customers.map(customer => ({
  to: [{ email: customer.email }],
  dynamicTemplateData: {
    firstName: customer.firstName,
    accountBalance: customer.balance,
    lastLoginDate: customer.lastLogin
  }
}));

await sgMail.send({
  from: 'noreply@contoso.com',
  templateId: 'd-xyz789',
  personalizations: personalizationsList
});
```

---

## Testing & Validation

### Test Strategy

**Phase 1: Unit Testing**

```typescript
// Jest test example
import { sendEmail } from './emailService';
import sgMail from '@sendgrid/mail';

jest.mock('@sendgrid/mail');

describe('Email Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should send email successfully', async () => {
    (sgMail.send as jest.Mock).mockResolvedValue([{ statusCode: 202 }]);

    await sendEmail('test@example.com', 'Test Subject', 'Test Body');

    expect(sgMail.send).toHaveBeenCalledWith(
      expect.objectContaining({
        to: 'test@example.com',
        subject: 'Test Subject'
      })
    );
  });

  test('should handle errors gracefully', async () => {
    (sgMail.send as jest.Mock).mockRejectedValue(new Error('API Error'));

    await expect(
      sendEmail('test@example.com', 'Test', 'Body')
    ).rejects.toThrow('API Error');
  });
});
```

**Phase 2: Integration Testing**

```typescript
// Integration test with actual API calls (use test environment)
describe('SendGrid Integration', () => {
  test('should send real email to test account', async () => {
    const result = await sgMail.send({
      to: 'test@yourdomain.com',
      from: 'test@yourdomain.com',
      subject: 'Integration Test',
      text: 'This is a test email'
    });

    expect(result[0].statusCode).toBe(202);
  });
});
```

**Phase 3: Load Testing**

```javascript
// k6 load testing script
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '5m', target: 100 },  // Ramp up to 100 VUs
    { duration: '10m', target: 100 }, // Stay at 100 VUs
    { duration: '5m', target: 0 },    // Ramp down
  ],
};

export default function() {
  const payload = JSON.stringify({
    to: 'loadtest@example.com',
    from: 'noreply@contoso.com',
    subject: 'Load Test',
    text: 'Load testing email delivery'
  });

  const params = {
    headers: {
      'Authorization': `Bearer ${__ENV.SENDGRID_API_KEY}`,
      'Content-Type': 'application/json',
    },
  };

  let res = http.post('https://api.sendgrid.com/v3/mail/send', payload, params);

  check(res, {
    'status is 202': (r) => r.status === 202,
  });
}
```

### Validation Checklist

- [ ] All email types tested (transactional, notifications, marketing)
- [ ] Template rendering verified
- [ ] Attachments working correctly
- [ ] Personalization data populating
- [ ] Unsubscribe links functional
- [ ] Bounce handling configured
- [ ] SPF/DKIM/DMARC records validated
- [ ] Delivery rates match or exceed ACS baseline
- [ ] Error handling and retries working
- [ ] Monitoring and alerting configured
- [ ] Cost tracking in place
- [ ] Compliance requirements met

### Email Deliverability Testing

```bash
# Test SPF record
nslookup -type=txt yourdomain.com

# Test DKIM
nslookup -type=txt s1._domainkey.yourdomain.com

# Test DMARC
nslookup -type=txt _dmarc.yourdomain.com

# Send test emails to these services:
# - mail-tester.com
# - mxtoolbox.com/deliverability
# - Google Postmaster Tools
```

---

## Rollback Plan

### Preparation

1. **Keep ACS Email Active**
   - Maintain existing ACS resources during migration
   - Don't delete domains or resources until fully validated

2. **Feature Flags**
   ```typescript
   // Use feature flags for gradual rollout
   const useNewEmailProvider = await featureFlagClient.getFlag('use-sendgrid');

   if (useNewEmailProvider) {
     await sendViaSendGrid(emailData);
   } else {
     await sendViaACS(emailData);
   }
   ```

3. **Traffic Splitting**
   ```typescript
   // Route percentage of traffic to new provider
   const rolloutPercentage = 10; // Start with 10%
   const useSendGrid = Math.random() * 100 < rolloutPercentage;

   if (useSendGrid) {
     await sendViaSendGrid(emailData);
     telemetry.trackEvent('SendGrid', { success: true });
   } else {
     await sendViaACS(emailData);
     telemetry.trackEvent('ACS', { success: true });
   }
   ```

### Rollback Triggers

Execute rollback if:
- Email delivery rate drops below 95%
- Error rate exceeds 5%
- Cost exceeds budget by 20%
- Critical compliance issue discovered
- Severe bug in production

### Rollback Procedure

1. **Immediate Actions** (0-15 minutes)
   ```bash
   # Update feature flag to disable new provider
   az appconfig kv set \
     --name myAppConfig \
     --key use-sendgrid \
     --value false \
     --yes

   # Restart services to pick up configuration
   kubectl rollout restart deployment/email-service
   ```

2. **Communication** (15-30 minutes)
   - Notify stakeholders of rollback
   - Update status page
   - Document issues encountered

3. **Investigation** (30+ minutes)
   - Review logs and metrics
   - Identify root cause
   - Create action plan for re-attempt

---

## Post-Migration

### Week 1: Monitoring

**Key Metrics to Track:**

```typescript
// Application Insights custom metrics
const metrics = {
  emailsSent: 0,
  emailsDelivered: 0,
  emailsBounced: 0,
  emailsFailed: 0,
  averageDeliveryTime: 0,
  costPerEmail: 0
};

// Track daily
appInsights.trackMetric({ name: 'DailyEmailsSent', value: metrics.emailsSent });
appInsights.trackMetric({ name: 'DeliveryRate', value: (metrics.emailsDelivered / metrics.emailsSent) * 100 });
appInsights.trackMetric({ name: 'BounceRate', value: (metrics.emailsBounced / metrics.emailsSent) * 100 });
```

**Alert Configuration:**

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

- name: High Cost Alert
  condition: dailyCost > $100
  window: 1 day
  action: Send notification to finance team
```

### Month 1: Optimization

1. **Review Delivery Metrics**
   - Compare against ACS baseline
   - Identify and fix deliverability issues
   - Optimize send times

2. **Cost Analysis**
   ```sql
   -- Query to analyze email costs
   SELECT
     DATE(timestamp) as date,
     COUNT(*) as emails_sent,
     SUM(cost) as total_cost,
     AVG(cost) as avg_cost_per_email
   FROM email_logs
   WHERE provider = 'SendGrid'
   GROUP BY DATE(timestamp)
   ORDER BY date DESC;
   ```

3. **Performance Tuning**
   - Optimize batch sizes
   - Implement connection pooling
   - Cache templates

### Decommissioning ACS Email

**Only after:**
- [ ] 30+ days of stable operation on new platform
- [ ] All metrics meeting or exceeding targets
- [ ] Stakeholder sign-off obtained
- [ ] Documentation updated
- [ ] Team trained on new platform

**Decommission Steps:**

```bash
# 1. Stop sending via ACS (already done)

# 2. Export historical data
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
# 6. Notify team of decommission completion
```

---

## Frequently Asked Questions

### General Questions

**Q: Do I have to migrate immediately?**
A: No, you have 36 months from the retirement announcement. However, starting early reduces risk and allows for thorough testing.

**Q: Will Microsoft help with migration costs?**
A: Migration tooling and documentation are provided at no cost. Some customers may qualify for Azure migration credits - contact your Microsoft account team.

**Q: Can I continue using ACS Email after the deadline?**
A: No, the service will be completely decommissioned. Plan to complete your migration before the deadline.

### Technical Questions

**Q: How do I migrate email templates?**
A: Both SendGrid and Microsoft 365 support HTML templates. You'll need to:
1. Export existing templates
2. Convert to new provider's format
3. Test rendering across email clients
4. Update code to use new template IDs

**Q: What about email tracking and analytics?**
A: SendGrid provides advanced analytics via their dashboard and webhooks. Microsoft 365 HVE has basic reporting through the admin center. Both can integrate with Application Insights.

**Q: How do I handle GDPR compliance?**
A: Both providers support GDPR. Ensure you:
- Update privacy policies
- Configure data residency
- Implement unsubscribe mechanisms
- Review data processing agreements

**Q: What if I have custom email domains?**
A: Both providers support custom domains. You'll need to:
1. Update DNS records (SPF, DKIM, DMARC)
2. Verify domain ownership
3. Configure sender authentication
4. Test email delivery

### Cost Questions

**Q: Will my costs increase?**
A: It depends on your volume and features used. Generally:
- Low volume (<10k/month): Similar or lower cost
- Medium volume (10k-100k/month): Comparable
- High volume (>100k/month): May be higher, but with more features

**Q: Are there free tiers?**
A: Yes, SendGrid offers 100 emails/day free. Microsoft 365 HVE is included with certain subscriptions.

**Q: What about overage charges?**
A: SendGrid charges for overages based on your plan. Monitor usage closely and set up billing alerts.

---

## Support Resources

### Documentation

- **SendGrid:**
  - Official Docs: https://docs.sendgrid.com
  - API Reference: https://docs.sendgrid.com/api-reference
  - Migration Guide: https://docs.sendgrid.com/for-developers/sending-email/migrating-from-v2-to-v3-mail-send

- **Microsoft 365:**
  - Graph API: https://learn.microsoft.com/graph/api/user-sendmail
  - Best Practices: https://learn.microsoft.com/microsoft-365/compliance/high-volume-email

- **Azure Communication Services:**
  - Retirement Announcement: [Azure Updates]
  - Support Timeline: [Azure Portal]

### Community Support

- **Stack Overflow:**
  - SendGrid: https://stackoverflow.com/questions/tagged/sendgrid
  - Microsoft Graph: https://stackoverflow.com/questions/tagged/microsoft-graph

- **GitHub:**
  - SendGrid SDK: https://github.com/sendgrid
  - Microsoft Graph SDK: https://github.com/microsoftgraph

### Microsoft Support

- **Azure Support:** Open ticket via Azure Portal
- **Account Team:** Contact your Microsoft account manager
- **FastTrack:** Available for Enterprise customers

### Migration Assistance

For complex migrations or enterprise support:
- Microsoft Consulting Services (MCS)
- Certified Azure Partners
- SendGrid Professional Services

---

## Appendix

### A. DNS Configuration Examples

**SPF Record:**
```
v=spf1 include:sendgrid.net include:spf.protection.outlook.com -all
```

**DKIM Records (SendGrid):**
```
s1._domainkey IN CNAME s1.domainkey.u12345.wl.sendgrid.net.
s2._domainkey IN CNAME s2.domainkey.u12345.wl.sendgrid.net.
```

**DMARC Record:**
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc@yourdomain.com; fo=1
```

### B. Cost Calculator

```typescript
function calculateMigrationCost(
  monthlyVolume: number,
  provider: 'sendgrid' | 'm365'
): number {
  if (provider === 'sendgrid') {
    if (monthlyVolume <= 3000) return 0;
    if (monthlyVolume <= 50000) return 19.95;
    if (monthlyVolume <= 100000) return 89.95;

    const overage = monthlyVolume - 100000;
    return 89.95 + (overage / 1000) * 0.85;
  } else {
    // M365 HVE (included in E3/E5)
    const usersNeeded = Math.ceil(monthlyVolume / 150000); // 5k/day/user
    return usersNeeded * 36; // E3 license cost
  }
}

// Example usage
console.log('Cost for 75k emails/month:');
console.log('SendGrid:', calculateMigrationCost(75000, 'sendgrid'));
console.log('M365 HVE:', calculateMigrationCost(75000, 'm365'));
```

### C. Sample Migration Runbook

```yaml
title: ACS Email to SendGrid Migration Runbook
version: 1.0
owner: Platform Team

pre-migration:
  - task: Inventory current email usage
    command: "node scripts/inventory.js"
    duration: 2 hours

  - task: Set up SendGrid account
    steps:
      - Create account
      - Verify domain
      - Generate API key
    duration: 1 hour

  - task: Update DNS records
    records:
      - SPF
      - DKIM
      - DMARC
    verification: "Wait 24-48 hours for propagation"

migration:
  - task: Deploy code changes
    steps:
      - Deploy to dev environment
      - Run integration tests
      - Deploy to staging
      - Smoke test
      - Deploy to production
    rollback: "Revert to previous deployment"

  - task: Enable feature flag
    command: "az appconfig kv set --key use-sendgrid --value true"
    validation: "Check metrics dashboard"

post-migration:
  - task: Monitor for 24 hours
    alerts:
      - Delivery rate
      - Error rate
      - Cost

  - task: Optimize and tune
    duration: 1 week

  - task: Decommission ACS resources
    when: "After 30 days of stable operation"
```

### D. Compliance Checklist

- [ ] Data Processing Agreement signed with provider
- [ ] Data residency requirements verified
- [ ] GDPR compliance reviewed
- [ ] HIPAA compliance (if applicable)
- [ ] SOC 2 certification verified
- [ ] Privacy policy updated
- [ ] Terms of service updated
- [ ] Customer notification sent
- [ ] Opt-out mechanism implemented
- [ ] Data retention policy aligned
- [ ] Security assessment completed
- [ ] Vendor risk assessment updated

---

**Document End**

*For questions or support, contact: acs-migration-support@microsoft.com*

*Last Updated: January 2026*
