# ACS Azure Monitor Metric Names & Channel Detection

**Source:** Azure Monitor `az monitor metrics list-definitions` (live query) + https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/microsoft-communication_communicationservices
**Last Verified:** 2026-04-22
**Update This File When:** Microsoft adds, renames, or deprecates metric names or log tables for ACS resources.

---

## Rules
- Every metric name and table name in this file has been verified against a live resource or authoritative Microsoft documentation.
- Do not add names that have not been verified. Mark anything unverified explicitly.

---

## Platform Metrics
Verified via `az monitor metrics list-definitions` on a live `Microsoft.Communication/CommunicationServices` resource.
Queryable via `az monitor metrics list` with Reader + Monitoring Reader access. No Diagnostic Settings required.

| Metric Name | Display Name | Channel | Aggregation |
|-------------|-------------|---------|-------------|
| `ApiRequests` | Email Service API Requests | Email | Count |
| `DeliveryStatusUpdate` | Email Service Delivery Status Updates | Email | Count |
| `UserEngagement` | Email Service User Engagement | Email | Count |
| `APIRequestSMS` | SMS API Requests | SMS | Count |
| `APIRequestChat` | Chat API Requests | Chat | Count |
| `APIRequestsAdvancedMessaging` | Advanced Messaging API Requests | Advanced Messaging / WhatsApp | Count |
| `ApiRequestRooms` | Rooms API Requests | Rooms | Count |
| `ApiRequestRouter` | Job Router API Requests | Job Router | Count |
| `APIRequestCallAutomation` | Call Automation API Requests | Call Automation | Count |
| `AcsCallAutomationCallbackEvent` | Call Automation Callback Event | Call Automation | Count |
| `APIRequestCallRecording` | Call Recording API Requests | Call Recording | Count |
| `APIRequestAuthentication` | Authentication API Requests | Identity (not retiring) | Count |

---

## Log Analytics Tables
Verified via https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/microsoft-communication_communicationservices
Requires Diagnostic Settings enabled and a Log Analytics workspace configured on the ACS resource.

| Table | Description | Channel |
|-------|-------------|---------|
| `ACSEmailSendMailOperational` | Email send operations | Email |
| `ACSEmailStatusUpdateOperational` | Email delivery status updates | Email |
| `ACSEmailUserEngagementOperational` | Email open/click engagement | Email |
| `ACSSMSIncomingOperations` | SMS API operations | SMS |
| `ACSOptOutManagementOperations` | SMS opt-out management | SMS |
| `ACSChatIncomingOperations` | Chat API operations | Chat |
| `ACSAdvancedMessagingOperations` | Advanced Messaging (WhatsApp) operations | Advanced Messaging / WhatsApp |
| `ACSRoomsIncomingOperations` | Rooms API operations | Rooms |
| `ACSJobRouterIncomingOperations` | Job Router API operations | Job Router |
| `ACSCallAutomationIncomingOperations` | Call Automation API operations (CreateCall, Play, Recognize, etc.) | Call Automation |
| `ACSCallAutomationMediaSummary` | Call Automation media operations summary | Call Automation |
| `ACSCallAutomationStreamingUsage` | Audio streaming session usage (start/stop, duration, participantId) | Audio Streaming |
| `ACSCallRecordingIncomingOperations` | Call Recording API operations (Start/Stop/Pause/Resume) | Call Recording |
| `ACSCallRecordingSummary` | Recording summary (duration, format, content type) | Call Recording |
| `ACSCallSummary` | Per-participant call summary (VoIP, PSTN, SDK version, OS) | Voice/Video Calling |
| `ACSCallSummaryUpdates` | Near-real-time call summary updates | Voice/Video Calling |
| `ACSCallDiagnostics` | Per-stream media diagnostics | Voice/Video Calling |
| `ACSCallDiagnosticsUpdates` | Near-real-time media stream diagnostics | Voice/Video Calling |
| `ACSCallClientOperations` | Calling SDK client events (state changes, createView, startAudio) | Voice/Video Calling |
| `ACSCallClientMediaStatsTimeSeries` | Granular media quality timeseries (bitrate, jitter, codec) | Voice/Video Calling |
| `ACSCallClientServiceRequestAndOutcome` | Service-side call join/hangup with HTTP payloads | Voice/Video Calling |
| `ACSCallingMetrics` | Aggregated calling metrics in daily bins (SDK API reliability, UFDs) | Voice/Video Calling |
| `ACSCallSurvey` | End-of-call quality surveys | Voice/Video Calling |
| `ACSCallClosedCaptionsSummary` | Closed captions sessions (duration, language, end reason) | Closed Captions |
| `ACSAuthIncomingOperations` | Auth/identity API operations | Identity (not retiring) |
| `ACSBillingUsage` | Usage records across all ACS modes — covers every channel | All channels |
| `AzureMetrics` | Platform metrics routed to Log Analytics | All channels |
| `AzureActivity` | Azure subscription-level activity log | General |

---

## Phone Number Detection
Phone numbers in ACS are data-plane resources, not ARM child resources.
Detection requires the ACS data plane API authenticated with an Entra token (Reader access on the subscription is sufficient).

```bash
# Step 1 — get ACS resource hostname
HOSTNAME=$(az resource show \
  --name <resource-name> \
  --resource-group <resource-group> \
  --resource-type "Microsoft.Communication/CommunicationServices" \
  --query "properties.hostName" -o tsv)

# Step 2 — get Entra token for ACS data plane
TOKEN=$(az account get-access-token \
  --resource "https://communication.azure.com" \
  --query accessToken -o tsv)

# Step 3 — list phone numbers
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://$HOSTNAME/phoneNumbers?api-version=2022-12-01"
```

If `phoneNumbers` array is non-empty → phone numbers detected.

---

## Full Channel Detection Map

| Channel | Status | Platform Metric | Log Analytics Table | Phone Number API |
|---------|--------|----------------|-------------------|-----------------|
| Email | Retirement | `ApiRequests`, `DeliveryStatusUpdate`, `UserEngagement` | `ACSEmailSendMailOperational`, `ACSEmailStatusUpdateOperational`, `ACSEmailUserEngagementOperational` | — |
| SMS | Retirement | `APIRequestSMS` | `ACSSMSIncomingOperations`, `ACSOptOutManagementOperations` | — |
| Chat | Retirement | `APIRequestChat` | `ACSChatIncomingOperations` | — |
| Advanced Messaging / WhatsApp | Retirement | `APIRequestsAdvancedMessaging` | `ACSAdvancedMessagingOperations` | — |
| Rooms | Retirement | `ApiRequestRooms` | `ACSRoomsIncomingOperations` | — |
| Job Router | Retirement | `ApiRequestRouter` | `ACSJobRouterIncomingOperations` | — |
| Phone Numbers | Retirement | — | — | Data plane API: `GET /phoneNumbers?api-version=2022-12-01` |
| Call Automation | Breaking Change | `APIRequestCallAutomation`, `AcsCallAutomationCallbackEvent` | `ACSCallAutomationIncomingOperations`, `ACSCallAutomationMediaSummary` | — |
| Audio Streaming | Breaking Change | — | `ACSCallAutomationStreamingUsage` | — |
| Call Recording | Breaking Change | `APIRequestCallRecording` | `ACSCallRecordingIncomingOperations`, `ACSCallRecordingSummary` | — |
| Voice/Video Calling | Breaking Change | — | `ACSCallSummary`, `ACSCallSummaryUpdates`, `ACSCallDiagnostics`, `ACSCallingMetrics` | — |
| Closed Captions | Breaking Change | — | `ACSCallClosedCaptionsSummary` | — |