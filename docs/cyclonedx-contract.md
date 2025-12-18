# Compometa CycloneDX Contract

This document defines what Compometa accepts, what it emits, and the guarantees it makes.

## Scope

Compometa is a CycloneDX JSON **post-processor**. It ingests a CycloneDX JSON SBOM and emits a CycloneDX JSON SBOM of the **same format**, guaranteeing two FDA-expected supportability fields are present for each component:

- `softwareMaintenanceStatus`
- `softwareEndOfLifeDate`

At the current milestone (`provider=none`), values default to `"unknown"`.

---

## Supported Inputs

### Required

- **Format:** CycloneDX JSON (JSON text)
- **Top-level object:** must be valid JSON and parse as a CycloneDX SBOM object
- **Primary processing target:** `components` array (if present)

### Expected (Syft-shaped)

Compometa is designed around real-world CycloneDX JSON shapes commonly produced by SBOM generators (notably Syft). The test corpus is anchored on Syft-style output to ensure predictable interoperability.

---

## Explicit Non-Support

- SPDX (any form) is not supported at this milestone
- CycloneDX XML is not supported (JSON only)
- No automatic CycloneDX version migration (no schema upgrade/downgrade)

---

## Component Handling

### Top-level components

If the SBOM includes `components` as an array, Compometa processes each component object.

### Nested components (defensive support)

If a component includes a nested `components` array, Compometa traverses nested components recursively.

> Note: Some generators flatten dependency graphs; others may include nested structures. Compometa supports nested structures defensively to avoid contract failure.

---

## Provider Modes

### Provider = `none` (current milestone)

For every component encountered (top-level + nested), Compometa guarantees the presence of:

- `softwareMaintenanceStatus: "unknown"`
- `softwareEndOfLifeDate: "unknown"`

Rules:
- If fields already exist, Compometa does **not overwrite** them.
- Compometa performs no external lookups.

---

## Output Guarantees

### Format preservation

- Output remains CycloneDX JSON.
- No conversion to other formats.

### Determinism

Compometa aims for deterministic output:
- No UUID regeneration
- No timestamps are introduced
- Stable component ordering

Compometa uses a deterministic sort key for components at each level:
1. `purl` (preferred when present)
2. `name`
3. `version`

### Idempotence

Running Compometa multiple times in `provider=none` mode is idempotent:
- Fields remain present after the first run.
- Values remain `"unknown"` unless already set.
- Output stabilizes.

---

## Failure Behavior

Compometa is conservative:

- If `components` is missing or not a list, Compometa leaves the SBOM unchanged (aside from stable serialization) and emits valid JSON.
- Non-object entries inside `components` are skipped.

Compometa does not attempt to “repair” malformed SBOMs beyond safe traversal.

---

## Test Corpus

Golden fixtures are stored in:

- `examples/input/*.json` (inputs)
- `examples/expected/*.json` (golden outputs)

Golden tests assert byte-for-byte equality (after the CLI’s normalization), ensuring stability across refactors.

---

## Non-Goals (This Milestone)

- No enrichment provider logic
- No network calls
- No auth / API keys
- No billing or pricing
- No vulnerability scanning, VEX, or advisory enrichment
- No schema extensions beyond the two FDA fields

---

## Planned Evolution

Future milestones may add provider-backed enrichment (e.g., `provider=gcs`) while preserving:
- format preservation (CycloneDX → CycloneDX)
- deterministic serialization and stable ordering
- idempotent behavior (given stable provider data)
