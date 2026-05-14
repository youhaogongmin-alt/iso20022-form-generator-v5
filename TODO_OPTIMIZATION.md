# 页面体积优化方案

## 问题背景

v4 表单需要嵌入业务系统，当前页面体积偏大：

| 资源 | 大小 | 说明 |
|------|------|------|
| index.html | 1.03 MB | 813个input、305个panel、13564行 |
| fieldMeta.js | 551 KB | 1195条元数据 |
| app.js | 75 KB | 应用逻辑 |
| appConfig.js | 24 KB | 配置 |
| app.css | 19 KB | 样式 |
| **合计** | **1.68 MB** | 不含 vendor（jQuery+Bootstrap） |

## 根本原因：结构重复

PDF 规范本身以内联方式展开所有数据类型，parse_pdf.py 忠实复制了这种重复。

### 完整组件清单（非重叠顶层统计）

| 组件 | 实例数 | 叶子/实例 | 总叶子 | 占比 | 结构一致性 |
|------|--------|----------|--------|------|-----------|
| **PartyIdentification** | 9 | 29 | 261 | 32.1% | 完全一致 |
| **FinInstnId (完整版)** | 12 | 20 | 240 | 29.5% | 完全一致 |
| **Account** | 14 | 12 | 168 | 20.6% | 完全一致 |
| FinInstnId (精简版) | 2 | 4 | 8 | 1.0% | — |
| **可组件化合计** | **35** | — | **669** | **82.2%** | — |
| 剩余独立字段 | — | — | 145 | 17.8% | — |

### 组件内部结构

**PartyIdentification (9x, 29叶子)** — 出现在: UltmtDbtr, InitgPty, Dbtr, Cdtr, UltmtCdtr, Invcr, Invcee, Grnshee, GrnshmtAdmstr
```
├── Nm (名称)
├── PstlAdr (邮政地址, 15叶子)
│   ├── Dept, SubDept, StrtNm, BldgNb, BldgNm, Flr
│   ├── PstBx, Room, PstCd, TwnNm, TwnLctnNm
│   ├── DstrctNm, CtrySubDvsn, Ctry, AdrLine
├── Id (身份标识)
│   ├── OrgId (组织标识, 5叶子)
│   │   ├── AnyBIC, LEI
│   │   └── Othr [0..2] → Id, SchmeNm/Cd, Issr
│   └── PrvtId (个人标识, 7叶子)
│       ├── DtAndPlcOfBirth → BirthDt, PrvcOfBirth, CityOfBirth, CtryOfBirth
│       └── Othr [0..2] → Id, SchmeNm/Cd, Issr
└── CtryOfRes (居住国)
```

**FinInstnId-完整版 (12x, 20叶子)** — 出现在: InstgRmbrsmntAgt, InstdRmbrsmntAgt, ThrdRmbrsmntAgt, ChrgsInf/Agt, PrvsInstgAgt1/2/3, IntrmyAgt1/2/3, DbtrAgt, CdtrAgt
```
├── BICFI
├── ClrSysMmbId (清算系统成员标识, 2叶子)
│   ├── ClrSysId/Cd
│   └── MmbId
├── LEI
├── Nm (名称)
└── PstlAdr (邮政地址, 15叶子) — 同上
```

**Account (14x, 12叶子)** — 出现在: SttlmAcct, InstgRmbrsmntAgtAcct, InstdRmbrsmntAgtAcct, ThrdRmbrsmntAgtAcct, PrvsInstgAgt1/2/3Acct, IntrmyAgt1/2/3Acct, DbtrAcct, DbtrAgtAcct, CdtrAgtAcct, CdtrAcct
```
├── Id (账户标识)
│   ├── IBAN
│   └── Othr → Id, SchmeNm(Cd+Prtry), Issr
├── Tp (类型) → Cd, Prtry
├── Ccy (币种)
├── Nm (名称)
└── Prxy (代理标识)
    ├── Tp → Cd, Prtry
    └── Id
```

### 其他重复子结构（已包含在上述组件内）

| 子组件 | 实例数 | 叶子 | 说明 |
|--------|--------|------|------|
| PstlAdr | 21 | 15 | 9个在Party内 + 12个在FinInstnId内 |
| Othr (Id+SchmeNm+Issr) | 32 | 3 | 分布在Account/OrgId/PrvtId内 |
| Tp (Cd+Prtry) | 32 | 2 | Choice组，分布在各处 |
| ClrSysMmbId | 14 | 2 | 全部在FinInstnId内 |
| Prxy (Tp+Id) | 14 | 3 | 全部在Account内 |
| DtAndPlcOfBirth | 9 | 4 | 全部在Party/PrvtId内 |
| OrgId (AnyBIC+LEI+Othr) | 9 | 5 | 全部在Party/Id内 |
| PrvtId (DtAndPlcOfBirth+Othr) | 9 | 7 | 全部在Party/Id内 |

