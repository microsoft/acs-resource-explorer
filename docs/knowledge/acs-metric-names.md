# ACS Azure Monitor Metric Names

**Source:** Azure Monitor metrics for Microsoft.Communication/CommunicationServices
**Last Verified:** 2026-02-27
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

---

## Fast Detection (no metrics required)

For Email and Phone Numbers only, child resource existence can be used as a proxy:

| Channel | Child Resource Type |
|---------|-------------------|
| Email | `Microsoft.Communication/EmailServices/Domains` |
| Phone Numbers | `Microsoft.Communication/CommunicationServices/phoneNumbers` |

> SMS, Chat, Call Automation, Job Router, Advance Messaging, and Rooms have no child resource type and **require Azure Monitor metrics** for detection.
