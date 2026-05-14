window.COMPONENT_TEMPLATES = {
  "FinInstnId": {
    "leafCount": 20,
    "fields": [
      {
        "tag": "BICFI",
        "nameZh": "金融机构BIC",
        "nameEn": "BICFI",
        "type": "text"
      },
      {
        "tag": "ClrSysMmbId",
        "nameZh": "清算系统成员标识",
        "nameEn": "Clearing System Member Identification",
        "type": "container",
        "children": [
          {
            "tag": "ClrSysId",
            "nameZh": "清算系统标识",
            "nameEn": "Clearing System Identification",
            "type": "container",
            "children": [
              {
                "tag": "Cd",
                "nameZh": "代码",
                "nameEn": "Code",
                "type": "text",
                "maxLen": 5
              }
            ]
          },
          {
            "tag": "MmbId",
            "nameZh": "成员标识",
            "nameEn": "Member Identification",
            "type": "text",
            "maxLen": 35
          }
        ]
      },
      {
        "tag": "LEI",
        "nameZh": "法人实体标识",
        "nameEn": "LEI",
        "type": "text"
      },
      {
        "tag": "Nm",
        "nameZh": "名称",
        "nameEn": "Name",
        "type": "text",
        "maxLen": 140
      },
      {
        "tag": "PstlAdr",
        "nameZh": "邮政地址",
        "nameEn": "Postal Address",
        "type": "container",
        "children": [
          {
            "tag": "Dept",
            "nameZh": "部门",
            "nameEn": "Department",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "SubDept",
            "nameZh": "子部门",
            "nameEn": "Sub Department",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "StrtNm",
            "nameZh": "街道名称",
            "nameEn": "Street Name",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "BldgNb",
            "nameZh": "楼号",
            "nameEn": "Building Number",
            "type": "text",
            "maxLen": 16
          },
          {
            "tag": "BldgNm",
            "nameZh": "楼名",
            "nameEn": "Building Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "Flr",
            "nameZh": "楼层",
            "nameEn": "Floor",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "PstBx",
            "nameZh": "邮政信箱",
            "nameEn": "Post Box",
            "type": "text",
            "maxLen": 16
          },
          {
            "tag": "Room",
            "nameZh": "房间",
            "nameEn": "Room",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "PstCd",
            "nameZh": "邮编",
            "nameEn": "Post Code",
            "type": "text",
            "maxLen": 16
          },
          {
            "tag": "TwnNm",
            "nameZh": "城镇名称",
            "nameEn": "Town Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "TwnLctnNm",
            "nameZh": "城镇位置名称",
            "nameEn": "Town Location Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "DstrctNm",
            "nameZh": "区名",
            "nameEn": "District Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "CtrySubDvsn",
            "nameZh": "国家行政区",
            "nameEn": "Country Sub Division",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "Ctry",
            "nameZh": "国家",
            "nameEn": "Country",
            "type": "text"
          },
          {
            "tag": "AdrLine",
            "nameZh": "地址行",
            "nameEn": "Address Line",
            "type": "text",
            "maxLen": 70,
            "multMax": 2
          }
        ]
      }
    ]
  },
  "PartyIdentification": {
    "leafCount": 29,
    "fields": [
      {
        "tag": "Nm",
        "nameZh": "名称",
        "nameEn": "Name",
        "type": "text",
        "maxLen": 140
      },
      {
        "tag": "PstlAdr",
        "nameZh": "邮政地址",
        "nameEn": "Postal Address",
        "type": "container",
        "children": [
          {
            "tag": "Dept",
            "nameZh": "部门",
            "nameEn": "Department",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "SubDept",
            "nameZh": "子部门",
            "nameEn": "Sub Department",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "StrtNm",
            "nameZh": "街道名称",
            "nameEn": "Street Name",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "BldgNb",
            "nameZh": "楼号",
            "nameEn": "Building Number",
            "type": "text",
            "maxLen": 16
          },
          {
            "tag": "BldgNm",
            "nameZh": "楼名",
            "nameEn": "Building Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "Flr",
            "nameZh": "楼层",
            "nameEn": "Floor",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "PstBx",
            "nameZh": "邮政信箱",
            "nameEn": "Post Box",
            "type": "text",
            "maxLen": 16
          },
          {
            "tag": "Room",
            "nameZh": "房间",
            "nameEn": "Room",
            "type": "text",
            "maxLen": 70
          },
          {
            "tag": "PstCd",
            "nameZh": "邮编",
            "nameEn": "Post Code",
            "type": "text",
            "maxLen": 16
          },
          {
            "tag": "TwnNm",
            "nameZh": "城镇名称",
            "nameEn": "Town Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "TwnLctnNm",
            "nameZh": "城镇位置名称",
            "nameEn": "Town Location Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "DstrctNm",
            "nameZh": "区名",
            "nameEn": "District Name",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "CtrySubDvsn",
            "nameZh": "国家行政区",
            "nameEn": "Country Sub Division",
            "type": "text",
            "maxLen": 35
          },
          {
            "tag": "Ctry",
            "nameZh": "国家",
            "nameEn": "Country",
            "type": "text"
          },
          {
            "tag": "AdrLine",
            "nameZh": "地址行",
            "nameEn": "Address Line",
            "type": "text",
            "maxLen": 70,
            "multMax": 2
          }
        ]
      },
      {
        "tag": "Id",
        "nameZh": "标识",
        "nameEn": "Identification",
        "type": "container",
        "children": [
          {
            "tag": "OrgId",
            "nameZh": "组织标识",
            "nameEn": "Organisation Identification",
            "type": "container",
            "children": [
              {
                "tag": "AnyBIC",
                "nameZh": "任意BIC",
                "nameEn": "Any BIC",
                "type": "text"
              },
              {
                "tag": "LEI",
                "nameZh": "法人实体标识",
                "nameEn": "LEI",
                "type": "text"
              },
              {
                "tag": "Othr",
                "nameZh": "其他",
                "nameEn": "Other",
                "type": "container",
                "children": [
                  {
                    "tag": "Id",
                    "nameZh": "标识",
                    "nameEn": "Identification",
                    "type": "text",
                    "maxLen": 35
                  },
                  {
                    "tag": "SchmeNm",
                    "nameZh": "方案名称",
                    "nameEn": "Scheme Name",
                    "type": "container",
                    "children": [
                      {
                        "tag": "Cd",
                        "nameZh": "代码",
                        "nameEn": "Code",
                        "type": "text",
                        "maxLen": 4
                      }
                    ]
                  },
                  {
                    "tag": "Issr",
                    "nameZh": "签发者",
                    "nameEn": "Issuer",
                    "type": "text",
                    "maxLen": 35
                  }
                ],
                "multMax": 2
              }
            ]
          },
          {
            "tag": "PrvtId",
            "nameZh": "个人标识",
            "nameEn": "Private Identification",
            "type": "container",
            "children": [
              {
                "tag": "DtAndPlcOfBirth",
                "nameZh": "出生日期和地点",
                "nameEn": "Date And Place Of Birth",
                "type": "container",
                "children": [
                  {
                    "tag": "BirthDt",
                    "nameZh": "出生日期",
                    "nameEn": "Birth Date",
                    "type": "date"
                  },
                  {
                    "tag": "PrvcOfBirth",
                    "nameZh": "出生省份",
                    "nameEn": "Province Of Birth",
                    "type": "text",
                    "maxLen": 35
                  },
                  {
                    "tag": "CityOfBirth",
                    "nameZh": "出生城市",
                    "nameEn": "City Of Birth",
                    "type": "text",
                    "maxLen": 35
                  },
                  {
                    "tag": "CtryOfBirth",
                    "nameZh": "出生国家",
                    "nameEn": "Country Of Birth",
                    "type": "text"
                  }
                ]
              },
              {
                "tag": "Othr",
                "nameZh": "其他",
                "nameEn": "Other",
                "type": "container",
                "children": [
                  {
                    "tag": "Id",
                    "nameZh": "标识",
                    "nameEn": "Identification",
                    "type": "text",
                    "maxLen": 35
                  },
                  {
                    "tag": "SchmeNm",
                    "nameZh": "方案名称",
                    "nameEn": "Scheme Name",
                    "type": "container",
                    "children": [
                      {
                        "tag": "Cd",
                        "nameZh": "代码",
                        "nameEn": "Code",
                        "type": "text",
                        "maxLen": 4
                      }
                    ]
                  },
                  {
                    "tag": "Issr",
                    "nameZh": "签发者",
                    "nameEn": "Issuer",
                    "type": "text",
                    "maxLen": 35
                  }
                ],
                "multMax": 2
              }
            ]
          }
        ]
      },
      {
        "tag": "CtryOfRes",
        "nameZh": "居住国",
        "nameEn": "Country Of Residence",
        "type": "text"
      }
    ]
  }
};

