"""Page-level HTML assembly for generated ISO 20022 forms (v4, IE8+).

Assembles the complete HTML page by combining:
- Bootstrap 3 HTML shell with IE conditional comments
- Field HTML from field_renderer.py
- Field metadata collection for fieldMeta.js
- App configuration for appConfig.js
- References to external CSS/JS files

Individual field/card HTML belongs in field_renderer.py.
Collection-specific rule constants belong in form_rules.py.
"""

from __future__ import annotations

import html as html_mod
import json

from field_renderer import detect_component_type, render_field_html
from form_rules import (
    BUSINESS_RULES,
    COMPONENT_SIGNATURES,
    FIELD_STATE_OVERRIDES,
    FIELD_STATE_STYLES,
    QUICK_FILL_FIELDS,
    TEMPLATES,
    force_date_type,
    is_proxy_tp_field,
    should_remove_field,
)


# ==================== Public API ====================


def generate_html(schema: dict, safe_name: str = "") -> str:
    """Generate complete HTML form page from parsed schema.

    Returns a full HTML document string referencing external CSS/JS files.
    safe_name is used for per-message JS file references (e.g. 'pacs_008_001_08').
    """
    message_id = schema.get("message_id", "Unknown")
    if not safe_name:
        safe_name = message_id.replace('.', '_')
    message_name_en = schema.get("message_name_en", "Unknown Message")
    message_name_zh = schema.get("message_name_zh", message_name_en)
    collection_name = schema.get("collection_name", "")
    app_hdr_fields = schema.get("app_hdr_fields", [])
    document_fields = schema.get("document_fields", [])

    # --- Render field HTML ---
    app_hdr_html = ""
    for field in app_hdr_fields:
        app_hdr_html += render_field_html(field, "AH", "")

    document_html = ""
    for field in document_fields:
        document_html += render_field_html(field, "DOC", "")

    # --- Collect field metadata ---
    all_fields, _component_instances = _collect_field_metadata(app_hdr_fields, document_fields)

    # --- Collect at-least-one groups ---
    at_least_one_groups = _collect_at_least_one_groups(app_hdr_fields, document_fields)

    # --- Build at-least-one groups script block ---
    at_least_one_js = (
        "<script>\nwindow.AT_LEAST_ONE_GROUPS = "
        + json.dumps(at_least_one_groups, ensure_ascii=False)
        + ";\n</script>"
    )

    # --- Build choice groups script block ---
    choice_groups = schema.get("choice_groups", [])
    choice_groups_js = (
        "<script>\nwindow.CHOICE_GROUPS = "
        + json.dumps(choice_groups, ensure_ascii=False)
        + ";\n</script>"
    )

    # --- Escape user-facing text for HTML ---
    esc_msg_id = html_mod.escape(message_id)
    esc_name_zh = html_mod.escape(message_name_zh)
    esc_name_en = html_mod.escape(message_name_en)
    esc_collection = html_mod.escape(collection_name)

    # --- Assemble page ---
    parts = [
        _html_head(esc_msg_id, esc_name_zh, esc_name_en, esc_collection),
        _html_command_bar(),
        _html_progress_template_search(),
        _html_form_sections(app_hdr_html, document_html),
        _html_json_panel(esc_msg_id),
        _html_footer(at_least_one_js + "\n" + choice_groups_js, safe_name),
    ]
    return "\n".join(parts)


def generate_field_meta_js(schema: dict) -> str:
    """Generate the contents of fieldMeta.js for external file output.

    Returns a string with 3 sections:
    - window.COMPONENT_TEMPLATES: template definitions for reusable components
    - window.COMPONENT_INSTANCES: instance mappings (type + pathPrefix)
    - window.FIELD_META: independent (non-component) field metadata
    """
    app_hdr_fields = schema.get("app_hdr_fields", [])
    document_fields = schema.get("document_fields", [])
    independent_fields, component_instances = _collect_field_metadata(
        app_hdr_fields, document_fields
    )

    # Generate component templates from schema
    templates = _build_component_templates(schema)

    parts = []
    parts.append(
        "window.COMPONENT_TEMPLATES = "
        + json.dumps(templates, ensure_ascii=False, indent=2) + ";\n"
    )
    parts.append(
        "window.COMPONENT_INSTANCES = "
        + json.dumps(component_instances, ensure_ascii=False) + ";\n"
    )
    parts.append(
        "window.FIELD_META = "
        + json.dumps(independent_fields, ensure_ascii=False) + ";\n"
    )
    return "\n".join(parts)


