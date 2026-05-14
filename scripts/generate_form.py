#!/usr/bin/env python3
"""CLI entry point for the ISO 20022 form generator v4 (IE8+ compatible).

Supports two output modes:
  - Multi-file (default): index.html + js/ + css/ directory structure
  - Single-file (--single-file): all JS/CSS/vendor inlined into one HTML

This file should stay small. Parsing lives in parse_pdf.py, rendering in
form_page.py/field_renderer.py, and CBPR+/preset data in form_rules.py.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from form_app import get_app_js
from form_css import get_app_css
from form_page import generate_app_config_js, generate_field_meta_js, generate_html
from parse_pdf import parse_pdf


VENDOR_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vendor")


def resolve_output_dir() -> str:
    output_dir = os.environ.get('ISO20022_OUTPUT_DIR')
    if output_dir:
        return os.path.abspath(output_dir)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def write_multi_file(schema: dict, output_dir: str) -> str:
    """Write multi-file output: index.html + js/ + css/ + js/vendor/."""
    message_id = schema.get("message_id", "unknown")

    # Create directories
    js_dir = os.path.join(output_dir, "js")
    css_dir = os.path.join(output_dir, "css")
    vendor_js_dir = os.path.join(js_dir, "vendor")
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(vendor_js_dir, exist_ok=True)

    # Write CSS
    css_path = os.path.join(css_dir, "app.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(get_app_css())
    print(f"  css/app.css ({os.path.getsize(css_path):,} bytes)")

    # Write JS files
    app_js_path = os.path.join(js_dir, "app.js")
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(get_app_js(message_id))
    print(f"  js/app.js ({os.path.getsize(app_js_path):,} bytes)")

    field_meta_path = os.path.join(js_dir, "fieldMeta.js")
    with open(field_meta_path, "w", encoding="utf-8") as f:
        f.write(generate_field_meta_js(schema))
    print(f"  js/fieldMeta.js ({os.path.getsize(field_meta_path):,} bytes)")

    app_config_path = os.path.join(js_dir, "appConfig.js")
    with open(app_config_path, "w", encoding="utf-8") as f:
        f.write(generate_app_config_js(schema))
    print(f"  js/appConfig.js ({os.path.getsize(app_config_path):,} bytes)")

    # Copy vendor files
    vendor_files = {
        "jquery-1.12.4.min.js": "jquery-1.12.4.min.js",
        "bootstrap-3.4.1/js/bootstrap.min.js": "bootstrap.min.js",
        "html5shiv-3.7.3.min.js": "html5shiv.min.js",
        "respond-1.4.2.min.js": "respond.min.js",
        "es5-shim.min.js": "es5-shim.min.js",
        "es5-sham.min.js": "es5-sham.min.js",
        "json2.min.js": "json2.min.js",
    }
    for src_rel, dst_name in vendor_files.items():
        src = os.path.join(VENDOR_DIR, src_rel)
        dst = os.path.join(vendor_js_dir, dst_name)
        if os.path.exists(src):
            with open(src, "rb") as sf:
                with open(dst, "wb") as df:
                    df.write(sf.read())

    # Copy Bootstrap CSS
    bs_css_files = ["bootstrap.min.css", "bootstrap-theme.min.css"]
    for css_file in bs_css_files:
        src = os.path.join(VENDOR_DIR, "bootstrap-3.4.1", "css", css_file)
        dst = os.path.join(css_dir, css_file)
        if os.path.exists(src):
            with open(src, "rb") as sf:
                with open(dst, "wb") as df:
                    df.write(sf.read())

    # Write index.html
    html = generate_html(schema)
    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  index.html ({os.path.getsize(html_path):,} bytes)")

    return html_path


def write_single_file(schema: dict, output_path: str) -> str:
    """Write single-file output with all JS/CSS inlined."""
    message_id = schema.get("message_id", "unknown")
    html = generate_html(schema)

    # Read vendor files for inlining
    vendor_js_contents = []
    vendor_js_files = [
        "es5-shim.min.js",
        "es5-sham.min.js",
        "json2.min.js",
        "html5shiv-3.7.3.min.js",
        "respond-1.4.2.min.js",
        "jquery-1.12.4.min.js",
        "bootstrap-3.4.1/js/bootstrap.min.js",
    ]
    for vf in vendor_js_files:
        path = os.path.join(VENDOR_DIR, vf)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                vendor_js_contents.append(f.read())

    # Read Bootstrap CSS
    bs_css = ""
    for css_file in ["bootstrap.min.css", "bootstrap-theme.min.css"]:
        path = os.path.join(VENDOR_DIR, "bootstrap-3.4.1", "css", css_file)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                bs_css += f.read() + "\n"

    # Build inline replacements
    app_css = get_app_css()
    app_js = get_app_js(message_id)
    field_meta_js = generate_field_meta_js(schema)
    app_config_js = generate_app_config_js(schema)

    # Replace external references with inline content
    # Replace CSS links with inline style
    css_inline = "<style>\n" + bs_css + "\n" + app_css + "\n</style>"
    html = html.replace(
        '  <link rel="stylesheet" href="css/bootstrap.min.css">\n'
        '  <link rel="stylesheet" href="css/bootstrap-theme.min.css">\n'
        '  <link rel="stylesheet" href="css/app.css">',
        css_inline
    )

    # Replace IE conditional scripts with inline
    ie_inline = (
        "<!--[if lt IE 9]>\n"
        "  <script>\n" + vendor_js_contents[3] + "\n</script>\n"  # html5shiv
        "  <script>\n" + vendor_js_contents[4] + "\n</script>\n"  # respond
        "  <script>\n" + vendor_js_contents[0] + "\n</script>\n"  # es5-shim
        "  <script>\n" + vendor_js_contents[1] + "\n</script>\n"  # es5-sham
        "  <script>\n" + vendor_js_contents[2] + "\n</script>\n"  # json2
        "  <![endif]-->"
    )
    html = html.replace(
        '<!--[if lt IE 9]>\n'
        '  <script src="js/vendor/html5shiv.min.js"></script>\n'
        '  <script src="js/vendor/respond.min.js"></script>\n'
        '  <script src="js/vendor/es5-shim.min.js"></script>\n'
        '  <script src="js/vendor/es5-sham.min.js"></script>\n'
        '  <script src="js/vendor/json2.min.js"></script>\n'
        '  <![endif]-->',
        ie_inline
    )

    # Replace footer scripts with inline
    jquery_js = vendor_js_contents[5] if len(vendor_js_contents) > 5 else ""
    bootstrap_js = vendor_js_contents[6] if len(vendor_js_contents) > 6 else ""

    scripts_inline = (
        '  <script>\n' + jquery_js + '\n</script>\n'
        '  <script>\n' + bootstrap_js + '\n</script>\n'
        '  <script>\n' + field_meta_js + '\n</script>\n'
        '  <script>\n' + app_config_js + '\n</script>\n'
        '  <script>\n' + app_js + '\n</script>'
    )
    html = html.replace(
        '  <script src="js/vendor/jquery-1.12.4.min.js"></script>\n'
        '  <script src="js/vendor/bootstrap.min.js"></script>\n'
        '  <script src="js/fieldMeta.js"></script>\n'
        '  <script src="js/appConfig.js"></script>\n'
        '  <script src="js/app.js"></script>',
        scripts_inline
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Single-file: {output_path} ({os.path.getsize(output_path):,} bytes)")
    return output_path


def merge_rules(schema: dict, rules: dict) -> None:
    """Merge parsed rules into schema fields."""
    # --- Fixed values ---
    fixed_map = {fv["xml_tag"]: fv["value"] for fv in rules.get("fixed_values", [])}

    def walk_fixed(fields: list) -> None:
        for f in fields:
            tag = f.get("xml_tag", "")
            if tag in fixed_map and f.get("is_fixed"):
                f["fixed_value"] = fixed_map[tag]
            walk_fixed(f.get("children", []))

    walk_fixed(schema.get("app_hdr_fields", []))
    walk_fixed(schema.get("document_fields", []))

    # --- Build name-to-tag map for path resolution ---
    name_to_tag = {}
    tag_to_name = {}

    def build_name_map(fields: list) -> None:
        for f in fields:
            name_en = f.get("name_en", "").replace(" ", "")
            tag = f.get("xml_tag", "")
            if name_en and tag:
                name_to_tag[name_en] = tag
                tag_to_name[tag] = name_en
            build_name_map(f.get("children", []))

    build_name_map(schema.get("app_hdr_fields", []))
    build_name_map(schema.get("document_fields", []))

    # --- Business rules ---
    biz_rules = rules.get("business_rules", [])
    if biz_rules:
        def walk_rules(fields: list) -> None:
            for f in fields:
                tag = f.get("xml_tag", "")
                name_en = f.get("name_en", "").replace(" ", "")
                matched = [r for r in biz_rules if _path_matches_field(r.get("path", ""), tag, name_en)]
                if matched:
                    f.setdefault("business_rules", []).extend(matched)
                walk_rules(f.get("children", []))

        walk_rules(schema.get("app_hdr_fields", []))
        walk_rules(schema.get("document_fields", []))

    # --- Removed elements ---
    removed_paths = rules.get("removed_elements", [])
    if removed_paths:
        _apply_removed_elements(schema, removed_paths, name_to_tag)

    # --- Mandatory overrides ---
    mandatory = rules.get("mandatory_overrides", [])
    if mandatory:
        _apply_mandatory_overrides(schema, mandatory, name_to_tag)

    # --- Type changes ---
    type_changes = rules.get("type_changes", [])
    if type_changes:
        _apply_type_changes(schema, type_changes, name_to_tag)

    # --- Choice groups: mark is_choice on matching fields ---
    choice_groups = rules.get("choice_groups", [])
    if choice_groups:
        _apply_choice_groups(schema, choice_groups)

    # --- Pass-through data for frontend ---
    schema["choice_groups"] = choice_groups
    schema["conditional_presence"] = rules.get("conditional_presence", [])
    schema["not_allowed_values"] = rules.get("not_allowed_values", [])
    schema["iso_rules"] = rules.get("iso_rules", [])


def _resolve_path_segments(path: str, name_to_tag: dict) -> list:
    """Convert a PDF path to a list of XML tags."""
    parts = path.split("/")
    if parts and "." in parts[0]:
        parts = parts[1:]
    tags = []
    for part in parts:
        part = part.strip().rstrip("-")
        if not part or part.startswith("."):
            continue
        if part in name_to_tag:
            tags.append(name_to_tag[part])
        else:
            tags.append(part)
    return tags


def _apply_removed_elements(schema: dict, removed_paths: list, name_to_tag: dict) -> None:
    """Mark fields as removed based on path matching."""
    removed_tag_chains = []
    for path in removed_paths:
        tags = _resolve_path_segments(path, name_to_tag)
        if tags:
            removed_tag_chains.append(tags)

    def walk_remove(fields: list, ancestors: list) -> None:
        for f in fields:
            tag = f.get("xml_tag", "")
            current_chain = ancestors + [tag]
            for chain in removed_tag_chains:
                if len(chain) <= len(current_chain):
                    if current_chain[-len(chain):] == chain[-len(chain):]:
                        f["_removed"] = True
                        break
            walk_remove(f.get("children", []), current_chain)

    walk_remove(schema.get("app_hdr_fields", []), [])
    walk_remove(schema.get("document_fields", []), [])


def _apply_mandatory_overrides(schema: dict, overrides: list, name_to_tag: dict) -> None:
    """Apply mandatory overrides to matching fields."""
    override_chains = []
    for ov in overrides:
        tags = _resolve_path_segments(ov["path"], name_to_tag)
        if tags:
            override_chains.append((tags, ov["min_occurrence"]))

    def walk_mandatory(fields: list, ancestors: list) -> None:
        for f in fields:
            tag = f.get("xml_tag", "")
            current_chain = ancestors + [tag]
            for chain, min_occ in override_chains:
                if len(chain) <= len(current_chain):
                    if current_chain[-len(chain):] == chain[-len(chain):]:
                        f["mult_min"] = max(f.get("mult_min", 0), min_occ)
                        break
            walk_mandatory(f.get("children", []), current_chain)

    walk_mandatory(schema.get("app_hdr_fields", []), [])
    walk_mandatory(schema.get("document_fields", []), [])


def _apply_type_changes(schema: dict, type_changes: list, name_to_tag: dict) -> None:
    """Apply type change overrides (max_length, type_code)."""
    TYPE_MAP = {
        "CBPR_RestrictedFINXMax10Text": {"max_length": 10},
        "CBPR_RestrictedFINXMax16Text_Extended": {"max_length": 16},
        "CBPR_RestrictedFINXMax34Text": {"max_length": 34},
        "CBPR_RestrictedFINXMax35Text": {"max_length": 35},
        "CBPR_RestrictedFINXMax35Text_Extended": {"max_length": 35},
        "CBPR_RestrictedFINXMax70Text": {"max_length": 70},
        "CBPR_RestrictedFINXMax70Text_Extended": {"max_length": 70},
        "CBPR_RestrictedFINXMax140Text": {"max_length": 140},
        "CBPR_RestrictedFINXMax140Text_Extended": {"max_length": 140},
        "CBPR_RestrictedFINXMax320Text_Extended": {"max_length": 320},
        "CBPR_Date": {"type_code": "date", "max_length": 10},
        "CBPR_DateTime": {"type_code": "dateTime"},
        "CBPR_Time": {"type_code": "time"},
        "CBPR_Amount": {},
        "Priority2Code": {},
    }

    change_chains = []
    for tc in type_changes:
        tags = _resolve_path_segments(tc["path"], name_to_tag)
        if tags:
            change_chains.append((tags, tc["target_type"]))

    def walk_type(fields: list, ancestors: list) -> None:
        for f in fields:
            tag = f.get("xml_tag", "")
            current_chain = ancestors + [tag]
            for chain, target in change_chains:
                if len(chain) <= len(current_chain):
                    if current_chain[-len(chain):] == chain[-len(chain):]:
                        f["type_override"] = target
                        overrides = TYPE_MAP.get(target, {})
                        if "max_length" in overrides:
                            f["max_length"] = overrides["max_length"]
                        if "type_code" in overrides:
                            f["type_code"] = overrides["type_code"]
                        break
            walk_type(f.get("children", []), current_chain)

    walk_type(schema.get("app_hdr_fields", []), [])
    walk_type(schema.get("document_fields", []), [])


def _apply_choice_groups(schema: dict, choice_groups: list) -> None:
    """Mark fields that are part of choice groups.

    Choice options have [1..1] in the PDF but this means "required IF chosen",
    not "always required". Set mult_min=0 so they render as optional,
    and let the JS handle "at least one" validation.
    """
    def walk_choice(fields: list) -> None:
        for f in fields:
            children = f.get("children", [])
            child_tags = [c.get("xml_tag", "") for c in children]
            for group in choice_groups:
                opts = [o["tag"] for o in group.get("options", [])]
                if len(opts) >= 2 and all(t in child_tags for t in opts):
                    f["is_choice"] = True
                    f["choice_options"] = opts
                    for c in children:
                        if c.get("xml_tag", "") in opts:
                            c["is_choice_option"] = True
                            c["_original_mult_min"] = c.get("mult_min", 0)
                            c["mult_min"] = 0
                            _clear_children_required(c)
                    break
            walk_choice(children)

    walk_choice(schema.get("app_hdr_fields", []))
    walk_choice(schema.get("document_fields", []))


def _clear_children_required(field: dict) -> None:
    """Recursively set mult_min=0 for all leaf children of a choice option."""
    for c in field.get("children", []):
        if c.get("mult_min", 0) >= 1:
            c["_original_mult_min"] = c.get("mult_min", 0)
            c["mult_min"] = 0
        _clear_children_required(c)


def _path_matches_field(rule_path: str, xml_tag: str, name_en_no_space: str) -> bool:
    """Check if a rule path's last segment matches a field."""
    if not rule_path or rule_path == ".fullmessage":
        return False
    last_seg = rule_path.rstrip("/").split("/")[-1].rstrip("-")
    if not last_seg or last_seg.startswith("."):
        return False
    return last_seg == name_en_no_space or last_seg == xml_tag


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_form.py <input.pdf> [output_dir] [--single-file]")
        print()
        print("Parses an ISO 20022 PDF specification and generates an interactive HTML form.")
        print("The generated form is compatible with IE8+ and modern browsers.")
        print()
        print("Arguments:")
        print("  input.pdf     Path to ISO 20022 usage guideline PDF")
        print("  output_dir    Output directory (default: output/)")
        print()
        print("Options:")
        print("  --single-file  Also generate a single self-contained HTML file")
        sys.exit(1)

    pdf_path = sys.argv[1]
    single_file = "--single-file" in sys.argv
    rules_pdf = None
    if "--rules-pdf" in sys.argv:
        idx = sys.argv.index("--rules-pdf")
        if idx + 1 < len(sys.argv):
            rules_pdf = sys.argv[idx + 1]

    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("ISO 20022 Form Generator v4 (IE8+ Compatible)")
    print("=" * 60)

    schema = parse_pdf(pdf_path)

    if rules_pdf:
        from parse_rules_pdf import parse_rules_pdf
        rules = parse_rules_pdf(rules_pdf)
        merge_rules(schema, rules)
        print(f"Rules merged: {len(rules.get('fixed_values', []))} fixed values, "
              f"{len(rules.get('business_rules', []))} business rules, "
              f"{len(rules.get('choice_groups', []))} choice groups, "
              f"{len(rules.get('removed_elements', []))} removed, "
              f"{len(rules.get('mandatory_overrides', []))} mandatory overrides")

    if not schema.get('message_id'):
        print("ERROR: Could not detect message type from PDF.", file=sys.stderr)
        print("Please ensure the PDF is a valid ISO 20022 usage guideline.", file=sys.stderr)
        sys.exit(1)

    message_id = schema["message_id"]
    safe_name = message_id.replace('.', '_')

    output_dir = resolve_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Save schema JSON
    schema_path = os.path.join(output_dir, f"{message_id}.json")
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSchema saved: {schema_path}")

    # Multi-file output (always)
    form_dir = os.path.join(output_dir, "form")
    os.makedirs(form_dir, exist_ok=True)
    print("\nMulti-file output:")
    write_multi_file(schema, form_dir)

    # Single-file output (optional)
    if single_file:
        single_path = os.path.join(output_dir, f"{safe_name}.html")
        print("\nSingle-file output:")
        write_single_file(schema, single_path)

    print("\n" + "=" * 60)
    print("Done. Open output/form/index.html in browser (IE8+ compatible).")
    if single_file:
        print(f"Single-file version: output/{safe_name}.html")
    print("=" * 60)


if __name__ == '__main__':
    main()

