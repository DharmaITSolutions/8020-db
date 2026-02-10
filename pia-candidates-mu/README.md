# PIA Candidates (MU) — v0.01 (official)

Note: the plugin header `Version:` value may differ; this README reflects the **v0.01** release behavior and setup.

Per-site candidate profiles for the PIA WordPress multisite. This MU plugin registers a **Candidate** custom post type, a **Candidate Category** taxonomy, and provides shortcodes that can be dropped into Avada Builder pages.

This README documents the **official v0.01** behavior/configuration.

## Key features

- **Per-site candidates** (each multisite site manages its own candidates).
- **Manual + automated data**: keep manual entries and import from JSON (local file, URL, or inline).
- Candidate details stored as post meta (portrait image/URL, video URL, CTA buttons, location fields).
- **PIA Approved** badge support for approved candidates.
- Shortcodes to render directory listings and profile layouts.
- Template override for single candidate pages if the theme does not provide one.
- **Grouped JSON supported**: imports can auto-flatten objects like `{ "federal": [ ... ], "state": [ ... ] }`.
- **Non-destructive imports**: blank values in the dataset will **not** overwrite manual edits in WordPress.
- **Missing data UX**: front-end displays `Information pending/not provided` for missing fields.

## Install (MU)

WordPress only auto-loads MU plugins located directly in `wp-content/mu-plugins/`, so this plugin ships with a loader file.

- Copy the folder to: `wp-content/mu-plugins/pia-candidates-mu/`
- Copy the loader file to: `wp-content/mu-plugins/pia-candidates-mu-loader.php`
- Ensure the dataset file exists (Option A default): `wp-content/mu-plugins/pia-candidates-mu/data/texas_candidates_2026-0.json`

After copying files, flush permalinks once:

- WP Admin → **Settings → Permalinks** → **Save Changes**

## Admin settings

Go to **Settings → PIA Candidates**:

- **Data Source Type**: choose Custom JSON, FEC API, or Texas SOS import.
- **Data Source URL**: JSON feed URL for national/state/county candidate data.
- **Local JSON File (MU plugin)**: store a JSON file inside the MU plugin folder and reference it by path (relative to `pia-candidates-mu/`). Default/recommended: `data/texas_candidates_2026-0.json` (Option A).
- **Inline JSON**: paste JSON data directly in the admin.
- **FEC API Key / Cycle / Offices**: pulls federal candidates (US House, US Senate, President) for Texas.
- **Texas SOS URL**: provide a JSON or CSV export link from the Texas Secretary of State.
- **Default State/County/District**: per-site defaults used by the directory shortcode.
- **PIA Approved Badge Image**: upload or paste a badge URL to overlay on approved candidates.

Use **Run Import** to populate candidates. Imported candidates become normal WordPress `pia_candidate` posts (editable in WP Admin → Candidates).

### Custom JSON import order (v0.01)

When **Data Source Type = Custom JSON**, the plugin loads data in this order:

1. **Local JSON File (MU plugin)** (Option A)
2. **Data Source URL**
3. **Inline JSON**

### Import safety rules (v0.01)

- Imports are **additive** and will **not delete** candidates.
- Updates match existing candidates by **External ID** (recommended).
- If an imported field is present but blank (e.g. `"website": ""`), the import will **not** overwrite the existing WordPress value.

## Shortcodes (Avada Builder)

Use these in Avada Builder content blocks.

### Directory

```
[pia_candidate_directory per_page="12" state="Texas" county="Potter" district="District 5" featured="1" approved="1"]
```

**Attributes**
- `per_page` (number) — candidates per page.
- `scope` — controls how location filtering works:
  - `auto` (default): use the site defaults (`Default State/County/District`) if set.
  - `county`: force county-only (uses `Default County` if you don’t pass `county`).
  - `state`: statewide (ignores `Default County` unless you explicitly pass `county`).
  - `all`: ignore site defaults; show all candidates on the site (unless you explicitly pass filters).
- `state`, `county`, `district` — optional filters (default to the site settings unless `scope="all"` or `scope="state"`).
- `featured` — `1` to show featured only.
- `approved` — `1` to show PIA Approved only.
- `category` — optional candidate category filter (comma-separated slugs).

**Examples**

```
[pia_candidate_directory per_page="30" scope="county"]
```

```
[pia_candidate_directory per_page="30" scope="state"]
```

```
[pia_candidate_directory per_page="30" scope="all"]
```

### Profile

```
[pia_candidate_profile]
```

- Renders the current candidate profile on single candidate pages.
- Can also be used with `id` to embed a specific candidate:

```
[pia_candidate_profile id="123"]
```

## JSON schema (example)

The importer accepts either a **flat list** or a **grouped object** (it will auto-flatten groups like `federal`, `state`, etc.).

### Flat list

```
[
  {
    "external_id": "tx-2024-001",
    "name": "Apollo Hernandez",
    "state": "Texas",
    "county": "Potter",
    "district": "SD-5",
    "office": "Texas State Senate District 5",
    "summary": "Conservative leader focused on ...",
    "bio": "Longer biography text ...",
    "website": "https://example.com",
    "video_url": "https://www.youtube.com/watch?v=...",
    "portrait_url": "https://example.com/images/apollo.jpg",
    "featured": true,
    "approved": true,
    "buttons": [
      { "label": "Candidate Profile", "url": "https://patriotsinactiontx.com/apollo" },
      { "label": "Website", "url": "https://example.com" }
    ],
    "category": ["state-senate"]
  }
]
```

### Grouped object (auto-flattened)

```
{
  "federal": [
    { "external_id": "tx-2026-senate-001", "name": "Example Candidate", "office": "U.S. Senate", "state": "Texas" }
  ],
  "state": [
    { "external_id": "tx-2026-state-001", "name": "Example Candidate 2", "office": "Texas State Senate", "state": "Texas" }
  ]
}
```

## Notes

- If an API/URL fails, the import exits with a notice and existing candidates remain unchanged.
- If the active theme provides `single-pia_candidate.php`, it will take precedence.
- The plugin template is used otherwise and simply renders the profile shortcode.

## Reference links for data sources

- Texas Secretary of State elections resources: `https://www.sos.texas.gov/elections/`
- FEC API documentation: `https://api.open.fec.gov/developers/`

## Generating JSON locally

See `candidates-data/README.md` for Python scripts that fetch and normalize FEC and Texas SOS data into the plugin’s JSON format.
