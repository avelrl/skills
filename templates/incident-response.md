# Incident Response: [Incident Title]

**Severity**: [S1-Critical / S2-Major / S3-Moderate / S4-Minor]
**Status**: [Active / Mitigated / Resolved / Post-Mortem Complete]
**Detected**: [Date Time UTC]
**Resolved**: [Date Time UTC or ONGOING]
**Duration**: [Total time from detection to resolution]
**Incident Commander**: [Name/Role]

---

## Impact Summary

[2-3 sentences describing what users, customers, or operators experienced.]

- **Affected users / requests / systems**: [estimated count or percentage]
- **Affected surfaces**: [service, app, API, region, platform]
- **Regions affected**: [All / specific regions]
- **Business impact**: [estimated if applicable]

---

## Timeline

| Time (UTC) | Event | Action Taken |
| ---- | ---- | ---- |
| [HH:MM] | Incident detected via [monitoring/player report/etc.] | Incident commander assigned |
| [HH:MM] | Root cause identified | [Brief description of cause] |
| [HH:MM] | Mitigation deployed | [What was done] |
| [HH:MM] | Service restored / Fix confirmed | Monitoring for recurrence |
| [HH:MM] | All-clear declared | Post-mortem scheduled |

---

## Root Cause

### What Happened
[Technical description of the root cause. Be specific about the chain of events
that led to the incident.]

### Why It Happened
[Systemic cause — why did existing processes, tests, or safeguards fail to
prevent this? This is more important than the technical cause.]

### Contributing Factors
- [Factor 1 — e.g., "Insufficient load testing for the new matchmaking system"]
- [Factor 2 — e.g., "Monitoring alert threshold was set too high"]
- [Factor 3]

---

## Mitigation and Resolution

### Immediate Actions (during incident)
1. [Action taken to stop the bleeding]
2. [Action taken to restore service]
3. [Action taken to verify resolution]

### Follow-Up Actions (after resolution)
1. [Permanent fix if immediate action was a workaround]
2. [Additional testing or monitoring added]
3. [Process changes to prevent recurrence]

---

## Player Communication
## Communication

### Initial Acknowledgment
*Sent: [Time] via [channel]*
> [Exact text of the first public message acknowledging the issue]

### Status Updates
*Sent: [Time] via [channel]*
> [Text of each subsequent update]

### Resolution Notice
*Sent: [Time] via [channel]*
> [Text announcing the fix and any compensation]

### Remediation Credit / Customer Follow-Up (Optional)
- **What**: [credit, SLA action, apology, refund, service extension]
- **Who**: [affected customers only / all impacted accounts / internal stakeholders]
- **When**: [delivery date and method]
- **Rationale**: [why this is the appropriate follow-up]

---

## Prevention

### What We Are Changing

| Action Item | Owner | Deadline | Status |
| ---- | ---- | ---- | ---- |
| [Specific preventive measure] | [Role] | [Date] | [TODO/Done] |
| [Add monitoring for X] | [Role] | [Date] | [TODO/Done] |
| [Add test coverage for Y] | [Role] | [Date] | [TODO/Done] |
| [Update runbook for Z] | [Role] | [Date] | [TODO/Done] |

### Process Improvements
- [Process change to prevent similar incidents]
- [Monitoring/alerting improvement]
- [Testing improvement]

---

## Lessons Learned

### What Went Well
- [Positive aspect of incident response — e.g., "Detection was fast due to
  monitoring alerts"]
- [Positive aspect]

### What Went Poorly
- [Problem with response — e.g., "Took 20 minutes to identify the correct
  on-call person"]
- [Problem]

### Where We Got Lucky
- [Factor that reduced impact by chance rather than design — these are hidden
  risks to address]

---

## Sign-Offs

- [ ] Technical Owner — Root cause accurate, prevention plan sufficient
- [ ] Quality / Test Owner — coverage gaps addressed
- [ ] Delivery Owner — timeline and execution reviewed
- [ ] Communications Owner — external/internal communication reviewed

---
*Store this alongside incident, operations, or release records used by the project.*
