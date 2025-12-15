# CompoMeta

CompoMeta post-processes existing SBOMs (SPDX or CycloneDX) to enrich them with FDA-expected supportability metadata (e.g., maintenance/support status and end-of-support information) while preserving the original SBOM format.

## Why it exists

Most SBOM generators produce standards-compliant SBOMs aligned to the NTIA minimum elements. FDA premarket cybersecurity guidance goes further by expecting additional component supportability context. CompoMeta helps close that gap without replacing your existing SBOM generator.

## What it does

- Accepts an input SBOM (SPDX or CycloneDX)
- Adds supportability fields (support/maintenance status and end-of-support/end-of-life info)
- Outputs an SBOM in the same original format

## Status

Early development. Interfaces and field mappings may change.

## Contributing

Issues and PRs are welcome, especially real-world med-tech use cases and field-mapping feedback.

## Support

If this project helps your team, GitHub Sponsors supports ongoing maintenance and development.