def generate_app_config_js(schema: dict) -> str:
    """Generate the contents of appConfig.js for external file output.

    Returns a string suitable for writing directly to js/appConfig.js.
    """
    message_id = schema.get("message_id", "Unknown")
    config = {
        "messages": {
            message_id: {
                "templates": TEMPLATES,
                "quickFillFields": QUICK_FILL_FIELDS,
                "fieldStateStyles": FIELD_STATE_STYLES,
                "fieldStateOverrides": FIELD_STATE_OVERRIDES,
                "fieldAliases": {},
                "valueMappings": {},
                "conditionalPresence": schema.get("conditional_presence", []),
                "notAllowedValues": schema.get("not_allowed_values", []),
                "isoRules": schema.get("iso_rules", []),
            }
        }
    }
    return (
        "window.ISO20022_APP_CONFIG = "
        + json.dumps(config, ensure_ascii=False, indent=2)
        + ";\n"
    )


# ==================== Component Template Generation ====================


def _build_component_templates(schema: dict) -> dict:
    """Build component template definitions from the first instance of each type in schema.

    Walks the schema tree, finds the first field matching each component signature,
    and extracts its child structure as a reusable template.
    """
    templates = {}
    document_fields = schema.get("document_fields", [])

    def find_first_instance(fields: list, comp_type: str, signature: set) -> dict | None:
        for f in fields:
            children = f.get("children", [])
            if children:
                child_tags = {c.get("xml_tag", "") for c in children}
                if signature.issubset(child_tags):
                    return f
                result = find_first_instance(children, comp_type, signature)
                if result:
                    return result
        return None

    def field_to_template(f: dict) -> dict:
        """Convert a schema field to a template node."""
        node = {
            "tag": f.get("xml_tag", ""),
            "nameZh": f.get("name_zh", f.get("name_en", "")),
            "nameEn": f.get("name_en", ""),
        }
        children = f.get("children", [])
        type_code = f.get("type_code", "text")
        if force_date_type(f):
            type_code = "date"

        if children:
            node["type"] = "container"
            node["children"] = [field_to_template(c) for c in children
                                if not should_remove_field(c, f.get("xml_tag", ""))
                                and not c.get("is_attribute", False)]
        else:
            node["type"] = type_code if type_code else "text"
            if f.get("max_length", 0) > 0:
                node["maxLen"] = f["max_length"]
            if f.get("regex_pattern", ""):
                node["pattern"] = f["regex_pattern"]
            if f.get("code_values"):
                node["codeValues"] = f["code_values"]
            if f.get("is_fixed", False):
                node["isFixed"] = True
                node["fixedValue"] = f.get("fixed_value", "")

        mult_min = f.get("mult_min", 0)
        mult_max = f.get("mult_max", 1)
        if mult_min > 0:
            node["multMin"] = mult_min
        if mult_max > 1:
            node["multMax"] = mult_max

        return node

    for comp_type, signature in COMPONENT_SIGNATURES.items():
        instance = find_first_instance(document_fields, comp_type, signature)
        if not instance:
            continue
        children = instance.get("children", [])
        template_fields = []
        leaf_count = 0
        for c in children:
            if should_remove_field(c, instance.get("xml_tag", "")):
                continue
            if c.get("is_attribute", False):
                continue
            tpl_node = field_to_template(c)
            template_fields.append(tpl_node)
            leaf_count += _count_template_leaves(tpl_node)

        templates[comp_type] = {
            "leafCount": leaf_count,
            "fields": template_fields,
        }

    return templates


def _count_template_leaves(node: dict) -> int:
    """Count leaf fields in a template node recursively."""
    children = node.get("children", [])
    if not children:
        return 1
    total = 0
    for c in children:
        total += _count_template_leaves(c)
    return total


# ==================== Field Metadata Collection ====================


