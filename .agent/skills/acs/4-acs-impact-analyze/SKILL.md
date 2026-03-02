---
name: 4-acs-impact-analyze
description: Calculate severity and migration effort for ACS resources using ACS-specific severity thresholds, retirement dates, and channel complexity. Produces prioritized migration plan with links to ACS migration guides.
---

## When to use this skill
Use this skill after ACS channel detection to assess business impact and prioritize migration.

Examples:
  - "Analyze the impact of my ACS usage"
  - "Which ACS resources need urgent attention?"
  - "Calculate migration effort for my ACS resources"
  - "Prioritize my ACS migration work"

## Preconditions
- ACS resources discovered (use **1-acs-resource-scan**)
- Channel detection complete (use **2-acs-channel-detect** OR **3-acs-metrics-collect**)
- Session state contains ACS resource inventory with detection results

## Knowledge References

> Authoritative reference data for this skill — update these files when thresholds, dates, or migration paths change:
> - **Severity thresholds & effort matrix:** [docs/knowledge/acs-severity-thresholds.md](../../../../docs/knowledge/acs-severity-thresholds.md)
> - **Retirement dates & urgency tiers:** [docs/knowledge/acs-retirement-dates.md](../../../../docs/knowledge/acs-retirement-dates.md)
> - **Migration paths & guide links:** [docs/knowledge/acs-migration-paths.md](../../../../docs/knowledge/acs-migration-paths.md)

## ACS-Specific Severity Rules

### Usage-Based Severity

| Severity | Email | SMS | Chat | Calling | Phone Numbers |
|----------|-------|-----|------|---------|---------------|
| **Critical** | >1,000 messages | >500 messages | >10,000 messages | >500 calls | >1,000 operations |
| **Warning** | >100 messages | >50 messages | >1,000 messages | >50 calls | >100 operations |
| **Info** | Any usage | Any usage | Any usage | Any usage | Any detected |

> Usage thresholds are evaluated against the **total usage count** over the lookback period.

### Retirement Timeline Urgency

| Retirement Window | Effect |
|-------------------|--------|
| < 30 days | +Critical override (immediate action) |
| < 90 days | Escalate severity by one level |
| < 180 days | Add urgency flag |

### ACS Service Status and Effective Dates

| Channel | Status Type | Effective Date |
|---------|------------|---------------|
| Email Service (standalone) | 🔴 Retirement | **2029-03-31** |
| SMS API (standalone) | 🔴 Retirement | **2029-03-31** |
| Chat SDK (standalone) | 🔴 Retirement | **2029-03-31** |
| Calling SDK (standalone) | 🟡 Breaking Change | **2029-03-31** — must integrate with Teams |
| Phone Numbers SDK (standalone) | 🔴 Retirement | **2029-03-31** ⚠️ New customers cannot acquire numbers after 2026-03-18 |

> Always verify current retirement dates at: https://aka.ms/acs-retirement-and-breaking-changes-guide

## ACS Migration Effort Estimation

### Factor 1: Number of Impacted Channels
| Channels with Usage | Effort |
|--------------------|--------|
| 3+ channels | High (complex multi-service migration) |
| 2 channels | Medium |
| 1 channel | Low |

### Factor 2: Channel Complexity
| Channel | Base Effort |
|---------|-------------|
| Calling SDK | High (real-time communications architecture) |
| Chat SDK | Medium (message threading, history, participants) |
| Email Service | Medium (templates, attachments, delivery tracking) |
| SMS API | Low (simple send/receive pattern) |
| Phone Numbers SDK | Low (number management, routing) |

### Factor 3: Usage Volume
| Volume | Effort Modifier |
|--------|----------------|
| >10,000 operations | +High (extensive testing required) |
| >1,000 operations | +Medium |
| <1,000 operations | No change |

## Workflow

### 0) **Load Knowledge References**
   Read the following knowledge files before beginning analysis:
   - Read `docs/knowledge/acs-severity-thresholds.md` — severity thresholds and migration effort matrix
   - Read `docs/knowledge/acs-retirement-dates.md` — channel status types, effective dates, and urgency tiers
   - Read `docs/knowledge/acs-migration-paths.md` — migration paths and guide links per channel

### 1) **Load ACS Resource Inventory**
   - Retrieve inventory with detection results from session state
   - Verify detection data exists (from skill 2 or skill 3)
   - If no detection data: Exit with "Run 2-acs-channel-detect or 3-acs-metrics-collect first"

### 2) **For Each ACS Resource**
   - Display: "🔍 Analyzing impact: [Resource Name]"
   - Initialize ACS impact assessment object:
     ```
     {
       ResourceName: "...",
       SubscriptionName: "...",
       ResourceGroup: "...",
       Location: "...",

       TotalChannelsImpacted: 0,
       ChannelsWithUsage: [],
       ChannelUsageSummary: {},

       HighestSeverity: "None",
       SeverityReason: "",

       MigrationEffortEstimate: "None",
       EffortReason: "",
       EffortBreakdownByChannel: {},

       RecommendedPriority: 0,
       MigrationGuideLinks: [],
       NextSteps: []
     }
     ```

