#!/usr/bin/env python3
"""Normalize a Texas SOS CSV into the plugin JSON schema."""

import argparse
import csv
import json
import re
from typing import Dict, List


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_bool(value: str) -> bool:
    value = (value or "").strip().lower()
    return value in {"1", "true", "t", "yes", "y", "on"}


def normalize_row(
    row: Dict[str, str],
    mapping: Dict[str, str],
    *,
    default_state: str,
    external_id_prefix: str,
    seen_external_ids: Dict[str, int],
) -> Dict:
    def read(field: str) -> str:
        return row.get(mapping.get(field, ""), "").strip()

    name = read("name") or " ".join(filter(None, [read("first_name"), read("last_name")])).strip()
    office = read("office") or read("race")
    county = read("county")
    district = read("district")

    external_id = read("external_id")
    if not external_id and name:
        base = "-".join(
            part
            for part in [
                external_id_prefix,
                slugify(name),
                slugify(office),
                slugify(county),
                slugify(district),
            ]
            if part
        )
        if not base:
            base = external_id_prefix
        count = seen_external_ids.get(base, 0) + 1
        seen_external_ids[base] = count
        external_id = base if count == 1 else f"{base}-{count}"

    buttons = []
    for i in range(1, 4):
        label = read(f"button_{i}_label")
        url = read(f"button_{i}_url")
        if label and url:
            buttons.append({"label": label, "url": url})

    categories: List[str] = []
    raw_category = read("category")
    if raw_category:
        categories = [slugify(c) for c in raw_category.split(",") if slugify(c)]

    return {
        "external_id": external_id,
        "name": name,
        "state": read("state") or default_state,
        "county": county,
        "district": district,
        "office": office,
        "website": read("website"),
        "video_url": read("video_url"),
        "portrait_url": read("portrait_url"),
        "summary": read("summary"),
        "bio": read("bio"),
        "featured": parse_bool(read("featured")),
        "approved": parse_bool(read("approved")),
        "buttons": buttons,
        "category": categories,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--output", default="sos-tx.json", help="Output JSON file path")
    parser.add_argument("--default-state", default="Texas", help="Fallback state value if missing")
    parser.add_argument(
        "--external-id-prefix",
        default="txsos",
        help="Prefix used to generate a stable external_id when missing",
    )
    parser.add_argument("--name", default="candidate_name", help="CSV column for candidate name")
    parser.add_argument("--first-name", default="first_name", help="CSV column for first name")
    parser.add_argument("--last-name", default="last_name", help="CSV column for last name")
    parser.add_argument("--external-id", default="candidate_id", help="CSV column for external ID")
    parser.add_argument("--state", default="state", help="CSV column for state")
    parser.add_argument("--county", default="county", help="CSV column for county")
    parser.add_argument("--district", default="district", help="CSV column for district")
    parser.add_argument("--office", default="office", help="CSV column for office")
    parser.add_argument("--race", default="race", help="CSV column for race")
    parser.add_argument("--website", default="website", help="CSV column for website")
    parser.add_argument("--video-url", default="video_url", help="CSV column for video URL")
    parser.add_argument("--portrait-url", default="portrait_url", help="CSV column for portrait image URL")
    parser.add_argument("--summary", default="summary", help="CSV column for summary")
    parser.add_argument("--bio", default="bio", help="CSV column for bio")
    parser.add_argument("--featured", default="featured", help="CSV column for featured flag (truthy/falsey)")
    parser.add_argument("--approved", default="approved", help="CSV column for approved flag (truthy/falsey)")
    for i in range(1, 4):
        parser.add_argument(f"--button-{i}-label", default=f"button_{i}_label", help=f"CSV column for button {i} label")
        parser.add_argument(f"--button-{i}-url", default=f"button_{i}_url", help=f"CSV column for button {i} URL")
    parser.add_argument("--category", default="category", help="CSV column for category slugs (comma-separated)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mapping = {
        "name": args.name,
        "first_name": args.first_name,
        "last_name": args.last_name,
        "external_id": args.external_id,
        "state": args.state,
        "county": args.county,
        "district": args.district,
        "office": args.office,
        "race": args.race,
        "website": args.website,
        "video_url": args.video_url,
        "portrait_url": args.portrait_url,
        "summary": args.summary,
        "bio": args.bio,
        "featured": args.featured,
        "approved": args.approved,
        "category": args.category,
    }
    for i in range(1, 4):
        mapping[f"button_{i}_label"] = getattr(args, f"button_{i}_label")
        mapping[f"button_{i}_url"] = getattr(args, f"button_{i}_url")

    data: List[Dict] = []
    seen_external_ids: Dict[str, int] = {}
    with open(args.input, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row:
                continue
            normalized = normalize_row(
                row,
                mapping,
                default_state=args.default_state,
                external_id_prefix=args.external_id_prefix,
                seen_external_ids=seen_external_ids,
            )
            if normalized["name"]:
                data.append(normalized)

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)

    print(f"Wrote {len(data)} candidates to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