def _compute_instance_overrides(field: dict, comp_type: str) -> dict:
    """Compute per-instance overrides relative to the component template.

    Checks for fields that have different mult_min (mandatory overrides),
    different max_length (type changes), or are marked as removed in this
    specific instance but present in the template.

    Returns a dict with keys: mandatory, typeChanges, removed (only if non-empty).
    """
    overrides = {}
    mandatory = []
    type_changes = {}

    def walk(children: list, parent_tag: str) -> None:
        for c in children:
            tag = c.get("xml_tag", "")
            # Check mandatory overrides (mult_min forced to 1 by rules)
            if c.get("mult_min", 0) >= 1 and not c.get("is_fixed", False):
                if not c.get("children"):
                    mandatory.append(tag)
            # Check type/length overrides from rules
            if c.get("type_override"):
                tc = {}
                if c.get("max_length", 0) > 0:
                    tc["maxLen"] = c["max_length"]
                if c.get("type_code") in ("date", "time"):
                    tc["type"] = c["type_code"]
                if tc:
                    type_changes[tag] = tc
            # Recurse into children
            if c.get("children"):
                walk(c["children"], tag)

    walk(field.get("children", []), field.get("xml_tag", ""))

    if mandatory:
        overrides["mandatory"] = mandatory
    if type_changes:
        overrides["typeChanges"] = type_changes
    return overrides


def _collect_field_metadata(app_hdr_fields: list, document_fields: list) -> tuple:
    """Walk field trees and collect metadata.

    Returns (independent_fields, component_instances) where:
    - independent_fields: flat list of field metadata dicts (non-component fields)
    - component_instances: list of component instance dicts for lazy rendering
    """
    independent_fields: list[dict] = []
    component_instances: list[dict] = []

    def build_iso_path(prefix: str, cur_path: str) -> str:
        dot_path = cur_path.replace("_", ".")
        if prefix == "AH":
            return dot_path if dot_path.startswith("AppHdr") else f"AppHdr.{dot_path}"
        if prefix == "DOC":
            return f"Document.{dot_path}"
        return dot_path

    def collect(fields: list, prefix: str, path: str = "", parent_tag: str = "") -> None:
        for f in fields:
            tag = f.get("xml_tag", "")
            cur_path = f"{path}_{tag}" if path else tag
            form_name = f"{prefix}_{cur_path}" if prefix else cur_path
            iso_path = build_iso_path(prefix, cur_path)

            # F01/F02/F08: Skip removed fields per CBPR+ SR2026 CRs
            if should_remove_field(f, parent_tag):
                continue

            # F03: Make Proxy/Type mandatory
            mult_min = f.get("mult_min", 0)
            if is_proxy_tp_field(f, parent_tag):
                mult_min = 1

            # F05: Force date type
            type_code = f.get("type_code", "text")
            if force_date_type(f):
                type_code = "date"

            # Check if this is a component instance (lazy rendered)
            comp_type = detect_component_type(f) if f.get("children") else None
            if comp_type:
                overrides = _compute_instance_overrides(f, comp_type)
                instance_data = {
                    "type": comp_type,
                    "pathPrefix": form_name,
                    "isoPath": iso_path,
                    "nameZh": f.get("name_zh", f.get("name_en", "")),
                    "nameEn": f.get("name_en", ""),
                    "multMin": mult_min,
                    "multMax": f.get("mult_max", 1),
                }
                if overrides:
                    instance_data["overrides"] = overrides
                component_instances.append(instance_data)
                # Skip children — they'll be rendered by JS component template
                continue

            independent_fields.append({
                "xml_tag": tag,
                "name_en": f.get("name_en", ""),
                "name_zh": f.get("name_zh", ""),
                "type_code": type_code,
                "mult_min": mult_min,
                "mult_max": f.get("mult_max", 1),
                "regex_pattern": f.get("regex_pattern", ""),
                "max_length": f.get("max_length", 0),
                "decimal_td": f.get("decimal_td", 0),
                "decimal_fd": f.get("decimal_fd", 0),
                "is_fixed": f.get("is_fixed", False),
                "fixed_value": f.get("fixed_value", ""),
                "form_name": form_name,
                "iso_path": iso_path,
                "code_values": f.get("code_values", []),
                "business_rules": f.get("business_rules", []),
            })
            if f.get("children"):
                collect(f["children"], prefix, cur_path, tag)

    collect(app_hdr_fields, "AH")
    collect(document_fields, "DOC")
    return independent_fields, component_instances


