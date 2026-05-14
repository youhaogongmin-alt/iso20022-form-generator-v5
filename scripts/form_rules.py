"""CBPR+/ISO 20022 rendering rules and demo presets.

This module is intentionally data-heavy. Keep collection-specific overrides here
so field and page renderers stay focused on HTML generation.
"""

from __future__ import annotations
# ==================== CBPR+ SR2026 CR Fixes ====================

# F02 (CR 3031): Remove Prtry from Scheme Name
SCHMENM_FIELDS_TO_REMOVE = {'Prtry'}

# F08 (CR 3032): Branch Identifier fields to remove under Creditor Agent
BRANCH_ID_FIELDS_TO_REMOVE = {'BrnchId'}

# Fields that should use date type (not dateTime) per CR 3039
FORCE_DATE_FIELDS = {'IntrBkSttlmDt', 'BirthDt', 'RltdDt', 'FrDt', 'ToDt', 'Dt'}


def should_remove_field(field: dict, parent_tag: str) -> bool:
    """Check if a field should be removed based on CBPR+ SR2026 CRs."""
    tag = field.get('xml_tag', '')

    # F02: Remove Prtry from SchmeNm
    if parent_tag == 'SchmeNm' and tag in SCHMENM_FIELDS_TO_REMOVE:
        return True

    # F08: Remove Branch Identifier under Creditor Agent
    if tag in BRANCH_ID_FIELDS_TO_REMOVE:
        return True

    return False


def is_proxy_tp_field(field: dict, parent_tag: str) -> bool:
    """Check if a field is Proxy/Type that should be mandatory (CR 3012)."""
    return field.get('xml_tag') == 'Tp' and parent_tag == 'Prxy'


def force_date_type(field: dict) -> bool:
    """Check if a field should use date type instead of dateTime (CR 3039)."""
    tag = field.get('xml_tag', '')
    return tag in FORCE_DATE_FIELDS and field.get('type_code') == 'dateTime'


# ==================== Example Values & Business Rules ====================

EXAMPLE_VALUES = {
    # BIC
    'BICFI': 'CHASUS33',
    'BIC': 'CHASUS33',
    # IBAN
    'IBAN': 'DE89370400440532013000',
    # Amount
    'IntrBkSttlmAmt': '10000.00',
    'InstdAmt': '10000.00',
    # Dates
    'IntrBkSttlmDt': '2026-05-15',
    'CreDtTm': '2026-05-10T10:30:00',
    'CreDt': '2026-05-10T10:30:00',
    # Identifiers
    'MsgId': 'MSG20260510001',
    'BizMsgIdr': 'BIZ20260510001',
    'EndToEndId': 'E2E/2026/05/10/001',
    'TxId': 'TXN20260510001',
    'UETR': 'f1b1d1e1-a1b1-c1d1-e1f1-a1b1c1d1e1f1',
    'InstrId': 'INS20260510001',
    'ClrSysRef': 'CLR20260510001',
    # Names
    'Nm': 'Zhang San / 张三',
    # Country
    'CtryOfRes': 'CN',
    # LEI
    'LEI': '529900T8BM49AURSDO55',
    # Member ID
    'MmbId': 'CHASUS33XXX',
    # Postal
    'PstlAdr': 'No.1 Finance Street, Beijing',
    # Purpose
    'Cd': 'CASH',
    'Prtry': 'CASH',
    # Charge bearer
    'ChrgBr': 'SHAR',
    # Remittance
    'Ustrd': 'Invoice INV-2026-001',
    'RmtId': 'RMT20260510001',
    # Exchange rate
    'XchgRate': '7.2500',
    # Clearing system
    'ClrChanl': 'RTGS',
    'InstrPrty': 'HIGH',
}

# Business rule descriptions shown as warnings
BUSINESS_RULES = {
    'ChrgBr': {
        'SHAR': '⚠️ SHAR模式：手续费由双方分担，收款人实际到账金额将减少',
        'CRED': '⚠️ CRED模式：手续费由收款人承担，到账金额会扣除手续费',
        'DEBT': 'DEBT模式：手续费由付款人承担，收款人收到全额',
    },
}