## 优化方案

### 方案A：模板化渲染

**思路：** 将重复组件抽为 JS 模板，HTML 中只放占位符。

实现：
1. 定义 3 个顶层组件模板（PartyIdentification、FinInstnId、Account）为 JS 对象
2. HTML 中输出 `<div data-component="PartyIdentification" data-path="DOC_..._Dbtr">`
3. JS 初始化时根据模板 + path 动态生成 DOM

预估效果：
- HTML: 1.03MB → ~183KB（-82%）
- fieldMeta: 可改为模板定义 + 实例路径映射
- 首屏 input 数量: 813 → ~179

### 方案B：按需加载（懒渲染）

**思路：** 首屏只渲染折叠的 panel 标题，展开时才渲染内部字段。

实现：
1. 首屏输出所有 panel-heading，panel-body 为空
2. 用户点击展开时，从预存的 HTML 片段或 JS 模板渲染内容
3. repeat-group 的"添加"操作从模板克隆（已有此逻辑）

预估效果：
- 首屏 DOM 节点: ~3000 → ~200
- 首屏渲染时间大幅缩短
- 总体积不变，但感知性能提升

### 方案C：A+B 结合（推荐）

**思路：** 模板化 + 懒渲染，最大化优化。

实现：
1. parse_pdf.py 输出 schema 时标记组件类型（新增 `component_type` 字段）
2. field_renderer.py 对已知组件只输出占位 div（含 data-component + data-path）
3. form_app.py 新增 Module: Component Renderer
   - 维护 3 个组件模板的 HTML 生成函数
   - panel 展开时检查是否有未渲染的组件占位符，动态渲染
   - 渲染后注册到 fieldMeta 和验证系统
4. fieldMeta.js 拆分为：
   - 模板字段定义（3个模板 × 各自叶子数 = ~61条）
   - 实例映射表（35个实例 × 组件类型 + 路径前缀）
   - 独立字段（~526条）

预估效果：
- HTML: 1.03MB → ~183KB（-82%）
- fieldMeta: 551KB → ~120KB（-78%）
- 首屏 DOM: ~3000 → ~200
- 总传输: 1.68MB → ~450KB（-73%）

### IE8 兼容性评估

| 技术点 | IE8 可行性 |
|--------|-----------|
| jQuery clone + innerHTML | 正常工作 |
| 动态生成 form_name | 字符串拼接，无兼容问题 |
| 事件委托 (document.on) | 已在用，无需改动 |
| JSON 模板数据 | json2 polyfill 已引入 |

### 需要调整的现有逻辑

| 模块 | 影响 |
|------|------|
| 验证 (Module 5) | 需支持动态注册的字段 |
| 进度条 (Module 3) | 需在组件渲染后重新计算 |
| 搜索定位 (Module 4) | 需先渲染目标组件再定位 |
| 数据收集/导出 (Module 7) | 需遍历已渲染 DOM 或维护数据模型 |
| Draft 自动保存 (Module 11) | 需保存未渲染组件的数据 |
| Choice 互斥 (Module 9) | 组件内部的 Choice 需在渲染后初始化 |

## 实施建议

1. 优先实施方案B（懒渲染），改动最小，效果明显
2. 在方案B基础上逐步引入方案A（模板化），进一步压缩体积
3. 模板化优先级：PartyIdentification(32.1%) > FinInstnId(29.5%) > Account(20.6%)

---

## 跨报文复用设计

### ISO 20022 数据类型的复用特性

ISO 20022 的数据类型体系是标准化的，同一数据类型在所有报文家族中结构完全相同：