# ==================== At-Least-One Groups ====================


def _collect_at_least_one_groups(app_hdr_fields: list, document_fields: list) -> list:
    """Identify parent-required groups where all leaf children are optional.

    These groups require at least one child to be filled for the parent to be
    valid (ISO 20022 structural constraint).
    """
    at_least_one_groups: list[dict] = []

    def walk(fields: list, prefix: str, path: str = "") -> None:
        for f in fields:
            children = f.get("children", [])
            if not children:
                continue
            tag = f.get("xml_tag", "")
            mult_min = f.get("mult_min", 0)
            name_zh = f.get("name_zh", f.get("name_en", ""))
            cur_path = f"{path}_{tag}" if path else tag

            # Filter out removed fields from leaf_children
            leaf_children = [
                c for c in children
                if not c.get("children") and not should_remove_field(c, tag)
            ]
            if len(leaf_children) >= 2 and mult_min >= 1:
                all_optional = all(c.get("mult_min", 0) == 0 for c in leaf_children)
                if all_optional:
                    child_names = []
                    child_labels = []
                    for lc in leaf_children:
                        lc_tag = lc.get("xml_tag", "")
                        lc_name = lc.get("name_zh", lc.get("name_en", ""))
                        form_name = f"{prefix}_{cur_path}_{lc_tag}"
                        child_names.append(form_name)
                        child_labels.append(
                            f"{lc_name} ({lc_tag})" if lc_tag else lc_name
                        )

                    at_least_one_groups.append({
                        "parent_tag": tag,
                        "parent_name_zh": name_zh,
                        "parent_path": cur_path,
                        "children": child_names,
                        "child_labels": child_labels,
                    })

            walk(children, prefix, cur_path)

    walk(app_hdr_fields, "AH")
    walk(document_fields, "DOC")

    # Deduplicate by parent_path
    seen: set[str] = set()
    unique: list[dict] = []
    for g in at_least_one_groups:
        key = g["parent_path"]
        if key not in seen:
            seen.add(key)
            unique.append(g)
    return unique


# ==================== HTML Page Assembly Functions ====================


def _html_head(message_id: str, name_zh: str, name_en: str, collection: str) -> str:
    """Return <!DOCTYPE> through opening <body> and page header bar."""
    return (
        '<!DOCTYPE html>\n'
        '<html lang="zh-CN">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <title>{message_id} - ISO 20022 Message Form</title>\n'
        '  <link rel="stylesheet" href="css/bootstrap.min.css">\n'
        '  <link rel="stylesheet" href="css/bootstrap-theme.min.css">\n'
        '  <link rel="stylesheet" href="css/app.css">\n'
        '  <!--[if lt IE 9]>\n'
        '  <script src="js/vendor/html5shiv.min.js"></script>\n'
        '  <script src="js/vendor/respond.min.js"></script>\n'
        '  <script src="js/vendor/es5-shim.min.js"></script>\n'
        '  <script src="js/vendor/es5-sham.min.js"></script>\n'
        '  <script src="js/vendor/json2.min.js"></script>\n'
        '  <![endif]-->\n'
        '</head>\n'
        '<body class="theme-light">\n'
        '\n'
        '  <div id="page-wrapper">\n'
        '  <!-- Page Header Bar -->\n'
        '  <div class="page-header-bar">\n'
        f'    <h1>{name_zh} / {name_en}</h1>\n'
        f'    <p class="subtitle">ISO 20022 {collection}</p>\n'
        f'    <span class="msg-id">{message_id}</span>\n'
        '    <span class="audit-badge">审核只读模式</span>\n'
        '  </div>\n'
    )


