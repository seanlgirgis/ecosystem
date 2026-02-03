"""Test SecondBrain API

Quick validation that the core functions work.
Run this to verify Phase 1 implementation.
"""

import sys
sys.path.insert(0, "C:/ecosystem")

from secondbrain import (
    remember, recall, cache_store, cache_get,
    search_knowledge, get_cache_stats, log_interaction
)

print("=" * 60)
print("SecondBrain API Test")
print("=" * 60)

# Test 1: Remember and Recall
print("\n[1] Testing remember() and recall()...")
remember("test_client", {"name": "Acme Corp", "rate": 150}, 
         {"type": "client", "priority": "high"})
result = recall("test_client")
assert result is not None, "Failed to recall memory"
assert result["value"]["name"] == "Acme Corp", "Wrong value recalled"
print(f"   [OK] Stored and recalled: {result['value']}")

# Test 2: Cache Store and Get
print("\n[2] Testing cache_store() and cache_get()...")
cache_store(
    query="What is Python?",
    response="Python is a programming language.",
    model="test"
)
cached = cache_get("What is Python?")
assert cached is not None, "Failed to get cached response"
assert "programming language" in cached, "Wrong cached response"
print(f"   [OK] Cached and retrieved: {cached[:50]}...")

# Test 3: Cache Stats
print("\n[3] Testing get_cache_stats()...")
stats = get_cache_stats()
print(f"   [OK] Cache stats: {stats}")

# Test 4: Log Interaction
print("\n[4] Testing log_interaction()...")
log_id = log_interaction(
    query="Test query",
    response="Test response",
    model="test",
    cost=0.01
)
print(f"   [OK] Logged interaction: {log_id}")

# Test 5: Multiple memories
print("\n[5] Testing multiple memories...")
remember("project_alpha", {"status": "active", "hours": 40}, {"type": "project"})
remember("skill_python", {"level": "expert", "years": 15}, {"type": "skill"})
remember("rate_2024", {"hourly": 150}, {"type": "rate"})

for key in ["project_alpha", "skill_python", "rate_2024"]:
    r = recall(key)
    print(f"   [OK] {key}: {r['value']}")

print("\n" + "=" * 60)
print("All tests passed! SecondBrain API is working.")
print("=" * 60)
