# 待实现：高级跨字段验证规则

规则数据已通过 `--rules-pdf` 解析并传递到前端 `appConfig.js`，但 JS 验证逻辑尚未实现。

## 1. 条件存在性规则 (conditionalPresence)

数据位置：`appConfig.js` → `conditionalPresence` 数组

需实现的逻辑：
- Agent Name/PostalAddress 必须同时存在（18+ 个上下文）
- Party: 如果 PostalAddress 存在，Name 必填（Debtor, Creditor, UltimateDebtor, UltimateCreditor, InitiatingParty）
- Debtor: 如果 AnyBIC 不存在，Name 必填

## 2. 业务互斥规则 (businessRules)

数据位置：`appConfig.js` → `businessRules` 数组

需实现的逻辑：
- InstructionForCreditorAgent/Code: HOLD 和 CHQB 不能同时存在
- InstructionForCreditorAgent/Code: TELB 和 PHOB 不能同时存在
- RelatedRemittanceInformation 和 RemittanceInformation 互斥
- Structured 和 Unstructured 汇款信息互斥

## 3. ISO 规则 (isoRules)

数据位置：`appConfig.js` → `isoRules` 数组

需实现的逻辑：
- R6: InstructedAgent 在 GroupHeader 和 Transaction 级别互斥
- R7: InstructingAgent 在 GroupHeader 和 Transaction 级别互斥
- R8: TotalInterbankSettlementAmount 币种必须与各笔 InterbankSettlementAmount 一致
- R42: ExchangeRate 仅在 InstructedAmount 存在时允许

## 实现建议

在 `form_app.py` 中新增 Module（如 Module 15: Cross-Field Validation），读取 `appConfig` 中的规则数据，在表单提交/验证时执行跨字段检查，违规时在相关字段显示错误提示。