def _html_command_bar() -> str:
    """Return the command bar with action buttons."""
    return (
        '    <div class="main-panel">\n'
        '      <!-- Command Bar -->\n'
        '      <div class="command-bar">\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnRequiredOnly">'
        '\U0001f441️ 仅显示必填</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnExportJson">'
        '\U0001f4cb 复制JSON</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnExportXml">'
        '\U0001f4c4 导出XML</button>\n'
        '        <button type="button" class="btn btn-primary btn-sm" id="btnValidate">'
        '✅ 校验全部</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnClearDraft">'
        '\U0001f5d1️ 清除草稿</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnAuditMode">'
        '\U0001f512 审核模式</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnLangZh">'
        '中</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnLangEn">'
        'EN</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnLangFr">'
        'FR</button>\n'
        '        <button type="button" class="btn btn-default btn-sm" id="btnTheme">'
        '\U0001f313 主题</button>\n'
        '        <span class="autosave-indicator">\n'
        '          <span class="autosave-dot" id="autosaveDot"></span>\n'
        '          <span id="autosaveText">自动暂存已开启</span>\n'
        '        </span>\n'
        '      </div>\n'
    )


def _html_progress_template_search() -> str:
    """Return progress bar, template bar, and search bar."""
    return (
        '\n'
        '      <!-- Progress Bar -->\n'
        '      <div class="progress-container">\n'
        '        <span class="progress-label">\U0001f4ca 必填字段完成度 / Required Fields</span>\n'
        '        <div class="progress">\n'
        '          <div class="progress-bar" id="progressFill" role="progressbar"'
        ' style="width:0%"></div>\n'
        '        </div>\n'
        '        <span class="progress-text" id="progressText">0 / 0</span>\n'
        '      </div>\n'
        '\n'
        '      <!-- Template Bar -->\n'
        '      <div class="template-bar">\n'
        '        <span class="label-text">\U0001f4cb 快速模板 / Templates:</span>\n'
        '        <span id="runtimeTemplateList"></span>\n'
        '      </div>\n'
        '\n'
        '      <!-- Search Bar -->\n'
        '      <div class="search-bar">\n'
        '        <div class="input-group">\n'
        '          <span class="input-group-addon">\U0001f50d</span>\n'
        '          <input type="text" class="form-control" id="fieldSearch"'
        ' placeholder="输入字段名定位 (中文/英文/XML标签)...">\n'
        '          <span class="input-group-btn">\n'
        '            <button class="btn btn-default" type="button" id="searchPrev"'
        ' disabled="disabled">&#8593;</button>\n'
        '            <button class="btn btn-default" type="button" id="searchNext"'
        ' disabled="disabled">&#8595;</button>\n'
        '            <button class="btn btn-default" type="button" id="searchClear"'
        '>&#215;</button>\n'
        '          </span>\n'
        '        </div>\n'
        '        <span class="search-count" id="searchCount"></span>\n'
        '      </div>\n'
    )


def _html_form_sections(app_hdr_html: str, document_html: str) -> str:
    """Return section dividers and rendered form fields."""
    return (
        '\n'
        '      <!-- Section: AppHdr -->\n'
        '      <div class="section-divider"><span>'
        '业务应用头 / Business Application Header</span></div>\n'
        + app_hdr_html +
        '\n'
        '      <!-- Section: Document -->\n'
        '      <div class="section-divider"><span>'
        '报文正文 / Document</span></div>\n'
        + document_html +
        '\n'
        '    </div>\n'
    )


def _html_json_panel(message_id: str) -> str:
    """Return the right-side JSON preview panel."""
    return (
        '\n'
        '    <!-- JSON Panel -->\n'
        '    <div class="json-panel">\n'
        '      <div class="panel panel-default">\n'
        '        <div class="panel-heading">\n'
        '          <div class="json-tabs btn-group btn-group-xs">\n'
        '            <button type="button" class="btn btn-default active"'
        ' id="tabSummary">摘要</button>\n'
        '            <button type="button" class="btn btn-default"'
        ' id="tabJson">JSON</button>\n'
        '          </div>\n'
        '          <div class="pull-right">\n'
        '            <button type="button" class="btn btn-default btn-xs"'
        ' id="btnImport">导入</button>\n'
        '            <button type="button" class="btn btn-default btn-xs"'
        ' id="btnCopyJson">复制</button>\n'
        '            <button type="button" class="btn btn-default btn-xs"'
        ' id="btnPrint">打印</button>\n'
        '          </div>\n'
        '        </div>\n'
        '        <div class="panel-body">\n'
        '          <div id="summaryView" class="summary-view">\n'
        '            <div class="summary-item"><span class="summary-label">'
        '报文类型</span><span class="summary-value" id="sumMsgType">'
        + message_id + '</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '付款人</span><span class="summary-value" id="sumDebtor">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '付款行</span><span class="summary-value" id="sumDebtorAgent">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '收款人</span><span class="summary-value" id="sumCreditor">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '收款行</span><span class="summary-value" id="sumCreditorAgent">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '结算金额</span><span class="summary-value" id="sumAmount">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '费用承担</span><span class="summary-value" id="sumChrgBr">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '汇款附言</span><span class="summary-value" id="sumRmtInf">'
        '—</span></div>\n'
        '            <div class="summary-item"><span class="summary-label">'
        '端到端ID</span><span class="summary-value" id="sumE2E">'
        '—</span></div>\n'
        '          </div>\n'
        '          <textarea id="jsonPreview" style="display:none"'
        ' readonly="readonly"></textarea>\n'
        '        </div>\n'
        '        <div class="validation-summary" id="validationSummary"></div>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
    )

