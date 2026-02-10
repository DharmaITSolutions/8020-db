# 8020-db — v0.01 (official)

This README documents the **v0.01** release workflow for the candidate plugin and its data pipeline.

This repository contains the **PIA Candidates (MU)** WordPress plugin plus supporting scripts for generating candidate JSON data.

## What’s included

- **MU plugin**: `pia-candidates-mu/`
  - WordPress custom post type: `pia_candidate`
  - Directory and profile shortcodes
  - Imports from JSON (local file, URL, or inline)
- **MU loader**: `pia-candidates-mu-loader.php`
  - Required because WordPress only auto-loads MU plugins located directly in `wp-content/mu-plugins/`
- **Candidate data tooling**: `candidates-data/`
  - Python scripts to fetch/normalize/merge candidate data into the plugin’s import schema

## Quick start (WordPress / multisite)

Copy these into your WordPress install:

- `pia-candidates-mu/` → `wp-content/mu-plugins/pia-candidates-mu/`
- `pia-candidates-mu-loader.php` → `wp-content/mu-plugins/pia-candidates-mu-loader.php`
- Dataset (Option A default) → `wp-content/mu-plugins/pia-candidates-mu/data/texas_candidates_2026-0.json`

Then, in WP Admin (per site):

- **Settings → Permalinks** → **Save Changes**
- **Settings → PIA Candidates** → **Run Import**

Shortcode example:

```
[pia_candidate_directory per_page="30"]
```

For full plugin documentation, see `pia-candidates-mu/README.md`.
For data generation scripts, see `candidates-data/README.md`.