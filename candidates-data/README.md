# Candidate Data Scripts

These scripts generate JSON that matches the **PIA Candidates MU** import schema.

This documentation reflects the **official v0.01** plugin workflow (local `/data` JSON supported, grouped JSON supported by importer).

## Development environment (recommended)

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r candidates-data/requirements-dev.txt
```

If you don’t care about linting, you can use `candidates-data/requirements.txt` instead.

## 1) FEC (federal candidates in Texas)

This pulls **US House, US Senate, and President** candidates for Texas via the FEC API.

```bash
python candidates-data/fetch_fec_tx.py \
  --api-key "YOUR_FEC_KEY" \
  --cycle 2024 \
  --offices H,S,P \
  --output fec-tx.json
```

Upload the resulting JSON to a URL and set that URL as the **Data Source URL** with
`Data Source Type = Custom JSON`, or paste the JSON into **Inline JSON**.

FEC API docs: `https://api.open.fec.gov/developers/`

## 2) Texas SOS CSV normalization

Texas SOS data is often provided as CSV or PDF. If you can export or convert a CSV
(Excel → Save As CSV), normalize it into the plugin’s schema:

```bash
python candidates-data/normalize_sos_csv.py \
  --input tx-sos.csv \
  --output sos-tx.json \
  --name "candidate_name" \
  --office "office" \
  --county "county" \
  --district "district"
```

If your CSV uses different column names, pass them via the CLI flags.

### Optional enrichment columns (recommended)

If you include these columns in your CSV, the JSON can fully populate the plugin:

- `website`, `summary`, `bio`
- `portrait_url` (image URL), `video_url` (YouTube/Vimeo URL)
- `featured` / `approved` (truthy values like `1`, `true`, `yes`)
- `button_1_label`, `button_1_url` (and 2/3)
- `category` (comma-separated slugs, e.g. `state-senate,county-office`)

### External IDs (important)

For reliable re-imports/updates, every candidate should have a stable `external_id`.
If your SOS CSV does not have a good unique ID column, this script will generate one
from name + office + county + district using `--external-id-prefix` (default `txsos`).

Texas SOS elections resources: `https://www.sos.texas.gov/elections/`

## 3) Combined FEC + SOS

This script merges FEC federal candidates and Texas SOS CSV data into a single JSON
file. It preserves **all source fields** under `source.raw` so nothing is lost.

```bash
python candidates-data/combine_fec_sos.py \
  --fec-api-key "YOUR_FEC_KEY" \
  --fec-cycle 2024 \
  --fec-offices H,S,P \
  --sos-csv tx-sos.csv \
  --output tx-candidates.json
```

Use `--sos-csv` only for SOS data, or `--fec-api-key` only for FEC data.

## Importing into WordPress (Option A / local file)

If you deploy the MU plugin with a dataset stored in:

- `wp-content/mu-plugins/pia-candidates-mu/data/texas_candidates_2026-0.json`

Then in WordPress (per site):

- **Settings → PIA Candidates**
- **Data Source Type** = `Custom JSON`
- **Local JSON File (MU plugin)** = `data/texas_candidates_2026-0.json`
- Click **Run Import**

## Validate before importing

Run this before you paste/upload JSON to WordPress:

```bash
python candidates-data/validate_candidates_json.py --input tx-candidates.json --strict
```

Note: `validate_candidates_json.py` expects a **flat list** (`[ { ... }, ... ]`). The plugin importer also supports a **grouped object** format for storage convenience, but you’ll need to flatten it (or validate the flattened output) to use this validator.
