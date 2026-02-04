# Spec: Verify OpenClaw Free Tier

**Status:** 🔲 NOT STARTED  
**Priority:** P0 (BLOCKS everything else)  
**Owner:** Sean Girgis  
**Goal:** Confirm OpenClaw free Kimi 2.5 actually works at zero cost

---

## 1. Purpose

Set up **fresh** OpenClaw instance on this PC with Kimi 2.5 free tier. Verify it works before building any bot features.

**Success = 100+ queries at $0.00 with acceptable quality.**

---

## 2. User Context (YOU ANSWERED)

| Question | Your Answer |
|----------|-------------|
| Access method | Telegram bot (@SeanJobsBot) |
| API credentials | Just Telegram bot, open to create new via BotFather |
| Current setup | Running on this PC, but **SCRAP IT - start fresh** |
| Billing | Unknown, but Kimi 2.5 is free; okay with metered if needed |

**Decision:** Fresh OpenClaw install on this PC. New Telegram bot. Kimi 2.5 free tier.

---

## 3. Setup Plan (Fresh Install)

### Step 1: Create New Telegram Bot (5 minutes)

```
1. Open Telegram
2. Message @BotFather
3. Send: /newbot
4. Name it: SeanJobsBot-v2 (or whatever)
5. Save the API token (looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)
```

**Store token in:** `C:\ecosystem\.env`

```
TELEGRAM_BOT_TOKEN=your_token_here
```

### Step 2: Install OpenClaw Fresh (10 minutes)

```powershell
# Option A: If OpenClaw has Windows installer
# Download from official site and install

# Option B: If Docker-based
docker pull openclaw/latest  # or whatever the image is

# Option C: Python package
pip install openclaw
```

**Need to research:** What is the actual OpenClaw install method?

### Step 3: Configure OpenClaw for Kimi 2.5 Free

Configuration file: `C:\ecosystem\openclaw-config.yaml`

```yaml
model:
  provider: openclaw
  name: kimi-k2.5
  tier: free  # Critical: explicitly select free tier

telegram:
  token: ${TELEGRAM_BOT_TOKEN}
  
server:
  host: localhost
  port: 8080
```

### Step 4: Start OpenClaw

```powershell
# Start the service
openclaw start --config C:\ecosystem\openclaw-config.yaml

# Or via Docker
docker-compose up -d openclaw
```

---

## 4. Verification Test (30 minutes)

### Test Script

```python
# test_openclaw_free.py
"""Verify OpenClaw free tier with fresh install."""

import asyncio
import time
from telegram import Bot
from datetime import datetime
from secondbrain import remember

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
TEST_QUERIES = [
    "Write a LinkedIn connection request for a data engineering manager",
    "Summarize this job description: Senior Python Developer at Acme Corp...",
    "Is this job posting a scam? Red flags to watch for?",
    "What salary should I ask for Senior Data Engineer in Dallas?",
    "Tailor my resume for this Python role requiring AWS and Spark",
    # ... 95 more realistic job-hunting queries
]

async def test_openclaw():
    bot = Bot(token=TELEGRAM_TOKEN)
    results = {
        "start_time": datetime.now().isoformat(),
        "queries_sent": 0,
        "success_count": 0,
        "error_count": 0,
        "total_latency_ms": 0,
        "errors": [],
        "responses": []
    }
    
    for i, query in enumerate(TEST_QUERIES[:10]):  # Start with 10
        print(f"Query {i+1}/10: {query[:50]}...")
        
        start = time.time()
        try:
            # Send to Telegram bot
            # Note: Need to know the chat_id or use bot's own messaging
            # This is placeholder - actual implementation depends on OpenClaw's interface
            
            latency = (time.time() - start) * 1000
            results["success_count"] += 1
            results["total_latency_ms"] += latency
            
        except Exception as e:
            results["error_count"] += 1
            results["errors"].append({"query": i, "error": str(e)})
        
        results["queries_sent"] += 1
        time.sleep(1)  # Be polite to free tier
    
    results["end_time"] = datetime.now().isoformat()
    results["avg_latency_ms"] = results["total_latency_ms"] / max(results["queries_sent"], 1)
    
    # Store results
    remember(
        key="openclaw_free_tier_test_results",
        value=results,
        metadata={"type": "test", "category": "cost_verification"}
    )
    
    print(f"\nResults:")
    print(f"  Success: {results['success_count']}/{results['queries_sent']}")
    print(f"  Avg latency: {results['avg_latency_ms']:.0f}ms")
    print(f"  Errors: {results['error_count']}")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_openclaw())
```

