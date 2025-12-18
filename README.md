# Compometa

**Deterministic CycloneDX SBOM completion for FDA-aligned supportability metadata**

Compometa is an open-source tool that ingests **CycloneDX JSON SBOMs** (expected: Syft-shaped per contract) and emits a **CycloneDX JSON SBOM** with FDA-expected supportability fields present for every component.

It is intentionally minimal, predictable, and regulator-friendly.

---

## What Compometa Does

Compometa:
- Accepts **CycloneDX JSON** SBOMs
- Emits **CycloneDX JSON** SBOMs (same format)
- Ensures every component contains:
  - `softwareMaintenanceStatus`
  - `softwareEndOfLifeDate`
- Provides deterministic, idempotent output:
  - stable ordering
  - no regenerated UUIDs
  - no timestamps added

At the current milestone (`provider=none`), both fields default to `"unknown"`.

---

## What Compometa Does Not Do

Compometa does **not**:
- guess lifecycle metadata
- scrape upstream repositories
- infer end-of-life dates
- claim authoritative truth for third-party support status

If lifecycle data is unknown, Compometa records `"unknown"` explicitly.

---

## Supported Formats

- **Input:** CycloneDX JSON
- **Output:** CycloneDX JSON
- **SPDX:** not supported (current scope)

---

## Architecture

![Compometa Architecture](docs/architecture/compometa-architecture.png)

Architecture explanation:
- `docs/architecture/architecture.md`

CycloneDX contract:
- `docs/cyclonedx-contract.md`

---

## Usage

Transform an SBOM (provider = none):

```bash
PYTHONPATH=src python -m compometa.cli \
  --in examples/input/python-app.json \
  --out out.json \
  --provider none
```
This guarantees that all components in the output SBOM contain the FDA supportability fields with value "unknown" unless already present.

## Testing

Compometa uses golden-file testing against real CycloneDX fixtures.
- Input fixtures: `examples/input/`
- Expected outputs: `examples/expected/`

Run tests with:

```bash
PYTHONPATH=src pytest -q
```
Golden tests assert byte-for-byte stability after normalization.

---

## Project Status

Current milestone:
- `provider=none`
- FDA supportability fields injected deterministically
- Real CycloneDX fixtures with golden outputs
- Idempotent behavior verified by tests

Planned evolution:
- Optional provider-backed enrichment (external, black-box)
- No change to core determinism or format guarantees

---

## License

MIT License. See `LICENSE`.

---
