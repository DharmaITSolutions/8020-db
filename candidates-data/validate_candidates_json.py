#!/usr/bin/env python3
"""Validate candidate JSON before importing into pia-candidates-mu.

This checks:
- JSON is a list of objects
- types for common fields
- booleans for featured/approved
- optional buttons/category structure
- duplicate external_id collisions
"""

import argparse
import json
import sys
from collections import Counter
from typing import Any, Dict, List, Tuple


def is_bool(value: Any) -> bool:
    return isinstance(value, bool)


def is_str(value: Any) -> bool:
    return isinstance(value, str)


def is_list(value: Any) -> bool:
    return isinstance(value, list)


def validate_candidate(candidate: Dict[str, Any], index: int, strict: bool) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    name = candidate.get("name", "")
    if not (is_str(name) and name.strip()):
        errors.append(f"[{index}] missing/invalid `name` (required)")

    external_id = candidate.get("external_id", "")
    if external_id is None:
        external_id = ""
    if not external_id:
        (errors if strict else warnings).append(f"[{index}] missing `external_id` (recommended for reliable updates)")
    elif not is_str(external_id):
        errors.append(f"[{index}] invalid `external_id` (must be string)")

    for key in ["state", "county", "district", "office", "summary", "bio", "website", "video_url", "portrait_url"]:
        if key in candidate and candidate[key] is not None and not is_str(candidate[key]):
            errors.append(f"[{index}] invalid `{key}` (must be string)")

    for key in ["featured", "approved"]:
        if key in candidate and candidate[key] is not None and not is_bool(candidate[key]):
            errors.append(f"[{index}] invalid `{key}` (must be boolean true/false)")

    if "buttons" in candidate and candidate["buttons"] is not None:
        buttons = candidate["buttons"]
        if not is_list(buttons):
            errors.append(f"[{index}] invalid `buttons` (must be list)")
        else:
            if len(buttons) > 3:
                warnings.append(f"[{index}] `buttons` has {len(buttons)} entries (plugin only stores first 3)")
            for b_i, button in enumerate(buttons):
                if not isinstance(button, dict):
                    errors.append(f"[{index}] buttons[{b_i}] must be an object with label/url")
                    continue
                label = button.get("label", "")
                url = button.get("url", "")
                if not (is_str(label) and label.strip() and is_str(url) and url.strip()):
                    errors.append(f"[{index}] buttons[{b_i}] requires non-empty string `label` and `url`")

    if "category" in candidate and candidate["category"] is not None:
        category = candidate["category"]
        if is_str(category):
            warnings.append(f"[{index}] `category` is a string; plugin expects an array of slugs (e.g. [\"state-senate\"])")
        elif not is_list(category):
            errors.append(f"[{index}] invalid `category` (must be list of strings)")
        else:
            for c_i, slug in enumerate(category):
                if not (is_str(slug) and slug.strip()):
                    errors.append(f"[{index}] category[{c_i}] must be a non-empty string slug")

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to candidate JSON file (array of objects)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat missing external_id as an error (recommended for production imports)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        with open(args.input, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        print(f"File not found: {args.input}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 2

    if not isinstance(payload, list):
        print("Top-level JSON must be a list/array of candidates.", file=sys.stderr)
        return 2

    all_errors: List[str] = []
    all_warnings: List[str] = []

    external_ids: List[str] = []
    states: List[str] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            all_errors.append(f"[{idx}] candidate must be an object/dict")
            continue
        external_id = item.get("external_id", "")
        if isinstance(external_id, str) and external_id.strip():
            external_ids.append(external_id.strip())
        state = item.get("state", "")
        if isinstance(state, str) and state.strip():
            states.append(state.strip())
        errors, warnings = validate_candidate(item, idx, args.strict)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    dupes = [eid for eid, count in Counter(external_ids).items() if count > 1]
    if dupes:
        all_errors.append(f"Duplicate external_id values detected ({len(dupes)}): {', '.join(dupes[:10])}" + (" ..." if len(dupes) > 10 else ""))

    unique_states = sorted({s for s in states if s})
    if "TX" in unique_states and "Texas" in unique_states:
        all_warnings.append("Mixed state values detected (`TX` and `Texas`). Standardize this for reliable directory filtering.")

    total = len(payload)
    print(f"Validated {total} candidates from {args.input}")
    if all_warnings:
        print(f"WARNINGS ({len(all_warnings)}):")
        for msg in all_warnings[:50]:
            print(f"- {msg}")
        if len(all_warnings) > 50:
            print(f"- ... {len(all_warnings) - 50} more warnings omitted")

    if all_errors:
        print(f"ERRORS ({len(all_errors)}):", file=sys.stderr)
        for msg in all_errors[:50]:
            print(f"- {msg}", file=sys.stderr)
        if len(all_errors) > 50:
            print(f"- ... {len(all_errors) - 50} more errors omitted", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

