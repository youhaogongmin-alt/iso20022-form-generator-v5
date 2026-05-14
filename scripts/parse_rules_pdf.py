"""Parse CBPR+ detailed rules PDF (Combined version) to extract all rule content.

Extracts from the Combined PDF:
- Message Components with Choice/OR groups (priority)
- Business rules (TextualRule / FormalRule)
- ISO 20022 Rules (R3, R6, R7, etc.)
- Removed elements
- Mandatory overrides
- Repeatability overrides
- Type changes
- Conditional presence rules
- Not-allowed values

Usage:
    python scripts/parse_rules_pdf.py <pdf_path> [--output <json_path>]
"""
from __future__ import annotations

import json
import re
import sys
from typing import List, Tuple

import pdfplumber


def parse_rules_pdf(pdf_path: str) -> dict:
    """Parse the Combined rules PDF and return structured rule data."""
    with pdfplumber.open(pdf_path) as pdf:
        message_id = _detect_message_id(pdf)
        pages = _extract_all_text(pdf)
        tables = _extract_all_tables(pdf)

    full_text = "\n".join(text for _, text in pages)

    choice_groups = _extract_choice_groups(tables, pages)
    business_rules = _extract_business_rules(full_text, message_id)
    iso_rules = _extract_iso_rules(pages)

    return {
        "message_id": message_id,
        "fixed_values": _extract_fixed_values(full_text),
        "business_rules": business_rules,
        "iso_rules": iso_rules,
        "choice_groups": choice_groups,
        "removed_elements": _extract_removed_elements(full_text),
        "mandatory_overrides": _extract_mandatory_overrides(full_text),
        "repeatability_overrides": _extract_repeatability_overrides(tables, pages),
        "type_changes": _extract_type_changes(full_text),
        "conditional_presence": _extract_conditional_presence(full_text),
        "not_allowed_values": _extract_not_allowed(full_text),
    }


# ==================== Core helpers ====================


def _detect_message_id(pdf) -> str:
    text = pdf.pages[0].extract_text() or ""
    m = re.search(
        r"((?:pacs|camt|pain|acmt|admi|auth|reda|semt|sese|setr|trea)"
        r"\.\d{3}\.\d{3}\.\d{2})",
        text,
    )
    return m.group(1) if m else "unknown"


def _extract_all_text(pdf) -> List[Tuple[int, str]]:
    """Return [(page_idx, text), ...] for all pages."""
    results = []
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        results.append((i, text))
    return results


def _extract_all_tables(pdf) -> List[Tuple[int, list]]:
    """Return [(page_idx, table_rows), ...] for all tables with standard headers."""
    results = []
    for i, page in enumerate(pdf.pages):
        for table in (page.extract_tables() or []):
            if not table or len(table) < 2:
                continue
            header = table[0]
            if not header or len(header) < 5:
                continue
            header_text = " ".join(str(c or "") for c in header)
            if "Message Item" in header_text or "XML Tag" in header_text:
                results.append((i, table))
    return results


def _get_component_name_for_page(page_idx: int, pages: List[Tuple[int, str]]) -> str:
    """Find the component section header (e.g. '5.1 AccountIdentification4Choice__1')
    on or before the given page."""
    for offset in range(0, 5):
        idx = page_idx - offset
        if idx < 0:
            break
        for pg_idx, text in pages:
            if pg_idx != idx:
                continue
            matches = re.findall(r'\d+\.\d+\s+([A-Z][a-zA-Z0-9]+(?:__\d+)?)', text)
            for name in reversed(matches):
                if len(name) > 10 and not name[0].islower():
                    return name
            if matches:
                return matches[-1]
    return ""


