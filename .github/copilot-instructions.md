# Copilot Instructions — ACS Transition Agent

This repository contains AI Agent Skills for assessing retiring Azure Communication Services (ACS) resources across Azure subscriptions.

## What This Project Does

Scans Azure subscriptions for ACS resources that use retiring standalone SDKs and APIs, measures actual usage over 90 days, calculates migration urgency, and generates reports with migration guidance.

**Five retiring ACS channels detected:**
- Email Service (standalone ACS SDK) — retires 2027-12-31
- SMS API (standalone ACS SDK)
- Chat SDK (standalone ACS SDK)
- Calling SDK (standalone ACS SDK)
- Phone Numbers SDK (standalone ACS SDK)

## How to Run an Assessment

To start a full ACS deprecation scan, type in chat:
```
Run an ACS deprecation scan
```

This triggers the `0-acs-full-scan` skill, which runs the complete 6-step workflow interactively.

## Prerequisites (user must have these before running)

- PowerShell with the Az module installed (`Install-Module -Name Az`)
- Azure authentication completed (`Connect-AzAccount` in PowerShell)
- Reader + Monitoring Reader access on target subscriptions

## Agent Skills Location

All agent skills are in `.agent/skills/`:
- `.agent/skills/azure/` — generic skills (auth, subscription select, resource scan, metrics, report)
- `.agent/skills/acs/` — ACS-specific skills (resource scan, channel detection, impact analysis, report)

## Knowledge Base

Reference data (retirement dates, metric names, migration paths) lives in `docs/knowledge/`. When Microsoft publishes updated retirement dates or migration guidance, update these files — the skills read from them.

## Output

Reports are saved to `./exports/` in CSV, Markdown, and JSON formats.

## Migration Guides

- Email: https://aka.ms/acs-email-migration
- SMS: https://aka.ms/acs-sms-migration
- Chat: https://aka.ms/acs-chat-migration
- Calling: https://aka.ms/acs-calling-migration
- Phone Numbers: https://aka.ms/acs-phone-migration
- Retirement & Breaking Changes (comprehensive): https://aka.ms/acs-retirement-and-breaking-changes-guide