| 数据类型 | XML标签 | 复用的报文 |
|---------|---------|-----------|
| PostalAddress24 | PstlAdr | pacs.008/009/004, camt.053/054/056, pain.001/002, sese.* |
| PartyIdentification135 | Dbtr/Cdtr/... | pacs.008/009/004, pain.001/002, camt.053/054/056/057 |
| FinancialInstitutionIdentification18 | FinInstnId | pacs.008/009/004/002/028, camt.053/054/056/057/029 |
| CashAccount38/40 | DbtrAcct/CdtrAcct/... | pacs.008/009/004, pain.001/002, camt.053/054/056 |
| GenericOrganisationIdentification1 | OrgId/Othr | pacs.008/009, pain.001, camt.053/054 |
| GenericPersonIdentification1 | PrvtId/Othr | pacs.008/009, pain.001, camt.053/054 |
| ProxyAccountIdentification1 | Prxy | pacs.008/009, pain.001 |
| ClearingSystemMemberIdentification2 | ClrSysMmbId | pacs.008/009/004/002/028 |
| DateAndPlaceOfBirth1 | DtAndPlcOfBirth | pacs.008/009, pain.001, camt.053/054 |
| RemittanceInformation16 | RmtInf | pacs.008/009, pain.001 |
| StructuredRemittanceInformation16 | Strd | pacs.008/009, pain.001 |
| RegulatoryReporting3 | RgltryRptg | pacs.008/009, pain.001 |

### 架构设计：通用层 + 差异层

```
┌─────────────────────────────────────────────────────────┐
│  组件模板（通用层）— 一次开发，所有报文复用              │
│                                                         │
│  PostalAddress / PartyId / FinInstnId / Account         │
│  定义「超集」结构，包含所有可能的字段                    │
└─────────────────────────────────────────────────────────┘
                          ×
┌─────────────────────────────────────────────────────────┐
│  报文配置（差异层）— 由 parse_rules_pdf.py 自动提取     │
│                                                         │
│  removed_elements:     哪些字段隐藏                     │
│  mandatory_overrides:  哪些字段必填                     │
│  type_changes:         字段长度/类型覆盖                │
│  multiplicity:         重复度覆盖                       │
│  choice_groups:        互斥组                           │
└─────────────────────────────────────────────────────────┘
```

### 不同报文间的差异示例

| 差异点 | pacs.008 (CBPR+) | pain.001 | camt.053 |
|--------|-----------------|----------|----------|
| BranchId | 移除 | 保留 | 保留 |
| Othr 重复度 | [0..2] | [0..*] | [0..*] |
| Party/Name maxLength | 140 | 70 | 140 |
| FinInstnId/Name | 保留 | 保留 | 可能移除 |
| SchmeNm/Prtry | 移除 | 保留 | 保留 |
| Proxy | 保留 | 保留 | 无 |

### 组件模板渲染逻辑

```javascript
// 组件模板定义（超集）
var COMPONENT_TEMPLATES = {
  PostalAddress: {
    fields: ["Dept","SubDept","StrtNm","BldgNb","BldgNm","Flr",
             "PstBx","Room","PstCd","TwnNm","TwnLctnNm",
             "DstrctNm","CtrySubDvsn","Ctry","AdrLine"],
    // 默认属性，可被报文配置覆盖
    defaults: { AdrLine: { mult_max: 7 } }
  },
  FinInstnId: {
    fields: ["BICFI","ClrSysMmbId","LEI","Nm","PstlAdr"],
    children: { ClrSysMmbId: ["ClrSysId/Cd","MmbId"], PstlAdr: "$PostalAddress" }
  },
  // ...
};

// 渲染时：模板 + 路径前缀 + 报文配置 → DOM
function renderComponent(type, pathPrefix, overrides) {
  var tpl = COMPONENT_TEMPLATES[type];
  var html = "";
  for (var i = 0; i < tpl.fields.length; i++) {
    var field = tpl.fields[i];
    if (overrides.removed && overrides.removed.indexOf(field) !== -1) continue;
    // ... 根据 overrides 调整 mult_min, max_length 等
    html += buildFieldHtml(field, pathPrefix, overrides);
  }
  return html;
}
```

### 支持新报文的流程

```
1. 获取新报文的 Usage Guideline PDF + Combined Rules PDF
2. python scripts/generate_form.py <usage.pdf> --rules-pdf <combined.pdf>
3. 组件模板零改动，自动复用
4. 差异由 rules.json 驱动（removed/mandatory/type_changes）
```

### 预期覆盖范围

| 报文家族 | 典型报文 | 组件复用率（预估） |
|---------|---------|------------------|
| pacs (支付清算) | pacs.008, pacs.009, pacs.004, pacs.002 | 80-85% |
| pain (支付发起) | pain.001, pain.002 | 75-80% |
| camt (现金管理) | camt.053, camt.054, camt.056, camt.029 | 70-75% |
| sese (证券结算) | sese.023, sese.024 | 60-65% |

组件复用率越高，新报文的开发成本越低——只需处理该报文特有的顶层结构和业务字段。
