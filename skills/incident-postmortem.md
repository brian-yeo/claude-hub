# Skill: Incident Postmortem
**Purpose:** Structure a post-incident review with timeline, root cause, and action items
**When to use:** After resolving a significant incident — outage, security event, data loss, or SLA breach

## Instructions

I need to write a post-incident review. I'll provide details about what happened — raw notes, ticket info, timeline fragments, whatever I have.

Generate a structured postmortem document:

### 1. Incident Summary
- **Date/time:** Start, detection, resolution (include timezone)
- **Duration:** Total downtime or impact window
- **Severity:** Critical / High / Medium
- **Affected client(s):** Who was impacted
- **Impact:** What broke, how many users, business effect

### 2. Timeline
Chronological table of events:

| Time | Event | Who |
|------|-------|-----|
| HH:MM | [What happened] | [Person/system] |

Include: first symptom, detection, escalation points, key troubleshooting steps, resolution, client communication.

### 3. Root Cause
- What specifically caused the incident
- Contributing factors (not just the trigger — what made it possible)

### 4. What Went Well
- Detection speed, response, communication, teamwork — call out what worked

### 5. What Needs Improvement
- Gaps in monitoring, process, communication, or tooling that this incident exposed

### 6. Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| [Specific action] | [Name] | [Date] | High/Med/Low |

Every action item must be specific and assignable. "Improve monitoring" is not an action item. "Add uptime check for [service] in [monitoring tool]" is.

### 7. Client Communication
- Draft a client-facing summary suitable for email: what happened, what we did, what we're doing to prevent recurrence. Professional tone, no blame, no unnecessary technical detail.

Keep the internal postmortem blameless. Focus on systems and processes, not individuals.
