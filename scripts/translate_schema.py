"""Step 2 of the form generation workflow: fill in name_zh translations.

Usage:
    python scripts/translate_schema.py output/pacs.008.001.08.json

Reads the schema JSON, fills all empty name_zh fields with Chinese translations,
and writes the result back to the same file.
"""

import json
import sys

TRANSLATIONS = {
    "Additional Information": "附加信息",
    "Additional Remittance Information": "附加汇款信息",
    "Address Line": "地址行",
    "Adjustment Amount And Reason": "调整金额及原因",
    "Administration Zone": "管辖区域",
    "Agent": "代理行",
    "Amount": "金额",
    "Any BIC": "任意BIC",
    "Authorisation": "授权",
    "Authority": "监管机构",
    "BICFI": "金融机构BIC",
    "Birth Date": "出生日期",
    "Building Name": "楼名",
    "Building Number": "楼号",
    "Business Application Header V02 (head.001.001.02)": "业务应用头V02 (head.001.001.02)",
    "Business Message Identifier": "业务消息标识",
    "Business Service": "业务服务",
    "CLS Time": "CLS时间",
    "Category": "类别",
    "Category Details": "类别明细",
    "Category Purpose": "类别目的",
    "Certificate Identification": "证书标识",
    "Character Set": "字符集",
    "Charge Bearer": "费用承担方",
    "Charges Information": "费用信息",
    "City Of Birth": "出生城市",
    "Clearing Channel": "清算渠道",
    "Clearing System Identification": "清算系统标识",
    "Clearing System Member Identification": "清算系统成员标识",
    "Clearing System Reference": "清算系统参考",
    "Code": "代码",
    "Code Or Proprietary": "代码或自定义",
    "Copy Duplicate": "副本/重复",
    "Country": "国家",
    "Country Of Birth": "出生国家",
    "Country Of Residence": "居住国",
    "Country Sub Division": "国家行政区",
    "Creation Date": "创建日期",
    "Creation Date Time": "创建日期时间",
    "Credit Date Time": "贷记日期时间",
    "Credit Debit Indicator": "借贷指示",
    "Credit Note Amount": "贷项通知金额",
    "Credit Transfer Transaction Information": "贷记转账交易信息",
    "Creditor": "收款人",
    "Creditor Account": "收款人账户",
    "Creditor Agent": "收款行",
    "Creditor Agent Account": "收款行账户",
    "Creditor Reference Information": "收款人参考信息",
    "Currency": "货币",
    "Date": "日期",
    "Date And Place Of Birth": "出生日期和地点",
    "Debit Credit Reporting Indicator": "借贷报告指示",
    "Debit Date Time": "借记日期时间",
    "Debtor": "付款人",
    "Debtor Account": "付款人账户",
    "Debtor Agent": "付款行",
    "Debtor Agent Account": "付款行账户",
    "Debtor Status": "付款人状态",
    "Department": "部门",
    "Description": "描述",
    "Details": "明细",
    "Discount Applied Amount": "已用折扣金额",
    "District Name": "区名",
    "Document": "文档",
    "Due Payable Amount": "应付金额",
    "Electronic Address": "电子地址",
    "Employee Termination Indicator": "雇员终止指示",
    "End To End Identification": "端到端标识",
    "Exchange Rate": "汇率",
    "FI To FI Customer Credit Transfer V08 (pacs.008.001.08)": "金融机构间客户贷记转账V08 (pacs.008.001.08)",
    "Family Medical Insurance Indicator": "家庭医疗保险指示",
    "Financial Institution Identification": "金融机构标识",
    "Floor": "楼层",
    "Forms Code": "表格代码",
    "From": "发送方",
    "From Date": "起始日期",
    "From Time": "起始时间",
    "From To Date": "起止日期",
    "Garnishee": "被扣押方",
    "Garnishment Administrator": "扣押管理人",
    "Garnishment Remittance": "扣押汇款",
    "Group Header": "组头",
    "IBAN": "IBAN",
    "Identification": "标识",
    "Information": "信息",
    "Initiating Party": "发起方",
    "Instructed Agent": "被指示代理行",
    "Instructed Amount": "指示金额",
    "Instructed Reimbursement Agent": "被指示偿付行",
    "Instructed Reimbursement Agent Account": "被指示偿付行账户",
    "Instructing Agent": "指示代理行",
    "Instructing Reimbursement Agent": "指示偿付行",
    "Instructing Reimbursement Agent Account": "指示偿付行账户",
    "Instruction For Creditor Agent": "收款行指令",
    "Instruction For Next Agent": "下一行指令",
    "Instruction Identification": "指令标识",
    "Instruction Information": "指令信息",
    "Instruction Priority": "指令优先级",
    "Interbank Settlement Amount": "银行间结算金额",
    "Interbank Settlement Date": "银行间结算日期",
    "Intermediary Agent 1": "中间行1",
    "Intermediary Agent 1 Account": "中间行1账户",
    "Intermediary Agent 2": "中间行2",
    "Intermediary Agent 2 Account": "中间行2账户",
    "Intermediary Agent 3": "中间行3",
    "Intermediary Agent 3 Account": "中间行3账户",
    "Invoicee": "受票方",
    "Invoicer": "开票方",
    "Issuer": "签发者",
    "LEI": "法人实体标识",
    "Line Details": "行明细",
    "Local Instrument": "本地工具",
    "Market Practice": "市场惯例",
    "Member Identification": "成员标识",
    "Message Definition Identifier": "消息定义标识",
    "Message Identification": "消息标识",
    "Method": "方式",
    "Name": "名称",
    "Number": "编号",
    "Number Of Transactions": "交易数量",
    "Organisation Identification": "组织标识",
    "Other": "其他",
    "Payment Identification": "支付标识",
    "Payment Type Information": "支付类型信息",
    "Period": "期间",
    "Possible Duplicate": "可能重复",
    "Post Box": "邮政信箱",
    "Post Code": "邮编",
    "Postal Address": "邮政地址",
    "Previous Instructing Agent 1": "前指示代理行1",
    "Previous Instructing Agent 1 Account": "前指示代理行1账户",
    "Previous Instructing Agent 2": "前指示代理行2",
    "Previous Instructing Agent 2 Account": "前指示代理行2账户",
    "Previous Instructing Agent 3": "前指示代理行3",
    "Previous Instructing Agent 3 Account": "前指示代理行3账户",
    "Priority": "优先级",
    "Private Identification": "个人标识",
    "Proprietary": "专有",
    "Province Of Birth": "出生省份",
    "Proxy": "代理",
    "Purpose": "目的",
    "Rate": "税率",
    "Reason": "原因",
    "Record": "记录",
    "Reference": "参考",
    "Reference Number": "参考编号",
    "Referred Document Amount": "引用文档金额",
    "Referred Document Information": "引用文档信息",
    "Registration Identification": "登记标识",
    "Registry": "注册机构",
    "Regulatory Reporting": "监管报告",
    "Reject Time": "拒绝时间",
    "Related": "关联",
    "Related Date": "相关日期",
    "Related Remittance Information": "相关汇款信息",
    "Remittance Identification": "汇款标识",
    "Remittance Information": "汇款信息",
    "Remittance Location Details": "汇款地点明细",
    "Remitted Amount": "汇出金额",
    "Room": "房间",
    "Scheme Name": "方案名称",
    "Sequence Number": "序列号",
    "Service Level": "服务等级",
    "Settlement Account": "结算账户",
    "Settlement Information": "结算信息",
    "Settlement Method": "结算方式",
    "Settlement Priority": "结算优先级",
    "Settlement Time Indication": "结算时间指示",
    "Settlement Time Request": "结算时间请求",
    "Street Name": "街道名称",
    "Structured": "结构化信息",
    "Sub Department": "子部门",
    "Tax Amount": "税额",
    "Tax Identification": "税务标识",
    "Tax Remittance": "税务汇款",
    "Tax Type": "税种",
    "Taxable Base Amount": "应税基础金额",
    "Third Reimbursement Agent": "第三偿付行",
    "Third Reimbursement Agent Account": "第三偿付行账户",
    "Till Time": "截止时间",
    "Title": "头衔",
    "To": "接收方",
    "To Date": "截止日期",
    "Total Amount": "总金额",
    "Total Tax Amount": "总税额",
    "Total Taxable Base Amount": "应税基础总额",
    "Town Location Name": "城镇位置名称",
    "Town Name": "城镇名称",
    "Transaction Identification": "交易标识",
    "Type": "类型",
    "UETR": "唯一端到端交易引用",
    "Ultimate Creditor": "最终收款人",
    "Ultimate Debtor": "最终付款人",
    "Unstructured": "非结构化信息",
    "Xml Attribute Currency": "货币(属性)",
    "Year": "年度",
}


def fill_translations(fields):
    """Recursively fill empty name_zh fields."""
    filled = 0
    for f in fields:
        name_en = f.get("name_en", "")
        if name_en and not f.get("name_zh"):
            zh = TRANSLATIONS.get(name_en, "")
            if zh:
                f["name_zh"] = zh
                filled += 1
        if f.get("children"):
            filled += fill_translations(f["children"])
    return filled


def main():
    if len(sys.argv) < 2:
        print("Usage: python translate_schema.py <schema.json>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    count = fill_translations(schema.get("app_hdr_fields", []))
    count += fill_translations(schema.get("document_fields", []))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2, default=str)

    print(f"Translated {count} fields in {path}")


if __name__ == "__main__":
    main()