def _get_used_in(page_idx: int, pages: List[Tuple[int, str]]) -> List[str]:
    """Extract 'Used in element(s)' references from the page text."""
    for _, text in pages:
        if _ != page_idx:
            continue
        m = re.search(r'Used in element\(s\)\s*\n(.+?)(?:\n\d+\.\d+|\Z)', text, re.DOTALL)
        if m:
            refs = re.findall(r'"([^"]+)"\s+on\s+page\s+(\d+)', m.group(1))
            return [f"{name} on page {pg}" for name, pg in refs]
    return []


# ==================== Choice/OR Groups (Priority) ====================


def _extract_choice_groups(tables: list, pages: list) -> List[dict]:
    """Extract Choice/OR component groups from Message Component tables.

    Identifies {Or / Or} markers in the Or column (index 3).
    """
    groups = []
    seen = set()

    for page_idx, table in tables:
        if len(table) < 2:
            continue
        header = table[0]
        if not header or len(header) < 5:
            continue

        or_col_idx = -1
        for ci, cell in enumerate(header):
            if str(cell or "").strip() == "Or":
                or_col_idx = ci
                break
        if or_col_idx < 0:
            continue

        current_options = []
        in_choice = False

        for row in table[1:]:
            if not row or len(row) <= or_col_idx:
                continue
            or_val = str(row[or_col_idx] or "").strip()
            tag_val = re.sub(r'[<>]', '', str(row[2] or "").strip()) if len(row) > 2 else ""
            name_val = str(row[1] or "").strip() if len(row) > 1 else ""
            mult_val = str(row[4] or "").strip() if len(row) > 4 else ""

            if or_val.startswith("{Or"):
                in_choice = True
                current_options = []
                if tag_val:
                    current_options.append({
                        "tag": tag_val, "name": name_val, "mult": mult_val
                    })
            elif or_val.startswith("Or}") and in_choice:
                if tag_val:
                    current_options.append({
                        "tag": tag_val, "name": name_val, "mult": mult_val
                    })
                if len(current_options) >= 2:
                    comp_name = _get_component_name_for_page(page_idx, pages)
                    key = comp_name + "|" + ",".join(o["tag"] for o in current_options)
                    if key not in seen:
                        seen.add(key)
                        used_in = _get_used_in(page_idx, pages)
                        groups.append({
                            "component_name": comp_name,
                            "options": current_options,
                            "used_in": used_in,
                        })
                in_choice = False
                current_options = []
            elif in_choice and "Or" in or_val:
                if tag_val:
                    current_options.append({
                        "tag": tag_val, "name": name_val, "mult": mult_val
                    })

    return groups


# ==================== Business Rules ====================


def _extract_business_rules(full_text: str, message_id: str) -> List[dict]:
    """Extract CBPR_*_TextualRule and CBPR_*_FormalRule from Usage Guideline details."""
    rules = []

    pattern = re.compile(
        r'–\s+(CBPR_[A-Za-z0-9_]+_(TextualRule|FormalRule)):\s*\n(.*?)(?=\n\s*–\s+CBPR_|\n\d+\.\d+\.\d+\s|\nUsed in element|\n\d+\s+CBPRPlus)',
        re.DOTALL
    )
    path_pattern = re.compile(
        r'•\s+on\s+(' + re.escape(message_id) + r'/[^\n]+)'
    )

    chunks = re.split(r'(•\s+on\s+' + re.escape(message_id) + r'/[^\n]+)', full_text)

    current_path = ""
    for chunk in chunks:
        path_m = path_pattern.match(chunk)
        if path_m:
            current_path = path_m.group(1).strip()
            continue

        for m in pattern.finditer(chunk):
            rule_name = m.group(1)
            rule_type = m.group(2)
            rule_text = m.group(3).strip()
            rule_text = re.sub(r'\s+', ' ', rule_text)[:500]
            rules.append({
                "name": rule_name,
                "type": rule_type,
                "path": current_path,
                "text": rule_text,
            })

    if not rules:
        rules = _extract_business_rules_fallback(full_text, message_id)

    return rules


