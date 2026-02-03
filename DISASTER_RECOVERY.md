# Disaster Recovery & Backup Strategy

> **Your AI ecosystem is now protected against hardware failure.**

---

## Architecture: Code vs Data Separation

```
C:\ecosystem\                    # ← GIT REPO (GitHub backed up)
├── .git\                        # Full version history
├── All Python code               # Reproducible on any machine
├── Configuration files           # docker-compose.yml, etc.
├── requirements.txt              # Dependencies locked
└── README.md, docs               # Documentation
│
C:\ecosystem\data\               # ← NOT IN GIT (local only)
├── cache\                       # Cached AI responses (regenerable)
│   └── cache.pkl
├── memory\                      # Knowledge base (BACKUP SEPARATELY if critical)
│   ├── memory.pkl
│   └── conversations.pkl
└── qdrant\                      # Vector database (recreatable from memory.pkl)
    └── storage/
```

---

## What Goes to GitHub

| In Git | Not in Git |
|--------|-----------|
| All `.py` files | `.pkl` data files |
| `docker-compose.yml` | `data/` directory |
| `requirements.txt` | `.env` (secrets) |
| Docs, READMEs | Qdrant storage |
| `.env.example` (template) | Cache files |

---

## Recovery Scenarios

### Scenario 1: New Computer / Fresh Install

```powershell
# 1. Clone the repository
git clone https://github.com/seanlgirgis/ecosystem.git C:\ecosystem

# 2. Create data directory (gitignored, won't exist)
mkdir C:\ecosystem\data\cache
mkdir C:\ecosystem\data\memory
mkdir C:\ecosystem\data\qdrant

# 3. Create environment file
copy C:\ecosystem\.env.example C:\ecosystem\.env
# Edit .env with your API keys

# 4. Install dependencies
.\scripts\install.ps1

# 5. Start infrastructure
docker-compose up -d

# 6. You're back online!
```

**Result:** Code restored 100%. Data starts fresh (cache empty, memory empty).

---

### Scenario 2: Hard Drive Dies (with data backup)

If you've been backing up `C:\ecosystem\data\memory\`:

```powershell
# 1. Restore code from GitHub (same as Scenario 1)
git clone https://github.com/seanlgirgis/ecosystem.git C:\ecosystem

# 2. Restore data from your backup
# Copy memory.pkl from backup to C:\ecosystem\data\memory\
# Copy conversations.pkl to C:\ecosystem\data\memory\

# 3. Rebuild Qdrant vectors (optional)
# System will regenerate embeddings from memory.pkl
```

**Result:** Full restoration including knowledge base.

---

### Scenario 3: Just Data Corruption

```powershell
# If cache gets corrupted - just delete it
rm C:\ecosystem\data\cache\*.pkl
# System rebuilds cache automatically

# If Qdrant gets corrupted
rm -rf C:\ecosystem\data\qdrant\*
docker-compose restart qdrant
# Re-upsert vectors from memory.pkl
```

---

## Backup Recommendations

### Option A: Cloud Sync (Recommended)

Sync `C:\ecosystem\data\memory\` to cloud storage:
- OneDrive: `mklink /J C:\Users\...\OneDrive\ecosystem-memory C:\ecosystem\data\memory`
- Dropbox, Google Drive: Similar junction/symlink

### Option B: Scheduled Backup Script

```powershell
# backup.ps1 - Run daily
$date = Get-Date -Format "yyyy-MM-dd"
Compress-Archive `
    -Path "C:\ecosystem\data\memory\*" `
    -DestinationPath "D:\backups\ecosystem-memory-$date.zip"
    -Force
```

### Option C: Git for Data (Selective)

```powershell
# If you want memory in git (not recommended for large files)
# But useful for critical configs:
git add -f data/memory/critical_config.json
```

---

## Critical vs Regenerable Data

| Data Type | Location | Backup Priority | If Lost |
|-----------|----------|-----------------|---------|
| **memory.pkl** | `data/memory/` | 🔴 HIGH | Years of knowledge gone |
| **conversations.pkl** | `data/memory/` | 🟡 MEDIUM | Analytics lost, but code works |
| **cache.pkl** | `data/cache/` | 🟢 LOW | Regenerates automatically |
| **Qdrant vectors** | `data/qdrant/` | 🟢 LOW | Rebuild from memory.pkl |
| **.env secrets** | Root (gitignored) | 🔴 HIGH | Need to recreate API keys |

---

## Git Workflow

```powershell
# Daily workflow
cd C:\ecosystem
git status                    # See what changed
git add .                     # Stage code changes
git commit -m "feat: description"  # Commit
git push origin main          # Push to GitHub

# Before major changes
git branch feature-x          # Create branch
git checkout feature-x        # Switch to branch
# ... make changes ...
git merge feature-x           # Merge when done
```

---

## Testing Recovery

**Do this once to verify:**

```powershell
# 1. Make a test clone
git clone C:\ecosystem C:\ecosystem-test-clone

# 2. Verify it runs
cd C:\ecosystem-test-clone
C:\py_venv\clawbot\Scripts\python.exe test_secondbrain.py

# 3. Clean up
rm -rf C:\ecosystem-test-clone
```

---

## Summary

| Question | Answer |
|----------|--------|
| Is my code safe? | ✅ Yes, in GitHub |
| Is my data safe? | ⚠️ Only if YOU back it up |
| Can I recover from dead PC? | ✅ Yes, clone + restore data backup |
| How long to restore? | 10 minutes (code) + data restore time |

---

**Next Steps:**
1. ✅ Git repo initialized
2. 🔄 Create GitHub repository (manual step for you)
3. 🔄 Add remote and push
4. 🔄 Set up data backup (cloud sync or scheduled)

---

*Created: 2026-02-03*  
*Repo: C:\ecosystem (.git)*  
*GitHub: Pending*
