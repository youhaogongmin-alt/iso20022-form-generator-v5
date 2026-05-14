"""Field-level HTML rendering helpers (Bootstrap 3 / IE8+ version).

Generates Bootstrap 3 panels, form-groups, and collapse components.
All output is IE8-compatible (no HTML5-only input types, no flexbox).
Page-wide chrome, toolbars, and JavaScript live in form_page.py.
"""

from __future__ import annotations

import html

from form_rules import (
    COMPONENT_SIGNATURES,
    force_date_type,
    is_proxy_tp_field,
    should_remove_field,
)


# ==================== Component Detection ====================

# Which component types are currently enabled for lazy rendering.
# Start with Account only (Phase 2), expand later.
LAZY_COMPONENTS_ENABLED = {'Account', 'FinInstnId', 'PartyIdentification'}


def detect_component_type(field: dict) -> str | None:
    """Detect if a container field matches a known reusable component type.

    Returns the component type name or None.
    Only returns a match if the component is enabled for lazy rendering.
    """
    children = field.get("children", [])
    if not children:
        return None
    child_tags = {c.get("xml_tag", "") for c in children}
    for comp_type, signature in COMPONENT_SIGNATURES.items():
        if comp_type not in LAZY_COMPONENTS_ENABLED:
            continue
        if signature.issubset(child_tags):
            return comp_type
    return None


# ==================== Public API ====================


def render_field_html(field: dict, prefix: str, parent_path: str) -> str:
    """Render a single field or group as HTML.

    Parameters
    ----------
    field : dict
        Field descriptor with keys like xml_tag, name_en, children, etc.
    prefix : str
        'AH' for AppHdr or 'DOC' for Document.
    parent_path : str
        Underscore-separated ancestor path (empty string for root children).

    Returns
    -------
    str
        HTML fragment.
    """
    xml_tag = field.get("xml_tag", "")
    name_en = field.get("name_en", "")
    name_zh = field.get("name_zh", name_en)
    type_code = field.get("type_code", "text")
    mult_min = field.get("mult_min", 0)
    mult_max = field.get("mult_max", 1)
    regex_pattern = field.get("regex_pattern", "")
    max_length = field.get("max_length", 0)
    is_fixed = field.get("is_fixed", False)
    fixed_value = field.get("fixed_value", "")
    code_values = field.get("code_values", [])
    children = field.get("children", [])

    # Build form_name and iso_path
    field_path = f"{parent_path}_{xml_tag}" if parent_path else xml_tag
    form_name = f"{prefix}_{field_path}"
    iso_path = _build_iso_path(prefix, field_path)

    # --- Rule overrides ---
    # F03 (CR 3012): Make Proxy/Type mandatory
    parent_tag = parent_path.split("_")[-1] if parent_path else ""
    if is_proxy_tp_field(field, parent_tag):
        mult_min = 1

    # F05 (CR 3039): Force date type
    if force_date_type(field):
        type_code = "date"

    # --- Dispatch ---
    # Amount + Currency combo: decimal field with a single Ccy child
    if children and type_code == "decimal":
        ccy_child = None
        for c in children:
            if c.get("xml_tag") == "Ccy" or (
                c.get("is_attribute") or c.get("name_en", "").startswith("Xml Attribute")
            ):
                ccy_child = c
                break
        if ccy_child:
            return _render_amount_with_currency(
                field, prefix, field_path, form_name, iso_path,
                xml_tag, name_en, name_zh, mult_min, max_length,
            )

    if children:
        return _render_container(field, prefix, field_path, form_name, iso_path,
                                 mult_min, mult_max, is_fixed, fixed_value)

    # Skip attribute fields
    if field.get("is_attribute", False):
        return ""

    return _render_leaf(
        field, prefix, field_path, form_name, iso_path,
        xml_tag, name_en, name_zh, type_code,
        mult_min, mult_max, regex_pattern, max_length,
        is_fixed, fixed_value, code_values,
    )


# ==================== Internal Helpers ====================


def _build_iso_path(prefix: str, field_path: str) -> str:
    """Convert prefix + underscore path to dotted ISO path."""
    dot_path = field_path.replace("_", ".")
    if prefix == "AH":
        return f"AppHdr.{dot_path}"
    return f"Document.{dot_path}"


def _mult_display(mult_max: int) -> str:
    """Return display string for mult_max."""
    if mult_max == float("inf") or mult_max >= 9999:
        return "*"
    return str(mult_max)


