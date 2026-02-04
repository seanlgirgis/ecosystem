# Spec: Verify OpenClaw Free Tier

**Status:** 🔲 NOT STARTED  
**Priority:** P0 (BLOCKS everything else)  
**Owner:** Sean Girgis  
**Goal:** Confirm OpenClaw free Kimi K2.5 actually works at zero cost

---

## 1. Purpose

Before building any bot features, verify that OpenClaw's "unlimited free" Kimi K2.5 claim is real. If it fails, we pivot to Ollama local immediately.

**Success = 100+ queries at $0.00 with acceptable quality.**

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| R1 | Connect to OpenClaw platform | P0 |
| R2 | Send 100 test queries via Kimi K2.5 | P0 |
| R3 | Receive responses without error | P0 |
| R4 | Confirm zero charges incurred | P0 |
| R5 | Measure response latency (< 5s acceptable) | P1 |
| R6 | Document actual rate limits (if any) | P1 |

### 2.2 Test Queries

Mix of realistic job-hunting prompts:

```
1. "Write a LinkedIn connection request for a data engineering manager"
2. "Summarize this job description: [paste]"
3. "Is this job posting a scam? Red flags?"
4. "Tailor my resume for this Python role: [paste]"
5. "What salary should I ask for Senior Data Engineer in Dallas?"
... (95 more varied queries)
```

---

## 3. Test Plan

### 3.1 Setup Phase (5 minutes)

```powershell
# 1. Ensure OpenClaw is running
#    (You mentioned @SeanJobsBot exists - verify it's active)

# 2. Check current OpenClaw configuration
#    Where is it running? Localhost? Cloud? Telegram bot?

# 3. Identify API endpoint or interface
#    - Telegram bot interface?
#    - HTTP API?
#    - CLI tool?
```

### 3.2 Test Execution

**Method A: If OpenClaw has HTTP API**
```python
import requests
import time

results = []
for i, query in enumerate(test_queries):
    start = time.time()
    response = requests.post(OPENCLAW_ENDPOINT, json={"prompt": query})
    latency = time.time() - start
    
    results.append({
        "query_num": i,
        "latency_ms": latency * 1000,
        "status_code": response.status_code,
        "response_length": len(response.text),
        "error": None if response.ok else response.text
    })
```

**Method B: If Telegram bot interface**
```python
# Use python-telegram-bot to send messages to @SeanJobsBot
# Measure response time and quality
```

**Method C: Manual testing**
```
Send 100 messages to @SeanJobsBot manually
Log: time, response quality, any errors
```

### 3.3 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Queries sent | 100 | Counter |
| Successful responses | >= 95 | 95% success rate |
| Average latency | < 5000ms | Timer |
| Errors | <= 5 | Error log |
| Cost incurred | $0.00 | Billing check |
| Rate limit hit | Never | Error log review |

---

## 4. What We're Verifying

### The "Unlimited" Claim

From research file `00000002.md`:
> "OpenClaw announced free, unlimited access to Kimi K2.5 — no usage caps, no time limits"

**We test for:**
- [ ] Hard rate limit (X queries per hour)
- [ ] Soft rate limit (slowdown after N queries)
- [ ] Daily/weekly cap
- [ ] Quality degradation at scale
- [ ] Surprise charges

### Red Flags to Watch For

| Symptom | Interpretation |
|---------|----------------|
| "Please upgrade to continue" | Not actually free |
| Responses get slower | Throttling |
| Random errors after 50 queries | Hidden rate limit |
| Request for credit card | Trial, not free |
| Different model returned | Bait and switch |

---

## 5. Implementation (One-Time Test Script)

```python
# test_openclaw_free.py
"""Verify OpenClaw free tier claim. Run once, document results."""

import json
import time
from datetime import datetime
from secondbrain import remember

# Configuration
OPENCLAW_ENDPOINT = "TODO: Fill in after investigating @SeanJobsBot"
TEST_QUERIES = [
    "Write a LinkedIn connection request",
    "Summarize this job description",
    # ... 98 more
]

def test_openclaw():
    results = {
        "start_time": datetime.now().isoformat(),
        "queries_sent": 0,
        "success_count": 0,
        "error_count": 0,
        "total_latency_ms": 0,
        "errors": []
    }
    
    for i, query in enumerate(TEST_QUERIES):
        print(f"Query {i+1}/100: {query[:50]}...")
        
        start = time.time()
        try:
            # TODO: Implement actual OpenClaw call
            # response = call_openclaw(query)
            
            latency = (time.time() - start) * 1000
            results["success_count"] += 1
            results["total_latency_ms"] += latency
            
        except Exception as e:
            results["error_count"] += 1
            results["errors"].append({"query": i, "error": str(e)})
        
        results["queries_sent"] += 1
        time.sleep(0.5)  # Be polite
    
    results["end_time"] = datetime.now().isoformat()
    results["avg_latency_ms"] = results["total_latency_ms"] / results["queries_sent"]
    
    # Store results in SecondBrain
    remember(
        key="openclaw_free_tier_test_results",
        value=results,
        metadata={"type": "test", "category": "cost_verification"}
    )
    
    return results

if __name__ == "__main__":
    print("Starting OpenClaw free tier verification...")
    results = test_openclaw()
    print(f"\nResults:")
    print(f"  Success: {results['success_count']}/{results['queries_sent']}")
    print(f"  Avg latency: {results['avg_latency_ms']:.0f}ms")
    print(f"  Errors: {results['error_count']}")
```

---

## 6. Decision Matrix

After testing, one of three outcomes:

| Outcome | Result | Next Action |
|---------|--------|-------------|
| **✅ Success** | 95%+ success, $0 cost, <5s latency | Proceed with OpenClaw as primary LLM |
| **⚠️ Partial** | Works but rate limits or slow | Use OpenClaw + Ollama fallback |
| **❌ Fail** | Errors, charges, or unusable | Pivot to Ollama local only |

---

## 7. Open Questions (You Need to Answer)

Before I can implement the test:

1. **How do you currently access OpenClaw?**
   - Telegram bot (@SeanJobsBot)?
   - Web interface?
   - API endpoint?
   - CLI tool?

2. **Do you have API credentials?**
   - API key?
   - Token?
   - Just the Telegram bot?

3. **Where is OpenClaw running?**
   - Your local machine?
   - Cloud server?
   - I don't know?

4. **How do you currently check billing?**
   - OpenClaw dashboard?
   - You don't (trust "free")?
   - Credit card statement?

---

## 8. Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| "Free" actually has limits | Medium | Test with 100 queries, watch for throttling |
| OpenClaw shuts down | Low | Fallback to Ollama local |
| Test takes too long | Low | Can run overnight |
| No API access (only Telegram) | Medium | Use Telegram bot library instead of HTTP |

---

## 9. References

- Research: `C:\secondBrain\Conversation_Tracker\00000002.md`
- OpenClaw announcement: https://vertu.com/ai-tools/openclaw-drops-bombshell-kimi-k2-5-becomes-first-free-premium-model/
- Kimi Code: https://www.kimi.com/code

---

## 10. Next Step

**You answer the 4 questions in Section 7.**

Then I complete the test script and we run it.

**Estimated time:** 30 minutes to run test, immediate results.
