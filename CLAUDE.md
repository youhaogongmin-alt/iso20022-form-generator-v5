# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Build & Run

```bash
# Generate form from PDF (multi-file output)
python scripts/generate_form.py dev/input/CBPRPlus_SR2026.pdf

# Generate form with single-file output
python scripts/generate_form.py dev/input/CBPRPlus_SR2026.pdf --single-file
```

No test framework exists. Verify by opening output in a browser and checking key features.

## Architecture

**Pipeline: PDF → Schema JSON → HTML Form**

```
parse_pdf.py → form_page.py (calls field_renderer.py + form_rules.py + form_api.py) → generate_form.py (multi-file + single-file)
```

### Script Roles

| Script | Role |
|--------|------|
| `parse_pdf.py` | Extracts field definitions from ISO 20022 usage guideline PDFs into a schema dict |
| `form_rules.py` | Centralized CBPR+ presets, business rules, templates, quick-fill fields, field removal lists |
| `field_renderer.py` | Renders individual fields/panels as HTML (Bootstrap 3 panels, repeat groups, leaf fields) |
| `form_page.py` | Orchestrates page assembly: calls renderer, builds fieldMeta JS, generates appConfig |
| `form_app.py` | Generates complete app.js (ES5 + jQuery, 14 modules) |
| `form_css.py` | Generates app.css (IE8-compatible, dual theme, float-based layout) |
| `form_api.py` | Provides `window.PACS008_FORM_API` — browser-side API for external integration |
| `generate_form.py` | CLI entry point — multi-file and single-file output routing |

### Key Data Structures

- **Schema JSON** (`output/pacs.008.001.08.json`): hierarchical field tree with `message_id`, `app_hdr_fields`, `document_fields`
- **fieldMeta** (JS array in `fieldMeta.js`): flat list of all fields with form_name, iso_path, type_code, mult_min/max, code_values
- **AT_LEAST_ONE_GROUPS** (JS array): parent-child groups where parent is mandatory but all children are optional
- **appConfig.js**: developer-editable runtime config (templates, quick-fill fields, field state overrides)

### Output Modes

- **Multi-file** (always generated): `output/form/` with index.html + js/ + css/ + js/vendor/
- **Single-file** (with `--single-file`): all JS/CSS/vendor inlined into one HTML (~2MB), works via `file://`

## Dependencies

- Python 3.8+, `pdfplumber`
- Frontend: jQuery 1.12.4, Bootstrap 3.4.1, IE polyfills (all in `vendor/`)

## IE8+ Compatibility Rules

- All JS must be ES5 (var, function, no arrow functions, no template strings, no Promise)
- CSS: no var(), no flexbox, no grid, no :has(), no CSS variables — use float-based layout
- Bootstrap 3 collapse plugin handles panel expand/collapse (data-toggle="collapse")
- HTML uses `.panel` / `.panel-body.collapse.in` structure (NOT custom `.card` class)
- IE conditional comments load polyfills: html5shiv, respond.js, es5-shim/sham, json2

## CBPR+ Collection Rules

`form_rules.py` implements specific Change Requests:
- CR 3012: Proxy/Type mandatory override
- CR 3020: Field removal
- CR 3031: SchmeNm field removal
- CR 3032: BranchId field removal
- CR 3039: Force date type (strip time component)
- CR 3072: Additional removals

## Conventions

- All UI text uses I18N dict (Chinese/English/French) — never hardcode display strings
- Field naming: `DOC_Parent_Child_Leaf` or `AH_Parent_Child_Leaf` prefix path
- Collapsible sections use Bootstrap 3 panels with `collapse in` for expanded, `collapse` for collapsed
- Progress logic uses `.panel-all-optional` class (tagged at init) to exclude unused optional sections
- Repeating groups use `data-repeat-group` attribute with add/remove buttons
- Generated HTML must work on `file://` protocol (no fetch for critical resources)
