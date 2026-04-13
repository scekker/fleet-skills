# Fleet Skills Changelog

All notable additions and changes to the fleet skills library.

---

## 2026-04-13

### Added
- **`magika-scout` v1.1** (Uvy) — AI-powered file type detection and parser routing using Google's Magika model (~99% accuracy, 200+ types, ~5ms/file on CPU). Pre-flight safety check before parsing any externally-fetched file. Includes GitHub/HuggingFace-specific risk guidance (pickle/torch.load attack vector, safetensors preference). Files: `SKILL.md`, `scripts/scout.py`, `references/router-map.md`. Packaged as `magika-scout.skill`.

---

## 2026-04-10

### Added
- **`assess-input` v1.0 + v1.1** (Uvy + Atlas) — Input assessment skill. Pushed to fleet-skills GitHub.
- **`check-siblings`** (Uvy) — Pre-action check for sibling sessions before destructive ops.
- **`session-ledger`** (Uvy) — Shared append-only log for sibling session awareness; prevents double-execution.

---

*Format: Added | Changed | Fixed | Deprecated | Removed*
*Authors: skill entry includes originating agent in parentheses.*
