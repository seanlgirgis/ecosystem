# Spec Template

Use this template for all new specs per Constitution Rule 4.

---

## Spec: [Feature Name]

**Status:** 🔲 NOT STARTED / 🚧 IN PROGRESS / ✅ IMPLEMENTED  
**Target Date:** YYYY-MM-DD  
**Spec Version:** 1.0

---

## 1. Purpose

One sentence what this does.

Two sentences why we need it.

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| R1 | What it must do | P0 |
| R2 | What it should do | P1 |
| R3 | Nice to have | P2 |

### 2.2 Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| N1 | Performance target | < 100ms |
| N2 | Availability | 99.9% |

---

## 3. Architecture

Diagram or description of components.

---

## 4. Interface Specification

```python
def function_name(param: type) -> return_type:
    """Docstring explaining behavior."""
```

---

## 5. Data Models

```python
@dataclass
class ModelName:
    field: type
```

---

## 6. Implementation Details

Key algorithms, strategies, error handling.

---

## 7. Acceptance Criteria

- [ ] Criterion 1: How to verify
- [ ] Criterion 2: How to verify

---

## 8. Dependencies

What needs to exist first.

---

## 9. Out of Scope (Explicitly)

What we're NOT building.

---

## 10. Test Plan

How we'll test this.

---

## 11. References

Links to related specs, ADRs, code files.
