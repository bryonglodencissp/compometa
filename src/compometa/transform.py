from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

FDA_STATUS_KEY = "softwareMaintenanceStatus"
FDA_EOS_KEY = "softwareEndOfLifeDate"
UNKNOWN = "unknown"


def _sort_components(components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Deterministic ordering: prefer purl, else name+version
    def key(c: Dict[str, Any]) -> Tuple[str, str, str]:
        purl = str(c.get("purl") or "")
        name = str(c.get("name") or "")
        ver = str(c.get("version") or "")
        return (purl, name, ver)

    return sorted(components, key=key)


def _inject_recursive(component: Dict[str, Any]) -> None:
    component.setdefault(FDA_STATUS_KEY, UNKNOWN)
    component.setdefault(FDA_EOS_KEY, UNKNOWN)

    children = component.get("components")
    if isinstance(children, list):
        # recurse first
        for child in children:
            if isinstance(child, dict):
                _inject_recursive(child)
        # then stabilize ordering at this level
        component["components"] = _sort_components([c for c in children if isinstance(c, dict)])


def transform_cyclonedx(sbom: Dict[str, Any]) -> Dict[str, Any]:
    """
    Provider=none milestone:
    - Input: CycloneDX JSON dict
    - Output: CycloneDX JSON dict, deterministic
    - Adds two FDA fields per component with value 'unknown' if missing
    - Supports nested components defensively (CycloneDX allows it)
    - Does NOT add timestamps/UUIDs or touch unrelated fields
    """
    out = copy.deepcopy(sbom)

    components = out.get("components")
    if isinstance(components, list):
        for c in components:
            if isinstance(c, dict):
                _inject_recursive(c)

        out["components"] = _sort_components([c for c in components if isinstance(c, dict)])

    return out

