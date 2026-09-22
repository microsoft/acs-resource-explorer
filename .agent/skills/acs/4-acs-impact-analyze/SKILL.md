---
name: 4-acs-impact-analyze
description: Map detected ACS channel usage to the appropriate Retirement Guide or Breaking Change Guide. Links each impacted resource to Microsoft migration resources per channel.
---

## When to use this skill
Use this skill after ACS channel detection to map detected channel usage to migration guides.

Examples:
  - "Which ACS channels are in use on my resources?"
  - "Show me the migration guides for my ACS resources"
  - "Summarize what needs to be migrated for each ACS resource"

## Preconditions
- ACS resources discovered (use **1-acs-resource-scan**)
- Channel detection complete (use **2-acs-channel-detect** OR **3-acs-metrics-collect**)
- Session state contains ACS resource inventory with detection results

## Knowledge References

> Authoritative reference data for this skill — update these files when retirement dates or migration paths change:
> - **Retirement dates & status types:** [docs/knowledge/acs-retirement-dates.md](../../../../docs/knowledge/acs-retirement-dates.md)
> - **Migration paths & guide links:** [docs/knowledge/acs-migration-paths.md](../../../../docs/knowledge/acs-migration-paths.md)

## Channel Guide Mapping

| Channel | Status Type | Guide |
|---------|------------|-------|
| Email Service | 🔴 Retirement | https://aka.ms/acs-retirement#acs-email |
| SMS API | 🔴 Retirement | https://aka.ms/acs-retirement#acs-sms |
| Chat SDK | 🔴 Retirement | https://aka.ms/acs-retirement#acs-chat |
| Call Automation API | 🟡 Breaking Change | https://aka.ms/acs-retirement#acs-voicevideo-calling-sdk |
| Job Router API | 🟡 Breaking Change | https://aka.ms/acs-retirement |
| Advance Messaging API | 🟡 Breaking Change | https://aka.ms/acs-retirement |
| Rooms API | 🟡 Breaking Change | https://aka.ms/acs-retirement |
| Phone Numbers SDK | 🔴 Retirement | https://aka.ms/acs-retirement#acs-number-management-direct-offer |

> Full guide: https://aka.ms/acs-retirement

## Workflow

### 0) **Load Knowledge References**
   Read the following knowledge files before beginning:
   - Read `docs/knowledge/acs-retirement-dates.md` — channel status types and effective dates
   - Read `docs/knowledge/acs-migration-paths.md` — migration paths and guide links per channel

### 1) **Load ACS Resource Inventory**
   - Retrieve inventory with detection results from session state
   - Verify detection data exists (from skill 2 or skill 3)
   - If no detection data: Exit with "Run 2-acs-channel-detect or 3-acs-metrics-collect first"

### 2) **For Each ACS Resource**
   - Display: "🔍 Mapping channels: [Resource Name]"
   - Identify all channels with detected usage (flag = true)
   - For each detected channel, assign the migration guide link from the channel guide mapping above

### 3) **Display Channel Summary**
   ```
   === ACS Channel Detection Results ===

   ┌──────────────────┬──────────────────────────────┬───────────────┐
   │ Resource         │ Channels Detected             │ Channel Count │
   ├──────────────────┼──────────────────────────────┼───────────────┤
   │ ACSProd          │ Email, Chat, Phone Numbers    │ 3             │
   │ ACSDevAndTest    │ None                          │ 0             │
   └──────────────────┴──────────────────────────────┴───────────────┘

   Channel Totals Across All Resources:
     📧 Email:         [N] resource(s) — Retirement Guide: https://aka.ms/acs-retirement#acs-email
     📱 SMS:           [N] resource(s) — Retirement Guide: https://aka.ms/acs-retirement#acs-sms
     💬 Chat:          [N] resource(s) — Retirement Guide: https://aka.ms/acs-retirement#acs-chat
   📞 Call Auto:     [N] resource(s) — Breaking Change Guide: https://aka.ms/acs-retirement#acs-voicevideo-calling-sdk
   🧭 Job Router:    [N] resource(s) — Guide: https://aka.ms/acs-retirement
   📨 Advance Msg:   [N] resource(s) — Guide: https://aka.ms/acs-retirement
   🏠 Rooms:         [N] resource(s) — Guide: https://aka.ms/acs-retirement
     ☎️ Phone Numbers: [N] resource(s) — Retirement Guide: https://aka.ms/acs-retirement#acs-number-management-direct-offer

   📘 Full Guide: https://aka.ms/acs-retirement
   ```

### 4) **Save Channel Analysis to Session State**
   - Update inventory with detected channel list and assigned guide links per resource

## Output
- Detected channels per resource
- Migration or breaking change guide link per detected channel
- Channel totals across all resources

## Related Skills
- Requires **1-acs-resource-scan** + either **2-acs-channel-detect** or **3-acs-metrics-collect**
- Use **5-acs-report-generate** after this skill to export results