def _html_footer(at_least_one_js: str, safe_name: str = "") -> str:
    """Return modals, toast, quick panel, scripts, and closing tags."""
    return (
        '\n'
        '  <!-- Toast -->\n'
        '  <div class="toast-msg" id="toast"></div>\n'
        '\n'
        '  <!-- Quick Fill Panel -->\n'
        '  <button type="button" class="quick-panel-toggle" id="quickPanelToggle"'
        ' title="业务快捷字段">&#9889;</button>\n'
        '  <div class="quick-panel" id="quickPanel">\n'
        '    <div class="panel panel-default">\n'
        '      <div class="panel-heading">\n'
        '        <span>业务快捷字段 / Business Quick Fields</span>\n'
        '        <button type="button" class="btn btn-xs btn-default pull-right"'
        ' id="quickPanelClose">&#215;</button>\n'
        '      </div>\n'
        '      <div class="panel-body">\n'
        '        <div id="quickFillFields"></div>\n'
        '        <div style="margin-top:10px;text-align:right">\n'
        '          <button type="button" class="btn btn-default btn-sm"'
        ' id="btnQuickClear">清空</button>\n'
        '          <button type="button" class="btn btn-primary btn-sm"'
        ' id="btnQuickSync">同步到表单</button>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <!-- Confirm Modal -->\n'
        '  <div class="modal fade" id="confirmModal" tabindex="-1">\n'
        '    <div class="modal-dialog modal-sm">\n'
        '      <div class="modal-content">\n'
        '        <div class="modal-header">'
        '<h4 class="modal-title" id="confirmTitle"></h4></div>\n'
        '        <div class="modal-body"><p id="confirmBody"></p></div>\n'
        '        <div class="modal-footer">\n'
        '          <button type="button" class="btn btn-default"'
        ' data-dismiss="modal">取消</button>\n'
        '          <button type="button" class="btn btn-primary"'
        ' id="confirmOk">确定</button>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <!-- Import Modal -->\n'
        '  <div class="modal fade" id="importModal" tabindex="-1">\n'
        '    <div class="modal-dialog">\n'
        '      <div class="modal-content">\n'
        '        <div class="modal-header">'
        '<h4 class="modal-title">导入 JSON</h4></div>\n'
        '        <div class="modal-body">\n'
        '          <p>粘贴之前导出的 JSON 数据，将自动填充表单。</p>\n'
        '          <textarea id="importJsonText" class="form-control"'
        ' rows="12"></textarea>\n'
        '        </div>\n'
        '        <div class="modal-footer">\n'
        '          <button type="button" class="btn btn-default"'
        ' data-dismiss="modal">取消</button>\n'
        '          <button type="button" class="btn btn-primary"'
        ' id="btnDoImport">导入</button>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <!-- Inline Data -->\n'
        + at_least_one_js + '\n'
        '\n'
        '  <!-- Scripts -->\n'
        '  <script src="js/vendor/jquery-1.12.4.min.js"></script>\n'
        '  <script src="js/vendor/bootstrap.min.js"></script>\n'
        f'  <script src="js/{safe_name}_fieldMeta.js"></script>\n'
        f'  <script src="js/{safe_name}_appConfig.js"></script>\n'
        '  <script src="js/app.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )
