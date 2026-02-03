# Ecosystem — Personal AI Operating System

> **Business dashboard for Sean's freelance AI ecosystem**

---

## Overview

Not just a job search bot. A Personal AI Operating System for a freelance business.

| Goal | Status |
|------|--------|
| Continuous Job Hunting | 🔲 Phase 2 |
| Second Brain (reduce API costs) | ✅ Phase 1 Complete |
| Environment Control | 🔲 Phase 2 |
| Future Extensibility | ✅ Architecture defined |

---

## Quick Start

```powershell
# 1. Set up environment (activates venv)
. .\env_setter.ps1

# 2. Run tests to verify
python test_secondbrain.py

# 3. Start infrastructure (Qdrant + Ollama)
docker-compose up -d

# 4. Start all services
.\scripts\start_all.ps1
```

### Environment Setup

This project uses the standard `env_setter.ps1` pattern:
- Virtual environment: `C:\py_venv\ecosystem`
- Run `. .\env_setter.ps1` before working on the project
- Flags: `-Install` (create venv), `-Update` (refresh packages), `-Reset` (recreate)

---

## Project Structure

```
ecosystem/
├── secondbrain/     # IMMORTAL KNOWLEDGE LAYER ✅
├── clawbot/         # SKILL EXECUTOR (AI Employee)
├── shared/          # SHARED COMPONENTS
└── scripts/         # Installation, setup
```

---

## Phase Status

| Phase | Timeline | Focus | Status |
|-------|----------|-------|--------|
| 1 | Week 1 | SecondBrain API | ✅ Complete |
| 2 | Week 2 | ClawBot core + skills | 🔲 Not started |
| 3 | Week 3-4 | Freelance engine | 🔲 Not started |
| 4 | Ongoing | Optimization | 🔲 Not started |

---

## Phase 1: SecondBrain API ✅

Implemented core memory functions:

```python
from secondbrain import remember, recall, cache_store, cache_get

# Store knowledge permanently
remember("client_acme", {"name": "Acme Corp", "rate": 150})

# Retrieve by key
client = recall("client_acme")

# Cache AI responses (cost reduction)
cache_store("What is Python?", "Python is a programming language...")

# Check cache before calling API
response = cache_get("What is Python?", similarity_threshold=0.90)
```

### Storage Architecture
- **Pickle files**: Fast local storage (`memory.pkl`, `cache.pkl`)
- **Qdrant**: Vector database for semantic similarity (requires `docker-compose up`)
- **Ollama**: Local embeddings via `nomic-embed-text` model

---

## Testing

```powershell
# Run SecondBrain API tests
C:\py_venv\clawbot\Scripts\python.exe test_secondbrain.py
```

---

*Last Updated: 2026-02-03*
*Phase 1 Status: Complete*
