# ACS Azure Monitor Metric Names

**Source:** Azure Monitor metrics for Microsoft.Communication/CommunicationServices
**Last Verified:** 2026-09-15
**Update This File When:** Microsoft adds, renames, or deprecates metric names for ACS resources.

---

## Metrics by Channel

| Channel | Metric Name | Aggregation | Unit | Notes |
|---------|-------------|-------------|------|-------|
| **Email** | `ApiRequests` | Total | Count | Email Service API Requests |
| **Email** | `DeliveryStatusUpdate` | Total | Count | Email Service Delivery Status Updates |
| **Email** | `UserEngagement` | Total | Count | Email Service User Engagement |
| **SMS** | `APIRequestSMS` | Total | Count | SMS API Requests |
| **Chat** | `APIRequestChat` | Total | Count | Chat API Requests |
| **CallAutomation** | `APIRequestCallAutomation` | Total | Count | Call Automation API Requests |
| **CallAutomation** | `APIRequestCallRecording` | Total | Count | Call Recording API Requests |
| **CallAutomation** | `AcsCallAutomationCallbackEvent` | Total | Count | Call Automation Callback Event |
| **Job Router** | `ApiRequestRouter` | Total | Count | Job Router API Requests |
| **AdvanceMessaging** | `APIRequestsAdvancedMessaging` | Total | Count | Advanced Messaging API Requests |
| **Rooms** | `ApiRequestRooms` | Total | Count | Rooms API Requests |
---

## PSTN and VoIP Billing Usage

PSTN and VoIP billable usage is not exposed as an ACS platform metric. Full scans query the `ACSBillingUsage` table in each Log Analytics workspace connected to the ACS resource through diagnostic settings.

| Report Field | `UsageType` Match | Values Collected |
|--------------|-------------------|------------------|
| **PSTN billing usage** | Contains `PSTN` (case-insensitive) | Sum of `Quantity`, unique `RecordId` count, distinct `UnitType` values |
| **VoIP billing usage** | `Audio` or `VoIP` (case-insensitive) | Sum of `Quantity`, unique `RecordId` count, distinct `UnitType` values |

Records are deduplicated by `RecordId` across workspaces. `Quantity` represents billable usage units such as minutes, messages, or megabytes; it is not a currency cost.

Collection status is reported explicitly:

- `Collected` — the billing table was queried successfully, including when no matching records exist.
- `NotConfigured` — no Log Analytics diagnostic destination is configured for the ACS resource.
- `DiagnosticSettingsQueryFailed` — diagnostic settings could not be read.
- `QueryFailed` — destinations exist, but none of their billing tables could be queried.

> Billing logs are not stored retroactively. The `Usage`/`allLogs` diagnostic category must be enabled and routed to Log Analytics before calls occur.

## Detection Logic

A channel is considered **in use** when the **sum of all its metrics** over the lookback period is **greater than zero**.

```
EmailTotal    = ApiRequests + DeliveryStatusUpdate + UserEngagement
SMSTotal      = APIRequestSMS
ChatTotal     = APIRequestChat
CallAutomationTotal  = APIRequestCallAutomation + APIRequestCallRecording + AcsCallAutomationCallbackEvent
JobRouterTotal    = ApiRequestRouter
AdvanceMessagingTotal    = APIRequestsAdvancedMessaging
RoomsTotal    = ApiRequestRooms

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
  --metric "ApiRequests" \
  --start-time <startTime> \
  --end-time <endTime> \
  --interval PT1H \
  --aggregation Total \
  --output json

# Sum the results (jq):
# .value[0].timeseries[].data[].total | select(. != null) | add
```

Billing usage query pattern:

```kusto
ACSBillingUsage
| where TimeGenerated between (datetime(<start-time>) .. datetime(<end-time>))
| where _ResourceId =~ "<acs-resource-id>"
| summarize arg_max(TimeGenerated, *) by RecordId
| project RecordId, UsageType, UnitType, Quantity
```

---

## Fast Detection (no metrics required)

For Email and Phone Numbers only, child resource existence can be used as a proxy:

| Channel | Child Resource Type |
|---------|-------------------|
| Email | `Microsoft.Communication/EmailServices/Domains` |
| Phone Numbers | `Microsoft.Communication/CommunicationServices/phoneNumbers` |

> SMS, Chat, Call Automation, Job Router, Advance Messaging, and Rooms have no child resource type and **require Azure Monitor metrics** for detection.
