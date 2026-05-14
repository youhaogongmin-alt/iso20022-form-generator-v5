# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Build & Run

```bash
# 标准流程：解析 PDF → 翻译 → 生成表单
python scripts/generate_form.py dev/input/pacs.008/structure.pdf \
  --rules-pdf dev/input/pacs.008/rules.pdf
python scripts/translate_schema.py output/pacs.008.001.08.json
python scripts/generate_form.py --schema output/pacs.008.001.08.json

# 快速生成（跳过翻译，英文字段名）
python scripts/generate_form.py dev/input/pacs.008/structure.pdf \
  --rules-pdf dev/input/pacs.008/rules.pdf
```

No test framework exists. Verify by opening output in a browser and checking key features.

## Input Files

- `dev/input/<msg>/structure.pdf` — CompactPDF (8列, parse_pdf.py 解析字段结构)
- `dev/input/<msg>/rules.pdf` — PlainPDF (7列, parse_rules_pdf.py 解析互斥/移除规则)
- 目录名含变体时自动识别: `pacs.008.stp/` → variant=stp

## Architecture

**Pipeline: PDF → Schema JSON → [AI translate] → HTML Form**

```
structure.pdf → parse_pdf.py ──→ schema.json → generate_form.py --schema → HTML
rules.pdf → parse_rules_pdf.py ↗      ↑
                                  AI fills name_zh
```

### Script Roles

| Script | Role |
|--------|------|
| `parse_pdf.py` | 解析 CompactPDF 提取字段树 (Level/Type/Mult) |
| `parse_rules_pdf.py` | 解析 PlainPDF 提取规则 (Or互斥/移除/必填) |
| `generate_form.py` | CLI 入口，支持 `--schema` 和 `--rules-pdf` |
| `translate_schema.py` | AI 翻译步骤示例（补全 name_zh） |
| `form_page.py` | 页面组装、fieldMeta/appConfig 生成 |
| `field_renderer.py` | 字段/面板 HTML 渲染（含组件懒渲染占位） |
| `form_app.py` | app.js 生成（ES5, 15个模块含 Component Renderer） |
| `form_rules.py` | CBPR+ 规则常量、默认互斥组、组件签名 |
| `form_css.py` | app.css 生成（IE8 兼容双主题） |
| `form_api.py` | 浏览器端 Form API |

### Output Structure

```
output/
├── pacs.008.001.08.json                    ← schema
└── form/
    ├── pacs_008_001_08.html                ← 报文页面
    ├── js/app.js                           ← 共享逻辑
    ├── js/<safe_name>_fieldMeta.js         ← 报文字段元数据
    ├── js/<safe_name>_appConfig.js         ← 报文配置
    ├── js/vendor/                          ← jQuery, Bootstrap, polyfills
    └── css/                                ← 共享样式
```

### Key Data Structures

- **Schema JSON**: hierarchical field tree with `message_id`, `app_hdr_fields`, `document_fields`, `choice_groups`
- **COMPONENT_TEMPLATES** (JS): 3 个懒渲染组件模板 (Account/FinInstnId/PartyIdentification)
- **COMPONENT_INSTANCES** (JS): 35 个组件实例映射 (pathPrefix + overrides)
- **FIELD_META** (JS): 独立字段元数据
- **appConfig.js**: 运行时配置 (templates, quick-fill, field state overrides)

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
- DEFAULT_CHOICE_GROUPS: OrgId/PrvtId, IBAN/Othr, Cd/Prtry 互斥兜底

## Conventions

- All UI text uses I18N dict (Chinese/English/French) — never hardcode display strings
- Field naming: `DOC_Parent_Child_Leaf` or `AH_Parent_Child_Leaf` prefix path
- Collapsible sections use Bootstrap 3 panels with `collapse in` for expanded, `collapse` for collapsed
- Progress logic uses `.panel-all-optional` class (tagged at init) to exclude unused optional sections
- Repeating groups use `data-repeat-group` attribute with add/remove buttons
- Generated HTML must work on `file://` protocol (no fetch for critical resources)
- Component lazy rendering: `data-component` + `data-path-prefix` + `show.bs.collapse` trigger
