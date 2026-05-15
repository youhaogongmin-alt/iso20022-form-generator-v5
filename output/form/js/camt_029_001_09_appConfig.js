(function(window) {
var apiKey = "CAMT029";
window.ISO20022_FORM_DATA = window.ISO20022_FORM_DATA || {};
window.ISO20022_FORM_DATA[apiKey] = window.ISO20022_FORM_DATA[apiKey] || {};
var bucket = window.ISO20022_FORM_DATA[apiKey];
bucket.appConfig = {
  "showTemplateBar": true,
  "messages": {
    "camt.029.001.09": {
      "templates": {
        "cross_border_standard": {
          "icon": "🌐",
          "shortName": "跨境汇款",
          "name": "标准跨境汇款 / Standard Cross-Border Transfer",
          "desc": "企业间跨境货款支付，使用序列法/代理行路径，双方分担费用",
          "values": {
            "AH_AppHdr_Fr_FIId_FinInstnId_BICFI": "BANKUS33XXX",
            "AH_AppHdr_To_FIId_FinInstnId_BICFI": "BANKGB2LXXX",
            "AH_AppHdr_BizMsgIdr": "BANKUS33-20260510-0001",
            "AH_AppHdr_MsgDefIdr": "pacs.008.001.08",
            "AH_AppHdr_BizSvc": "swift.cbprplus.02",
            "AH_AppHdr_CreDt": "2026-05-10T10:30:00",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId": "BANKUS33-20260510-0001",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_CreDtTm": "2026-05-10T10:30:00",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_NbOfTxs": "1",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_SttlmInf_SttlmMtd": "INDA",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_InstrId": "BANKUS330001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_EndToEndId": "E2E/2026/05/10/001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_TxId": "TXN20260510001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_UETR": "d0b7077f-49fb-42ed-b78d-af331c0e5012",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY": "USD",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt": "565000.00",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt": "2026-05-15",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr": "SHAR",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_SvcLvl_Cd": "SDVA",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_CtgyPurp_Cd": "SUPP",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm": "ABC Corporation",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN": "DE89370400440532013000",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAgt_FinInstnId_BICFI": "BANKUS33XXX",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI": "BANKGB2LXXX",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm": "DEF Electronics Ltd",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN": "GB29NWBK60161331926819",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd": "TRAD",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd": "Invoice INV-2026-001 / Contract 123"
          }
        },
        "salary_payment": {
          "icon": "💰",
          "shortName": "薪资发放",
          "name": "薪资发放 / Salary Payment",
          "desc": "跨境员工薪资发放，付款人承担费用，保留 SALA 用途标识",
          "values": {
            "AH_AppHdr_Fr_FIId_FinInstnId_BICFI": "BANKCNBJXXX",
            "AH_AppHdr_To_FIId_FinInstnId_BICFI": "BANKSGSGXXX",
            "AH_AppHdr_BizMsgIdr": "PAYROLL-202605-001",
            "AH_AppHdr_MsgDefIdr": "pacs.008.001.08",
            "AH_AppHdr_BizSvc": "swift.cbprplus.02",
            "AH_AppHdr_CreDt": "2026-05-10T09:00:00",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId": "PAYROLL-202605-001",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_CreDtTm": "2026-05-10T09:00:00",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_NbOfTxs": "1",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_SttlmInf_SttlmMtd": "INDA",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_InstrId": "PAYROLL050001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_EndToEndId": "SALARY/2026/05/001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_TxId": "SAL20260510001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_UETR": "8f4c6f8a-7c99-4d6e-b4a1-6b645b6f06a1",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY": "USD",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt": "3200.00",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt": "2026-05-15",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr": "DEBT",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm": "Global Payroll Services Ltd",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN": "DE89370400440532013000",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAgt_FinInstnId_BICFI": "BANKCNBJXXX",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI": "BANKSGSGXXX",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm": "Employee Name",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN": "GB29NWBK60161331926819",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd": "SALA",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_CtgyPurp_Cd": "SALA",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd": "Salary May 2026"
          }
        },
        "urgent_trade": {
          "icon": "⚡",
          "shortName": "紧急贸易",
          "name": "紧急贸易付款 / Urgent Trade Payment",
          "desc": "紧急贸易结算，高优先级/加急服务，付款人承担费用",
          "values": {
            "AH_AppHdr_Fr_FIId_FinInstnId_BICFI": "BANKUS33XXX",
            "AH_AppHdr_To_FIId_FinInstnId_BICFI": "BANKDEFFXXX",
            "AH_AppHdr_BizMsgIdr": "URGTRD-20260510-001",
            "AH_AppHdr_MsgDefIdr": "pacs.008.001.08",
            "AH_AppHdr_BizSvc": "swift.cbprplus.02",
            "AH_AppHdr_CreDt": "2026-05-10T08:15:00",
            "AH_AppHdr_Prty": "HIGH",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId": "URGTRD-20260510-001",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_CreDtTm": "2026-05-10T08:15:00",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_NbOfTxs": "1",
            "DOC_FIToFICstmrCdtTrf_GrpHdr_SttlmInf_SttlmMtd": "INDA",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_InstrId": "URGTRD000001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_EndToEndId": "URGENT/TRADE/20260510",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_TxId": "URG20260510001",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtId_UETR": "4b6f0e42-1f1d-4bd5-98cf-2e5d241b9f01",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY": "EUR",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt": "250000.00",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt": "2026-05-10",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr": "DEBT",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_InstrPrty": "HIGH",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_SvcLvl_Cd": "URGP",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_PmtTpInf_CtgyPurp_Cd": "SUPP",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm": "ABC Trading Co., Ltd.",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN": "GB29NWBK60161331926819",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAgt_FinInstnId_BICFI": "BANKUS33XXX",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI": "BANKDEFFXXX",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm": "Machine Parts GmbH",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN": "DE89370400440532013000",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd": "TRAD",
            "DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd": "Urgent trade settlement / Invoice TRD-2026-7788"
          }
        }
      },
      "quickFillFields": [
        {
          "key": "msgId",
          "label_zh": "报文编号",
          "label_en": "Message ID",
          "xml_tag": "MsgId",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_GrpHdr_MsgId\"]",
          "control": "input",
          "placeholder": "MSG20260510001"
        },
        {
          "key": "settlementCurrency",
          "label_zh": "清算币种",
          "label_en": "Settlement Currency",
          "xml_tag": "IntrBkSttlmAmt/Ccy",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt_CCY\"]",
          "control": "select",
          "options": [
            "USD",
            "EUR",
            "CNY",
            "HKD",
            "GBP",
            "JPY",
            "CHF",
            "CAD",
            "AUD"
          ]
        },
        {
          "key": "settlementAmount",
          "label_zh": "清算金额",
          "label_en": "Interbank Settlement Amount",
          "xml_tag": "IntrBkSttlmAmt",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmAmt\"]",
          "control": "number",
          "step": "0.00001",
          "placeholder": "10000.00"
        },
        {
          "key": "settlementDate",
          "label_zh": "清算日期",
          "label_en": "Settlement Date",
          "xml_tag": "IntrBkSttlmDt",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_IntrBkSttlmDt\"]",
          "control": "date"
        },
        {
          "key": "chargeBearer",
          "label_zh": "费用承担",
          "label_en": "Charge Bearer",
          "xml_tag": "ChrgBr",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_ChrgBr\"]",
          "control": "select",
          "options": [
            {
              "value": "DEBT",
              "label": "DEBT - 付款人承担"
            },
            {
              "value": "CRED",
              "label": "CRED - 收款人承担"
            },
            {
              "value": "SHAR",
              "label": "SHAR - 双方分担"
            }
          ]
        },
        {
          "key": "debtorName",
          "label_zh": "付款人名称",
          "label_en": "Debtor Name",
          "xml_tag": "Dbtr/Nm",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Dbtr_Nm\"]",
          "control": "textarea",
          "rows": 2,
          "placeholder": "ABC Trading Co., Ltd."
        },
        {
          "key": "debtorAccount",
          "label_zh": "付款人账号/IBAN",
          "label_en": "Debtor Account",
          "xml_tag": "DbtrAcct/IBAN",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_DbtrAcct_Id_IBAN\"]",
          "control": "input",
          "placeholder": "DE89370400440532013000"
        },
        {
          "key": "creditorName",
          "label_zh": "收款人名称",
          "label_en": "Creditor Name",
          "xml_tag": "Cdtr/Nm",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Cdtr_Nm\"]",
          "control": "textarea",
          "rows": 2,
          "placeholder": "XYZ Supplier Ltd."
        },
        {
          "key": "creditorAccount",
          "label_zh": "收款人账号/IBAN",
          "label_en": "Creditor Account",
          "xml_tag": "CdtrAcct/IBAN",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAcct_Id_IBAN\"]",
          "control": "input",
          "placeholder": "DE89370400440532013000"
        },
        {
          "key": "creditorAgentBic",
          "label_zh": "收款行 BIC",
          "label_en": "Creditor Agent BIC",
          "xml_tag": "CdtrAgt/BICFI",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_CdtrAgt_FinInstnId_BICFI\"]",
          "control": "input",
          "placeholder": "CHASUS33"
        },
        {
          "key": "purposeCode",
          "label_zh": "交易用途代码",
          "label_en": "Purpose Code",
          "xml_tag": "Purp/Cd",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_Purp_Cd\"]",
          "control": "input",
          "placeholder": "TRAD"
        },
        {
          "key": "ustrd",
          "label_zh": "业务附言",
          "label_en": "Unstructured Remittance",
          "xml_tag": "RmtInf/Ustrd",
          "target": "[name=\"DOC_FIToFICstmrCdtTrf_CdtTrfTxInf_RmtInf_Ustrd\"]",
          "control": "textarea",
          "rows": 3,
          "placeholder": "Invoice INV-2026-001, Payment for goods"
        }
      ],
      "fieldStateStyles": {
        "required": {
          "color": "#000000",
          "background": "#9EB5F9"
        },
        "readonly": {
          "color": "#000000",
          "background": "#cad1e2"
        },
        "editable": {
          "color": "#000000",
          "background": "#ffffff"
        }
      },
      "fieldStateOverrides": [],
      "fieldAliases": {},
      "valueMappings": {},
      "conditionalPresence": [
        {
          "context": "Full Message/Document/ResolutionOfInvestigationV09/CancellationDe-\ntails/TransactionInformationAndStatus/ResolvedCase/Creator/Agent/FinancialInsti-\ntutionIdentification",
          "if_path": "FinancialInstitu-\ntionIdentification/Name",
          "then_path": "FinancialInstitu-\ntionIdentification/PostalAddress",
          "if_field": "Name",
          "then_field": "PostalAddress"
        },
        {
          "context": "",
          "if_path": "FinancialInstitu-\ntionIdentification/PostalAddress",
          "then_path": "FinancialInstitu-\ntionIdentification/Name",
          "if_field": "PostalAddress",
          "then_field": "Name"
        }
      ],
      "notAllowedValues": [],
      "isoRules": [
        {
          "rule_id": "R1",
          "name": "RelatedPresentWhenCopyDupl",
          "text": "Related MUST contain the relevant BusinessMessageHeader elements of the BusinessMes- sage to which this BusinessMessage relates. If CopyDuplicate is present, then Related MUST be present.",
          "severity": "Warning",
          "error_code": "H00001"
        },
        {
          "rule_id": "R4",
          "name": "PartialOrRejectedCancellationRule",
          "text": "If Status/Confirmation is present and equal to PECR or RJCR then CancellationDetails must be present.",
          "severity": "Fatal",
          "error_code": "X00095"
        },
        {
          "rule_id": "R5",
          "name": "MessageOrGroupResolvedCaseRule",
          "text": "ResolvedCase may be present at either ResolvedCase, OriginalGroupInformationAndStatus, OriginalPaymentInformationAndStatus or TransactionInformationAndStatus level.",
          "severity": "Fatal",
          "error_code": "X00113"
        },
        {
          "rule_id": "R6",
          "name": "MessageOrPaymentInformationResolvedCaseRule",
          "text": "ResolvedCase may be present at either ResolvedCase, OriginalGroupInformationAndStatus, OriginalPaymentInformationAndStatus or TransactionInformationAndStatus level.",
          "severity": "Fatal",
          "error_code": "X00114"
        },
        {
          "rule_id": "R7",
          "name": "MessageOrInitiationTransactionResolvedCaseRule",
          "text": "ResolvedCase may be present at either ResolvedCase, OriginalGroupInformationAndStatus, OriginalPaymentInformationAndStatus or TransactionInformationAndStatus level.",
          "severity": "Fatal",
          "error_code": "X00115"
        },
        {
          "rule_id": "R8",
          "name": "MessageOrInterbankTransactionResolvedCaseRule",
          "text": "ResolvedCase may be present at either ResolvedCase, OriginalGroupInformationAndStatus, OriginalPaymentInformationAndStatus or TransactionInformationAndStatus level.",
          "severity": "Fatal",
          "error_code": "X00116"
        }
      ]
    }
  }
};
window.ISO20022_APP_CONFIG = bucket.appConfig;
})(window);