def _badge_html(mult_min: int, is_fixed: bool, fixed_value: str) -> str:
    """Return the appropriate Bootstrap label badge."""
    if is_fixed:
        return (
            f'<span class="label label-success">'
            f"固定值 / Fixed: {html.escape(fixed_value)}</span>"
        )
    if mult_min >= 1:
        return '<span class="label label-danger">必填 / Required</span>'
    return '<span class="label label-info">可选 / Optional</span>'


def _required_mark(mult_min: int) -> str:
    """Return required asterisk span if field is mandatory."""
    if mult_min >= 1:
        return '<span class="required text-danger">*</span>'
    return ""


def _build_input_html(
    form_name: str,
    prefix: str,
    xml_tag: str,
    iso_path: str,
    type_code: str,
    max_length: int,
    is_fixed: bool,
    fixed_value: str,
    code_values: list,
) -> str:
    """Build the appropriate <input> or <select> element."""
    common_attrs = (
        f'class="form-control" id="{html.escape(form_name)}" '
        f'name="{html.escape(form_name)}" '
        f'data-prefix="{html.escape(prefix)}" '
        f'data-tag="{html.escape(xml_tag)}" '
        f'data-iso-path="{html.escape(iso_path)}" '
        f'data-form-name="{html.escape(form_name)}" '
        f'data-type-code="{html.escape(type_code)}"'
    )
    maxlen_attr = f' maxlength="{max_length}"' if max_length > 0 else ""

    # Fixed value
    if is_fixed:
        return (
            f'<input type="text" {common_attrs}{maxlen_attr} '
            f'readonly="readonly" value="{html.escape(fixed_value)}">'
        )

    # Boolean → select
    if type_code == "boolean":
        return (
            f'<select {common_attrs}>\n'
            f'  <option value="">-- 请选择 / Please select --</option>\n'
            f'  <option value="true">是 / Yes (true)</option>\n'
            f'  <option value="false">否 / No (false)</option>\n'
            f'</select>'
        )

    # Code list → select
    if code_values:
        opts = '<option value="">-- 请选择 / Please select --</option>\n'
        for cv in code_values:
            code = html.escape(cv.get("code", ""))
            desc_en = html.escape(cv.get("description_en", ""))
            desc_zh = html.escape(cv.get("description_zh", desc_en))
            opts += f'    <option value="{code}">{code} - {desc_zh} / {desc_en}</option>\n'
        return f'<select {common_attrs}>\n    {opts}</select>'

    # Date/time types → text with placeholder (IE8 safe)
    if type_code == "date":
        return (
            f'<input type="text" {common_attrs}{maxlen_attr} '
            f'placeholder="YYYY-MM-DD">'
        )
    if type_code == "dateTime":
        return (
            f'<input type="text" {common_attrs}{maxlen_attr} '
            f'placeholder="YYYY-MM-DDThh:mm:ss">'
        )
    if type_code == "time":
        return (
            f'<input type="text" {common_attrs}{maxlen_attr} '
            f'placeholder="hh:mm:ss">'
        )

    # Decimal → text (not number, for IE8)
    if type_code == "decimal":
        return f'<input type="text" {common_attrs}{maxlen_attr} placeholder="0.00">'

    # Default text
    return f'<input type="text" {common_attrs}{maxlen_attr}>'


