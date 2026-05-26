# Claude Instructions — ACS Transition Agent

## Non-negotiable rules

**Never make assumptions.**
If data is missing, a query returns zero results, or documentation is ambiguous, say so and ask. Do not fill gaps with inferred, fabricated, or "likely" values.

Zero results from a query means zero results — it does not mean the metric does not exist. It may mean the resource has no activity, the wrong resource was queried, or the metric names were incorrect.

**Never use phantom data or false data.**
Do not invent metric names, API names, field names, or any other technical values. Every name, ID, or value used in knowledge files, skill files, or code must be verified against a live query or authoritative Microsoft documentation. If it cannot be verified, leave it blank and flag it explicitly.
