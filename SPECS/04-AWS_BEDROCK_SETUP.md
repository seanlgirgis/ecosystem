# Spec: AWS Bedrock Setup (URGENT - Life or Death Mode)

**Status:** 🔲 IN PROGRESS  
**Priority:** P0 (BLOCKER - Unemployed, need job ASAP)  
**Owner:** Sean Girgis  
**Budget:** $199 AWS credits + $30-40/month when depleted  
**Timeline:** 24 hours to working setup

---

## 1. Purpose

Get AWS Bedrock working TODAY. Use $199 credits for 4-6 months of job hunting. Speed > Cost optimization.

---

## 2. Provider Comparison (Why Bedrock Wins)

| Provider | Cost | Reliability | Speed | Your Credits |
|----------|------|-------------|-------|--------------|
| **AWS Bedrock** | Pay per token | Enterprise | Fast | **$199 FREE** ✅ |
| **Kimi API direct** | ~$0.80/1M tokens | Good | Fast | ❌ None |
| **xAI Grok** | Unknown/expensive | Beta | Fast | ❌ None |
| **OpenRouter** | +20% markup | Good | Medium | ❌ None |
| **Ollama local** | $0 | Your hardware | Slow | N/A |

**Winner: AWS Bedrock** — Use your credits, enterprise reliability, no setup friction.

---

## 3. Available Models on Your Bedrock

From OpenClaw list, these are available:

| Model | Use Case | Price Tier |
|-------|----------|------------|
| `moonshot.kimi-k2-thinking` | Primary — coding, analysis | Low |
| `anthropic.claude-3-5-sonnet` | Fallback — reasoning | Medium |
| `anthropic.claude-3-haiku` | Fast tasks — cheap | Low |
| `meta.llama3-1-70b` | Long context | Low |

**Primary:** Kimi K2.5 (matches your current tool)  
**Fallback:** Claude 3.5 Sonnet (if Kimi fails)

---

## 4. Cost Projection (AWS Bedrock)

| Activity | Monthly Usage | Cost |
|----------|--------------|------|
| Job search (50 jobs) | 100K tokens | ~$0.80 |
| Resume tailoring | 150K tokens | ~$1.20 |
| Cover letters | 100K tokens | ~$0.80 |
| Daily bot queries | 300K tokens | ~$2.40 |
| **TOTAL** | **650K tokens** | **~$5/month** |

**Your $199 credit = 40 months of usage** (or 4-6 months of intensive 10x usage).

---

## 5. Implementation Checklist (24 Hour Sprint)

### Hour 1-2: AWS Verification
- [ ] Run setup script: `.\scripts\setup_aws_bedrock.ps1`
- [ ] Verify profile "study" works
- [ ] List available models
- [ ] Test simple inference

### Hour 3-4: Integration
- [ ] Create Bedrock client wrapper
- [ ] Connect to SecondBrain (cache responses)
- [ ] Test job description analysis

### Hour 5-8: Job Search Skill (MVP)
- [ ] Scrape LinkedIn/Indeed
- [ ] Analyze 10 jobs with Bedrock
- [ ] Store results in SecondBrain

### Hour 9-16: Resume Tailoring
- [ ] Upload resume versions
- [ ] Tailor resume per job description
- [ ] Generate cover letters

### Hour 17-24: Application Pipeline
- [ ] Track applications
- [ ] Set follow-up reminders
- [ ] Generate daily report

---

## 6. Out of Scope (For Speed)

- ❌ Perfect caching (optimize later)
- ❌ Full Telegram integration (MVP first)
- ❌ Complex deduplication (simple check)
- ❌ Social media automation (after job)

---

## 7. Success Criteria (24 Hours)

- [ ] AWS Bedrock responding to queries
- [ ] 10 jobs analyzed and stored
- [ ] 5 tailored resumes generated
- [ ] Application tracking working
- [ ] Cost <$1 in testing

---

## 8. Script Reference

```powershell
# Setup (Hour 1)
.\scripts\setup_aws_bedrock.ps1

# Test (Hour 2)
.\scripts\test_bedrock.ps1

# Daily use
. .\env_setter.ps1
python -c "from secondbrain import bedrock_client; client.analyze_job('...')"
```

---

## 9. Fallback Plan

If AWS Bedrock fails:
1. Use existing Kimi Code CLI (current tool)
2. Pay $5-10/month for direct Kimi API
3. Still faster than Ollama setup

---

## 10. Emergency Contacts

If stuck:
- AWS Console: https://console.aws.amazon.com/bedrock
- Bedrock docs: https://docs.aws.amazon.com/bedrock/
- Cost dashboard: https://console.aws.amazon.com/billing/

---

**Mission: Job in 30 days. AWS Bedrock is the weapon.**

Ready? Run the setup script now.
