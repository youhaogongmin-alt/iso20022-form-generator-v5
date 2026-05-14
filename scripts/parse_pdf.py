#!/usr/bin/env python3
"""
ISO 20022 PDF Specification Parser
Extracts field definitions from ISO 20022 usage guideline PDFs.
"""

import re
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


class Multiplicity(Enum):
    MANDATORY = "mandatory"      # [1..1]
    OPTIONAL = "optional"        # [0..1]
    REQUIRED = "required"        # [1..*]
    CONDITIONAL = "conditional"  # [0..*]


@dataclass
class CodeValue:
    """A code value for enumerated fields."""
    code: str
    description_en: str
    description_zh: str = ""
    rules: str = ""


@dataclass
class FieldDefinition:
    """Definition of a single field in the message."""
    index: str = ""
    level: int = 0
    name_en: str = ""
    name_zh: str = ""
    xml_tag: str = ""
    multiplicity: str = ""      # e.g., "[1..1]", "[0..1]", "[0..*]"
    mult_min: int = 0
    mult_max: int = 1
    type_code: str = ""         # e.g., "text", "dateTime", "decimal", "date", "boolean"
    type_detail: str = ""       # e.g., "text{1,35}", "[A-Z]{2,2}"
    restriction: str = ""       # e.g., "FixedValue: pacs.008.001.08"
    regex_pattern: str = ""     # Extracted regex
    max_length: int = 0
    min_length: int = 0
    fixed_value: str = ""
    is_fixed: bool = False
    rules: str = ""             # Business rules references
    synonym: str = ""           # MT field synonym
    code_values: list = field(default_factory=list)
    children: list = field(default_factory=list)
    is_choice: bool = False
    decimal_td: int = 0         # total digits for decimal
    decimal_fd: int = 0         # fractional digits for decimal
    min_value: float = 0
    max_value: float = 0
    is_attribute: bool = False  # XML attribute
    parent_tag: str = ""

    def to_dict(self):
        d = asdict(self)
        d['children'] = [c.to_dict() for c in self.children]
        return d


