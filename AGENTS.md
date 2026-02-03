# AGENTS.md

Ground rules for AI agents working on this project.
See `KIMI_CONSTITUTION` in `C:\secondBrain` for global rules.

---

## Project Structure

| Component | Responsibility |
|-----------|---------------|
| **secondbrain/** | Immortal knowledge layer — store everything |
| **clawbot/** | Skill executor — take actions |
| **shared/** | Common models, config, utilities |

---

## 7-Stage Protocol (Mandatory)

1. **Requirements Lockdown** — Eliminate ambiguity first
2. **High-Level Architecture** — 2-3 options with tradeoffs
3. **Module Breakdown** — Define components (no code)
4. **Internal Module Design** — Blueprint internals (still no code)
5. **Cross-Module Contracts** — Lock data formats, signatures
6. **Project Skeleton** — Folders, empty files, docstrings ← WE ARE HERE
7. **Controlled Implementation** — One module at a time

---

## Coding Standards

- **Paradigm:** OOP (single paradigm, no random mixing)
- **Explain design choices** — no magic without context
- **Maintenance guide included** for complex components
- **Code at Sean's level** — Senior Data Engineer, 20+ years experience