def _render_amount_with_currency(
    field: dict,
    prefix: str,
    field_path: str,
    form_name: str,
    iso_path: str,
    xml_tag: str,
    name_en: str,
    name_zh: str,
    mult_min: int,
    max_length: int,
) -> str:
    """Render amount field with inline currency selector (IE8 compatible)."""
    is_required = mult_min >= 1
    state_class = "field-required" if is_required else "field-editable"
    req_mark = _required_mark(mult_min)
    decimal_fd = field.get("decimal_fd", 5)
    step = "0." + "0" * (decimal_fd - 1) + "1" if decimal_fd > 0 else "0.01"

    ccy_options = '<option value="">币种</option>'
    for ccy in ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "HKD", "CNY"]:
        ccy_options += f'<option value="{ccy}">{ccy}</option>'

    ccy_name = f"{form_name}_CCY"

    label_html = (
        f'<label class="control-label" for="{html.escape(form_name)}">\n'
        f"    {html.escape(name_zh)} "
        f'<span class="en">{html.escape(name_en)} ({html.escape(xml_tag)})</span>\n'
        f"    {req_mark}\n"
        f"  </label>"
    )

    return (
        f'<div class="field-group {state_class}" '
        f'data-iso-path="{html.escape(iso_path)}" '
        f'data-form-name="{html.escape(form_name)}" '
        f'data-required="{"true" if is_required else "false"}">\n'
        f"  {label_html}\n"
        f'  <div class="amount-row">\n'
        f'    <select class="ccy-select" '
        f'name="{html.escape(ccy_name)}" '
        f'data-prefix="{html.escape(prefix)}" data-tag="Ccy">\n'
        f"      {ccy_options}\n"
        f"    </select>\n"
        f'    <div class="amt-input">\n'
        f'      <input type="text" class="form-control" '
        f'id="{html.escape(form_name)}" '
        f'name="{html.escape(form_name)}" '
        f'data-prefix="{html.escape(prefix)}" '
        f'data-tag="{html.escape(xml_tag)}" '
        f'data-iso-path="{html.escape(iso_path)}" '
        f'data-form-name="{html.escape(form_name)}" '
        f'data-type-code="decimal" '
        f'placeholder="0.00">\n'
        f"    </div>\n"
        f"  </div>\n"
        f'  <div class="amount-display" style="display:none"></div>\n'
        f'  <div class="hint">金额精度 / Precision: 最多{decimal_fd}位小数</div>\n'
        f'  <div class="error-msg"></div>\n'
        f''
        f"</div>"
    )


def _render_leaf(
    field: dict,
    prefix: str,
    field_path: str,
    form_name: str,
    iso_path: str,
    xml_tag: str,
    name_en: str,
    name_zh: str,
    type_code: str,
    mult_min: int,
    mult_max: int,
    regex_pattern: str,
    max_length: int,
    is_fixed: bool,
    fixed_value: str,
    code_values: list,
) -> str:
    """Render a leaf field (no children) as a field-group div."""
    # Repeatable leaf field (mult_max > 1) → render as repeat-leaf group
    if mult_max > 1 and not is_fixed:
        return _render_repeat_leaf(
            field, prefix, field_path, form_name, iso_path,
            xml_tag, name_en, name_zh, type_code,
            mult_min, mult_max, regex_pattern, max_length,
            code_values,
        )

    is_required = mult_min >= 1
    state_class = "field-required" if is_required else "field-editable"
    if is_fixed:
        state_class = "field-readonly"

    req_mark = _required_mark(mult_min)
    max_disp = _mult_display(mult_max)

    input_html = _build_input_html(
        form_name, prefix, xml_tag, iso_path, type_code,
        max_length, is_fixed, fixed_value, code_values,
    )

    label_html = (
        f'<label class="control-label" for="{html.escape(form_name)}">\n'
        f"    {html.escape(name_zh)} "
        f'<span class="en">{html.escape(name_en)} ({html.escape(xml_tag)})</span>\n'
        f"    {req_mark}\n"
        f'    <span class="mult-tag">[{mult_min}..{max_disp}]</span>\n'
        f"  </label>"
    )

    hint_html = ""
    if regex_pattern:
        hint_html = f'<div class="hint">格式 / Format: {html.escape(regex_pattern)}</div>'
    elif max_length > 0:
        hint_html = f'<div class="hint">最大长度 / Max: {max_length}</div>'

    return (
        f'<div class="field-group {state_class}" '
        f'data-iso-path="{html.escape(iso_path)}" '
        f'data-form-name="{html.escape(form_name)}" '
        f'data-required="{"true" if is_required else "false"}">\n'
        f"  {label_html}\n"
        f"  {input_html}\n"
        f"  {hint_html}\n"
        f'  <div class="error-msg"></div>\n'
        f''
        f"</div>"
    )


