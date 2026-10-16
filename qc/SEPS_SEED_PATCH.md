# SEPS SEED PATCH (Gate 1)

Date: 2026-10-16 UTC.

## Patch
`scripts/exp01_descriptors.py`: added

```python
def spec_seed(key, mod):
    h = int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")
    return h % mod
```

- line 20: `seed=abs(hash(name)) % 2**31` → `seed=spec_seed(name, 2**31)`
- line 28: `10_000 + abs(hash(name)) % 1000` → `10_000 + spec_seed(name, 1000)`

SHA-256 of the canonical UTF-8 spec key, first 8 bytes → big-endian int → mod. Cross-process, cross-platform, PYTHONHASHSEED-independent. Stream semantics preserved (one independent stream per spec, same mod structure and 10_000 offset). No seed was selected for its results — the mapping is fixed by the hash function, chosen before any output was inspected.

## Collisions
All 10 CANONICAL_SPECS keys map to distinct seeds at both moduli (verified; test `test_no_collision_across_canonical_specs`).

## Tests (tests/test_exp01_seed_determinism.py — 4 tests, all PASS)
1. Same key → same seed across separate Python processes.
2. Different keys → distinct seeds.
3. PYTHONHASHSEED=0 vs 12345 → identical seeds.
4. No collisions across all canonical spec keys.

## Repeatability (Gate 4 partial)
Two fresh `python3 scripts/exp01_descriptors.py` runs, second under `PYTHONHASHSEED=424242` → all 3 CSVs **byte-identical** (sha256 match).

## Policy note
Deterministic-seed rule documented in public README (no salted `hash()` seeds anywhere in the pipeline).
