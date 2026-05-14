---
name: iso20022-form-generator-ie
description: Generate IE8-compatible interactive HTML forms from ISO 20022 usage guideline PDFs. Use when the target environment requires Internet Explorer 8+ support, or when generating forms with jQuery/Bootstrap 3 for legacy browser deployment.
---

# ISO 20022 Form Generator (IE8+ Compatible)

Use this skill to turn ISO 20022 usage guideline PDFs into interactive HTML forms that work in IE8+ and all modern browsers.

## Quick Start

Run the generator from this skill directory:

```bash
python scripts/generate_form.py <input.pdf> [--single-file]
```

The script writes:

- `output/<message_id>.json` — extracted message schema.
- `output/form/` — multi-file deployment (index.html + js/ + css/).
- `output/<message_id>.html` — single-file offline form (with `--single-file` flag).

## Workflow

1. Confirm the user provided an ISO 20022 usage guideline PDF, or ask for the PDF path.
2. Run `scripts/generate_form.py` with the PDF path.
3. Inspect stderr/stdout if parsing fails; non-ISO PDFs should be rejected.
4. Open or reference `output/form/index.html` for the user.
5. Use `--single-file` when the user needs a fully self-contained offline HTML.

## Output Modes

**Multi-file** (always generated):
```
output/form/
├── index.html
├── css/app.css, bootstrap.min.css, bootstrap-theme.min.css
├── js/app.js, fieldMeta.js, appConfig.js
└── js/vendor/ (jQuery, Bootstrap, polyfills)
```

**Single-file** (with `--single-file`):
All vendor JS, CSS, and application code inlined into one HTML file (~2MB). Works via `file://` protocol with no server needed.

## IE8+ Compatibility

- All JavaScript is ES5 + jQuery 1.12.4 (no ES6 syntax).
- CSS uses no variables, no flexbox, no grid — float-based layout with clearfix.
- IE conditional comments load polyfills: html5shiv, respond.js, es5-shim, es5-sham, json2.
- Bootstrap 3.4.1 provides UI components (panels, modals, buttons, collapse).
- No inline event handlers — all events bound via jQuery delegation.

## Scope Notes

- The parser is strongest on CBPR+ style usage guideline PDFs with field tables.
- UI presets and business-rule helpers are CBPR+/pacs.008 oriented. Treat them as convenience defaults.
- `appConfig.js` is developer-editable without regeneration (templates, quick fields, field state overrides).

## Dependencies

- Python 3.8+
- `pdfplumber`

```bash
python -m pip install pdfplumber
```

## Maintenance

After changing form generation, run the generator on a known PDF and verify:
1. Multi-file output loads correctly in a browser.
2. `fieldMeta.js` loads before `app.js`.
3. Repeat groups can add/remove items.
4. Validation, search, and template features work.

### File Map

- `scripts/generate_form.py`: CLI entry point, multi-file and single-file output routing.
- `scripts/form_page.py`: page-level HTML assembly, field metadata collection, appConfig generation.
- `scripts/field_renderer.py`: field/panel HTML rendering (leaf fields, containers, repeat groups).
- `scripts/form_rules.py`: CBPR+ presets, business rules, templates, field state overrides.
- `scripts/form_app.py`: complete app.js generation (ES5 + jQuery, 14 modules).
- `scripts/form_css.py`: app.css generation (IE8-compatible, dual theme).
- `scripts/form_api.py`: browser-side Form API (`window.PACS008_FORM_API`).
- `scripts/parse_pdf.py`: PDF extraction and schema building.
- `scripts/parse_rules_pdf.py`: rules PDF extraction (fixed values + business rules).
- `vendor/`: jQuery 1.12.4, Bootstrap 3.4.1, IE polyfills.

## Rules PDF Parsing

Extract fixed value constraints and business rules from a CBPR+ combined rules PDF:

```bash
python scripts/parse_rules_pdf.py <rules_pdf_path> [--output <json_path>]
```

Outputs JSON with:
- `message_id`: auto-detected from PDF (e.g., "pacs.008.001.08")
- `fixed_values`: list of `{xml_tag, value}` (e.g., MsgDefIdr = "pacs.008.001.08")
- `business_rules`: list of `{name, type, path, text}` (CBPR_ TextualRule/FormalRule)

Works with any CBPR+ message type PDF — message ID is detected automatically.