# Chinese translations for common ISO 20022 field names
FIELD_TRANSLATIONS = {
    # Business Application Header
    "Character Set": "字符集",
    "From": "发送方",
    "To": "接收方",
    "Business Message Identifier": "业务消息标识",
    "Message Definition Identifier": "消息定义标识",
    "Business Service": "业务服务",
    "Market Practice": "市场惯例",
    "Creation Date": "创建日期",
    "Copy Duplicate": "副本/重复",
    "Possible Duplicate": "可能重复",
    "Priority": "优先级",
    "Signature": "签名",
    "Related": "关联",
    "Financial Institution Identification": "金融机构标识",
    "BICFI": "金融机构BIC",
    "Clearing System Member Identification": "清算系统成员标识",
    "Clearing System Identification": "清算系统标识",
    "Code": "代码",
    "Member Identification": "成员标识",
    "LEI": "法人实体标识",
    "Registry": "注册机构",
    "Identification": "标识",
    "Xml Attribute Currency": "货币(属性)",

    # Group Header
    "Message Identification": "消息标识",
    "Creation Date Time": "创建日期时间",
    "Number Of Transactions": "交易数量",
    "Settlement Information": "结算信息",
    "Settlement Method": "结算方式",
    "Settlement Account": "结算账户",
    "Instructing Reimbursement Agent": "指示偿付行",
    "Instructing Reimbursement Agent Account": "指示偿付行账户",
    "Instructed Reimbursement Agent": "被指示偿付行",
    "Instructed Reimbursement Agent Account": "被指示偿付行账户",
    "Third Reimbursement Agent": "第三偿付行",
    "Third Reimbursement Agent Account": "第三偿付行账户",

    # Credit Transfer Transaction Information
    "Credit Transfer Transaction Information": "贷记转账交易信息",
    "Payment Identification": "支付标识",
    "Instruction Identification": "指令标识",
    "End To End Identification": "端到端标识",
    "Transaction Identification": "交易标识",
    "UETR": "唯一端到端交易引用",
    "Clearing System Reference": "清算系统参考",
    "Payment Type Information": "支付类型信息",
    "Instruction Priority": "指令优先级",
    "Clearing Channel": "清算渠道",
    "Service Level": "服务等级",
    "Local Instrument": "本地工具",
    "Category Purpose": "类别目的",
    "Interbank Settlement Amount": "银行间结算金额",
    "Interbank Settlement Date": "银行间结算日期",
    "Settlement Priority": "结算优先级",
    "Settlement Time Indication": "结算时间指示",
    "Debit Date Time": "借记日期时间",
    "Credit Date Time": "贷记日期时间",
    "Settlement Time Request": "结算时间请求",
    "CLS Time": "CLS时间",
    "Till Time": "截止时间",
    "From Time": "起始时间",
    "Reject Time": "拒绝时间",
    "Instructed Amount": "指示金额",
    "Exchange Rate": "汇率",
    "Charge Bearer": "费用承担方",
    "Charges Information": "费用信息",
    "Amount": "金额",
    "Agent": "代理行",
    "Previous Instructing Agent 1": "前指示代理行1",
    "Previous Instructing Agent 1 Account": "前指示代理行1账户",
    "Previous Instructing Agent 2": "前指示代理行2",
    "Previous Instructing Agent 2 Account": "前指示代理行2账户",
    "Previous Instructing Agent 3": "前指示代理行3",
    "Previous Instructing Agent 3 Account": "前指示代理行3账户",
    "Instructing Agent": "指示代理行",
    "Instructed Agent": "被指示代理行",
    "Intermediary Agent 1": "中间行1",
    "Intermediary Agent 1 Account": "中间行1账户",
    "Intermediary Agent 2": "中间行2",
    "Intermediary Agent 2 Account": "中间行2账户",
    "Intermediary Agent 3": "中间行3",
    "Intermediary Agent 3 Account": "中间行3账户",
    "Creditor Agent": "收款行",
    "Creditor Agent Account": "收款行账户",
    "Debtor Agent": "付款行",
    "Debtor Agent Account": "付款行账户",
    "Debtor": "付款人",
    "Debtor Account": "付款人账户",
    "Creditor": "收款人",
    "Creditor Account": "收款人账户",
    "Name": "名称",
    "Postal Address": "邮政地址",
    "Department": "部门",
    "Sub Department": "子部门",
    "Street Name": "街道名称",
    "Building Number": "楼号",
    "Building Name": "楼名",
    "Floor": "楼层",
    "Post Box": "邮政信箱",
    "Room": "房间",
    "Post Code": "邮编",
    "Town Name": "城镇名称",
    "Town Location Name": "城镇位置名称",
    "District Name": "区名",
    "Country Sub Division": "国家行政区",
    "Country": "国家",
    "Address Line": "地址行",
    "Type": "类型",
    "Currency": "货币",
    "Issuer": "签发者",
    "Proprietary": "专有",
    "Scheme Name": "方案名称",
    "IBAN": "IBAN",
    "Other": "其他",
    "Organisation Identification": "组织标识",
    "Private Identification": "个人标识",
    "Date And Place Of Birth": "出生日期和地点",
    "Birth Date": "出生日期",
    "Province Of Birth": "出生省份",
    "City Of Birth": "出生城市",
    "Country Of Birth": "出生国家",
    "Country Of Residence": "居住国",
    "Remittance Information": "汇款信息",
    "Remittance Information Unstructured": "非结构化汇款信息",
    "Remittance Information Structured": "结构化汇款信息",
    "Instruction For Creditor Agent": "收款行指令",
    "Instruction For Next Agent": "下一行指令",
    "Instruction Information": "指令信息",
    "Supplementary Data": "补充数据",
    "Supplementary DataEnvelope": "补充数据信封",
    "Proxy": "代理",
    "Full Message": "完整消息",
    "Business Application Header V02": "业务应用头V02",
    "Business Application Header V02 (head.001.001.02)": "业务应用头V02 (head.001.001.02)",
    "Document": "文档",
    "FI To FI Customer Credit Transfer V08": "金融机构间客户贷记转账V08",
    "FI To FI Customer Credit Transfer V08 (pacs.008.001.08)": "金融机构间客户贷记转账V08 (pacs.008.001.08)",
    "Group Header": "组头",
    "Xml Attribute": "XML属性",
    "Identification Number": "识别号",
    "Issuer Identification Number": "签发者识别号",
    "Regulatory Reporting": "监管报告",
    "Purpose": "目的",
    "Related Remittance Information": "相关汇款信息",
    "Referred Document Information": "引用文档信息",
    "Line Details": "行明细",
    "Creditor Reference Information": "收款人参考信息",
    "Document Adjustment": "文档调整",
    "Original Amount": "原始金额",
    "Discount Amount": "折扣金额",
    "Discount Percentage": "折扣百分比",
    "Credit Debit Indicator": "借贷指示",
    "Referred Document Amount": "引用文档金额",
    "Due Date": "到期日",
    "Invoice Date": "发票日期",
    "Document Number": "文档编号",

    # Additional translations for container/repeat fields
    "Ultimate Debtor": "最终付款人",
    "Ultimate Creditor": "最终收款人",
    "Initiating Party": "发起方",
    "Authority": "监管机构",
    "Code Or Proprietary": "代码或自定义",
    "Invoicer": "开票方",
    "Invoicee": "受票方",
    "Tax Remittance": "税务汇款",
    "Authorisation": "授权",
    "Period": "期间",
    "From To Date": "起止日期",
    "Tax Amount": "税额",
    "Garnishment Remittance": "扣押汇款",
    "Garnishee": "被扣押方",
    "Garnishment Administrator": "扣押管理人",
    "Details": "明细",
    "Information": "信息",
    "Remittance Location Details": "汇款地点明细",
    "Structured": "结构化信息",
    "Discount Applied Amount": "已用折扣金额",
    "Adjustment Amount And Reason": "调整金额及原因",
    "Record": "记录",
    "Additional Remittance Information": "附加汇款信息",
    "Additional Information": "附加信息",
    "Any BIC": "任意BIC",
    "Category": "类别",
    "Category Details": "类别明细",
    "Certificate Identification": "证书标识",
    "Credit Note Amount": "贷项通知金额",
    "Date": "日期",
    "Debit Credit Reporting Indicator": "借贷报告指示",
    "Debtor Status": "付款人状态",
    "Description": "描述",
    "Due Payable Amount": "应付金额",
    "Electronic Address": "电子地址",
    "Employee Termination Indicator": "雇员终止指示",
    "Family Medical Insurance Indicator": "家庭医疗保险指示",
    "Forms Code": "表格代码",
    "From Date": "起始日期",
    "Administration Zone": "管辖区域",
    "Number": "编号",
    "Related Date": "相关日期",
    "Reference": "参考",
    "Tax Identification Number": "税务识别号",
    "Remittance Location Method": "汇款地点方式",
    "Remittance Location Electronic Address": "汇款地点电子地址",
    "Remittance Location Postal Address": "汇款地点邮政地址",
}

