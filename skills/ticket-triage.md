# Skill: Ticket Triage
**Purpose:** Prioritize and categorize incoming tickets by urgency, impact, and SLA
**When to use:** When reviewing a batch of new tickets or when unsure how to prioritize a specific ticket

## Instructions

I'm going to give you one or more support tickets. For each ticket:

1. **Categorize** — assign a category (e.g., connectivity, email/M365, security, hardware, software, access/permissions, backup, onboarding, general request)
2. **Priority** — assign Critical / High / Medium / Low based on:
   - How many users are affected
   - Whether there's a workaround
   - Business impact (revenue, compliance, safety)
   - SLA obligations
3. **Recommended action** — suggest the first troubleshooting step or escalation path
4. **Assignment** — suggest Tier 1, 2, or 3 based on complexity

Format your response as a table:

| Ticket | Category | Priority | Reasoning | Next Step | Tier |
|--------|----------|----------|-----------|-----------|------|

If a ticket is ambiguous, flag what additional info is needed from the client.

## Example Usage

**Input:**
> "Can't print to the shared printer in the conference room. It was working yesterday."

**Output:**
| Ticket | Category | Priority | Reasoning | Next Step | Tier |
|--------|----------|----------|-----------|-----------|------|
| Printer - conference room | Hardware/Printing | Medium | Single location, workaround exists (other printers) | Check print spooler, verify network connectivity to printer, check for driver updates | Tier 1 |
