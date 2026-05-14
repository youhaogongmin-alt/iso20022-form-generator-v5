---
name: iso20022-form-generator
description: Generate IE8-compatible interactive HTML forms from ISO 20022 CBPR+ usage guideline PDFs. Supports multiple message types (pacs/camt/pain) with variants (STP/ADV/COV), Chinese translation via AI, and lazy-rendered component architecture.
---

# ISO 20022 Form Generator v5

将 CBPR+ Usage Guideline PDF 转换为 IE8+ 兼容的交互式 HTML 表单。支持多报文类型、变体识别、AI 中文翻译。

## Quick Start

```bash
# 完整流程（解析 + 翻译 + 生成）
python scripts/generate_form.py dev/input/pacs.008/structure.pdf \
  --rules-pdf dev/input/pacs.008/rules.pdf
python scripts/translate_schema.py output/pacs.008.001.08.json
python scripts/generate_form.py --schema output/pacs.008.001.08.json
```

## Input File Organization

```
dev/input/
├── pacs.008/
│   ├── structure.pdf    ← CompactPDF (parse_pdf.py 解析字段结构)
│   └── rules.pdf        ← PlainPDF (parse_rules_pdf.py 解析互斥/移除规则)
├── pacs.008.stp/        ← STP 变体 (variant 从目录名自动推断)
│   ├── structure.pdf
│   └── rules.pdf
├── pacs.009/
├── pacs.009.adv/
└── pacs.009.cov/
```

**structure.pdf** = MyStandards **CompactPDF** 导出
- ~108页, 8列: Index | Lvl | Name | XML Tag | Mult | Type/Code | Restr | Additional details
- 提供: 字段层级、类型、长度、正则、Type Changed

**rules.pdf** = MyStandards **PlainPDF** 导出
- ~366页, 7列: Index | Message Item | \<XML Tag\> | Or | Mult. | Usage Guidelines | Page
- 提供: Or 列互斥关系、Usage Guidelines 移除/必填标记、规则详情页引用

## Workflow

### 标准流程（含 AI 翻译）

1. 用户提供 PDF 文件路径（可以是原始文件名）
2. **归档 PDF**：从文件名解析报文类型和变体，自动创建目录并复制重命名:
   - 文件名格式: `CBPRPlus_SR2026_(Combined)_CBPRPlus-<msg_id>_[<variant>_]<name>_<date>.pdf`
   - 解析规则:
     - `pacs_008_001_08_FIToFICustomerCreditTransfer` → msg=`pacs.008`, variant=无
     - `pacs_008_001_08_STP_FIToFICustomerCreditTransfer` → msg=`pacs.008`, variant=`stp`
     - `pacs_009_001_08_ADV_FinancialInstitutionCreditTransfer` → msg=`pacs.009`, variant=`adv`
     - `pacs_009_001_08_COV_FinancialInstitutionCreditTransfer` → msg=`pacs.009`, variant=`cov`
   - 已知变体关键词: `STP`, `ADV`, `COV`, `MultipleCharges`
   - 目标目录: `dev/input/<msg_family>.<number>[.<variant>]/`
   - CompactPDF 来源 → 命名为 `structure.pdf`
   - PlainPDF 来源 → 命名为 `rules.pdf`
   - 判断方式: 用 pdfplumber 打开第一个表格页，8列=CompactPDF(structure)，7列=PlainPDF(rules)
3. 解析 PDF 生成 schema JSON（name_zh 为空）:
   ```bash
   python scripts/generate_form.py dev/input/<msg>/structure.pdf \
     --rules-pdf dev/input/<msg>/rules.pdf
   ```
4. 读取 `output/<message_id>.json`，补全所有空的 `name_zh` 字段（基于 ISO 20022 / SWIFT / CIPS 标准术语），写回 JSON
5. 从已翻译的 schema 生成表单:
   ```bash
   python scripts/generate_form.py --schema output/<message_id>.json
   ```
6. 打开 `output/form/<safe_name>.html` 验证

### 快速流程（跳过翻译）

```bash
python scripts/generate_form.py dev/input/<msg>/structure.pdf \
  --rules-pdf dev/input/<msg>/rules.pdf
# 直接打开 output/form/<safe_name>.html（缺少中文的字段显示英文）
```

## Output Structure

```
output/
├── pacs.008.001.08.json              ← schema (可被 AI 翻译后重新生成)
├── pacs.008.001.08_stp.json          ← STP 变体 schema
└── form/
    ├── pacs_008_001_08.html          ← 报文页面
    ├── pacs_008_001_08_stp.html      ← STP 变体页面
    ├── js/
    │   ├── app.js                    ← 共享应用逻辑
    │   ├── pacs_008_001_08_fieldMeta.js      ← 报文字段元数据
    │   ├── pacs_008_001_08_appConfig.js      ← 报文配置
    │   ├── pacs_008_001_08_stp_fieldMeta.js  ← 变体字段元数据
    │   └── vendor/                   ← jQuery 1.12.4, Bootstrap 3.4.1, polyfills
    └── css/                          ← 共享样式
        ├── app.css
        ├── bootstrap.min.css
        └── bootstrap-theme.min.css
```

## IE8+ Compatibility

- ES5 + jQuery 1.12.4（无箭头函数、模板字符串、Promise）
- CSS float 布局（无 flexbox/grid/var()）
- Bootstrap 3.4.1 面板/折叠/模态框
- IE 条件注释加载 polyfills: html5shiv, respond.js, es5-shim/sham, json2

## Architecture

```
structure.pdf → parse_pdf.py → schema.json → [AI translate name_zh] → generate_form.py → HTML
rules.pdf → parse_rules_pdf.py ↗                                        ↓
                                                              form_page.py + field_renderer.py
                                                              form_app.py + form_rules.py
```

### Key Scripts

| Script | Role |
|--------|------|
| `parse_pdf.py` | 解析 CompactPDF 提取字段树 (Level/Type/Mult) |
| `parse_rules_pdf.py` | 解析 PlainPDF 提取规则 (Or互斥/移除/必填/choice_groups) |
| `generate_form.py` | CLI 入口，支持 `--schema` 和 `--rules-pdf` |
| `translate_schema.py` | AI 翻译步骤示例（补全 name_zh） |
| `form_page.py` | 页面组装、fieldMeta/appConfig 生成 |
| `field_renderer.py` | 字段/面板 HTML 渲染（含组件懒渲染占位） |
| `form_app.py` | app.js 生成（ES5, 15个模块含 Component Renderer） |
| `form_rules.py` | CBPR+ 规则常量、默认互斥组、组件签名 |
| `form_css.py` | app.css 生成（IE8 兼容双主题） |
| `form_api.py` | 浏览器端 Form API |

### Component Lazy Rendering (v5 核心)

3 个 ISO 20022 标准数据类型组件化懒渲染，覆盖 82% 字段：
- **Account** (14实例 × 12叶子)
- **FinInstnId** (12实例 × 20叶子)
- **PartyIdentification** (9实例 × 29叶子)

HTML 只输出折叠占位面板，展开时通过 `show.bs.collapse` 事件触发 Module 15 动态渲染。

## Dependencies

```bash
python -m pip install pdfplumber
```

- Python 3.8+
- Frontend: jQuery 1.12.4, Bootstrap 3.4.1, IE polyfills (vendor/ 目录)