# Code value translations
CODE_TRANSLATIONS = {
    # Settlement Method
    "INDA": ("Instructed Agent", "被指示代理行"),
    "INGA": ("Instructing Agent", "指示代理行"),
    "COVE": ("Cover Method", "头寸法"),
    "CLRG": ("Clearing System", "清算系统"),

    # Charge Bearer
    "DEBT": ("Borne By Debtor", "付款人承担"),
    "CRED": ("Borne By Creditor", "收款人承担"),
    "SHAR": ("Shared", "共同承担"),

    # Priority
    "HIGH": ("High", "高"),
    "NORM": ("Normal", "普通"),
    "URGT": ("Urgent", "紧急"),

    # Clearing Channel
    "RTGS": ("Real Time Gross Settlement System", "实时全额结算系统"),
    "RTNS": ("Real Time Net Settlement System", "实时净额结算系统"),
    "MPNS": ("Mass Payment Net System", "批量支付净额系统"),
    "BOOK": ("Book Transfer", "簿记转账"),

    # Copy Duplicate
    "CODU": ("Copy Duplicate", "副本重复"),
    "COPY": ("Copy", "副本"),
    "DUPL": ("Duplicate", "重复"),

    # Instruction For Creditor Agent
    "CHQB": ("Pay Creditor By Cheque", "支票支付收款人"),
    "HOLD": ("Hold Cash For Creditor", "为收款人持有现金"),
    "PHOB": ("Phone Beneficiary", "电话联系受益人"),
    "TELB": ("Telecom", "电信"),

    # Clearing System Codes
    "TWNCC": ("Financial Institution Code", "金融机构代码"),
    "ESNCC": ("Spanish Domestic Interbanking Code", "西班牙国内银行间代码"),
    "USPID": ("CHIPS Participant Identifier", "CHIPS参与者标识"),
    "USABA": ("United States Routing Number Fedwire NACHA", "美国路由号"),
    "THCBC": ("Thai Central Bank Identification Code", "泰国央行识别码"),
    "GBDSC": ("UK Domestic Sort Code", "英国国内分类代码"),
    "SGIBG": ("IBG Sort Code", "IBG分类代码"),
    "NZRSA": ("New Zealand RTGS Clearing Code", "新西兰RTGS清算代码"),
    "DEBLZ": ("German Bankleitzahl", "德国银行代码"),
    "CNAPS": ("CNAPS Identifier", "CNAPS标识"),
    "CHSIC": ("Swiss Financial Institution Identification Long", "瑞士金融机构标识(长)"),
    "CHBCC": ("Swiss Financial Institution Identification Short", "瑞士金融机构标识(短)"),
    "CACPA": ("Canadian Payments Association Payment Routing Number", "加拿大支付路由号"),
    "SESBA": ("Sweden Bankgiro Clearing Code", "瑞典银行清算代码"),
    "RUCBC": ("Russian Central Bank Identification Code", "俄罗斯央行识别码"),
    "PTNCC": ("Portuguese National Clearing Code", "葡萄牙国家清算代码"),
    "ZANCC": ("South African National Clearing Code", "南非国家清算代码"),
    "AUBSB": ("Australian Bank State Branch Code BSB", "澳大利亚银行分支代码"),
    "ATBLZ": ("Austrian Bankleitzahl", "奥地利银行代码"),
    "PLKNR": ("Polish National Clearing Code", "波兰国家清算代码"),
    "NZNCC": ("New Zealand National Clearing Code", "新西兰国家清算代码"),
    "JPZGN": ("Japan Zengin Clearing Code", "日本全银清算代码"),
    "ITNCC": ("Italian Domestic Identification Code", "意大利国内识别码"),
    "INFSC": ("Indian Financial System Code", "印度金融系统代码"),
    "IENCC": ("Irish National Clearing Code", "爱尔兰国家清算代码"),
    "HKNCC": ("HongKong Bank Code", "香港银行代码"),
    "GRBIC": ("Helenic Bank Identification Code", "希腊银行识别码"),

    # Scheme Name Codes
    "CUID": ("CHIPS Universal Identifier", "CHIPS通用标识"),
    "UPIC": ("UPIC Identifier", "UPIC标识"),
    "AIIN": ("Issuer Identification Number", "签发者识别号"),
    "BBAN": ("BBAN Identifier", "BBAN标识"),
}