def _extract_business_rules_fallback(full_text: str, message_id: str) -> List[dict]:
    """Fallback: scan line by line for rule patterns."""
    rules = []
    lines = full_text.split('\n')
    current_path = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        path_m = re.match(r'\s*•\s+on\s+(' + re.escape(message_id) + r'/\S+)', line)
        if path_m:
            current_path = path_m.group(1).strip()
            i += 1
            continue

        rule_m = re.match(r'\s*[–\-]+\s+(CBPR_[A-Za-z0-9_]+_(TextualRule|FormalRule)):', line)
        if rule_m:
            rule_name = rule_m.group(1)
            rule_type = rule_m.group(2)
            text_lines = []
            i += 1
            while i < len(lines) and not re.match(r'\s*[–\-]+\s+CBPR_', lines[i]) and not re.match(r'\s*•\s+on\s+', lines[i]):
                if lines[i].strip():
                    text_lines.append(lines[i].strip())
                i += 1
                if len(text_lines) > 20:
                    break
            rule_text = ' '.join(text_lines)[:500]
            rules.append({
                "name": rule_name,
                "type": rule_type,
                "path": current_path,
                "text": rule_text,
            })
            continue
        i += 1
    return rules


# ==================== ISO 20022 Rules ====================


def _extract_iso_rules(pages: List[Tuple[int, str]]) -> List[dict]:
    """Extract R3, R6, R7... rules from the ISO 20022 Rules section."""
    rules = []
    iso_section_text = ""

    in_section = False
    for pg_idx, text in pages:
        if pg_idx < 5:
            continue
        if not in_section and re.search(r'3\s+ISO 20022 Rules', text):
            in_section = True
        if in_section:
            if re.search(r'4\s+Message Building Blocks', text):
                break
            iso_section_text += text + "\n"

    if not iso_section_text:
        return rules

    pattern = re.compile(
        r'(R\d+)\s+(\w+)\s*[^\n]*\n(.*?)(?=\nR\d+\s+\w|\Z)',
        re.DOTALL
    )

    for m in pattern.finditer(iso_section_text):
        rule_id = m.group(1)
        rule_name = m.group(2)
        body = m.group(3).strip()

        severity = ""
        error_code = ""
        sev_m = re.search(r'Error severity:\s*(\w+)', body)
        if sev_m:
            severity = sev_m.group(1)
        code_m = re.search(r'Error Code:\s*(\w+)', body)
        if code_m:
            error_code = code_m.group(1)

        rule_text = re.sub(r'Error handling:.*', '', body, flags=re.DOTALL).strip()
        rule_text = re.sub(r'\s+', ' ', rule_text)[:500]

        rules.append({
            "rule_id": rule_id,
            "name": rule_name,
            "text": rule_text,
            "severity": severity,
            "error_code": error_code,
        })

    return rules


# ==================== Removed Elements ====================


def _extract_removed_elements(full_text: str) -> List[str]:
    """Extract paths of removed elements."""
    pattern = re.compile(r'This element\(([^)]+)\) is removed\.')
    results = []
    seen = set()
    for m in pattern.finditer(full_text):
        path = m.group(1).strip()
        path = re.sub(r'\s+', '', path)
        path = path.replace('-\n', '').replace('\n', '')
        if path not in seen:
            seen.add(path)
            results.append(path)
    return results


# ==================== Mandatory Overrides ====================


def _extract_mandatory_overrides(full_text: str) -> List[dict]:
    """Extract elements that have been made mandatory."""
    results = []
    seen = set()
    lines = full_text.split('\n')
    i = 0
    while i < len(lines):
        if 'This element is now mandatory' in lines[i]:
            min_m = re.search(r'changed to\s*:\s*(\d+)', lines[i])
            min_occ = int(min_m.group(1)) if min_m else 1
            path_parts = []
            j = i - 1
            while j >= 0 and j >= i - 5:
                line = lines[j].strip()
                if line.startswith('•') or line.startswith('•'):
                    on_m = re.match(r'[••]\s+on\s+(.*)', line)
                    if on_m:
                        path_parts.insert(0, on_m.group(1))
                    break
                elif line and not line.startswith('–') and not line.startswith('Usage'):
                    path_parts.insert(0, line)
                else:
                    break
                j -= 1
            path = re.sub(r'[\s\-]+', '', ''.join(path_parts))
            if path and path not in seen:
                seen.add(path)
                results.append({"path": path, "min_occurrence": min_occ})
        i += 1
    return results