window.COMPONENT_INSTANCES = [{"type": "PartyIdentification", "pathPrefix": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_RslvdCase_Cretr_Pty", "isoPath": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.RslvdCase.Cretr.Pty", "nameZh": "当事方", "nameEn": "Party", "multMin": 0, "multMax": 1}, {"type": "FinInstnId", "pathPrefix": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_RslvdCase_Cretr_Agt_FinInstnId", "isoPath": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.RslvdCase.Cretr.Agt.FinInstnId", "nameZh": "金融机构标识", "nameEn": "Financial Institution Identification", "multMin": 0, "multMax": 1}, {"type": "PartyIdentification", "pathPrefix": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_CxlStsRsnInf_Orgtr", "isoPath": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.CxlStsRsnInf.Orgtr", "nameZh": "发起人", "nameEn": "Originator", "multMin": 0, "multMax": 1, "overrides": {"mandatory": ["TwnNm", "Ctry"]}}];

window.FIELD_META = [{"xml_tag": "AppHdr", "name_en": "Business Application Header V02 (head.001.001.02)", "name_zh": "业务应用头V02 (head.001.001.02)", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr", "iso_path": "AppHdr", "code_values": [], "business_rules": []}, {"xml_tag": "CharSet", "name_en": "Character Set", "name_zh": "字符集", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_CharSet", "iso_path": "AppHdr.CharSet", "code_values": [], "business_rules": []}, {"xml_tag": "Fr", "name_en": "From", "name_zh": "发送方", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr", "iso_path": "AppHdr.Fr", "code_values": [], "business_rules": []}, {"xml_tag": "FIId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId", "iso_path": "AppHdr.Fr.FIId", "code_values": [], "business_rules": []}, {"xml_tag": "FinInstnId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId", "iso_path": "AppHdr.Fr.FIId.FinInstnId", "code_values": [], "business_rules": []}, {"xml_tag": "BICFI", "name_en": "BICFI", "name_zh": "金融机构BIC", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId_BICFI", "iso_path": "AppHdr.Fr.FIId.FinInstnId.BICFI", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysMmbId", "name_en": "Clearing System Member Identification", "name_zh": "清算系统成员标识", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId_ClrSysMmbId", "iso_path": "AppHdr.Fr.FIId.FinInstnId.ClrSysMmbId", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysId", "name_en": "Clearing System Identification", "name_zh": "清算系统标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId_ClrSysMmbId_ClrSysId", "iso_path": "AppHdr.Fr.FIId.FinInstnId.ClrSysMmbId.ClrSysId", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 5, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId_ClrSysMmbId_ClrSysId_Cd", "iso_path": "AppHdr.Fr.FIId.FinInstnId.ClrSysMmbId.ClrSysId.Cd", "code_values": [], "business_rules": []}, {"xml_tag": "MmbId", "name_en": "Member Identification", "name_zh": "成员标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId_ClrSysMmbId_MmbId", "iso_path": "AppHdr.Fr.FIId.FinInstnId.ClrSysMmbId.MmbId", "code_values": [], "business_rules": []}, {"xml_tag": "LEI", "name_en": "LEI", "name_zh": "法人实体标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Fr_FIId_FinInstnId_LEI", "iso_path": "AppHdr.Fr.FIId.FinInstnId.LEI", "code_values": [], "business_rules": []}, {"xml_tag": "To", "name_en": "To", "name_zh": "接收方", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To", "iso_path": "AppHdr.To", "code_values": [], "business_rules": []}, {"xml_tag": "FIId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId", "iso_path": "AppHdr.To.FIId", "code_values": [], "business_rules": []}, {"xml_tag": "FinInstnId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId", "iso_path": "AppHdr.To.FIId.FinInstnId", "code_values": [], "business_rules": []}, {"xml_tag": "BICFI", "name_en": "BICFI", "name_zh": "金融机构BIC", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId_BICFI", "iso_path": "AppHdr.To.FIId.FinInstnId.BICFI", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysMmbId", "name_en": "Clearing System Member Identification", "name_zh": "清算系统成员标识", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId_ClrSysMmbId", "iso_path": "AppHdr.To.FIId.FinInstnId.ClrSysMmbId", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysId", "name_en": "Clearing System Identification", "name_zh": "清算系统标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId_ClrSysMmbId_ClrSysId", "iso_path": "AppHdr.To.FIId.FinInstnId.ClrSysMmbId.ClrSysId", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 5, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId_ClrSysMmbId_ClrSysId_Cd", "iso_path": "AppHdr.To.FIId.FinInstnId.ClrSysMmbId.ClrSysId.Cd", "code_values": [], "business_rules": []}, {"xml_tag": "MmbId", "name_en": "Member Identification", "name_zh": "成员标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId_ClrSysMmbId_MmbId", "iso_path": "AppHdr.To.FIId.FinInstnId.ClrSysMmbId.MmbId", "code_values": [], "business_rules": []}, {"xml_tag": "LEI", "name_en": "LEI", "name_zh": "法人实体标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_To_FIId_FinInstnId_LEI", "iso_path": "AppHdr.To.FIId.FinInstnId.LEI", "code_values": [], "business_rules": []}, {"xml_tag": "BizMsgIdr", "name_en": "Business Message Identifier", "name_zh": "业务消息标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_BizMsgIdr", "iso_path": "AppHdr.BizMsgIdr", "code_values": [], "business_rules": [{"name": "CBPR_Business_Message_Identifier_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/BusinessMessageIdentifier", "text": "The Business Message Identifier is the unique identifier of the Business Message instance that is being transported with this header, as defined by the sending application or system. Must contain the Message Identification element from the Group Header of the un- derlying message, where available (as is typically the case with pacs, pain, and camt messages, for example). If Message Identification is not available in the underlying message, then this field must contain the unique identifier of th"}, {"name": "CBPR_Business_Message_Identifier_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related/BusinessMessageIdentifier", "text": "The Business Message Identifier is the unique identifier of the Business Message instance that is being transported with this header, as defined by the sending application or system. Must contain the Message Identification element from the Group Header of the un- derlying message, where available (as is typically the case with pacs, pain, and camt messages, for example). If Message Identification is not available in the underlying message, then this element must contain the unique identifier of "}]}, {"xml_tag": "MsgDefIdr", "name_en": "Message Definition Identifier", "name_zh": "消息定义标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": true, "fixed_value": "", "form_name": "AH_AppHdr_MsgDefIdr", "iso_path": "AppHdr.MsgDefIdr", "code_values": [], "business_rules": [{"name": "CBPR_Message_Definition_Identifier_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related/MessageDefinitionIdentifier", "text": "The Message Definition Identifier of the Business Message instance that is be- ing transported with this header. In general, it must be formatted exactly as it appears in the namespace of the Business Message instance."}]}, {"xml_tag": "BizSvc", "name_en": "Business Service", "name_zh": "业务服务", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": true, "fixed_value": "", "form_name": "AH_AppHdr_BizSvc", "iso_path": "AppHdr.BizSvc", "code_values": [], "business_rules": [{"name": "CBPR_Related_BAH_Business_Service_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related/BusinessService", "text": "If related BAH is present, it should transport the element Business Service."}]}, {"xml_tag": "MktPrctc", "name_en": "Market Practice", "name_zh": "市场惯例", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_MktPrctc", "iso_path": "AppHdr.MktPrctc", "code_values": [], "business_rules": []}, {"xml_tag": "Regy", "name_en": "Registry", "name_zh": "注册机构", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 350, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_MktPrctc_Regy", "iso_path": "AppHdr.MktPrctc.Regy", "code_values": [], "business_rules": []}, {"xml_tag": "Id", "name_en": "Identification", "name_zh": "标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 2048, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_MktPrctc_Id", "iso_path": "AppHdr.MktPrctc.Id", "code_values": [], "business_rules": []}, {"xml_tag": "CreDt", "name_en": "Creation Date", "name_zh": "创建日期", "type_code": "dateTime", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_CreDt", "iso_path": "AppHdr.CreDt", "code_values": [], "business_rules": []}, {"xml_tag": "CpyDplct", "name_en": "Copy Duplicate", "name_zh": "副本/重复", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_CpyDplct", "iso_path": "AppHdr.CpyDplct", "code_values": [{"code": "CODU", "description_en": "Copy Duplicate", "description_zh": "副本重复", "rules": ""}, {"code": "COPY", "description_en": "Copy", "description_zh": "副本", "rules": ""}, {"code": "DUPL", "description_en": "Duplicate", "description_zh": "重复", "rules": ""}], "business_rules": []}, {"xml_tag": "PssblDplct", "name_en": "Possible Duplicate", "name_zh": "可能重复", "type_code": "boolean", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_PssblDplct", "iso_path": "AppHdr.PssblDplct", "code_values": [], "business_rules": []}, {"xml_tag": "Prty", "name_en": "Priority", "name_zh": "优先级", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Prty", "iso_path": "AppHdr.Prty", "code_values": [{"code": "HIGH", "description_en": "High", "description_zh": "高", "rules": ""}, {"code": "NORM", "description_en": "Normal", "description_zh": "普通", "rules": ""}], "business_rules": []}, {"xml_tag": "Rltd", "name_en": "Related", "name_zh": "关联", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd", "iso_path": "AppHdr.Rltd", "code_values": [], "business_rules": [{"name": "CBPR_Related_Business_Application_Header_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related", "text": "If used, the Related BAH must transport the exact same information as in the BAH of the related message. 4.2 Payload Building Blocks Note The following chapter identifies the building blocks of the CBPRPlus SR2026 (Combined) / CBPRPlus-camt.029.001.09_ResolutionOfInvestigation payload definition. Usage Guideline on Root Node • on camt.029.001.09/"}, {"name": "CBPR_Cancellation_Reason_FormalRule", "type": "FormalRule", "path": "camt.029.001.09/.header/Related", "text": "If Status/Confirmation =RJCR then CancellationStatus ReasonInformation/Reason is mandatory. ---- For each [Full Message/Document/ResolutionOfInvestigationV09], if every occurrence of [ResolutionOfInvestigationV09/Status/Confirmation] has value included in the following list 'RJCR' , then at least one occurrence of the following element(s) [ResolutionOfInvestiga- tionV09/CancellationDetails/TransactionInformationAndStatus/CancellationStatus- ReasonInformation/Reason] must be present 20 February 2"}]}, {"xml_tag": "CharSet", "name_en": "Character Set", "name_zh": "字符集", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_CharSet", "iso_path": "AppHdr.Rltd.CharSet", "code_values": [], "business_rules": []}, {"xml_tag": "Fr", "name_en": "From", "name_zh": "发送方", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr", "iso_path": "AppHdr.Rltd.Fr", "code_values": [], "business_rules": []}, {"xml_tag": "FIId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId", "iso_path": "AppHdr.Rltd.Fr.FIId", "code_values": [], "business_rules": []}, {"xml_tag": "FinInstnId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId", "code_values": [], "business_rules": []}, {"xml_tag": "BICFI", "name_en": "BICFI", "name_zh": "金融机构BIC", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId_BICFI", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId.BICFI", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysMmbId", "name_en": "Clearing System Member Identification", "name_zh": "清算系统成员标识", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId_ClrSysMmbId", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId.ClrSysMmbId", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysId", "name_en": "Clearing System Identification", "name_zh": "清算系统标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId_ClrSysMmbId_ClrSysId", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId.ClrSysMmbId.ClrSysId", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 5, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId_ClrSysMmbId_ClrSysId_Cd", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId.ClrSysMmbId.ClrSysId.Cd", "code_values": [], "business_rules": []}, {"xml_tag": "MmbId", "name_en": "Member Identification", "name_zh": "成员标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId_ClrSysMmbId_MmbId", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId.ClrSysMmbId.MmbId", "code_values": [], "business_rules": []}, {"xml_tag": "LEI", "name_en": "LEI", "name_zh": "法人实体标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Fr_FIId_FinInstnId_LEI", "iso_path": "AppHdr.Rltd.Fr.FIId.FinInstnId.LEI", "code_values": [], "business_rules": []}, {"xml_tag": "To", "name_en": "To", "name_zh": "接收方", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To", "iso_path": "AppHdr.Rltd.To", "code_values": [], "business_rules": []}, {"xml_tag": "FIId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId", "iso_path": "AppHdr.Rltd.To.FIId", "code_values": [], "business_rules": []}, {"xml_tag": "FinInstnId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId", "code_values": [], "business_rules": []}, {"xml_tag": "BICFI", "name_en": "BICFI", "name_zh": "金融机构BIC", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId_BICFI", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId.BICFI", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysMmbId", "name_en": "Clearing System Member Identification", "name_zh": "清算系统成员标识", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId_ClrSysMmbId", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId.ClrSysMmbId", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysId", "name_en": "Clearing System Identification", "name_zh": "清算系统标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId_ClrSysMmbId_ClrSysId", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId.ClrSysMmbId.ClrSysId", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 5, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId_ClrSysMmbId_ClrSysId_Cd", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId.ClrSysMmbId.ClrSysId.Cd", "code_values": [], "business_rules": []}, {"xml_tag": "MmbId", "name_en": "Member Identification", "name_zh": "成员标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId_ClrSysMmbId_MmbId", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId.ClrSysMmbId.MmbId", "code_values": [], "business_rules": []}, {"xml_tag": "LEI", "name_en": "LEI", "name_zh": "法人实体标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_To_FIId_FinInstnId_LEI", "iso_path": "AppHdr.Rltd.To.FIId.FinInstnId.LEI", "code_values": [], "business_rules": []}, {"xml_tag": "BizMsgIdr", "name_en": "Business Message Identifier", "name_zh": "业务消息标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_BizMsgIdr", "iso_path": "AppHdr.Rltd.BizMsgIdr", "code_values": [], "business_rules": [{"name": "CBPR_Business_Message_Identifier_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/BusinessMessageIdentifier", "text": "The Business Message Identifier is the unique identifier of the Business Message instance that is being transported with this header, as defined by the sending application or system. Must contain the Message Identification element from the Group Header of the un- derlying message, where available (as is typically the case with pacs, pain, and camt messages, for example). If Message Identification is not available in the underlying message, then this field must contain the unique identifier of th"}, {"name": "CBPR_Business_Message_Identifier_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related/BusinessMessageIdentifier", "text": "The Business Message Identifier is the unique identifier of the Business Message instance that is being transported with this header, as defined by the sending application or system. Must contain the Message Identification element from the Group Header of the un- derlying message, where available (as is typically the case with pacs, pain, and camt messages, for example). If Message Identification is not available in the underlying message, then this element must contain the unique identifier of "}]}, {"xml_tag": "MsgDefIdr", "name_en": "Message Definition Identifier", "name_zh": "消息定义标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_MsgDefIdr", "iso_path": "AppHdr.Rltd.MsgDefIdr", "code_values": [], "business_rules": [{"name": "CBPR_Message_Definition_Identifier_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related/MessageDefinitionIdentifier", "text": "The Message Definition Identifier of the Business Message instance that is be- ing transported with this header. In general, it must be formatted exactly as it appears in the namespace of the Business Message instance."}]}, {"xml_tag": "BizSvc", "name_en": "Business Service", "name_zh": "业务服务", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_BizSvc", "iso_path": "AppHdr.Rltd.BizSvc", "code_values": [], "business_rules": [{"name": "CBPR_Related_BAH_Business_Service_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/.header/Related/BusinessService", "text": "If related BAH is present, it should transport the element Business Service."}]}, {"xml_tag": "CreDt", "name_en": "Creation Date", "name_zh": "创建日期", "type_code": "dateTime", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_CreDt", "iso_path": "AppHdr.Rltd.CreDt", "code_values": [], "business_rules": []}, {"xml_tag": "CpyDplct", "name_en": "Copy Duplicate", "name_zh": "副本/重复", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_CpyDplct", "iso_path": "AppHdr.Rltd.CpyDplct", "code_values": [{"code": "CODU", "description_en": "Copy Duplicate", "description_zh": "副本重复", "rules": ""}, {"code": "COPY", "description_en": "Copy", "description_zh": "副本", "rules": ""}, {"code": "DUPL", "description_en": "Duplicate", "description_zh": "重复", "rules": ""}], "business_rules": []}, {"xml_tag": "Prty", "name_en": "Priority", "name_zh": "优先级", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "AH_AppHdr_Rltd_Prty", "iso_path": "AppHdr.Rltd.Prty", "code_values": [{"code": "HIGH", "description_en": "High", "description_zh": "高", "rules": ""}, {"code": "NORM", "description_en": "Normal", "description_zh": "普通", "rules": ""}], "business_rules": []}, {"xml_tag": "", "name_en": "Document", "name_zh": "文档", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_", "iso_path": "Document.", "code_values": [], "business_rules": []}, {"xml_tag": "RsltnOfInvstgtn", "name_en": "Resolution Of Investigation V09 (camt.029.001.09)", "name_zh": "调查处理V09 (camt.029.001.09)", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn", "iso_path": "Document.RsltnOfInvstgtn", "code_values": [], "business_rules": []}, {"xml_tag": "Assgnmt", "name_en": "Assignment", "name_zh": "任务分配", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt", "code_values": [], "business_rules": []}, {"xml_tag": "Id", "name_en": "Identification", "name_zh": "标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Id", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Id", "code_values": [], "business_rules": []}, {"xml_tag": "Assgnr", "name_en": "Assigner", "name_zh": "转让方", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr", "code_values": [], "business_rules": []}, {"xml_tag": "Agt", "name_en": "Agent", "name_zh": "代理行", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt", "code_values": [], "business_rules": []}, {"xml_tag": "FinInstnId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId", "code_values": [], "business_rules": []}, {"xml_tag": "BICFI", "name_en": "BICFI", "name_zh": "金融机构BIC", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId_BICFI", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId.BICFI", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysMmbId", "name_en": "Clearing System Member Identification", "name_zh": "清算系统成员标识", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId_ClrSysMmbId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId.ClrSysMmbId", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysId", "name_en": "Clearing System Identification", "name_zh": "清算系统标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId_ClrSysMmbId_ClrSysId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId.ClrSysMmbId.ClrSysId", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 5, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId_ClrSysMmbId_ClrSysId_Cd", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId.ClrSysMmbId.ClrSysId.Cd", "code_values": [], "business_rules": []}, {"xml_tag": "MmbId", "name_en": "Member Identification", "name_zh": "成员标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId_ClrSysMmbId_MmbId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId.ClrSysMmbId.MmbId", "code_values": [], "business_rules": []}, {"xml_tag": "LEI", "name_en": "LEI", "name_zh": "法人实体标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgnr_Agt_FinInstnId_LEI", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgnr.Agt.FinInstnId.LEI", "code_values": [], "business_rules": []}, {"xml_tag": "Assgne", "name_en": "Assignee", "name_zh": "受让方", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne", "code_values": [], "business_rules": []}, {"xml_tag": "Agt", "name_en": "Agent", "name_zh": "代理行", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt", "code_values": [], "business_rules": []}, {"xml_tag": "FinInstnId", "name_en": "Financial Institution Identification", "name_zh": "金融机构标识", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId", "code_values": [], "business_rules": []}, {"xml_tag": "BICFI", "name_en": "BICFI", "name_zh": "金融机构BIC", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId_BICFI", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId.BICFI", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysMmbId", "name_en": "Clearing System Member Identification", "name_zh": "清算系统成员标识", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId_ClrSysMmbId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId.ClrSysMmbId", "code_values": [], "business_rules": []}, {"xml_tag": "ClrSysId", "name_en": "Clearing System Identification", "name_zh": "清算系统标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId_ClrSysMmbId_ClrSysId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId.ClrSysMmbId.ClrSysId", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 5, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId_ClrSysMmbId_ClrSysId_Cd", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId.ClrSysMmbId.ClrSysId.Cd", "code_values": [], "business_rules": []}, {"xml_tag": "MmbId", "name_en": "Member Identification", "name_zh": "成员标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId_ClrSysMmbId_MmbId", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId.ClrSysMmbId.MmbId", "code_values": [], "business_rules": []}, {"xml_tag": "LEI", "name_en": "LEI", "name_zh": "法人实体标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_Assgne_Agt_FinInstnId_LEI", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.Assgne.Agt.FinInstnId.LEI", "code_values": [], "business_rules": []}, {"xml_tag": "CreDtTm", "name_en": "Creation Date Time", "name_zh": "创建日期时间", "type_code": "dateTime", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Assgnmt_CreDtTm", "iso_path": "Document.RsltnOfInvstgtn.Assgnmt.CreDtTm", "code_values": [], "business_rules": []}, {"xml_tag": "Sts", "name_en": "Status", "name_zh": "状态", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Sts", "iso_path": "Document.RsltnOfInvstgtn.Sts", "code_values": [], "business_rules": []}, {"xml_tag": "Conf", "name_en": "Confirmation", "name_zh": "确认", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 4, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_Sts_Conf", "iso_path": "Document.RsltnOfInvstgtn.Sts.Conf", "code_values": [{"code": "CNCL", "description_en": "CNCL", "description_zh": "CNCL", "rules": ""}, {"code": "PDCR", "description_en": "PDCR", "description_zh": "PDCR", "rules": ""}, {"code": "RJCR", "description_en": "RJCR", "description_zh": "RJCR", "rules": ""}], "business_rules": []}, {"xml_tag": "CxlDtls", "name_en": "Cancellation Details", "name_zh": "撤销明细", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls", "code_values": [], "business_rules": []}, {"xml_tag": "TxInfAndSts", "name_en": "Transaction Information And Status", "name_zh": "交易信息及状态", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts", "code_values": [], "business_rules": []}, {"xml_tag": "CxlStsId", "name_en": "Cancellation Status Identification", "name_zh": "撤销状态标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_CxlStsId", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.CxlStsId", "code_values": [], "business_rules": []}, {"xml_tag": "RslvdCase", "name_en": "Resolved Case", "name_zh": "已解决案件", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_RslvdCase", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.RslvdCase", "code_values": [], "business_rules": []}, {"xml_tag": "Id", "name_en": "Identification", "name_zh": "标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_RslvdCase_Id", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.RslvdCase.Id", "code_values": [], "business_rules": []}, {"xml_tag": "Cretr", "name_en": "Creator", "name_zh": "创建者", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_RslvdCase_Cretr", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.RslvdCase.Cretr", "code_values": [], "business_rules": []}, {"xml_tag": "Agt", "name_en": "Agent", "name_zh": "代理行", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_RslvdCase_Cretr_Agt", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.RslvdCase.Cretr.Agt", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlGrpInf", "name_en": "Original Group Information", "name_zh": "原始组信息", "type_code": "", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlGrpInf", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlGrpInf", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlMsgId", "name_en": "Original Message Identification", "name_zh": "原始消息标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlGrpInf_OrgnlMsgId", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlGrpInf.OrgnlMsgId", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlMsgNmId", "name_en": "Original Message Name Identification", "name_zh": "原始消息名称标识", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlGrpInf_OrgnlMsgNmId", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlGrpInf.OrgnlMsgNmId", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlCreDtTm", "name_en": "Original Creation Date Time", "name_zh": "原始创建日期时间", "type_code": "dateTime", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlGrpInf_OrgnlCreDtTm", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlGrpInf.OrgnlCreDtTm", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlInstrId", "name_en": "Original Instruction Identification", "name_zh": "原始指令标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlInstrId", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlInstrId", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlEndToEndId", "name_en": "Original End To End Identification", "name_zh": "原始端到端标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlEndToEndId", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlEndToEndId", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlTxId", "name_en": "Original Transaction Identification", "name_zh": "原始交易标识", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlTxId", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlTxId", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlClrSysRef", "name_en": "Original Clearing System Reference", "name_zh": "原始清算系统参考", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 35, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlClrSysRef", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlClrSysRef", "code_values": [], "business_rules": []}, {"xml_tag": "OrgnlUETR", "name_en": "Original UETR", "name_zh": "原始唯一端到端交易引用", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_OrgnlUETR", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.OrgnlUETR", "code_values": [], "business_rules": [{"name": "CBPR_Original_UETR_TextualRule", "type": "TextualRule", "path": "camt.029.001.09/CancellationDetails/TransactionInformationAndStatus/OriginalUETR", "text": "Must transport the UETR of the underlying transaction that is requested to be cancelled."}]}, {"xml_tag": "CxlStsRsnInf", "name_en": "Cancellation Status Reason Information", "name_zh": "撤销状态原因信息", "type_code": "", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_CxlStsRsnInf", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.CxlStsRsnInf", "code_values": [], "business_rules": []}, {"xml_tag": "Rsn", "name_en": "Reason", "name_zh": "原因", "type_code": "text", "mult_min": 0, "mult_max": 1, "regex_pattern": "", "max_length": 0, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_CxlStsRsnInf_Rsn", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.CxlStsRsnInf.Rsn", "code_values": [], "business_rules": []}, {"xml_tag": "Cd", "name_en": "Code", "name_zh": "代码", "type_code": "text", "mult_min": 1, "mult_max": 1, "regex_pattern": "", "max_length": 4, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_CxlStsRsnInf_Rsn_Cd", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.CxlStsRsnInf.Rsn.Cd", "code_values": [{"code": "NOOR", "description_en": "NOOR", "description_zh": "NOOR", "rules": ""}, {"code": "NOAS", "description_en": "NOAS", "description_zh": "NOAS", "rules": ""}, {"code": "ARDT", "description_en": "ARDT", "description_zh": "ARDT", "rules": ""}, {"code": "CUST", "description_en": "CUST", "description_zh": "CUST", "rules": ""}, {"code": "AGNT", "description_en": "AGNT", "description_zh": "AGNT", "rules": ""}, {"code": "LEGL", "description_en": "LEGL", "description_zh": "LEGL", "rules": ""}, {"code": "AC04", "description_en": "AC04", "description_zh": "AC04", "rules": ""}, {"code": "AM04", "description_en": "AM04", "description_zh": "AM04", "rules": ""}, {"code": "PTNA", "description_en": "PTNA", "description_zh": "PTNA", "rules": ""}, {"code": "RQDA", "description_en": "RQDA", "description_zh": "RQDA", "rules": ""}, {"code": "INDM", "description_en": "INDM", "description_zh": "INDM", "rules": ""}], "business_rules": []}, {"xml_tag": "AddtlInf", "name_en": "Additional Information", "name_zh": "附加信息", "type_code": "text", "mult_min": 0, "mult_max": 2, "regex_pattern": "", "max_length": 105, "decimal_td": 0, "decimal_fd": 0, "is_fixed": false, "fixed_value": "", "form_name": "DOC_RsltnOfInvstgtn_CxlDtls_TxInfAndSts_CxlStsRsnInf_AddtlInf", "iso_path": "Document.RsltnOfInvstgtn.CxlDtls.TxInfAndSts.CxlStsRsnInf.AddtlInf", "code_values": [], "business_rules": []}];