def _render_container(
    field: dict,
    prefix: str,
    field_path: str,
    form_name: str,
    iso_path: str,
    mult_min: int,
    mult_max: int,
    is_fixed: bool,
    fixed_value: str,
) -> str:
    """Render a container field (has children) as a Bootstrap panel or repeat group."""
    name_en = field.get("name_en", "")
    name_zh = field.get("name_zh", name_en)
    xml_tag = field.get("xml_tag", "")
    children = field.get("children", [])

    # Bug 6 fix: parent nodes without explicit multiplicity should be mandatory
    if not field.get("multiplicity", "") and children:
        mult_min = 1

    parent_tag = field_path.split("_")[-2] if "_" in field_path else ""

    # --- Component detection: emit placeholder for lazy rendering ---
    comp_type = detect_component_type(field)
    if comp_type and mult_max <= 1:
        return _render_component_placeholder(
            comp_type, form_name, name_en, name_zh, mult_min, is_fixed, fixed_value,
        )

    # Render children
    children_html = _render_children(children, prefix, field_path, xml_tag)

    badge = _badge_html(mult_min, is_fixed, fixed_value)

    # Repeatable container (mult_max > 1)
    if mult_max > 1 and not is_fixed:
        return _render_repeat_group(
            form_name, name_en, name_zh, mult_min, mult_max,
            children_html,
        )

    # Standard collapsible panel
    collapse_id = f"collapse_{form_name}"
    collapsed_in = "in" if mult_min >= 1 else ""
    heading_class = "" if mult_min >= 1 else " collapsed"

    return (
        f'<div class="panel panel-default">\n'
        f'  <div class="panel-heading{heading_class}" data-toggle="collapse" '
        f'data-target="#{collapse_id}">\n'
        f'    <h4 class="panel-title">\n'
        f"      {html.escape(name_zh)} / {html.escape(name_en)} {badge}\n"
        f'      <span class="toggle-icon">&#9660;</span>\n'
        f"    </h4>\n"
        f"  </div>\n"
        f'  <div id="{collapse_id}" class="panel-body collapse {collapsed_in}">\n'
        f"    {children_html}\n"
        f"  </div>\n"
        f"</div>"
    )


def _render_component_placeholder(
    comp_type: str,
    form_name: str,
    name_en: str,
    name_zh: str,
    mult_min: int,
    is_fixed: bool,
    fixed_value: str,
) -> str:
    """Render a component instance as a collapsed placeholder panel for lazy rendering."""
    badge = _badge_html(mult_min, is_fixed, fixed_value)
    collapse_id = f"collapse_{form_name}"

    return (
        f'<div class="panel panel-default">\n'
        f'  <div class="panel-heading collapsed" data-toggle="collapse" '
        f'data-target="#{collapse_id}">\n'
        f'    <h4 class="panel-title">\n'
        f"      {html.escape(name_zh)} / {html.escape(name_en)} {badge}\n"
        f'      <span class="toggle-icon">&#9660;</span>\n'
        f"    </h4>\n"
        f"  </div>\n"
        f'  <div id="{collapse_id}" class="panel-body collapse"\n'
        f'       data-component="{html.escape(comp_type)}"\n'
        f'       data-path-prefix="{html.escape(form_name)}"\n'
        f'       data-rendered="false">\n'
        f'    <div class="component-placeholder text-muted">'
        f'展开加载 / Expand to load</div>\n'
        f"  </div>\n"
        f"</div>"
    )


def _render_repeat_group(
    form_name: str,
    name_en: str,
    name_zh: str,
    mult_min: int,
    mult_max: int,
    children_html: str,
) -> str:
    """Render a repeatable container as a repeat-group panel."""
    max_disp = _mult_display(mult_max)
    repeat_id = f"repeat_{form_name}"

    # Always render one template item; hide it when min=0
    hide_style = ' style="display:none"' if mult_min == 0 else ""
    template_class = " repeat-template" if mult_min == 0 else ""

    return (
        f'<div class="repeat-group panel panel-default" id="{repeat_id}" '
        f'data-repeat-group="{repeat_id}" data-min="{mult_min}" data-max="{mult_max}">\n'
        f'  <div class="panel-heading">\n'
        f"    <span>{html.escape(name_zh)} / {html.escape(name_en)}</span>\n"
        f'    <span class="label label-default">[{mult_min}..{max_disp}]</span>\n'
        f'    <button type="button" class="btn btn-xs btn-primary btn-repeat-add pull-right">'
        f"+ 添加</button>\n"
        f"  </div>\n"
        f'  <div class="panel-body repeat-items" id="{repeat_id}_items">\n'
        f'    <div class="repeat-item{template_class}" data-index="1"{hide_style}>\n'
        f'      <span class="repeat-index">第1条</span>\n'
        f'      <button type="button" class="btn btn-xs btn-danger btn-repeat-remove">'
        f"×</button>\n"
        f"      {children_html}\n"
        f"    </div>\n"
        f"  </div>\n"
        f"</div>"
    )