# ==================== Repeatability Overrides ====================


def _extract_repeatability_overrides(tables: list, pages: list) -> List[dict]:
    """Extract reduced multiplicity from Usage Guidelines column (R[x..y] pattern)."""
    results = []
    seen = set()

    for page_idx, table in tables:
        if len(table) < 2:
            continue
        header = table[0]
        if not header or len(header) < 6:
            continue

        usage_col_idx = -1
        mult_col_idx = -1
        for ci, cell in enumerate(header):
            cell_text = str(cell or "").strip().replace('\n', ' ')
            if "Usage" in cell_text or "Guidelines" in cell_text:
                usage_col_idx = ci
            if "Mult" in cell_text:
                mult_col_idx = ci

        if usage_col_idx < 0:
            continue

        comp_name = _get_component_name_for_page(page_idx, pages)

        for row in table[1:]:
            if not row or len(row) <= usage_col_idx:
                continue
            usage_val = str(row[usage_col_idx] or "").strip().replace('\n', ' ')
            r_match = re.search(r'R\[(\d+)\.\.(\d+)\]', usage_val)
            if not r_match:
                continue

            tag_val = re.sub(r'[<>]', '', str(row[2] or "").strip()) if len(row) > 2 else ""
            name_val = str(row[1] or "").strip() if len(row) > 1 else ""
            orig_mult = str(row[mult_col_idx] or "").strip() if mult_col_idx >= 0 and len(row) > mult_col_idx else ""

            restricted = f"[{r_match.group(1)}..{r_match.group(2)}]"
            key = f"{comp_name}|{tag_val}|{restricted}"
            if key not in seen:
                seen.add(key)
                results.append({
                    "component": comp_name,
                    "tag": tag_val,
                    "name": name_val,
                    "original": orig_mult,
                    "restricted": restricted,
                })

    return results


# ==================== Type Changes ====================


def _extract_type_changes(full_text: str) -> List[dict]:
    """Extract type change directives."""
    results = []
    pattern = re.compile(
        r'•\s+on\s+([^\n]+)\n\s*Type changed to:\s*(\S+)'
    )
    seen = set()
    for m in pattern.finditer(full_text):
        path = m.group(1).strip()
        target_type = m.group(2).strip()
        key = f"{path}|{target_type}"
        if key not in seen:
            seen.add(key)
            results.append({"path": path, "target_type": target_type})
    return results


# ==================== Fixed Values ====================


def _extract_fixed_values(full_text: str) -> List[dict]:
    """Extract fixed value assignments."""
    results = []
    pattern = re.compile(r'Single value:\s*["\']?([^"\'\n]+)["\']?')
    for m in pattern.finditer(full_text):
        value = m.group(1).strip()
        context = full_text[max(0, m.start() - 200):m.start()]
        tag_m = re.search(r'<(\w+)>', context[::-1])
        xml_tag = ""
        if tag_m:
            xml_tag = tag_m.group(1)[::-1]
        else:
            tag_m2 = re.search(r'XML Tag:\s*(\w+)', context)
            if tag_m2:
                xml_tag = tag_m2.group(1)
        if xml_tag and value:
            results.append({"xml_tag": xml_tag, "value": value})
    return results


# ==================== Conditional Presence ====================