# Business quick field panel defaults.
#
# The generated page can override these in appConfig.js per message type. Keep
# only broadly useful defaults here; downstream projects should add their own
# frequently used business fields in runtime config.
QUICK_FILL_FIELDS = [
    {
        'key': 'msgId',
        'label_zh': '报文编号',
        'label_en': 'Message ID',
        'xml_tag': 'MsgId',
        'target': '[name="DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId"]',
        'control': 'input',
        'placeholder': 'MSG20260510001',
    },
    {
        'key': 'settlementCurrency',
        'label_zh': '清算币种',
        'label_en': 'Settlement Currency',
        'xml_tag': 'IntrBkSttlmAmt/Ccy',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY"]',
        'control': 'select',
        'options': ['USD', 'EUR', 'CNY', 'HKD', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD'],
    },
    {
        'key': 'settlementAmount',
        'label_zh': '清算金额',
        'label_en': 'Interbank Settlement Amount',
        'xml_tag': 'IntrBkSttlmAmt',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt"]',
        'control': 'number',
        'step': '0.00001',
        'placeholder': '10000.00',
    },
    {
        'key': 'settlementDate',
        'label_zh': '清算日期',
        'label_en': 'Settlement Date',
        'xml_tag': 'IntrBkSttlmDt',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt"]',
        'control': 'date',
    },
    {
        'key': 'chargeBearer',
        'label_zh': '费用承担',
        'label_en': 'Charge Bearer',
        'xml_tag': 'ChrgBr',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr"]',
        'control': 'select',
        'options': [
            {'value': 'DEBT', 'label': 'DEBT - 付款人承担'},
            {'value': 'CRED', 'label': 'CRED - 收款人承担'},
            {'value': 'SHAR', 'label': 'SHAR - 双方分担'},
        ],
    },
    {
        'key': 'debtorName',
        'label_zh': '付款人名称',
        'label_en': 'Debtor Name',
        'xml_tag': 'Dbtr/Nm',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm"]',
        'control': 'textarea',
        'rows': 2,
        'placeholder': 'ABC Trading Co., Ltd.',
    },
    {
        'key': 'debtorAccount',
        'label_zh': '付款人账号/IBAN',
        'label_en': 'Debtor Account',
        'xml_tag': 'DbtrAcct/IBAN',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN"]',
        'control': 'input',
        'placeholder': 'DE89370400440532013000',
    },
    {
        'key': 'creditorName',
        'label_zh': '收款人名称',
        'label_en': 'Creditor Name',
        'xml_tag': 'Cdtr/Nm',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm"]',
        'control': 'textarea',
        'rows': 2,
        'placeholder': 'XYZ Supplier Ltd.',
    },
    {
        'key': 'creditorAccount',
        'label_zh': '收款人账号/IBAN',
        'label_en': 'Creditor Account',
        'xml_tag': 'CdtrAcct/IBAN',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN"]',
        'control': 'input',
        'placeholder': 'DE89370400440532013000',
    },
    {
        'key': 'creditorAgentBic',
        'label_zh': '收款行 BIC',
        'label_en': 'Creditor Agent BIC',
        'xml_tag': 'CdtrAgt/BICFI',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI"]',
        'control': 'input',
        'placeholder': 'CHASUS33',
    },
    {
        'key': 'purposeCode',
        'label_zh': '交易用途代码',
        'label_en': 'Purpose Code',
        'xml_tag': 'Purp/Cd',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd"]',
        'control': 'input',
        'placeholder': 'TRAD',
    },
    {
        'key': 'ustrd',
        'label_zh': '业务附言',
        'label_en': 'Unstructured Remittance',
        'xml_tag': 'RmtInf/Ustrd',
        'target': '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd"]',
        'control': 'textarea',
        'rows': 3,
        'placeholder': 'Invoice INV-2026-001, Payment for goods',
    },
]

# Default visual styles for generated field states.
# Split output exposes these values again in appConfig.js so downstream
# developers can adjust colors without editing app.js or regenerating the form.
FIELD_STATE_STYLES = {
    'required': {
        'color': '#000000',
        'background': '#9EB5F9',
    },
    'readonly': {
        'color': '#000000',
        'background': '#cad1e2',
    },
    'editable': {
        'color': '#000000',
        'background': '#ffffff',
    },
}

# Optional downstream field state overrides.
#
# Example for appConfig.js:
# {
#   target: '[name="DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr"]',
#   state: 'readonly'
# }
FIELD_STATE_OVERRIDES = []

# F04 (CR 3020): Forbidden Service Level Codes for CBPR+ (per GPI rule on page 23)
FORBIDDEN_SVC_LVL_CODES = {'G002', 'G003', 'G004', 'G005', 'G006', 'G007', 'G009'}

# F07 (CR 3072): Fields that become mandatory when parent section has value
CONDITIONAL_MANDATORY = {
    # When Strd exists, CdtrRefInf/Ref is mandatory
    'CdtrRefInf': ['Ref'],
}

# Preset templates
# icon/shortName/name/desc 控制顶部快速模板按钮和提示展示；
# values 控制应用模板时写入正式表单的字段值。拆分输出会暴露到 appConfig.js。
TEMPLATES = {
    'cross_border_standard': {
        'icon': '🌐',
        'shortName': '跨境汇款',
        'name': '标准跨境汇款 / Standard Cross-Border Transfer',
        'desc': '企业间跨境货款支付，使用序列法/代理行路径，双方分担费用',
        'values': {
            'AH_AppHdr_Fr_FIId_FinInstnId_BICFI': 'BANKUS33XXX',
            'AH_AppHdr_To_FIId_FinInstnId_BICFI': 'BANKGB2LXXX',
            'AH_AppHdr_BizMsgIdr': 'BANKUS33-20260510-0001',
            'AH_AppHdr_MsgDefIdr': 'pacs.008.001.08',
            'AH_AppHdr_BizSvc': 'swift.cbprplus.02',
            'AH_AppHdr_CreDt': '2026-05-10T10:30:00',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId': 'BANKUS33-20260510-0001',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_CreDtTm': '2026-05-10T10:30:00',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_NbOfTxs': '1',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_SttlmInf_SttlmMtd': 'INDA',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_InstrId': 'BANKUS330001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_EndToEndId': 'E2E/2026/05/10/001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_TxId': 'TXN20260510001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_UETR': 'd0b7077f-49fb-42ed-b78d-af331c0e5012',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY': 'USD',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt': '565000.00',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt': '2026-05-15',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr': 'SHAR',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_SvcLvl_Cd': 'SDVA',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_CtgyPurp_Cd': 'SUPP',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm': 'ABC Corporation',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN': 'DE89370400440532013000',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAgt_FinInstnId_BICFI': 'BANKUS33XXX',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI': 'BANKGB2LXXX',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm': 'DEF Electronics Ltd',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN': 'GB29NWBK60161331926819',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd': 'TRAD',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd': 'Invoice INV-2026-001 / Contract 123',
        }
    },
    'salary_payment': {
        'icon': '💰',
        'shortName': '薪资发放',
        'name': '薪资发放 / Salary Payment',
        'desc': '跨境员工薪资发放，付款人承担费用，保留 SALA 用途标识',
        'values': {
            'AH_AppHdr_Fr_FIId_FinInstnId_BICFI': 'BANKCNBJXXX',
            'AH_AppHdr_To_FIId_FinInstnId_BICFI': 'BANKSGSGXXX',
            'AH_AppHdr_BizMsgIdr': 'PAYROLL-202605-001',
            'AH_AppHdr_MsgDefIdr': 'pacs.008.001.08',
            'AH_AppHdr_BizSvc': 'swift.cbprplus.02',
            'AH_AppHdr_CreDt': '2026-05-10T09:00:00',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId': 'PAYROLL-202605-001',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_CreDtTm': '2026-05-10T09:00:00',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_NbOfTxs': '1',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_SttlmInf_SttlmMtd': 'INDA',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_InstrId': 'PAYROLL050001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_EndToEndId': 'SALARY/2026/05/001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_TxId': 'SAL20260510001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_UETR': '8f4c6f8a-7c99-4d6e-b4a1-6b645b6f06a1',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY': 'USD',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt': '3200.00',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt': '2026-05-15',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr': 'DEBT',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm': 'Global Payroll Services Ltd',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN': 'DE89370400440532013000',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAgt_FinInstnId_BICFI': 'BANKCNBJXXX',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI': 'BANKSGSGXXX',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm': 'Employee Name',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN': 'GB29NWBK60161331926819',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd': 'SALA',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_CtgyPurp_Cd': 'SALA',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd': 'Salary May 2026',
        }
    },
    'urgent_trade': {
        'icon': '⚡',
        'shortName': '紧急贸易',
        'name': '紧急贸易付款 / Urgent Trade Payment',
        'desc': '紧急贸易结算，高优先级/加急服务，付款人承担费用',
        'values': {
            'AH_AppHdr_Fr_FIId_FinInstnId_BICFI': 'BANKUS33XXX',
            'AH_AppHdr_To_FIId_FinInstnId_BICFI': 'BANKDEFFXXX',
            'AH_AppHdr_BizMsgIdr': 'URGTRD-20260510-001',
            'AH_AppHdr_MsgDefIdr': 'pacs.008.001.08',
            'AH_AppHdr_BizSvc': 'swift.cbprplus.02',
            'AH_AppHdr_CreDt': '2026-05-10T08:15:00',
            'AH_AppHdr_Prty': 'HIGH',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId': 'URGTRD-20260510-001',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_CreDtTm': '2026-05-10T08:15:00',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_NbOfTxs': '1',
            'DOC_FIToFICstmrCdtTrf_GrpHdr_SttlmInf_SttlmMtd': 'INDA',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_InstrId': 'URGTRD000001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_EndToEndId': 'URGENT/TRADE/20260510',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_TxId': 'URG20260510001',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_UETR': '4b6f0e42-1f1d-4bd5-98cf-2e5d241b9f01',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY': 'EUR',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt': '250000.00',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt': '2026-05-10',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr': 'DEBT',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_InstrPrty': 'HIGH',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_SvcLvl_Cd': 'URGP',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_CtgyPurp_Cd': 'SUPP',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm': 'ABC Trading Co., Ltd.',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN': 'GB29NWBK60161331926819',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAgt_FinInstnId_BICFI': 'BANKUS33XXX',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI': 'BANKDEFFXXX',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm': 'Machine Parts GmbH',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN': 'DE89370400440532013000',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd': 'TRAD',
            'DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd': 'Urgent trade settlement / Invoice TRD-2026-7788',
        }
    },
}