### 3) **Calculate Severity Per Channel**
   For each detected channel:
   - Apply usage-based severity thresholds (see table above)
   - Apply timeline urgency modifier (if retirement date known)
   - Check resource tags: `Environment=Production` → increase severity
   - Track highest severity across all channels
   - Build severity reason string:
     ```
     Example: "Critical: Email (1,250 messages over 90 days) exceeds Warning threshold (>100)"
     ```

### 4) **Estimate Migration Effort Per Channel**
   For each channel with usage:
   - Assign base effort by channel complexity
   - Apply usage volume modifier
   - Combine: `max(base, volume_modifier)`

   **Final combined effort:**
   - High: Any single channel is High effort, OR 3+ channels impacted
   - Medium: Highest channel effort is Medium, OR 2 channels impacted
   - Low: All channels are Low effort AND only 1 channel impacted

   Build effort reason:
   ```
   Example: "High effort: Calling SDK requires real-time architecture changes (500+ calls)"
   ```

### 5) **Assign Migration Guide Links**
   Map each detected channel to its migration guide:

   | Channel | Migration Guide |
   |---------|----------------|
   | Email | Retirement Guide | https://aka.ms/acs-email-migration |
   | SMS | Retirement Guide | https://aka.ms/acs-sms-migration |
   | Chat | Retirement Guide | https://aka.ms/acs-chat-migration |
   | Calling | Breaking Change Guide | https://aka.ms/acs-calling-migration |
   | Phone Numbers | Retirement Guide | https://aka.ms/acs-phone-migration |

   > Full guide: https://aka.ms/acs-retirement-and-breaking-changes-guide

### 6) **Calculate Priority Score**
   ```
   Priority Score =
     Severity (Critical=100, Warning=50, Info=10) +
     Effort (High=30, Medium=20, Low=10) +
     Usage Volume (>10k ops=20, >1k ops=10) +
     Timeline (<30 days=50, <90 days=25, <180 days=10)
   ```
   Sort resources by priority score descending (highest = Priority 1).

### 7) **Generate ACS-Specific Next Steps**
   Based on severity + detected channels:

   **Critical Resources:**
   ```
   1. ⚠️ URGENT: Schedule migration planning meeting this sprint
   2. Review migration guide(s): [Links per channel]
   3. Estimate engineering effort: [Effort estimate] per channel
   4. Plan cutover timeline before [Retirement Date]
   5. Engage ACS support if migration guidance is unclear
   ```

   **Warning Resources:**
   ```
   1. Review channel usage patterns — confirm ongoing necessity
   2. Read migration guides: [Links per channel]
   3. Plan migration sprint within next quarter
   4. Consider ACS migration grace periods if available
   ```

   **Info Resources / Zero Usage:**
   ```
   1. Confirm resource is still needed (zero usage detected)
   2. Consider decommissioning if no longer in use
   3. If still needed, plan low-priority migration
   ```

### 8) **Display Impact Analysis Results**
   ```
   === ACS Impact Analysis Results ===

   ┌──────────────────┬────────────┬──────────────┬──────────────┬──────────┐
   │ Resource         │ Channels   │ Severity     │ Effort       │ Priority │
   ├──────────────────┼────────────┼──────────────┼──────────────┼──────────┤
   │ ACSProd          │ 3          │ 🔴 Critical  │ High         │ 1        │
   │ ACSDevAndTest    │ 0          │ ✅ None      │ None         │ -        │
   └──────────────────┴────────────┴──────────────┴──────────────┴──────────┘

   Severity Summary:
     🔴 Critical: 1 resource(s) — IMMEDIATE ACTION REQUIRED
     🟡 Warning:  0 resource(s)
     ℹ️ Info:     0 resource(s)
     ✅ None:     1 resource(s) — no migration needed

   Migration Effort:
     High:   1 resource(s) — 3-4 weeks per resource
     Medium: 0 resource(s)
     Low:    0 resource(s)
   ```

### 9) **Save Impact Analysis to Session State**
   - Update inventory with severity, effort, priority, and next steps
   - Store migration guide links per resource/channel

## Output
- Severity per resource (Critical / Warning / Info / None)
- Migration effort per resource and per channel
- Priority ranking (highest urgency first)
- ACS migration guide links for each impacted channel
- Specific next steps tailored to ACS retirement timeline

## Related Skills
- Requires **1-acs-resource-scan** + either **2-acs-channel-detect** or **3-acs-metrics-collect**
- Use **5-acs-report-generate** after this skill to export results

## Reference Implementation
See [scripts/powershell/acs-impact-assessment-tool.ps1](../../../../scripts/powershell/acs-impact-assessment-tool.ps1) lines 366-384 for example implementation.