---

## 5. What We're Verifying

### The "Free" Claim

From research:
> "OpenClaw announced free, unlimited access to Kimi K2.5"

**Test for:**
- [ ] No credit card required during setup
- [ ] 10 queries work without payment prompt
- [ ] 100 queries work without rate limit
- [ ] Response quality is acceptable
- [ ] No "upgrade to continue" messages

### If Free Tier Has Limits

Document what we find:
- Queries per minute/hour/day?
- Response quality degradation?
- Features locked behind paywall?

---

## 6. Decision Matrix

| Outcome | Criteria | Next Action |
|---------|----------|-------------|
| **✅ Full Success** | 100 queries, $0, <5s latency, good quality | **Proceed with OpenClaw as primary LLM** |
| **⚠️ Partial** | Works but rate limited (e.g., 50/day) | **Use OpenClaw for batch + Ollama for realtime** |
| **❌ Free Tier Broken** | Payment required or doesn't work | **Pivot to Ollama local only** |
| **❌ Metered Only** | No free tier, pay per token | **Your call: pay or go Ollama** |

---

## 7. Open Questions (Need Research)

### Critical: I Don't Know OpenClaw's Actual Setup

**Need to find out:**

1. **What IS OpenClaw exactly?**
   - A Python package? `pip install openclaw`?
   - A Docker container?
   - A Windows executable?
   - A cloud service?

2. **Where do we get it?**
   - GitHub: github.com/openclaw/openclaw?
   - Website: openclaw.io?
   - Package manager: pip/choco/winget?

3. **How do we configure Kimi 2.5 free tier?**
   - Config file?
   - Environment variables?
   - Web UI?

4. **Is there ACTUALLY a free tier?**
   - Or is it "free trial" for 7 days?
   - Or "free" with limited features?

---

## 8. Immediate Next Step

**You need to research OpenClaw installation.**

I cannot write the complete test script until we know:
- How to install OpenClaw
- How to configure it for Kimi 2.5
- Whether free tier actually exists

**Your homework:**

1. **Search:** "OpenClaw install Windows" or "OpenClaw Docker"
2. **Find:** The actual OpenClaw GitHub or website
3. **Check:** Is there a free tier, or just "free trial"?
4. **Report back:** Installation method and free tier confirmation

**Alternative:** If you have the old OpenClaw running, check its:
- Version number
- Installation location
- Configuration files

Then we can replicate or upgrade it.

---

## 9. Risk: OpenClaw May Not Exist As Described

**Reality check:** The research file mentioned:
- "OpenClaw (formerly Clawdbot/MoltBot)"
- Free Kimi K2.5 tier

**But:** I need to verify this is real and current.

**If OpenClaw doesn't exist or has no free tier:**
- Plan B: Use Kimi Code CLI (you already have Kimi CLI installed)
- Plan C: Use Kimi API directly (may have free credits)
- Plan D: Fall back to Ollama local

---

## 10. Summary

| Step | Status | Owner |
|------|--------|-------|
| Research OpenClaw install | 🔲 NOT DONE | You |
| Create Telegram bot | 🔲 NOT DONE | You |
| Install OpenClaw fresh | 🔲 NOT DONE | You/Me |
| Configure Kimi 2.5 free | 🔲 NOT DONE | You/Me |
| Run 100 query test | 🔲 NOT DONE | Me |
| Document results | 🔲 NOT DONE | Me |

**Blocker:** I need you to find the actual OpenClaw installation instructions.

---

## Your Action Items

1. **Google:** "OpenClaw install" or "Clawdbot install"
2. **Check:** Your current OpenClaw installation (version, location)
3. **Verify:** Is free Kimi 2.5 tier actually available?
4. **Report back:** What you find

**Then I complete the setup and test script.**