def _extract_conditional_presence(full_text: str) -> List[dict]:
    """Extract conditional presence rules from formal rule definitions."""
    results = []

    pattern = re.compile(
        r'if\s+at least one occurrence of the following element\(s\)\s*'
        r'\[([^\]]+)\]\s+is \(are\) present\s+'
        r'then\s+at least one occurrence of the following element\(s\)\s*'
        r'\[([^\]]+)\]\s+must be present',
        re.DOTALL | re.IGNORECASE
    )

    for m in pattern.finditer(full_text):
        if_path = m.group(1).strip()
        then_path = m.group(2).strip()
        if_field = if_path.split('/')[-1] if '/' in if_path else if_path
        then_field = then_path.split('/')[-1] if '/' in then_path else then_path

        context_start = max(0, m.start() - 500)
        context = full_text[context_start:m.start()]
        ctx_m = re.search(r'For each \[([^\]]+)\]', context)
        context_path = ctx_m.group(1) if ctx_m else ""

        results.append({
            "context": context_path,
            "if_path": if_path,
            "then_path": then_path,
            "if_field": if_field,
            "then_field": then_field,
        })

    return _dedupe_conditional(results)


def _dedupe_conditional(items: List[dict]) -> List[dict]:
    """Remove duplicate conditional presence rules."""
    seen = set()
    deduped = []
    for item in items:
        key = f"{item['if_field']}|{item['then_field']}|{item['context']}"
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


# ==================== Not-Allowed Values ====================


def _extract_not_allowed(full_text: str) -> List[dict]:
    """Extract not-allowed value restrictions."""
    results = []

    pattern1 = re.compile(
        r"must have value not included in the following list\s+'([^']+)'((?:\s+or\s+'[^']+')*)"
    )
    for m in pattern1.finditer(full_text):
        values = [m.group(1)]
        extra = m.group(2)
        if extra:
            values.extend(re.findall(r"'([^']+)'", extra))

        context_start = max(0, m.start() - 300)
        context = full_text[context_start:m.start()]
        path_m = re.search(r'\[([^\]]+)\]', context[::-1])
        path = ""
        if path_m:
            path = path_m.group(1)[::-1]
        else:
            path_m2 = re.search(r'on\s+(pacs\.\d+\.\d+\.\d+/[^\n]+)', context)
            if path_m2:
                path = path_m2.group(1)

        results.append({"path": path, "values": values})

    pattern2 = re.compile(
        r'(?:codes?|values?)\s+((?:[A-Z]{3,4}(?:,\s*| and ))+[A-Z]{3,4})\s+(?:are|is) not allowed'
    )
    for m in pattern2.finditer(full_text):
        codes_str = m.group(1)
        values = re.findall(r'[A-Z]{3,4}', codes_str)
        if not values:
            continue

        context_start = max(0, m.start() - 300)
        context = full_text[context_start:m.start()]
        path_m = re.search(r'on\s+(pacs\.\d+\.\d+\.\d+/[^\n]+)', context)
        path = path_m.group(1) if path_m else ""

        results.append({"path": path, "values": values})

    return results


# ==================== CLI ====================


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_rules_pdf.py <pdf_path> [--output <json_path>]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    print(f"Parsing rules PDF: {pdf_path}")
    result = parse_rules_pdf(pdf_path)

    print(f"\nExtraction summary:")
    print(f"  Message ID: {result['message_id']}")
    print(f"  Fixed values: {len(result['fixed_values'])}")
    print(f"  Business rules: {len(result['business_rules'])}")
    print(f"  ISO rules: {len(result['iso_rules'])}")
    print(f"  Choice groups: {len(result['choice_groups'])}")
    print(f"  Removed elements: {len(result['removed_elements'])}")
    print(f"  Mandatory overrides: {len(result['mandatory_overrides'])}")
    print(f"  Repeatability overrides: {len(result['repeatability_overrides'])}")
    print(f"  Type changes: {len(result['type_changes'])}")
    print(f"  Conditional presence: {len(result['conditional_presence'])}")
    print(f"  Not-allowed values: {len(result['not_allowed_values'])}")

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to: {output_path}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
