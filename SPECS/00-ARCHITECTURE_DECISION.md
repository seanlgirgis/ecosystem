# Architecture Decision: Two-Project Ecosystem

**Status:** ✅ Implemented  
**Date:** 2026-02-03  
**Decision ID:** ADR-001  

---

## Context

Sean Girgis needs a personal AI ecosystem that:
- Continuously hunts for jobs (full-time + freelance)
- Reduces commercial AI API costs through caching
- Controls local PC environment (files, projects, git)
- Scales with new capabilities over time

**Previous attempt:** `Prompter/Personal_Hybrid_AI` had architectural drift — mixed concerns, built before requirements locked, violated 7-Stage Protocol.

---

## Decision

Create a **NEW clean project** (`C:\ecosystem`) rather than fix Prompter.

### Two-Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ECOSYSTEM                               │
├──────────────────────────┬──────────────────────────────────┤
│      SecondBrain         │           ClawBot                │
│   (Immortal Knowledge)   │      (Skill Executor)            │
├──────────────────────────┼──────────────────────────────────┤
│ • remember()             │ • Execute skills                 │
│ • recall()               │ • Job search                     │
│ • cache_store()          │ • Lead generation                │
│ • cache_get()            │ • Environment control            │
│ • Semantic search        │ • Client management              │
│ • Conversation logging   │ • Telegram interface             │
├──────────────────────────┴──────────────────────────────────┤
│              SHARED: Config, Models, Utils                  │
├─────────────────────────────────────────────────────────────┤
│           INFRASTRUCTURE: Qdrant + Ollama                   │
└─────────────────────────────────────────────────────────────┘
```

### Separation of Concerns

| Component | Lifespan | Responsibility |
|-----------|----------|----------------|
| **SecondBrain** | Forever | Knowledge persists, survives skill changes |
| **ClawBot** | Evolves | Skills come and go, brain stays constant |
| **Skills** | Swappable | Individual capabilities can be added/removed |

---

## Rationale

### Why Not Fix Prompter?
- Architecture drift: Methodology docs + experiments + code mixed
- Violates 7-Stage Protocol (built before requirements locked)
- Not teachable/cloneable structure

### Why This Structure?
- **SecondBrain** = Cache layer + knowledge base = Reduce API costs
- **ClawBot** = Action layer = Actually does things
- **Skills** = Modular = Add freelance lead gen without touching core
- **Separation** = Can rewrite ClawBot without losing 5 years of memories

---

## Consequences

### Positive
- Clean slate with clear boundaries
- Brain survives bot rewrites
- Skills are truly swappable
- Teaches the 7-Stage Protocol by example

### Negative
- Migration effort (selective copy from Prompter)
- Dual maintenance during transition
- Need to establish data migration path

---

## Related Decisions

- **Storage:** Pickle (fast) + Qdrant (vectors) — not SQL, not pure files
- **Embeddings:** Ollama local (nomic-embed-text) — no OpenAI dependency
- **Language:** Python 3.12 — familiar, ecosystem, Sean's expertise
- **Paradigm:** OOP — single paradigm, no functional mixing

---

## References

- Original context: `C:\secondBrain\AI_CONTEXT_CACHE.md`
- Constitution: `C:\secondBrain\KIMI_CONSTITUTION\01-CORE_RULES.md`
- 7-Stage Protocol: Derived from Prompter methodology
