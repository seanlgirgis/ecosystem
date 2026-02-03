# Spec: Cost Optimization & Free Tier Integration

**Status:** 🔲 NOT STARTED  
**Priority:** HIGH (Financial Constraint)  
**Owner:** Sean Girgis  
**Context:** Unemployed, every dollar matters

---

## 1. Purpose

Maximize free resources, minimize paid API costs. Achieve 100% functionality at minimal expense.

**Primary Goal:** Reduce commercial AI API spend to **$0 or near-zero** while maintaining capability.

---

## 2. Financial Context

| Current State | Target State |
|--------------|--------------|
| OpenRouter API calls ($$$) | OpenClaw Free Tier ($0) |
| Commercial embeddings ($) | Ollama local ($0) |
| Cloud vector DB ($) | Local Qdrant ($0) |
| **Monthly burn: $X** | **Monthly burn: ~$0** |

---

## 3. Free Resources Inventory

### 3.1 Confirmed Free Tiers

| Service | What | Limits | Integration |
|---------|------|--------|-------------|
| **OpenClaw** | Kimi K2.5 | "Unlimited, no caps" | Primary LLM |
| **Ollama** | Local LLMs | Hardware limited | Fallback LLM |
| **GitHub** | Code hosting | Public repos | Project storage |
| **Docker Desktop** | Container runtime | Personal use | Infrastructure |
| **Qdrant** | Vector DB | Self-hosted | Knowledge storage |

### 3.2 Suspicious/Verify Before Using

| Service | Claim | Verification Needed |
|---------|-------|---------------------|
| NVIDIA NIM | "Free trial" | Time limits, credit card required |
| Various APIs | "Free tier" | Rate limits, data collection |

**Rule:** If it requires a credit card, it's not truly free. Verify "unlimited" claims with actual usage.

---

## 4. Architecture: Zero-Cost Stack

```
User Input
    |
    v
┌─────────────────────────────────────┐
│     ClawBot Model Router            │
│  (Priority-based selection)         │
└─────────┬──────────┬────────────────┘
          |          |
    ┌─────┘          └─────┐
    v                      v
┌─────────────┐      ┌─────────────┐
│  1st: Cache │      │  2nd:       │
│  (Second    │      │  OpenClaw   │
│   Brain)    │      │  FREE TIER  │
└──────┬──────┘      └──────┬──────┘
       |                    |
   Hit?├────Yes────→ Return cached
       |
       No
       |
       v
┌─────────────┐      ┌─────────────┐
│  3rd:       │      │  4th:       │
│  Ollama     │      │  Error/     │
│  Local      │      │  Queue      │
└─────────────┘      └─────────────┘
```

---

## 5. Implementation Plan

### Phase A: OpenClaw Free Tier Integration (Week 1)

**Goal:** Route all LLM calls through OpenClaw free tier.

**Tasks:**
- [ ] Verify OpenClaw free tier actually works (prototype)
- [ ] Configure @SeanJobsBot to use OpenClaw Kimi K2.5
- [ ] Test with real workload (job search queries)
- [ ] Measure: latency, quality, rate limits (if any)
- [ ] Document: actual vs claimed limits

**Acceptance Criteria:**
- [ ] 100 queries via OpenClaw free tier without cost
- [ ] Response quality comparable to OpenRouter
- [ ] No rate limiting encountered

### Phase B: Local Fallback Stack (Week 2-3)

**Goal:** If OpenClaw fails, fall back to local Ollama.

**Tasks:**
- [ ] Docker compose for Ollama (qwen2.5:32b, llama3.1:8b)
- [ ] Model router logic: OpenClaw → Ollama → Cache → Fail
- [ ] Benchmark local models vs OpenClay quality
- [ ] Document when to use which model

**Acceptance Criteria:**
- [ ] Local models respond < 5 seconds
- [ ] Graceful degradation when offline
- [ ] Zero paid API calls in local-only mode

### Phase C: Cache Maximization (Week 4)

**Goal:** Increase cache hit rate to 50%+.

**Tasks:**
- [ ] Analyze query patterns (what repeats?)
- [ ] Tune similarity threshold (90%? 85%?)
- [ ] Pre-warm cache with common queries
- [ ] Dashboard: $ saved, hit rate, cache size

**Acceptance Criteria:**
- [ ] Cache hit rate > 50%
- [ ] Dashboard shows estimated $ saved
- [ ] Pre-warmed cache covers 80% of common queries

---

## 6. Cost Monitoring

### 6.1 Tracking Metrics

```python
# Log every inference decision
cost_log = {
    "timestamp": "2026-02-03T10:00:00Z",
    "query": "Find Python jobs",
    "route": "openclaw_free",  # or "ollama_local", "cache_hit", "openrouter_paid"
    "cost_usd": 0.0,
    "latency_ms": 1200,
    "model": "kimi-k2.5"
}
```

### 6.2 Monthly Report

Auto-generate:
```
February 2026 Cost Report
=========================
Total Queries:    1,247
- Cache hits:     623 (50%)     $0.00
- OpenClaw free:  600 (48%)     $0.00
- Ollama local:    24 (2%)      $0.00
- OpenRouter:       0 (0%)      $0.00

Estimated Savings: $186.00 vs all-paid
Status: ZERO COST ACHIEVED
```

---

## 7. Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OpenClaw ends free tier | Medium | High | Local Ollama fallback ready |
| OpenClaw rate limits | Medium | Medium | Queue + retry logic |
| Local GPU insufficient | Low | Medium | Use smaller models (phi3) |
| Internet outage | Low | High | Full local mode (Ollama + pickle) |

---

## 8. Out of Scope (Too Expensive)

- ❌ Cloud GPU rentals (RunPod, Vast.ai)
- ❌ Commercial vector DB hosting (Pinecone, Weaviate Cloud)
- ❌ Managed Kubernetes
- ❌ CI/CD pipelines with paid minutes
- ❌ Any service requiring credit card

---

## 9. Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Monthly AI API spend | $0 | Review billing |
| Cache hit rate | > 50% | get_cache_stats() |
| Free tier reliability | 99% | Uptime log |
| Local fallback works | Yes | Test monthly |

---

## 10. Immediate Action Items

1. **Verify OpenClaw claim** — Test 100+ queries this week
2. **Document actual limits** — Not "unlimited", find the real number
3. **Set up cost dashboard** — Track every $0.00 saved
4. **Switch default to free** — Make OpenClaw primary immediately if it works

---

## 11. References

- Research: `C:\secondBrain\Conversation_Tracker\00000002.md`
- OpenClaw: https://vertu.com/ai-tools/openclaw-drops-bombshell-kimi-k2-5-becomes-first-free-premium-model/
- Kimi Code API: https://www.kimi.com/code

---

**Note:** This spec is written with the understanding that "free" services may change. The architecture must support rapid switching between free providers. Local-first is the ultimate zero-cost fallback.
