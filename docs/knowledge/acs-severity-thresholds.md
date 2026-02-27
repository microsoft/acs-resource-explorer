# ACS Severity Thresholds

**Used by:** acs/4-acs-impact-analyze, acs/5-acs-report-generate
**Last Updated:** 2026-02-27
**Update This File When:** Threshold values are recalibrated based on customer feedback or new channel data.

---

## Usage-Based Severity Thresholds

Thresholds are evaluated against **total usage count over the lookback period** (default: 90 days).

| Severity | Email | SMS | Chat | Calling | Phone Numbers |
|----------|-------|-----|------|---------|---------------|
| **Critical** | > 1,000 messages | > 500 messages | > 10,000 messages | > 500 calls | > 1,000 operations |
| **Warning** | > 100 messages | > 50 messages | > 1,000 messages | > 50 calls | > 100 operations |
| **Info** | Any usage | Any usage | Any usage | Any usage | Any usage |
| **None** | 0 | 0 | 0 | 0 | 0 |

> If **multiple channels** are detected, the **highest severity** across all channels is used as the resource's overall severity.

---

## Retirement Timeline Urgency Modifiers

Applied on top of usage-based severity when retirement date is known.

| Days Until Retirement | Override / Modifier |
|-----------------------|---------------------|
| < 30 days | **Override to Critical** (regardless of usage) |
| < 90 days | **Escalate severity** one level (Info→Warning, Warning→Critical) |
| < 180 days | Add urgency flag in report (no severity change) |
| > 180 days | No modifier — standard thresholds apply |

> Retirement dates are in [acs-retirement-dates.md](./acs-retirement-dates.md).

---

## Migration Effort Matrix

### Factor 1: Channels Impacted (primary driver)

| Channels with Usage | Effort |
|--------------------|--------|
| 3 or more | **High** |
| 2 | **Medium** |
| 1 | Determined by channel complexity (see below) |

### Factor 2: Channel Base Complexity

| Channel | Base Effort |
|---------|-------------|
| Calling SDK | High |
| Chat SDK | Medium |
| Email Service | Medium |
| SMS API | Low |
| Phone Numbers SDK | Low |

### Factor 3: Usage Volume Modifier

| Total Operations (across all channels) | Modifier |
|----------------------------------------|---------|
| > 10,000 | +High |
| > 1,000 | +Medium |
| ≤ 1,000 | No change |

### Combined Effort Rule

```
Final Effort = max(Factor1, Factor2, Factor3)

High   > Medium  > Low
```

---

## Priority Score Formula

Used to sort resources — highest score = Priority 1 (act first).

```
Priority Score =
  Severity score:    Critical=100, Warning=50, Info=10, None=0
  + Effort score:    High=30, Medium=20, Low=10, None=0
  + Volume score:    >10,000 ops=20, >1,000 ops=10, else=0
  + Timeline score:  <30 days=50, <90 days=25, <180 days=10, else=0
```

---

## Production Tag Modifier

If an ACS resource has the tag `Environment=Production`, increase severity by one level:

```
None → Info
Info → Warning
Warning → Critical
Critical → Critical (no change)
```

---

## Effort Time Estimates (for reporting)

| Effort Level | Estimated Engineering Time |
|-------------|---------------------------|
| High | 3–4 weeks per resource |
| Medium | 1–2 weeks per resource |
| Low | 2–5 days per resource |
| None | No action needed |
