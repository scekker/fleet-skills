---
name: pre-action-gate
description: >
  Structural memory check that fires BEFORE high-risk actions (SSH, fleet node operations,
  science claims, citations, external sends). Takes action_type + target + claim, returns
  MEMORY_CONFIRMS / MEMORY_SILENT / MEMORY_CONTRADICTS before the agent proceeds.
  Use when about to SSH a fleet node, post a citation, publish a result, or make any factual
  claim about a fleet node's configuration. This is the Fleet Memory Gate pilot skill — the
  answer to DIAGNOSIS_WITHOUT_MEMORY and CORRECTION_RESISTANCE failure modes.
---

# Pre-Action Gate

A structural habit, not a rule. Before high-risk actions, check what you already know.
The output changes the action. You can't un-read "MEMORY_CONTRADICTS."

## The Three Outputs

Every gate check returns exactly one of:

- **`MEMORY_CONFIRMS:`** — Memory has verified data. State it. Proceed.
- **`MEMORY_SILENT`** — Nothing in memory about this. Proceed with caution, stay alert.
- **`MEMORY_CONTRADICTS:`** — Memory says something different. STOP. Re-read. Update your plan.

## When to Fire the Gate

### Domain: fleet-infra (SSH, gateway, config)
**Trigger:** Any SSH command, `openclaw gateway restart`, config write, or status claim about a fleet node.

**Check:** Read the relevant section of `memory/infrastructure.md` for that node.

**State before proceeding:**
> "infrastructure.md says [node] is set up as: [summary of user, path, restart method]"

**Example:**
```
About to: ssh ekker@100.120.104.61 'openclaw gateway restart'
Gate fires: read memory/infrastructure.md → SARAH section
Output: MEMORY_CONFIRMS: SARAH runs as ekker, gateway at /Users/ekker/Library/LaunchAgents/..., restart via SSH as ekker ✅
Proceed.
```

---

### Domain: citations / literature
**Trigger:** Any PMID, DOI, or paper title stated in output destined for a channel or document.

**Check:** `ncbi_efetch(pmid)` → verify title + authors match what you claimed.

**State before proceeding:**
> "PubMed confirms PMID [X] = [title] by [authors] ✅" or "MISMATCH — claimed [X], actual [Y] ❌"

**Owner:** Zevo 🦓 (pilot lead for this domain)

---

### Domain: science-claims
**Trigger:** Any mechanistic claim ("RNAi doesn't work for mt-encoded genes"), structure detail, or sequence assertion not directly computed in this session.

**Check:** `memory_search("[topic]")` → verify claim is supported by what's in memory, not reconstructed.

**State before proceeding:**
> "memory confirms: [claim source]" or "memory silent on this — treating as uncertain"

**Owner:** Atlas 🏛️ (pilot lead for this domain)

---

### Domain: pipeline-results
**Trigger:** Any score, rank, or result posted to a channel or stated to a human.

**Check:** `read [actual output file]` — not from memory, not from the last log line. The file.

**State before proceeding:**
> "Read [filename] at [timestamp]: top result is [X] with score [Y]"

**Owner:** Buster 🐕 (pilot lead for this domain)

---

### Domain: fleet-status
**Trigger:** Any assertion about another fleet node's state ("Buster is running X", "SARAH is down").

**Check:** `ssh [node] 'ps aux | grep openclaw'` or equivalent live check. Not from memory alone.

**State before proceeding:**
> "Live check: [node] shows [result]"

**Owner:** SARAH 🏠 (pilot lead for this domain)

---

### Domain: external-send
**Trigger:** Any email, channel post containing factual claims, or Drive document publish.

**Check:** `memory_search("[topic of claim]")` — verify the claim is grounded before it leaves the fleet.

**State before proceeding:**
> "Memory confirms [claim] / Memory silent — flagging as uncertain in the output"

**Owner:** Atlas 🏛️ (co-lead with Uvy)

---

## The Correction Signal (when the gate catches something)

When MEMORY_CONTRADICTS fires, emit a structured correction signal immediately:

```json
{
  "signal_version": "0.1",
  "timestamp": "<ISO-8601>",
  "agent": "<agent name>",
  "domain": "<domain>",
  "session_context": "<brief: what was happening>",
  "action_taken": "<what agent was about to do or claim>",
  "ground_truth": "<what memory/tool says is actually correct>",
  "failure_mode": "skipped_check | stale_memory | wrong_assumption | confabulation | stale_context",
  "correction_source": "self | human | peer_agent | tool_output",
  "gate_fired": true,
  "severity": "low | medium | high",
  "session_age_hours": "<float>",
  "context_utilization_pct": "<int>"
}
```

Append to: `memory/correction-signals.jsonl` (local)
Also post to `#self-improvements` if severity = high.

Severity guide (Zevo's calibration):
- `high` = external action taken/nearly taken on wrong info, OR human was in degraded state (late night, long day)
- `medium` = internal claim wrong, caught before external action
- `low` = near-miss, caught before action, no external exposure

---

## Notes

- The gate is **not blocking** — it's structural. One extra step before proceeding.
- **Don't skip it in execution mode** — that's exactly when it matters most.
- If you're mid-task and realize you skipped the gate: stop, fire it retroactively, correct if needed.
- Session age and context % should always be included in the signal — Zevo confirmed failure rates correlate with these.
- Drive file as canonical signal store (Zevo's recommendation): lower infra cost, fleet-accessible, survives gateway restarts. API endpoint = later.

## Pilot Metrics

Track in `memory/correction-signals.jsonl`:
- Did the gate fire before the action?
- Did it catch a mismatch?
- What domain?
- What failure mode?

Fleet-level aggregation: "Uvy has emitted 3 DIAGNOSIS_WITHOUT_MEMORY signals in 24h" → pattern, different response than single event. MoE layer to aggregate (Zevo's question — yes, this needs a separate aggregation component).

*Fleet Memory Gate pilot — opened Apr 4, 2026. Zevo, Atlas, Buster, SARAH all contributing.*
