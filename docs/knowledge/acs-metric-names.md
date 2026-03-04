# ACS Azure Monitor Metric Names

**Source:** Azure Monitor metrics for Microsoft.Communication/CommunicationServices
**Last Verified:** 2026-02-27
**Update This File When:** Microsoft adds, renames, or deprecates metric names for ACS resources.

---

## Metrics by Channel

| Channel | Metric Name | Aggregation | Unit | Notes |
|---------|-------------|-------------|------|-------|
| **Email** | `EmailMessagesSent` | Total | Count | Messages successfully sent |
| **Email** | `EmailDeliveryAttempts` | Total | Count | Delivery attempts (including retries) |
| **Email** | `EmailOperations` | Total | Count | All email API operations |
| **SMS** | `SMSMessagesSent` | Total | Count | Outbound SMS messages |
| **SMS** | `SMSMessagesReceived` | Total | Count | Inbound SMS messages |
| **Chat** | `ChatMessageCount` | Total | Count | Messages sent in chat threads |
| **Chat** | `ChatThreadCount` | Total | Count | Chat threads created |
| **Chat** | `ActiveChatUsers` | Total | Count | Unique active chat participants |
| **Calling** | `CallDuration` | Total | Seconds | Total call duration across all calls |
| **Calling** | `CallCount` | Total | Count | Number of calls initiated |
| **Calling** | `ParticipantCount` | Total | Count | Unique call participants |
| **Phone Numbers** | `PhoneNumberOperations` | Total | Count | Phone number provisioning/management operations |

---

## Detection Logic

A channel is considered **in use** when the **sum of all its metrics** over the lookback period is **greater than zero**.

```
EmailTotal    = EmailMessagesSent + EmailDeliveryAttempts + EmailOperations
SMSTotal      = SMSMessagesSent + SMSMessagesReceived
ChatTotal     = ChatMessageCount + ChatThreadCount + ActiveChatUsers
CallingTotal  = CallDuration + CallCount + ParticipantCount
PhoneTotal    = PhoneNumberOperations

If Total > 0 → Channel detected = true
```

---

## Azure Monitor Query Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| TimeGrain | `01:00:00` (hourly) | Required for max lookback coverage |
| AggregationType | `Total` | Sum all data points in the period |
| Min Lookback | 1 day | — |
| Max Lookback | **93 days** | Azure Monitor hourly retention limit |
| Default Lookback | 90 days | Recommended |
| ResourceType | `Microsoft.Communication/CommunicationServices` | — |

---

## Azure CLI Query Pattern

```bash
az monitor metrics list \
  --resource <resourceId> \
  --metric "EmailMessagesSent" \
  --start-time <startTime> \
  --end-time <endTime> \
  --interval PT1H \
  --aggregation Total \
  --output json

# Sum the results (jq):
# .value[0].timeseries[].data[].total | select(. != null) | add
```

---

## Fast Detection (no metrics required)

For Email and Phone Numbers only, child resource existence can be used as a proxy:

| Channel | Child Resource Type |
|---------|-------------------|
| Email | `Microsoft.Communication/EmailServices/Domains` |
| Phone Numbers | `Microsoft.Communication/CommunicationServices/phoneNumbers` |

> SMS, Chat, and Calling have no child resource type and **require Azure Monitor metrics** for detection.