def _render_repeat_leaf(
    field: dict,
    prefix: str,
    field_path: str,
    form_name: str,
    iso_path: str,
    xml_tag: str,
    name_en: str,
    name_zh: str,
    type_code: str,
    mult_min: int,
    mult_max: int,
    regex_pattern: str,
    max_length: int,
    code_values: list,
) -> str:
    """Render a repeatable leaf field (mult_max > 1, no children) as a repeat-group."""
    max_disp = _mult_display(mult_max)
    repeat_id = f"repeat_{form_name}"

    input_html = _build_input_html(
        form_name, prefix, xml_tag, iso_path, type_code,
        max_length, False, "", code_values,
    )

    hint_html = ""
    if regex_pattern:
        hint_html = f'<div class="hint">格式 / Format: {html.escape(regex_pattern)}</div>'
    elif max_length > 0:
        hint_html = f'<div class="hint">最大长度 / Max: {max_length}</div>'

    item_html = (
        f'<div class="field-group field-editable" '
        f'data-iso-path="{html.escape(iso_path)}" '
        f'data-form-name="{html.escape(form_name)}" '
        f'data-required="false">\n'
        f"        {input_html}\n"
        f"        {hint_html}\n"
        f'        <div class="error-msg"></div>\n'
        f"      </div>"
    )

    # Always render one template item; hide it when min=0
    hide_style = ' style="display:none"' if mult_min == 0 else ""
    template_class = " repeat-template" if mult_min == 0 else ""

    return (
        f'<div class="repeat-group repeat-leaf panel panel-default" id="{repeat_id}" '
        f'data-repeat-group="{repeat_id}" data-min="{mult_min}" data-max="{mult_max}">\n'
        f'  <div class="panel-heading">\n'
        f"    <span>{html.escape(name_zh)} / {html.escape(name_en)}</span>\n"
        f'    <span class="label label-default">[{mult_min}..{max_disp}]</span>\n'
        f'    <button type="button" class="btn btn-xs btn-primary btn-repeat-add pull-right">'
        f"+ 添加</button>\n"
        f"  </div>\n"
        f'  <div class="panel-body repeat-items" id="{repeat_id}_items">\n'
        f'    <div class="repeat-item{template_class}" data-index="1"{hide_style}>\n'
        f'      <span class="repeat-index">第1条</span>\n'
        f'      <button type="button" class="btn btn-xs btn-danger btn-repeat-remove">'
        f"×</button>\n"
        f"      {item_html}\n"
        f"    </div>\n"
        f"  </div>\n"
        f"</div>"
    )


def _render_children(
    children: list,
    prefix: str,
    parent_path: str,
    parent_tag: str,
) -> str:
    """Render a list of child fields, applying rule filters.

    Consecutive leaf fields are grouped into pairs, each pair wrapped in a
    .field-grid container for two-column float layout. This prevents float
    height issues where unequal field heights cause misalignment.
    Container fields (panels) break the grid.
    """
    parts: list[str] = []
    leaf_buffer: list[str] = []

    def flush_leaves():
        # Group leaves into pairs (max 2 per .field-grid row)
        for i in range(0, len(leaf_buffer), 2):
            pair = leaf_buffer[i:i + 2]
            parts.append('<div class="field-grid">\n' + "\n".join(pair) + "\n</div>")
        leaf_buffer.clear()

    for child in children:
        if should_remove_field(child, parent_tag):
            continue
        if child.get("is_attribute", False):
            continue

        child_html = render_field_html(child, prefix, parent_path)
        if not child_html.strip():
            continue

        # Amount+currency combos render as leaf-like field-groups
        is_amount_combo = (
            child.get("children")
            and child.get("type_code") == "decimal"
            and any(c.get("xml_tag") == "Ccy" for c in child.get("children", []))
        )
        # Repeatable leaf fields render as repeat-group panels (full width)
        child_mult_max = child.get("mult_max", 1)
        is_repeat_leaf = (
            not child.get("children")
            and child_mult_max > 1
            and not child.get("is_fixed", False)
        )
        is_leaf = (not child.get("children") or is_amount_combo) and not is_repeat_leaf
        if is_leaf:
            leaf_buffer.append(child_html)
        else:
            flush_leaves()
            parts.append(child_html)

    flush_leaves()
    return "\n".join(parts)