def translate_name(en_name: str) -> str:
    """Get Chinese translation for a field name."""
    return FIELD_TRANSLATIONS.get(en_name, en_name)


def translate_code(code: str) -> tuple:
    """Get (en, zh) translation for a code value."""
    if code in CODE_TRANSLATIONS:
        return CODE_TRANSLATIONS[code]
    return (code, code)


def clean_text(text: str) -> str:
    """Clean extracted text."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text.strip())
    text = text.replace('\n', ' ')
    return text


def parse_multiplicity(mult_str: str) -> tuple:
    """Parse multiplicity string like '[1..1]', '[0..1]', '[0..*]', '[1..*]'."""
    mult_str = clean_text(mult_str)
    match = re.search(r'\[(\d+)\.\.(\*|\d+)\]', mult_str)
    if match:
        min_val = int(match.group(1))
        max_val = match.group(2)
        return min_val, float('inf') if max_val == '*' else int(max_val)
    return 0, 1


def extract_type_info(type_str: str) -> dict:
    """Extract type information from type/code column."""
    info = {
        'type': '',
        'detail': type_str,
        'regex': '',
        'max_length': 0,
        'min_length': 0,
        'decimal_td': 0,
        'decimal_fd': 0,
        'min_value': 0,
        'max_value': 0,
    }

    type_str = clean_text(type_str)

    # text{m,M} pattern
    match = re.search(r'text\{(\d+),(\d+)\}', type_str)
    if match:
        info['type'] = 'text'
        info['min_length'] = int(match.group(1))
        info['max_length'] = int(match.group(2))
        return info

    # text{L} pattern (max length)
    match = re.search(r'text\{(\d+)\}', type_str)
    if match:
        info['type'] = 'text'
        info['max_length'] = int(match.group(1))
        return info

    # text without length
    if type_str.startswith('text'):
        info['type'] = 'text'
        return info

    # dateTime
    if 'dateTime' in type_str:
        info['type'] = 'dateTime'
        return info

    # date
    if type_str.startswith('date'):
        info['type'] = 'date'
        return info

    # time
    if type_str.startswith('time'):
        info['type'] = 'time'
        return info

    # boolean
    if 'boolean' in type_str:
        info['type'] = 'boolean'
        return info

    # decimal with td/fd
    match = re.search(r'td\s*=\s*(\d+)', type_str)
    if match:
        info['type'] = 'decimal'
        info['decimal_td'] = int(match.group(1))
        match_fd = re.search(r'fd\s*=\s*(\d+)', type_str)
        if match_fd:
            info['decimal_fd'] = int(match_fd.group(1))
        # min/max values
        match_range = re.search(r'(\d+(?:\.\d+)?)\s*<=\s*decimal\s*<=\s*(\d+(?:\.\d+)?)', type_str)
        if match_range:
            info['min_value'] = float(match_range.group(1))
            info['max_value'] = float(match_range.group(2))
        match_min = re.search(r'(\d+(?:\.\d+)?)\s*<=\s*decimal', type_str)
        if match_min and not match_range:
            info['min_value'] = float(match_min.group(1))
        return info

    # decimal
    if 'decimal' in type_str:
        info['type'] = 'decimal'
        return info

    # Check for regex patterns
    regex_match = re.search(r'\[([^\]]+)\{[^}]*\}([^\]]*)\]', type_str)
    if regex_match or re.search(r'[A-Z]\{', type_str):
        info['type'] = 'text'
        info['regex'] = type_str
        return info

    # Default to text
    info['type'] = 'text'
    return info


def extract_regex_from_type(type_str: str) -> str:
    """Extract regex pattern from type string."""
    # Look for patterns like [A-Z]{2,2}[0-9]{2,2}...
    if re.search(r'[A-Z]\{', type_str) or re.search(r'\[', type_str):
        return type_str
    return ""


class ISO20022Parser:
    """Parser for ISO 20022 PDF specifications."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.message_id = ""
        self.message_name_en = ""
        self.message_name_zh = ""
        self.collection_name = ""
        self.fields = []
        self.raw_tables = []
        self.app_hdr_fields = []
        self.document_fields = []

    def parse(self) -> dict:
        """Parse the PDF and return the message schema."""
        print(f"Parsing PDF: {self.pdf_path}")

        with pdfplumber.open(self.pdf_path) as pdf:
            # First, extract metadata from first few pages
            self._extract_metadata(pdf)

            # Extract all tables
            self._extract_tables(pdf)

            # Build field tree
            self._build_field_tree()

            # Enrich with code values and rules
            self._enrich_fields()

        result = {
            'message_id': self.message_id,
            'message_name_en': self.message_name_en,
            'message_name_zh': self.message_name_zh,
            'collection_name': self.collection_name,
            'app_hdr_fields': [f.to_dict() for f in self.app_hdr_fields],
            'document_fields': [f.to_dict() for f in self.document_fields],
        }

        print(f"Parsed message: {self.message_id} - {self.message_name_en}")
        print(f"  AppHdr fields: {len(self.app_hdr_fields)}")
        print(f"  Document fields: {len(self.document_fields)}")

        return result

    def _extract_metadata(self, pdf):
        """Extract message metadata from first pages."""
        for page in pdf.pages[:5]:
            text = page.extract_text() or ""

            # Extract message ID (e.g., pacs.008.001.08) - take the first match
            msg_match = re.search(r'(pacs|camt|pain|acmt|sese|setr|auth|cain)\.(\d{3})\.(\d{3})\.(\d{2})', text)
            if msg_match and not self.message_id:
                self.message_id = msg_match.group(0)

            # Extract message name from title patterns
            if not self.message_name_en:
                # Try: "FI To FI Customer Credit Transfer"
                name_match = re.search(r'(FI\s*To\s*FI\s*Customer\s*Credit\s*Transfer)', text, re.IGNORECASE)
                if name_match:
                    self.message_name_en = name_match.group(0).strip()
                # Try other common patterns
                if not self.message_name_en:
                    name_match = re.search(r'(Payment\s*Status\s*Report|Customer\s*Credit\s*Transfer|Account\s*Statement)', text, re.IGNORECASE)
                    if name_match:
                        self.message_name_en = name_match.group(0).strip()

            # Extract collection name
            coll_match = re.search(r'(CBPRPlus\s+SR\d{4}\s*\([^)]*\)?)', text)
            if coll_match and not self.collection_name:
                self.collection_name = coll_match.group(0).strip()

        # Set Chinese name based on message ID
        msg_zh_map = {
            'pacs.008.001.08': '金融机构间客户贷记转账',
            'pacs.009.001.08': '金融机构间贷记转账',
            'pacs.010.001.08': '金融机构间借记转账',
            'pacs.002.001.12': '支付状态报告',
            'pacs.004.001.10': '支付退汇',
            'camt.053.001.12': '账户对账单',
            'camt.054.001.12': '账户借/贷通知',
            'camt.056.001.10': '支付撤销',
            'pain.001.001.11': '客户发起的贷记转账',
            'pain.002.001.12': '支付状态报告(客户)',
        }
        self.message_name_zh = msg_zh_map.get(self.message_id, self.message_name_en)

    def _extract_tables(self, pdf):
        """Extract field definition tables from PDF."""
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""

            # Only process pages that have the field definition table
            if 'Index' not in text or 'XML Tag' not in text:
                continue

            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 3:
                    continue

                # Find the header row to identify column indices
                header_row = None
                header_idx = -1
                for i, row in enumerate(table):
                    if row and len(row) >= 5:
                        row_text = ' '.join(str(c or '') for c in row)
                        if 'Index' in row_text and 'XML Tag' in row_text:
                            header_row = row
                            header_idx = i
                            break

                if header_idx < 0:
                    continue

                # Parse data rows (skip header)
                for row in table[header_idx + 1:]:
                    if not row or len(row) < 4:
                        continue
                    # Skip empty rows
                    if all(not c or str(c).strip() == '' for c in row):
                        continue
                    self.raw_tables.append(row)

    def _build_field_tree(self):
        """Build hierarchical field tree from extracted table rows."""
        stack = []  # Stack of (level, field) for building tree

        for row in self.raw_tables:
            try:
                field = self._parse_row(row)
                if not field:
                    continue

                # Skip Excluded (X) fields — they must not be populated
                if field.restriction == 'X':
                    continue

                # Determine which section this belongs to
                if not self.app_hdr_fields and not self.document_fields:
                    # First fields are AppHdr
                    current_section = 'app_hdr'
                elif field.name_en == 'Document' or (field.xml_tag and 'Document' in field.xml_tag):
                    current_section = 'document'

                # Build tree using level
                while stack and stack[-1][0] >= field.level:
                    stack.pop()

                if stack:
                    parent = stack[-1][1]
                    parent.children.append(field)
                    field.parent_tag = parent.xml_tag
                else:
                    # Top-level field
                    if self.app_hdr_fields and field.level <= 1:
                        self.document_fields.append(field)
                    else:
                        self.app_hdr_fields.append(field)

                stack.append((field.level, field))

            except Exception as e:
                continue

        # If we didn't find a clear Document section, split based on structure
        if not self.document_fields and self.app_hdr_fields:
            self._split_sections()

    def _split_sections(self):
        """Split fields into AppHdr and Document sections."""
        # The root is typically "Full Message" with children:
        # [0]: Business Application Header V02 (AppHdr)
        # [1]: Document
        if not self.app_hdr_fields:
            return

        root = self.app_hdr_fields[0]
        children = root.children if hasattr(root, 'children') else []

        if not children:
            return

        app_hdr = None
        document = None

        for child in children:
            name = child.name_en if hasattr(child, 'name_en') else ''
            tag = child.xml_tag if hasattr(child, 'xml_tag') else ''

            if 'AppHdr' in tag or 'Business Application Header' in name:
                app_hdr = child
            elif 'Document' in name or 'FIToFI' in tag:
                document = child

        if app_hdr and document:
            self.app_hdr_fields = [app_hdr]
            self.document_fields = [document]
        elif app_hdr:
            self.app_hdr_fields = [app_hdr]
            self.document_fields = [c for c in children if c != app_hdr]

    def _parse_row(self, row) -> Optional[FieldDefinition]:
        """Parse a single table row into a FieldDefinition.
        
        Fixed column layout from ISO 20022 PDFs:
        [0]: Index (usually empty)
        [1]: Level (number)
        [2]: Name
        [3]: XML Tag (with <> brackets)
        [4]: Multiplicity ([min..max])
        [5]: Type / Code
        [6]: Restriction
        [7]: Additional details / Rules
        """
        if not row or len(row) < 5:
            return None

        f = FieldDefinition()

        # [0] Index - usually empty, skip
        # [1] Level
        lvl_str = clean_text(str(row[1]).replace('\n', '')) if row[1] else ''
        if lvl_str.isdigit():
            f.level = int(lvl_str)
        else:
            return None  # Not a valid field row

        # [2] Name
        if row[2]:
            f.name_en = clean_text(str(row[2]).replace('\n', ' '))
            f.name_zh = ""
        else:
            return None

        # [3] XML Tag
        if row[3]:
            tag = clean_text(str(row[3]).replace('\n', ''))
            tag = re.sub(r'[<>]', '', tag)
            f.xml_tag = tag

        # [4] Multiplicity
        if row[4]:
            mult_str = clean_text(str(row[4]).replace('\n', ''))
            f.multiplicity = mult_str
            min_v, max_v = parse_multiplicity(mult_str)
            f.mult_min = min_v
            f.mult_max = max_v

        # [5] Type / Code
        if row[5]:
            type_str = clean_text(str(row[5]).replace('\n', ' '))
            type_info = extract_type_info(type_str)
            f.type_code = type_info['type']
            f.type_detail = type_info['detail']
            f.regex_pattern = type_info['regex']
            f.max_length = type_info['max_length']
            f.min_length = type_info['min_length']
            f.decimal_td = type_info['decimal_td']
            f.decimal_fd = type_info['decimal_fd']
            f.min_value = type_info['min_value']
            f.max_value = type_info['max_value']

        # [6] Restriction — THIS IS THE PRIMARY SOURCE OF TRUTH
        # Restr overrides Mult when present. Patterns:
        #   [1..1]    → mandatory (overrides Mult [0..1])
        #   [0..1]    → max 1 (overrides Mult [0..*])
        #   [0..2]    → max 2 (overrides Mult [0..*] or [0..7])
        #   [0..3]    → max 3 (overrides Mult [0..*])
        #   [0..6]    → max 6 (overrides Mult [0..*])
        #   T/C       → Type/Code change only (no multiplicity override)
        #   FV        → Fixed Value
        #   X         → Excluded (must not populate)
        #   I         → Ignored
        # Combined: [1..1] T/C, [0..2] T/C, FV [1..1]
        if len(row) > 6 and row[6]:
            rest = clean_text(str(row[6]).replace('\n', ' '))
            if rest:
                f.restriction = rest

                # Parse multiplicity override from Restr
                restr_mult = re.search(r'\[(\d+)\.\.(\*|\d+)\]', rest)
                if restr_mult:
                    r_min = int(restr_mult.group(1))
                    r_max = float('inf') if restr_mult.group(2) == '*' else int(restr_mult.group(2))
                    # Override Mult with Restr
                    f.mult_min = r_min
                    f.mult_max = r_max
                    f.multiplicity = f'[{r_min}..{"*" if r_max == float("inf") else r_max}]'

                # Fixed Value
                if 'FV' in rest:
                    fv_match = re.search(r'(?:FixedValue|Fixed)[:\s]*(.+)', rest)
                    if fv_match:
                        f.fixed_value = fv_match.group(1).strip()
                        f.is_fixed = True
                    else:
                        f.is_fixed = True

                # Excluded — mark for removal
                if rest.startswith('X') and not restr_mult:
                    f.restriction = 'X'

        # [7] Additional details / Rules
        if len(row) > 7 and row[7]:
            additional = clean_text(str(row[7]).replace('\n', ' '))
            if additional:
                f.rules = additional
                rule_match = re.findall(r'R\d+', additional)
                if rule_match:
                    f.rules = ', '.join(rule_match)

        return f

    def _enrich_fields(self):
        """Enrich fields with code values from child rows.
        
        In ISO 20022 PDFs, enumerated code values appear as child rows at level+1
        under the parent field. They have NO xml_tag, just a Name and a code in
        the Type/Code column. For example:
        
          Level 4: Charge Bearer <ChrgBr> [1..1] text
            Level 5: Borne By Debtor DEBT
            Level 5: Borne By Creditor CRED
            Level 5: Shared SHAR
        """
        all_sections = [self.app_hdr_fields, self.document_fields]
        for section in all_sections:
            for root_field in section:
                self._enrich_field_tree(root_field)

    def _enrich_field_tree(self, field):
        """Recursively enrich a field and its children with code values."""
        children_to_keep = []
        code_values = []

        for child in field.children:
            # A code value row: has NO xml_tag, has a code in type_code or type_detail
            if not child.xml_tag and child.name_en:
                # Check if the type/code column contains a code value
                code = self._extract_code_from_field(child)
                if code:
                    desc_en, desc_zh = translate_code(code)
                    code_values.append(CodeValue(
                        code=code,
                        description_en=desc_en,
                        description_zh=desc_zh,
                        rules=child.rules if child.rules else '',
                    ))
                    continue  # Don't keep as a child field

            # Not a code value — keep and recurse
            children_to_keep.append(child)
            self._enrich_field_tree(child)

        if code_values:
            field.children = children_to_keep
            field.code_values = code_values

    def _extract_code_from_field(self, field) -> str:
        """Extract a code value from a field's type_detail or restriction."""
        # The code is often in type_detail (e.g., "DEBT", "SHAR", "INDA")
        candidates = [
            clean_text(field.type_detail),
            clean_text(field.restriction),
            clean_text(field.fixed_value),
        ]

        for candidate in candidates:
            if not candidate:
                continue
            # Code values are typically 2-6 uppercase letters/numbers
            match = re.match(r'^([A-Z0-9]{2,6})$', candidate)
            if match:
                return match.group(1)

        # Also check if type_detail looks like a code (no spaces, short)
        td = clean_text(field.type_detail)
        if td and len(td) <= 6 and ' ' not in td and not td.startswith('text') and not td.startswith('date'):
            # Could be a code
            if re.match(r'^[A-Z0-9]+$', td):
                return td

        return ""


def parse_pdf(pdf_path: str) -> dict:
    """Main entry point for PDF parsing."""
    parser = ISO20022Parser(pdf_path)
    return parser.parse()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse_pdf.py <input.pdf> [output.json]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    result = parse_pdf(pdf_path)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Schema saved to: {output_path}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
