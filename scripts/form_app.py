"""Generate the main app.js for the v4 form (ES5 + jQuery, IE8+ compatible).

This module produces the full-featured application script including:
- Field validation (BIC, IBAN, LEI, date, decimal, etc.)
- Template system
- Field search with navigation
- Progress bar
- Theme switching (class-based, no CSS variables)
- JSON/XML preview and export
- Import JSON
- Audit/readonly mode
- Multi-language (zh/en/fr)
- Auto-save drafts
- Repeat groups
- Business rules
- At-least-one groups
- Currency consistency
- Quick fill panel
"""

from __future__ import annotations

from form_api import get_form_api_script


def get_app_js(message_id: str = "pacs.008.001.08") -> str:
    """Return the complete app.js content."""
    header = _APP_HEADER.replace("{MESSAGE_ID}", message_id)
    return header + _APP_BODY + "\n" + get_form_api_script()


# ==================== APP HEADER (IIFE open + globals) ====================

_APP_HEADER = r"""(function($, window, undefined) {
"use strict";

var MESSAGE_ID = "{MESSAGE_ID}";
var DRAFT_KEY = "iso20022-draft-" + MESSAGE_ID;
var QUICK_DRAFT_KEY = "iso20022-quick-draft-" + MESSAGE_ID;

var fieldMeta = window.FIELD_META || [];
var formData = {};
var validationErrors = {};
var requiredOnlyMode = false;
var auditMode = false;
var currentLang = "zh";
var locateMatches = [];
var locateIdx = -1;
var autoSaveTimer = null;

"""

# ==================== APP BODY (all modules) ====================

_APP_BODY = r"""
// ============================================================
// Module 1: Utilities
// ============================================================

function escapeCssAttr(value) {
  if (!value) return "";
  return value.replace(/[\\"']/g, "\\$&");
}

function escapeHtml(str) {
  if (!str) return "";
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

function findFieldMeta(name) {
  for (var i = 0; i < fieldMeta.length; i++) {
    if (fieldMeta[i].form_name === name) return fieldMeta[i];
  }
  return null;
}

function showToast(message) {
  var $toast = $("#toast");
  $toast.text(message).addClass("toast-show");
  setTimeout(function() {
    $toast.removeClass("toast-show");
  }, 2500);
}

function showConfirm(title, message, onConfirm, onCancel) {
  $("#confirmTitle").text(title);
  $("#confirmBody").text(message);
  $("#confirmOk").off("click").on("click", function() {
    $("#confirmModal").modal("hide");
    if (onConfirm) onConfirm();
  });
  $("#confirmModal").off("hidden.bs.modal").on("hidden.bs.modal", function() {
    if (onCancel) onCancel();
    onCancel = null;
  });
  $("#confirmModal").modal("show");
}

// ============================================================
// Module 2: I18N
// ============================================================

var I18N = {
  zh: {
    required: "必填",
    optional: "可选",
    fixed: "固定值",
    searchPlaceholder: "输入字段名定位 (中文/英文/XML标签)...",
    searchCount: "找到 {0} 个字段",
    searchNone: "无匹配结果",
    validatePass: "校验通过，无错误",
    validateFail: "发现 {0} 个错误",
    requiredFilter: "仅显示必填",
    showAll: "显示全部",
    auditMode: "审核模式",
    auditExit: "退出审核",
    auditOn: "审核模式 - 所有字段已锁定",
    auditOff: "已退出审核模式",
    templateApplied: "模板「{0}」已应用",
    templateConfirm: "应用模板将覆盖当前数据，是否继续？",
    copiedJSON: "JSON已复制到剪贴板",
    copiedXML: "XML已复制到剪贴板",
    draftCleared: "表单已清空",
    draftRestored: "草稿已恢复",
    rmtSynced: "业务字段已同步到表单",
    atLeastOne: "「{0}」下至少填写一项",
    pleaseSelect: "-- 请选择 --",
    progressLabel: "必填字段完成度",
    progressText: "{0} / {1}",
    addItem: "添加",
    removeItem: "删除",
    maxReached: "已达到最大数量 ({0})",
    importTitle: "导入 JSON",
    importHint: "粘贴之前导出的 JSON 数据",
    importSuccess: "JSON 导入成功",
    importError: "JSON 格式错误",
    clearConfirmTitle: "清除确认",
    clearConfirmMsg: "确定要清空所有已填数据？",
    themeLight: "浅色",
    themeDark: "深色",
    saveDraft: "暂存",
    autoSaved: "已自动暂存",
    fieldRequired: "此字段为必填项",
    fieldMaxLen: "超出最大长度 {0}",
    fieldInvalidBIC: "BIC格式错误 (8或11位字母数字)",
    fieldInvalidIBAN: "IBAN校验失败",
    fieldInvalidLEI: "LEI格式错误 (20位)",
    fieldInvalidCountry: "国家代码格式错误 (2位大写字母)",
    fieldInvalidCurrency: "币种代码格式错误 (3位大写字母)",
    fieldInvalidDecimal: "小数位数超出限制 (最多{0}位)",
    fieldInvalidE2E: "EndToEndId格式错误",
    fieldInvalidSvcLvl: "无效的服务级别代码",
    currencyMatch: "币种相同，无需填写汇率",
    currencyDiff: "币种不同，请填写汇率",
    r14Conflict: "BICFI已填写时不可填写Name",
    conditionalRef: "已填写结构化汇款信息时，CdtrRefInf/Ref为必填",
    choiceSelect: "选择类型：",
    valueNotAllowed: "不允许使用值: {0}",
    conditionalRequired: "当 {0} 有值时此字段为必填"
  },
  en: {
    required: "Required",
    optional: "Optional",
    fixed: "Fixed",
    searchPlaceholder: "Locate field (name/tag)...",
    searchCount: "{0} field(s) found",
    searchNone: "No match",
    validatePass: "Validation passed",
    validateFail: "{0} error(s) found",
    requiredFilter: "Required only",
    showAll: "Show all",
    auditMode: "Audit mode",
    auditExit: "Exit audit",
    auditOn: "Audit mode - all fields locked",
    auditOff: "Exited audit mode",
    templateApplied: "Template \"{0}\" applied",
    templateConfirm: "Applying template will overwrite current data. Continue?",
    copiedJSON: "JSON copied",
    copiedXML: "XML copied",
    draftCleared: "Form cleared",
    draftRestored: "Draft restored",
    rmtSynced: "Fields synced to form",
    atLeastOne: "At least one field under \"{0}\" is required",
    pleaseSelect: "-- Select --",
    progressLabel: "Required fields progress",
    progressText: "{0} / {1}",
    addItem: "Add",
    removeItem: "Remove",
    maxReached: "Maximum reached ({0})",
    importTitle: "Import JSON",
    importHint: "Paste exported JSON data",
    importSuccess: "JSON imported",
    importError: "Invalid JSON format",
    clearConfirmTitle: "Confirm clear",
    clearConfirmMsg: "Clear all filled data?",
    themeLight: "Light",
    themeDark: "Dark",
    saveDraft: "Save",
    autoSaved: "Auto-saved",
    fieldRequired: "This field is required",
    fieldMaxLen: "Exceeds max length {0}",
    fieldInvalidBIC: "Invalid BIC format",
    fieldInvalidIBAN: "IBAN validation failed",
    fieldInvalidLEI: "Invalid LEI format",
    fieldInvalidCountry: "Invalid country code",
    fieldInvalidCurrency: "Invalid currency code",
    fieldInvalidDecimal: "Decimal places exceed limit ({0})",
    fieldInvalidE2E: "Invalid EndToEndId format",
    fieldInvalidSvcLvl: "Invalid service level code",
    currencyMatch: "Same currency, exchange rate not needed",
    currencyDiff: "Different currencies, please fill exchange rate",
    r14Conflict: "Name not allowed when BICFI is filled",
    conditionalRef: "CdtrRefInf/Ref required when structured remittance info is present",
    choiceSelect: "Select type:",
    valueNotAllowed: "Value not allowed: {0}",
    conditionalRequired: "Required when {0} is present"
  },
  fr: {
    required: "Obligatoire",
    optional: "Facultatif",
    fixed: "Fixe",
    searchPlaceholder: "Rechercher un champ...",
    searchCount: "{0} champ(s) trouvé(s)",
    searchNone: "Aucun résultat",
    validatePass: "Validation réussie",
    validateFail: "{0} erreur(s)",
    requiredFilter: "Obligatoires",
    showAll: "Tout afficher",
    auditMode: "Mode audit",
    auditExit: "Quitter audit",
    auditOn: "Mode audit - champs verrouillés",
    auditOff: "Mode audit désactivé",
    templateApplied: "Modèle «{0}» appliqué",
    templateConfirm: "Appliquer le modèle écrasera les données. Continuer?",
    copiedJSON: "JSON copié",
    copiedXML: "XML copié",
    draftCleared: "Formulaire effacé",
    draftRestored: "Brouillon restauré",
    rmtSynced: "Champs synchronisés",
    atLeastOne: "Au moins un champ sous «{0}» requis",
    pleaseSelect: "-- Choisir --",
    progressLabel: "Progression champs obligatoires",
    progressText: "{0} / {1}",
    addItem: "Ajouter",
    removeItem: "Supprimer",
    maxReached: "Maximum atteint ({0})",
    importTitle: "Importer JSON",
    importHint: "Collez les données JSON",
    importSuccess: "JSON importé",
    importError: "Format JSON invalide",
    clearConfirmTitle: "Confirmer",
    clearConfirmMsg: "Effacer toutes les données?",
    themeLight: "Clair",
    themeDark: "Sombre",
    saveDraft: "Sauver",
    autoSaved: "Sauvegardé",
    fieldRequired: "Champ obligatoire",
    fieldMaxLen: "Dépasse la longueur max {0}",
    fieldInvalidBIC: "Format BIC invalide",
    fieldInvalidIBAN: "Validation IBAN échouée",
    fieldInvalidLEI: "Format LEI invalide",
    fieldInvalidCountry: "Code pays invalide",
    fieldInvalidCurrency: "Code devise invalide",
    fieldInvalidDecimal: "Décimales dépassent la limite ({0})",
    fieldInvalidE2E: "Format EndToEndId invalide",
    fieldInvalidSvcLvl: "Code niveau service invalide",
    currencyMatch: "Même devise, taux non requis",
    currencyDiff: "Devises différentes, remplir le taux",
    r14Conflict: "Name interdit quand BICFI rempli",
    conditionalRef: "CdtrRefInf/Ref requis avec info remise structurée",
    choiceSelect: "Sélectionner le type :",
    valueNotAllowed: "Valeur non autorisée : {0}",
    conditionalRequired: "Requis quand {0} est présent"
  }
};

function t(key, arg) {
  var dict = I18N[currentLang] || I18N.zh;
  var val = dict[key] || I18N.zh[key] || key;
  if (arg !== undefined) {
    val = val.replace("{0}", arg);
  }
  return val;
}

function switchLang(lang) {
  currentLang = lang;
  try { localStorage.setItem("iso20022-lang", lang); } catch(e) {}
  // Update UI text
  $("#btnRequiredOnly").text(requiredOnlyMode ? t("showAll") : t("requiredFilter"));
  $("#btnAuditMode").text(auditMode ? t("auditExit") : t("auditMode"));
  $("#fieldSearch").attr("placeholder", t("searchPlaceholder"));
  // Update language button active state
  $("#btnLangZh, #btnLangEn, #btnLangFr").removeClass("active");
  if (lang === "zh") $("#btnLangZh").addClass("active");
  else if (lang === "en") $("#btnLangEn").addClass("active");
  else if (lang === "fr") $("#btnLangFr").addClass("active");
  updateProgress();
}

// ============================================================
// Module 3: Theme & UI Controls
// ============================================================

function toggleTheme() {
  var $body = $("body");
  if ($body.hasClass("theme-dark")) {
    $body.removeClass("theme-dark").addClass("theme-light");
    try { localStorage.setItem("iso20022-theme", "light"); } catch(e) {}
  } else {
    $body.removeClass("theme-light").addClass("theme-dark");
    try { localStorage.setItem("iso20022-theme", "dark"); } catch(e) {}
  }
}

function toggleCard(header) {
  var $header = $(header);
  var $card = $header.closest(".card");
  $card.toggleClass("collapsed");
}

function toggleRequiredOnly() {
  requiredOnlyMode = !requiredOnlyMode;
  var $body = $("body");
  if (requiredOnlyMode) {
    $body.addClass("required-only");
  } else {
    $body.removeClass("required-only");
  }
  $("#btnRequiredOnly").text(requiredOnlyMode ? t("showAll") : t("requiredFilter"));
  try { localStorage.setItem("iso20022-required-only", requiredOnlyMode ? "1" : "0"); } catch(e) {}
}

function toggleAuditMode() {
  auditMode = !auditMode;
  var $body = $("body");
  if (auditMode) {
    $body.addClass("audit-mode");
    $(".audit-badge").show();
    validateAll();
    showToast(t("auditOn"));
  } else {
    $body.removeClass("audit-mode");
    $(".audit-badge").hide();
    showToast(t("auditOff"));
  }
  $("#btnAuditMode").text(auditMode ? t("auditExit") : t("auditMode"));
}

// ============================================================
// Module 4: Progress Bar
// ============================================================

function isEffectivelyRequired(el) {
  var $el = $(el);
  var $panel = $el.closest(".panel");
  while ($panel.length) {
    var $heading = $panel.children(".panel-heading");
    if ($heading.find(".label-info").length && !sectionHasValue($panel[0])) {
      return false;
    }
    $panel = $panel.parent().closest(".panel");
  }
  return true;
}

function sectionHasValue(section) {
  var $section = $(section);
  var hasVal = false;
  $section.find("input[name], select[name], textarea[name]").each(function() {
    if (this.disabled || this.readOnly) return;
    if ($.trim($(this).val())) {
      hasVal = true;
      return false; // break
    }
  });
  return hasVal;
}

function updateProgress() {
  var total = 0;
  var filled = 0;
  var atLeastOneGroups = window.AT_LEAST_ONE_GROUPS || [];

  // Build set of at-least-one group children for fast lookup
  var aloChildSet = {};
  for (var g = 0; g < atLeastOneGroups.length; g++) {
    var ch = atLeastOneGroups[g].children || [];
    for (var c = 0; c < ch.length; c++) {
      aloChildSet[ch[c]] = true;
    }
  }

  // Count rendered fields (DOM-based)
  $("input[name], select[name], textarea[name]").each(function() {
    var $input = $(this);
    var name = $input.attr("name") || "";
    var meta = findFieldMeta(name);
    var apiRequired = $input.attr("data-api-required") === "true";
    if (!((meta && meta.mult_min >= 1) || apiRequired)) return;
    if (!this.readOnly && !isEffectivelyRequired(this)) return;
    if (aloChildSet[name]) return;
    total++;
    if ($.trim($input.val())) filled++;
  });

  // Count unrendered component required fields (from templates)
  var instances = window.COMPONENT_INSTANCES || [];
  var templates = window.COMPONENT_TEMPLATES || {};
  for (var ci = 0; ci < instances.length; ci++) {
    var inst = instances[ci];
    if (renderState[inst.pathPrefix]) continue; // already counted via DOM
    var tpl = templates[inst.type];
    if (!tpl) continue;
    var reqCount = countTemplateRequired(tpl.fields);
    total += reqCount;
    // Check formData for filled values
    filled += countFilledFromFormData(inst.pathPrefix, tpl.fields);
  }

  // Count at-least-one groups as 1 slot each
  for (var i = 0; i < atLeastOneGroups.length; i++) {
    var group = atLeastOneGroups[i];
    total++;
    var groupFilled = false;
    var children = group.children || [];
    for (var j = 0; j < children.length; j++) {
      var val = formData[children[j]] || "";
      if (!val) {
        var $field = $("[name='" + escapeCssAttr(children[j]) + "']");
        if ($field.length) val = $.trim($field.val());
      }
      if (val) { groupFilled = true; break; }
    }
    if (groupFilled) filled++;
  }

  var pct = total > 0 ? Math.round((filled / total) * 100) : 0;
  $("#progressFill").css("width", pct + "%");
  $("#progressText").text(t("progressText", filled).replace("{1}", total) + " (" + pct + "%)");
}

function countTemplateRequired(fields) {
  var count = 0;
  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    var children = f.children || [];
    if (typeof children === "string" && children.charAt(0) === "$") {
      var refTpl = componentTemplates[children.substring(1)];
      if (refTpl) children = refTpl.fields;
      else children = [];
    }
    if (children.length > 0) {
      count += countTemplateRequired(children);
    } else if (f.multMin && f.multMin >= 1) {
      count++;
    }
  }
  return count;
}

function countFilledFromFormData(pathPrefix, fields) {
  var count = 0;
  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    var fieldPath = pathPrefix + "_" + f.tag;
    var children = f.children || [];
    if (typeof children === "string" && children.charAt(0) === "$") {
      var refTpl = componentTemplates[children.substring(1)];
      if (refTpl) children = refTpl.fields;
      else children = [];
    }
    if (children.length > 0) {
      count += countFilledFromFormData(fieldPath, children);
    } else if (f.multMin && f.multMin >= 1 && formData[fieldPath]) {
      count++;
    }
  }
  return count;
}

// ============================================================
// Module 5: Validation
// ============================================================

var FORBIDDEN_SVC_LVL = ["G002","G003","G004","G005","G006","G007","G009"];

function validateIBAN(iban) {
  iban = iban.replace(/\s/g, "").toUpperCase();
  if (iban.length < 5) return false;
  var rearranged = iban.substring(4) + iban.substring(0, 4);
  var numStr = "";
  for (var i = 0; i < rearranged.length; i++) {
    var ch = rearranged.charCodeAt(i);
    if (ch >= 65 && ch <= 90) {
      numStr += (ch - 55).toString();
    } else {
      numStr += rearranged.charAt(i);
    }
  }
  // Mod 97 in chunks (handle big numbers)
  var remainder = "";
  for (var j = 0; j < numStr.length; j++) {
    remainder += numStr.charAt(j);
    var num = parseInt(remainder, 10);
    remainder = (num % 97).toString();
  }
  return parseInt(remainder, 10) === 1;
}

function validateField(name, value) {
  var meta = findFieldMeta(name);
  if (!meta) return "";

  // Required check
  if (meta.mult_min >= 1 && !value) {
    return t("fieldRequired");
  }
  if (!value) return "";

  // Max length
  if (meta.max_length > 0 && value.length > meta.max_length) {
    return t("fieldMaxLen", meta.max_length);
  }

  // BIC
  if (name.indexOf("BICFI") !== -1 || name.indexOf("_BIC") !== -1) {
    if (!/^[A-Z0-9]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$/.test(value)) {
      return t("fieldInvalidBIC");
    }
  }

  // IBAN
  if (name.indexOf("IBAN") !== -1) {
    if (!validateIBAN(value)) {
      return t("fieldInvalidIBAN");
    }
  }

  // LEI
  if (name.indexOf("_LEI") !== -1) {
    if (!/^[A-Z0-9]{18}[0-9]{2}$/.test(value)) {
      return t("fieldInvalidLEI");
    }
  }

  // Country code
  if (name.indexOf("Ctry") !== -1 || name.indexOf("_CTRY") !== -1) {
    if (!/^[A-Z]{2}$/.test(value)) {
      return t("fieldInvalidCountry");
    }
  }

  // Currency code
  if (name.indexOf("_CCY") !== -1) {
    if (!/^[A-Z]{3}$/.test(value)) {
      return t("fieldInvalidCurrency");
    }
  }

  // Decimal places
  if (meta.type_code === "decimal" && meta.decimal_fd > 0) {
    var dotIdx = value.indexOf(".");
    if (dotIdx !== -1) {
      var fracLen = value.length - dotIdx - 1;
      if (fracLen > meta.decimal_fd) {
        return t("fieldInvalidDecimal", meta.decimal_fd);
      }
    }
  }

  // EndToEndId
  if (name.indexOf("EndToEndId") !== -1) {
    if (value !== "NOTPROVIDED" && !/^[A-Za-z0-9\/\-?:().,'+\s]{1,35}$/.test(value)) {
      return t("fieldInvalidE2E");
    }
  }

  // Service Level Code
  if (name.indexOf("SvcLvl") !== -1 && name.indexOf("_Cd") !== -1) {
    for (var i = 0; i < FORBIDDEN_SVC_LVL.length; i++) {
      if (FORBIDDEN_SVC_LVL[i] === value) return t("fieldInvalidSvcLvl");
    }
  }

  // Not-allowed values (from rules PDF)
  var notAllowedMsg = checkNotAllowedValues(name, value);
  if (notAllowedMsg) return notAllowedMsg;

  return "";
}

function setFieldError(name, msg) {
  var $field = $("[name='" + escapeCssAttr(name) + "']");
  var $group = $field.closest(".field-group");
  var $err = $group.find(".error-msg");
  if (msg) {
    validationErrors[name] = msg;
    $group.addClass("has-error");
    $err.text(msg).show();
  } else {
    delete validationErrors[name];
    $group.removeClass("has-error");
    $err.text("").hide();
  }
}

function checkBusinessRules(name, value) {
  var $field = $("[name='" + escapeCssAttr(name) + "']");
  var $group = $field.closest(".field-group");
  var $warn = $group.find(".biz-warn");
  var rulesAttr = $field.attr("data-biz-rules");
  if (!rulesAttr || !$warn.length) return;
  try {
    var rules = JSON.parse(rulesAttr);
    var msg = "";
    for (var i = 0; i < rules.length; i++) {
      if (rules[i].value === value) {
        msg = rules[i].warning || "";
        break;
      }
    }
    $warn.text(msg);
    if (msg) $warn.show(); else $warn.hide();
  } catch(e) {}
}

function checkAtLeastOneGroups(changedName) {
  var groups = window.AT_LEAST_ONE_GROUPS || [];
  for (var i = 0; i < groups.length; i++) {
    var group = groups[i];
    var children = group.children || [];
    var isRelevant = false;
    for (var c = 0; c < children.length; c++) {
      if (children[c] === changedName) { isRelevant = true; break; }
    }
    if (!isRelevant) continue;

    var anyFilled = false;
    for (var j = 0; j < children.length; j++) {
      var $f = $("[name='" + escapeCssAttr(children[j]) + "']");
      if ($f.length && $.trim($f.val())) { anyFilled = true; break; }
    }

    for (var k = 0; k < children.length; k++) {
      if (anyFilled) {
        setFieldError(children[k], "");
      } else {
        setFieldError(children[k], t("atLeastOne", group.parent_name_zh));
      }
    }
  }
}

function checkConditionalMandatory() {
  // F07 CR 3072: CdtrRefInf/Ref mandatory when Strd fields have values
  var hasStrd = false;
  $("[name*='_Strd_']").each(function() {
    if ($(this).val()) { hasStrd = true; return false; }
  });
  var $ref = $("[name*='CdtrRefInf_Ref']");
  if ($ref.length) {
    if (hasStrd && !$ref.val()) {
      setFieldError($ref.attr("name"), t("conditionalRef"));
    } else {
      setFieldError($ref.attr("name"), "");
    }
  }
}

function validateAll() {
  var errorCount = 0;
  validationErrors = {};

  // Validate each field
  $(".field-group input, .field-group select, .field-group textarea").each(function() {
    var $el = $(this);
    var name = $el.attr("name");
    if (!name) return;
    var value = $el.val() || "";
    var msg = validateField(name, value);
    setFieldError(name, msg);
    if (msg) errorCount++;
  });

  // R14: BICFI vs Name conflict
  $("[name*='_BICFI']").each(function() {
    var bicName = $(this).attr("name");
    if (!$(this).val()) return;
    var namePath = bicName.replace("_BICFI", "_Nm");
    var $nm = $("[name='" + escapeCssAttr(namePath) + "']");
    if ($nm.length && $nm.val()) {
      setFieldError(namePath, t("r14Conflict"));
      errorCount++;
    }
  });

  // At-least-one groups
  var groups = window.AT_LEAST_ONE_GROUPS || [];
  for (var i = 0; i < groups.length; i++) {
    var group = groups[i];
    var children = group.children || [];
    var anyFilled = false;
    for (var j = 0; j < children.length; j++) {
      var $f = $("[name='" + escapeCssAttr(children[j]) + "']");
      if ($f.length && $.trim($f.val())) { anyFilled = true; break; }
    }
    if (!anyFilled) {
      for (var k = 0; k < children.length; k++) {
        setFieldError(children[k], t("atLeastOne", group.parent_name_zh));
        errorCount++;
      }
    }
  }

  // Conditional mandatory
  checkConditionalMandatory();

  // Conditional presence rules (from rules PDF)
  errorCount += checkConditionalPresenceRules();

  // Currency consistency
  checkCurrencyConsistency();

  // Show summary
  var $summary = $("#validationSummary");
  if (errorCount > 0) {
    $summary.html('<span class="text-danger">' + t("validateFail", errorCount) + '</span>').show();
    showToast(t("validateFail", errorCount));
  } else {
    $summary.html('<span class="text-success">' + t("validatePass") + '</span>').show();
    showToast(t("validatePass"));
  }
  return errorCount;
}

// ============================================================
// Module 5b: Choice Group Handler
// ============================================================

function initChoiceGroups() {
  var groups = window.CHOICE_GROUPS || [];
  if (!groups.length) return;
  var choiceSets = [];

  for (var i = 0; i < groups.length; i++) {
    var group = groups[i];
    var options = group.options || [];
    if (options.length < 2) continue;

    var firstTag = options[0].tag;
    _findChoiceElements(firstTag).each(function() {
      var $first = $(this);
      var baseFormName = _getBaseName($first, firstTag);
      if (!baseFormName) return;

      var panelSet = [];
      var allFound = true;
      for (var j = 0; j < options.length; j++) {
        var targetName = baseFormName + options[j].tag;
        var $el = _findElementByName(targetName);
        if ($el && $el.length) {
          panelSet.push({ tag: options[j].tag, name: options[j].name, $el: $el });
        } else { allFound = false; break; }
      }
      if (!allFound || panelSet.length !== options.length) return;

      var key = baseFormName;
      for (var d = 0; d < choiceSets.length; d++) {
        if (choiceSets[d].key === key) return;
      }
      choiceSets.push({ key: key, panels: panelSet });
    });
  }

  for (var s = 0; s < choiceSets.length; s++) {
    (function(panels) {
      _updateChoiceState(panels);
      for (var p = 0; p < panels.length; p++) {
        panels[p].$el.on("input change", "input,select,textarea", function() {
          _updateChoiceState(panels);
        });
      }
    })(choiceSets[s].panels);
  }
}

function _updateChoiceState(panels) {
  var filledIdx = -1;
  for (var i = 0; i < panels.length; i++) {
    var hasValue = false;
    panels[i].$el.find("input,select,textarea").each(function() {
      if ($(this).val() && !$(this).prop("disabled")) { hasValue = true; return false; }
    });
    if (hasValue) { filledIdx = i; break; }
  }

  for (var j = 0; j < panels.length; j++) {
    if (filledIdx === -1) {
      // Nothing filled: all options editable, shown as optional
      panels[j].$el.removeClass("choice-disabled");
      panels[j].$el.find(".field-group").removeClass("field-disabled");
      panels[j].$el.find("input,select,textarea").prop("disabled", false).prop("readonly", false);
      if (panels[j].$el.hasClass("field-group")) {
        panels[j].$el.removeClass("field-disabled");
        panels[j].$el.find("input,select,textarea").prop("disabled", false).prop("readonly", false);
      }
    } else if (j === filledIdx) {
      // Active option: enable and restore required state
      panels[j].$el.removeClass("choice-disabled");
      panels[j].$el.find(".field-group").removeClass("field-disabled").addClass("field-required");
      panels[j].$el.find("input,select,textarea").prop("disabled", false).prop("readonly", false);
      if (panels[j].$el.hasClass("field-group")) {
        panels[j].$el.removeClass("field-disabled").addClass("field-required");
        panels[j].$el.find("input,select,textarea").prop("disabled", false).prop("readonly", false);
      }
    } else {
      // Inactive option: disabled/P state
      panels[j].$el.addClass("choice-disabled");
      panels[j].$el.find(".field-group").addClass("field-disabled").removeClass("field-required");
      panels[j].$el.find("input,select,textarea").prop("disabled", true).prop("readonly", true);
      if (panels[j].$el.hasClass("field-group")) {
        panels[j].$el.addClass("field-disabled").removeClass("field-required");
        panels[j].$el.find("input,select,textarea").prop("disabled", true).prop("readonly", true);
      }
    }
  }
}

function _findChoiceElements(tag) {
  var results = $();
  $(".field-group[data-form-name$='_" + tag + "']").each(function() { results = results.add($(this)); });
  $("[id^='collapse_']").each(function() {
    var id = $(this).attr("id");
    if (_endsWithTag(id, tag)) { results = results.add($(this).closest(".panel")); }
  });
  return results;
}

function _getBaseName($el, tag) {
  var suffix = "_" + tag;
  if ($el.hasClass("field-group")) {
    var name = $el.attr("data-form-name") || "";
    if (name.length > suffix.length && name.substring(name.length - suffix.length) === suffix) {
      return name.substring(0, name.length - suffix.length + 1);
    }
  }
  var $collapse = $el.find("[id^='collapse_']").first();
  if (!$collapse.length) $collapse = $el.children("[id^='collapse_']").first();
  if ($collapse.length) {
    var id = $collapse.attr("id").replace("collapse_", "");
    if (id.length > suffix.length && id.substring(id.length - suffix.length) === suffix) {
      return id.substring(0, id.length - suffix.length + 1);
    }
  }
  return "";
}

function _findElementByName(formName) {
  var $fg = $(".field-group[data-form-name='" + formName + "']");
  if ($fg.length) return $fg;
  var $collapse = $("#collapse_" + formName);
  if ($collapse.length) return $collapse.closest(".panel");
  return null;
}

function _endsWithTag(id, tag) {
  var suffix = "_" + tag;
  return id.length > suffix.length && id.substring(id.length - suffix.length) === suffix;
}

function checkNotAllowedValues(name, value) {
  if (!value) return "";
  var config = window.ISO20022_APP_CONFIG;
  if (!config || !config.messages) return "";
  var msgConfig = config.messages[MESSAGE_ID] || {};
  var notAllowed = msgConfig.notAllowedValues || [];

  var meta = findFieldMeta(name);
  if (!meta) return "";

  for (var i = 0; i < notAllowed.length; i++) {
    var rule = notAllowed[i];
    var pathSuffix = (rule.path || "").split("/").pop() || "";
    if (!pathSuffix) continue;
    if (meta.iso_path && meta.iso_path.indexOf(pathSuffix) !== -1) {
      var blocked = rule.values || [];
      for (var j = 0; j < blocked.length; j++) {
        if (value.toUpperCase() === blocked[j].toUpperCase()) {
          return t("valueNotAllowed", blocked[j]);
        }
      }
    }
  }
  return "";
}

function checkConditionalPresenceRules() {
  var config = window.ISO20022_APP_CONFIG;
  if (!config || !config.messages) return 0;
  var msgConfig = config.messages[MESSAGE_ID] || {};
  var conditionals = msgConfig.conditionalPresence || [];
  var errorCount = 0;

  for (var i = 0; i < conditionals.length; i++) {
    var rule = conditionals[i];
    var ifField = rule.if_field || "";
    var thenField = rule.then_field || "";
    if (!ifField || !thenField) continue;

    // Find fields matching the if/then names
    $("[name*='" + ifField + "']").each(function() {
      var $ifEl = $(this);
      if (!$ifEl.val()) return;
      var baseName = $ifEl.attr("name").replace(ifField, thenField);
      var $thenEl = $("[name='" + escapeCssAttr(baseName) + "']");
      if ($thenEl.length && !$thenEl.val() && !$thenEl.prop("disabled")) {
        setFieldError(baseName, t("conditionalRequired", ifField));
        errorCount++;
      }
    });
  }
  return errorCount;
}

// ============================================================
// Module 6: Amount & Currency
// ============================================================

var CCY_DECIMALS = {JPY:0,KRW:0,VND:0,KWD:3,BHD:3,OMR:3};

function formatAmount(value, ccy) {
  if (!value) return "";
  var num = parseFloat(value);
  if (isNaN(num)) return value;
  var decimals = CCY_DECIMALS[ccy] !== undefined ? CCY_DECIMALS[ccy] : 2;
  var parts = num.toFixed(decimals).split(".");
  var intPart = parts[0];
  var decPart = parts[1] || "";
  // Add thousand separators
  var formatted = "";
  var count = 0;
  for (var i = intPart.length - 1; i >= 0; i--) {
    if (count > 0 && count % 3 === 0) formatted = "," + formatted;
    formatted = intPart.charAt(i) + formatted;
    count++;
  }
  return decPart ? (formatted + "." + decPart) : formatted;
}

function updateAmountDisplay(name) {
  var $field = $("[name='" + escapeCssAttr(name) + "']");
  if (!$field.length) return;
  var $group = $field.closest(".field-group");
  var $display = $group.find(".amount-display");
  if (!$display.length) return;
  var value = $field.val();
  var ccyName = name + "_CCY";
  var $ccy = $("[name='" + escapeCssAttr(ccyName) + "']");
  if (!$ccy.length) {
    ccyName = name.replace(/_[^_]+$/, "_CCY");
    $ccy = $("[name='" + escapeCssAttr(ccyName) + "']");
  }
  var ccy = $ccy.length ? $ccy.val() : "";
  if (value) {
    $display.text(formatAmount(value, ccy) + " " + (ccy || "")).show();
  } else {
    $display.text("").hide();
  }
}

function checkCurrencyConsistency() {
  var $settlCcy = $("[name*='IntrBkSttlmAmt_CCY']").first();
  var $instdCcy = $("[name*='InstdAmt_CCY']").first();
  var $xchgRate = $("[name*='XchgRate']").first();
  if (!$settlCcy.length || !$instdCcy.length || !$xchgRate.length) return;

  var ccy1 = $settlCcy.val();
  var ccy2 = $instdCcy.val();
  var $xchgGroup = $xchgRate.closest(".field-group");

  if (!ccy1 || !ccy2) {
    $xchgGroup.css("opacity", "1");
    $xchgGroup.find(".currency-hint").remove();
    return;
  }

  if (ccy1 === ccy2) {
    $xchgGroup.css("opacity", "0.5");
    if (!$xchgGroup.find(".currency-hint").length) {
      $xchgGroup.append('<div class="currency-hint text-muted">' + t("currencyMatch") + '</div>');
    }
  } else {
    $xchgGroup.css("opacity", "1");
    $xchgGroup.find(".currency-hint").remove();
    if (!$xchgRate.val()) {
      setFieldError($xchgRate.attr("name"), t("currencyDiff"));
    }
  }
}

// ============================================================
// Module 7: JSON/XML Export & Import
// ============================================================

function buildISO20022JSON() {
  var json = {};
  // Use formData as authoritative source (includes unrendered component fields)
  for (var name in formData) {
    if (!formData.hasOwnProperty(name)) continue;
    var value = formData[name];
    if (!value) continue;
    if (name.indexOf("_CCY") !== -1) continue;

    var parts = name.split("_");
    var obj = json;
    for (var i = 1; i < parts.length; i++) {
      var key = parts[i];
      if (i === parts.length - 1) {
        obj[key] = value;
      } else {
        if (!obj[key]) obj[key] = {};
        obj = obj[key];
      }
    }
  }
  return json;
}

function syntaxHighlight(json) {
  json = json.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return json.replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
    function(match) {
      var cls = "json-number";
      if (/^"/.test(match)) {
        if (/:$/.test(match)) cls = "json-key";
        else cls = "json-string";
      } else if (/true|false/.test(match)) {
        cls = "json-boolean";
      } else if (/null/.test(match)) {
        cls = "json-null";
      }
      return '<span class="' + cls + '">' + match + '</span>';
    }
  );
}

function updateJSONPreview() {
  var json = buildISO20022JSON();
  var jsonStr = JSON.stringify(json, null, 2);
  var $preview = $("#jsonPreview");
  $preview.val(jsonStr);
  updateSummary(json);
}

function updateSummary(json) {
  var doc = json.DOC || json;
  var txInf = doc.FIToFICstmrCdtTrf && doc.FIToFICstmrCdtTrf.CdtTrfTxInf || {};
  var grpHdr = doc.FIToFICstmrCdtTrf && doc.FIToFICstmrCdtTrf.GrpHdr || {};

  var dbtr = txInf.Dbtr && txInf.Dbtr.Nm || "—";
  var cdtr = txInf.Cdtr && txInf.Cdtr.Nm || "—";
  var dbtrAgt = txInf.DbtrAgt && txInf.DbtrAgt.FinInstnId && txInf.DbtrAgt.FinInstnId.BICFI || "—";
  var cdtrAgt = txInf.CdtrAgt && txInf.CdtrAgt.FinInstnId && txInf.CdtrAgt.FinInstnId.BICFI || "—";
  var amt = txInf.IntrBkSttlmAmt || "—";
  var chrgBr = txInf.ChrgBr || "—";
  var rmtInf = txInf.RmtInf && txInf.RmtInf.Ustrd || "—";
  var e2e = txInf.PmtId && txInf.PmtId.EndToEndId || "—";

  $("#sumDebtor").text(dbtr);
  $("#sumCreditor").text(cdtr);
  $("#sumDebtorAgent").text(dbtrAgt);
  $("#sumCreditorAgent").text(cdtrAgt);
  $("#sumAmount").text(amt);
  $("#sumChrgBr").text(chrgBr);
  $("#sumRmtInf").text(typeof rmtInf === "string" ? rmtInf : JSON.stringify(rmtInf));
  $("#sumE2E").text(e2e);
}

function switchJsonTab(tab) {
  if (tab === "json") {
    $("#summaryView").hide();
    $("#jsonPreview").show();
    $("#tabSummary").removeClass("active");
    $("#tabJson").addClass("active");
  } else {
    $("#summaryView").show();
    $("#jsonPreview").hide();
    $("#tabSummary").addClass("active");
    $("#tabJson").removeClass("active");
  }
}

function exportJSON() {
  var json = buildISO20022JSON();
  var jsonStr = JSON.stringify(json, null, 2);
  copyToClipboard(jsonStr);
  showToast(t("copiedJSON"));
}

function exportXML() {
  var json = buildISO20022JSON();
  var xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + jsonToXML(json, "Document");
  copyToClipboard(xml);
  showToast(t("copiedXML"));
}

function jsonToXML(obj, rootTag) {
  var xml = "<" + rootTag + ">";
  for (var key in obj) {
    if (!obj.hasOwnProperty(key)) continue;
    var val = obj[key];
    if (typeof val === "object" && val !== null) {
      xml += "\n  " + jsonToXML(val, key);
    } else {
      xml += "\n  <" + key + ">" + escapeHtml(String(val)) + "</" + key + ">";
    }
  }
  xml += "\n</" + rootTag + ">";
  return xml;
}

function copyToClipboard(text) {
  var $ta = $("<textarea>");
  $ta.val(text).css({position:"fixed",left:"-9999px"}).appendTo("body");
  $ta[0].select();
  try { document.execCommand("copy"); } catch(e) {}
  $ta.remove();
}

function importJSON() {
  $("#importJsonText").val("");
  $("#importModal").modal("show");
}

function doImportJSON() {
  var text = $("#importJsonText").val();
  try {
    var json = JSON.parse(text);
    importNested(json, "");
    $("#importModal").modal("hide");
    updateJSONPreview();
    updateProgress();
    showToast(t("importSuccess"));
  } catch(e) {
    showToast(t("importError"));
  }
}

function importNested(obj, prefix) {
  for (var key in obj) {
    if (!obj.hasOwnProperty(key)) continue;
    var val = obj[key];
    var path = prefix ? (prefix + "_" + key) : key;
    if (typeof val === "object" && val !== null) {
      importNested(val, path);
    } else {
      // Try to find field by path suffix
      var $field = $("[name$='" + escapeCssAttr(path) + "']");
      if ($field.length) {
        $field.val(String(val)).trigger("change");
      }
    }
  }
}

// ============================================================
// Module 8: Template System
// ============================================================

function renderPresetTemplates() {
  var config = getRuntimeConfig();
  var templates = config.templates || {};
  var $list = $("#runtimeTemplateList");
  $list.empty();
  for (var key in templates) {
    if (!templates.hasOwnProperty(key)) continue;
    var tpl = templates[key];
    var icon = tpl.icon || "";
    var label = tpl.shortName || tpl.name || key;
    var $btn = $('<button type="button" class="btn btn-default btn-sm template-btn"></button>');
    $btn.attr("data-template-key", key);
    if (tpl.desc || tpl.name) $btn.attr("title", tpl.desc || tpl.name);
    $btn.text(icon + " " + label);
    $list.append($btn).append(" ");
  }
}

function applyTemplate(key) {
  var hasData = false;
  $(".field-group input, .field-group select, .field-group textarea").each(function() {
    if ($(this).val()) { hasData = true; return false; }
  });
  if (hasData) {
    showConfirm("", t("templateConfirm"), function() {
      doApplyTemplate(key);
    });
  } else {
    doApplyTemplate(key);
  }
}

function doApplyTemplate(key) {
  var config = getRuntimeConfig();
  var templates = config.templates || {};
  var tpl = templates[key];
  if (!tpl || !tpl.values) return;
  var values = tpl.values;
  for (var fieldKey in values) {
    if (!values.hasOwnProperty(fieldKey)) continue;
    var $field = $("[name$='" + escapeCssAttr(fieldKey) + "']");
    if ($field.length) {
      $field.val(values[fieldKey]).trigger("change");
    }
  }
  $(".template-btn").removeClass("active");
  $("[data-template-key='" + key + "']").addClass("active");
  showToast(t("templateApplied", tpl.label || key));
  updateJSONPreview();
  updateProgress();
}

// ============================================================
// Module 9: Field Search & Navigation
// ============================================================

function searchFields(query) {
  // Clear previous
  $(".field-locate, .field-locate-active").removeClass("field-locate field-locate-active");
  $(".search-highlight").each(function() {
    var $parent = $(this).parent();
    $parent.text($parent.text());
  });
  locateMatches = [];
  locateIdx = -1;

  if (!query || query.length < 1) {
    updateSearchCount(0);
    updateSearchNavState();
    return;
  }

  var q = query.toLowerCase();

  // Search parent section headers (panel-heading)
  $(".panel > .panel-heading").each(function() {
    var $heading = $(this);
    var $title = $heading.find(".panel-title");
    if (!$title.length) return;
    var text = $title.text().toLowerCase();
    if (text.indexOf(q) !== -1) {
      $heading.addClass("field-locate");
      locateMatches.push($heading[0]);
      highlightText($title[0], query);
      // Expand this panel and ancestors
      var $panel = $heading.closest(".panel");
      expandCardAncestors($panel);
      var $body = $panel.children(".panel-body.collapse");
      if ($body.length && !$body.hasClass("in")) {
        $body.collapse("show");
      }
    }
  });

  // Search field labels
  $(".field-group").each(function() {
    var $fg = $(this);
    var $input = $fg.find("input, select, textarea").first();
    if (!$input.length) return;
    var name = $input.attr("name") || "";
    var tag = $input.attr("data-tag") || "";
    var $label = $fg.find(".control-label");
    var labelText = $label.text().toLowerCase();

    if (labelText.indexOf(q) !== -1 || name.toLowerCase().indexOf(q) !== -1 || tag.toLowerCase().indexOf(q) !== -1) {
      $fg.addClass("field-locate");
      locateMatches.push($fg[0]);
      highlightText($label[0], query);
      expandCardAncestors($fg);
    }
  });

  // Search unrendered component fields (by template metadata)
  var instances = window.COMPONENT_INSTANCES || [];
  var templates = window.COMPONENT_TEMPLATES || {};
  for (var ci = 0; ci < instances.length; ci++) {
    var inst = instances[ci];
    if (renderState[inst.pathPrefix]) continue; // already searched via DOM
    var tpl = templates[inst.type];
    if (!tpl) continue;
    if (searchTemplateFields(tpl.fields, q, inst.pathPrefix)) {
      // Force render this component and re-search its DOM
      var $container = $("[data-path-prefix='" + inst.pathPrefix + "']");
      if ($container.length) {
        renderComponent(inst.pathPrefix, inst.type, $container);
        $container.collapse("show");
        // Now find matching fields in the newly rendered DOM
        $container.find(".field-group").each(function() {
          var $fg = $(this);
          var $label = $fg.find(".control-label");
          var labelText = $label.text().toLowerCase();
          var $input = $fg.find("input, select, textarea").first();
          var name = $input.attr("name") || "";
          var tag = $input.attr("data-tag") || "";
          if (labelText.indexOf(q) !== -1 || name.toLowerCase().indexOf(q) !== -1 || tag.toLowerCase().indexOf(q) !== -1) {
            $fg.addClass("field-locate");
            locateMatches.push($fg[0]);
            highlightText($label[0], query);
            expandCardAncestors($fg);
          }
        });
      }
    }
  }

  updateSearchCount(locateMatches.length);
  updateSearchNavState();

  if (locateMatches.length > 0) {
    setActiveMatch(0, true);
  }
}

function setActiveMatch(index, shouldScroll) {
  $(".field-locate-active").removeClass("field-locate-active");
  if (index < 0 || index >= locateMatches.length) return;
  locateIdx = ((index % locateMatches.length) + locateMatches.length) % locateMatches.length;
  var $match = $(locateMatches[locateIdx]);
  $match.addClass("field-locate-active");

  // Expand parent cards
  expandCardAncestors($match);

  if (shouldScroll) {
    setTimeout(function() {
      var offset = $match.offset();
      if (offset) {
        $("html, body").animate({scrollTop: offset.top - 150}, 200, function() {
          $("#fieldSearch").focus();
        });
      }
    }, 350);
  }
  updateSearchNavState();
}

function expandCardAncestors($el) {
  $el.parents(".panel-body.collapse").each(function() {
    var $body = $(this);
    if (!$body.hasClass("in")) {
      $body.collapse("show");
    }
  });
}

function stepMatch(direction) {
  if (locateMatches.length === 0) return;
  var next = locateIdx + direction;
  if (next >= locateMatches.length) next = 0;
  if (next < 0) next = locateMatches.length - 1;
  setActiveMatch(next, true);
}

function clearSearch() {
  $("#fieldSearch").val("");
  searchFields("");
}

function highlightText(element, query) {
  var $el = $(element);
  var text = $el.text();
  var idx = text.toLowerCase().indexOf(query.toLowerCase());
  if (idx === -1) return;
  var before = text.substring(0, idx);
  var match = text.substring(idx, idx + query.length);
  var after = text.substring(idx + query.length);
  $el.html(escapeHtml(before) + '<span class="search-highlight">' + escapeHtml(match) + '</span>' + escapeHtml(after));
}

function updateSearchCount(total) {
  var $count = $("#searchCount");
  if (total > 0) {
    $count.text(t("searchCount", total)).show();
  } else if ($("#fieldSearch").val()) {
    $count.text(t("searchNone")).show();
  } else {
    $count.text("").hide();
  }
}

function updateSearchNavState() {
  var hasMatches = locateMatches.length > 0;
  $("#searchPrev").prop("disabled", !hasMatches);
  $("#searchNext").prop("disabled", !hasMatches);
}

// ============================================================
// Module 10: Repeat Groups
// ============================================================

var repeatTemplates = {};

function getDirectRepeatItems($group) {
  return $group.children(".repeat-items").children(".repeat-item").not(".repeat-template");
}

function saveRepeatTemplate($group) {
  var groupId = $group.attr("data-repeat-group");
  if (!repeatTemplates[groupId]) {
    // Look for hidden template item first, then visible first item
    var $tpl = $group.find(".repeat-template").first();
    if ($tpl.length) {
      repeatTemplates[groupId] = $tpl.clone();
      repeatTemplates[groupId].removeClass("repeat-template").removeAttr("style");
      repeatTemplates[groupId].find("input, select, textarea").val("");
    } else {
      var $first = getDirectRepeatItems($group).first();
      if ($first.length) {
        repeatTemplates[groupId] = $first.clone();
        repeatTemplates[groupId].find("input, select, textarea").val("");
      }
    }
  }
}

function addRepeatItem(groupId) {
  var $group = $("[data-repeat-group='" + groupId + "']").first();
  if (!$group.length) return;

  // Ensure template is saved (needed for groups with rewritten IDs)
  saveRepeatTemplate($group);

  var max = parseInt($group.attr("data-max"), 10) || 0;
  var $items = getDirectRepeatItems($group);
  var count = $items.length;

  if (max > 0 && count >= max) {
    showToast(t("maxReached", max));
    return;
  }

  // Use saved template or clone first item
  var $newItem;
  if (repeatTemplates[groupId]) {
    $newItem = repeatTemplates[groupId].clone();
  } else if ($items.length > 0) {
    $newItem = $items.first().clone();
    $newItem.find("input, select, textarea").val("");
    repeatTemplates[groupId] = $newItem.clone();
  } else {
    $newItem = buildDefaultRepeatItem($group);
    if (!$newItem) return;
    repeatTemplates[groupId] = $newItem.clone();
  }

  $newItem.find(".has-error").removeClass("has-error");
  $newItem.find(".error-msg").text("").hide();

  // Rewrite nested IDs to avoid duplicates when cloning repeat items
  var newIndex = count + 1;
  rewriteNestedIds($newItem, newIndex);

  $group.children(".repeat-items").append($newItem);
  renumberRepeatItems($group);
  updateRepeatAddState($group);
  updateRepeatRemoveState($group);

  // Render any component placeholders that are already expanded (collapse in)
  $newItem.find("[data-component][data-rendered='false']").each(function() {
    var $comp = $(this);
    if ($comp.hasClass("in")) {
      var type = $comp.attr("data-component");
      var pathPrefix = $comp.attr("data-path-prefix");
      renderComponent(pathPrefix, type, $comp);
    }
  });
}

function buildDefaultRepeatItem($group) {
  // For repeat-leaf groups, build a simple input item
  if ($group.hasClass("repeat-leaf")) {
    var groupId = $group.attr("data-repeat-group");
    // Extract form-name from group id: "repeat_DOC_..._AdrLine" -> "DOC_..._AdrLine"
    var formName = groupId.replace(/^repeat_/, "");
    var html = '<div class="repeat-item" data-index="1">' +
      '<span class="repeat-index">第1条</span>' +
      '<button type="button" class="btn btn-xs btn-danger btn-repeat-remove">×</button>' +
      '<div class="field-group field-editable" data-form-name="' + escapeHtml(formName) + '" data-required="false">' +
      '<input type="text" class="form-control" name="' + escapeHtml(formName) + '" data-form-name="' + escapeHtml(formName) + '">' +
      '<div class="error-msg"></div></div></div>';
    return $(html);
  }
  // For container repeat groups, we need the inner template
  // This case is handled by saveRepeatTemplate during component init
  return null;
}

function removeRepeatItem(btn) {
  var $btn = $(btn);
  var $item = $btn.closest(".repeat-item");
  var $group = $item.closest("[data-repeat-group]");
  var minAttr = $group.attr("data-min");
  var min = (minAttr !== undefined && minAttr !== "") ? parseInt(minAttr, 10) : 1;
  var $items = getDirectRepeatItems($group);

  if ($items.length <= min) return;

  $item.remove();
  renumberRepeatItems($group);
  updateRepeatAddState($group);
  updateRepeatRemoveState($group);
  updateProgress();
}

function renumberRepeatItems($group) {
  getDirectRepeatItems($group).each(function(idx) {
    var $item = $(this);
    $item.attr("data-index", idx + 1);
    $item.children(".repeat-index").text("第" + (idx + 1) + "条");
  });
}

function rewriteNestedIds($item, index) {
  var suffix = "_" + index;

  // Rewrite inner repeat-group IDs
  $item.find("[data-repeat-group]").each(function() {
    var $rg = $(this);
    var oldId = $rg.attr("data-repeat-group");
    var newId = oldId + suffix;
    $rg.attr("id", newId).attr("data-repeat-group", newId);
    $rg.children(".repeat-items").attr("id", newId + "_items");
  });

  // Rewrite collapse panel IDs and their data-target references
  $item.find("[id^='collapse_']").each(function() {
    var $panel = $(this);
    var oldId = $panel.attr("id");
    var newId = oldId + suffix;
    $panel.attr("id", newId);
  });
  $item.find("[data-target^='#collapse_']").each(function() {
    var $heading = $(this);
    var oldTarget = $heading.attr("data-target");
    $heading.attr("data-target", oldTarget + suffix);
  });

  // Rewrite form field names/ids for formData uniqueness
  $item.find("[data-form-name]").each(function() {
    var $fg = $(this);
    var oldName = $fg.attr("data-form-name");
    var newName = oldName + suffix;
    $fg.attr("data-form-name", newName);
    $fg.find("input,select,textarea").each(function() {
      var $input = $(this);
      if ($input.attr("name") === oldName) {
        $input.attr("name", newName).attr("id", newName).attr("data-form-name", newName);
      }
    });
    $fg.find("label[for='" + oldName + "']").attr("for", newName);
  });

  $item.attr("data-index", index);
}

function updateRepeatAddState($group) {
  var max = parseInt($group.attr("data-max"), 10) || 0;
  var count = getDirectRepeatItems($group).length;
  var $addBtn = $group.children(".panel-heading").find(".btn-repeat-add");
  if (max > 0 && count >= max) {
    $addBtn.prop("disabled", true);
  } else {
    $addBtn.prop("disabled", false);
  }
}

function updateRepeatRemoveState($group) {
  var minAttr = $group.attr("data-min");
  var min = (minAttr !== undefined && minAttr !== "") ? parseInt(minAttr, 10) : 1;
  var count = getDirectRepeatItems($group).length;
  var $removeBtns = getDirectRepeatItems($group).find(".btn-repeat-remove");
  if (count <= min) {
    $removeBtns.prop("disabled", true);
  } else {
    $removeBtns.prop("disabled", false);
  }
}

// ============================================================
// Module 11: Draft Auto-Save
// ============================================================

function collectQuickDraft() {
  var draft = {};
  $("#quickFillFields input, #quickFillFields select, #quickFillFields textarea").each(function() {
    var $el = $(this);
    var id = $el.attr("id") || $el.attr("name");
    if (id && $el.val()) draft[id] = $el.val();
  });
  return draft;
}

function saveQuickDraft() {
  try {
    var draft = collectQuickDraft();
    localStorage.setItem(QUICK_DRAFT_KEY, JSON.stringify(draft));
    $("#autosaveDot").addClass("saved");
    $("#autosaveText").text(t("autoSaved") + " " + new Date().toLocaleTimeString());
    setTimeout(function() { $("#autosaveDot").removeClass("saved"); }, 1500);
  } catch(e) {}
}

function restoreQuickDraft() {
  try {
    var raw = localStorage.getItem(QUICK_DRAFT_KEY);
    if (!raw) return;
    var draft = JSON.parse(raw);
    for (var id in draft) {
      if (!draft.hasOwnProperty(id)) continue;
      var $el = $("#" + id);
      if (!$el.length) $el = $("[name='" + escapeCssAttr(id) + "']");
      if ($el.length) $el.val(draft[id]);
    }
  } catch(e) {}
}

function autoSave() {
  saveQuickDraft();
}

function restoreDraft() {
  try {
    var raw = localStorage.getItem(DRAFT_KEY);
    if (!raw) return false;
    var draft = JSON.parse(raw);
    // Populate formData (authoritative store)
    for (var name in draft) {
      if (!draft.hasOwnProperty(name)) continue;
      formData[name] = draft[name];
      // Apply to rendered DOM elements
      var $field = $("[name='" + escapeCssAttr(name) + "']");
      if ($field.length) $field.val(draft[name]);
    }
    return true;
  } catch(e) { return false; }
}

function saveDraft() {
  try {
    // Use formData as source (includes unrendered component values)
    var draft = {};
    for (var name in formData) {
      if (formData.hasOwnProperty(name) && formData[name]) {
        draft[name] = formData[name];
      }
    }
    localStorage.setItem(DRAFT_KEY, JSON.stringify(draft));
  } catch(e) {}
}

function clearDraft() {
  showConfirm(t("clearConfirmTitle"), t("clearConfirmMsg"), function() {
    $(".field-group input, .field-group select, .field-group textarea").each(function() {
      $(this).val("");
    });
    $(".has-error").removeClass("has-error");
    $(".error-msg").text("").hide();
    $(".biz-warn").text("").hide();
    validationErrors = {};
    formData = {};
    try {
      localStorage.removeItem(DRAFT_KEY);
      localStorage.removeItem(QUICK_DRAFT_KEY);
    } catch(e) {}
    updateJSONPreview();
    updateProgress();
    showToast(t("draftCleared"));
  });
}

// ============================================================
// Module 12: Quick Fill Panel
// ============================================================

function renderQuickFillPanel() {
  var config = getRuntimeConfig();
  var fields = config.quickFillFields || [];
  var $container = $("#quickFillFields");
  $container.empty();

  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    var $row = $('<div class="form-group form-group-sm"></div>');
    var labelText = f.label_zh || f.label_en || f.label || f.key || "";
    if (f.label_en && f.label_zh) {
      labelText = f.label_zh + " / " + f.label_en;
    }
    var $label = $('<label class="control-label"></label>').text(labelText);
    $row.append($label);
    $row.append(renderQuickFillControl(f));
    $container.append($row);
  }
}

function renderQuickFillControl(field) {
  var type = field.control || field.type || "input";
  var $ctrl;
  if (type === "select" && field.options) {
    $ctrl = $('<select class="form-control input-sm"></select>');
    $ctrl.append('<option value="">' + t("pleaseSelect") + '</option>');
    for (var i = 0; i < field.options.length; i++) {
      var opt = field.options[i];
      var label = typeof opt === "object" ? (opt.label || opt.value) : opt;
      var value = typeof opt === "object" ? opt.value : opt;
      $ctrl.append($('<option></option>').val(value).text(label));
    }
  } else if (type === "textarea") {
    $ctrl = $('<textarea class="form-control input-sm" rows="2"></textarea>');
  } else if (type === "number") {
    $ctrl = $('<input type="text" class="form-control input-sm">');
    if (field.step) $ctrl.attr("data-step", field.step);
  } else if (type === "date") {
    $ctrl = $('<input type="text" class="form-control input-sm" placeholder="YYYY-MM-DD">');
  } else {
    $ctrl = $('<input type="text" class="form-control input-sm">');
  }
  $ctrl.attr("id", "quick_" + (field.key || field.target || ""));
  $ctrl.attr("data-target", field.target || "");
  if (field.placeholder) $ctrl.attr("placeholder", field.placeholder);
  return $ctrl;
}

function toggleRmtInfPanel() {
  var $panel = $("#quickPanel");
  if ($panel.is(":visible")) {
    $panel.hide();
  } else {
    $panel.show();
  }
}

function syncRmtInfToForm() {
  $("#quickFillFields input, #quickFillFields select, #quickFillFields textarea").each(function() {
    var $el = $(this);
    var target = $el.attr("data-target");
    var value = $el.val();
    if (!target || !value) return;
    var $field = $("[name$='" + escapeCssAttr(target) + "']");
    if ($field.length) {
      $field.val(value).trigger("change");
    }
  });
  showToast(t("rmtSynced"));
  updateJSONPreview();
  updateProgress();
}

function clearRmtInfPanel() {
  $("#quickFillFields input, #quickFillFields select, #quickFillFields textarea").each(function() {
    $(this).val("");
  });
}

// ============================================================
// Module 13: Runtime Configuration
// ============================================================

function getRuntimeConfig() {
  var appConfig = window.ISO20022_APP_CONFIG || {};
  var msgConfig = appConfig.messages && appConfig.messages[MESSAGE_ID] || {};
  return {
    templates: msgConfig.templates || {},
    quickFillFields: msgConfig.quickFillFields || [],
    fieldStateStyles: msgConfig.fieldStateStyles || {},
    fieldStateOverrides: msgConfig.fieldStateOverrides || [],
    fieldAliases: msgConfig.fieldAliases || {},
    valueMappings: msgConfig.valueMappings || {}
  };
}

function applyRuntimeConfig() {
  var config = window.ISO20022_APP_CONFIG || {};
  if (config.showTemplateBar === false) {
    $("#templateBar").hide();
  }
  renderPresetTemplates();
  renderQuickFillPanel();
  applyFieldStateStyles();
  applyFieldStateOverrides();
  applyFieldApiMetadata();
}

function applyFieldApiMetadata() {
  for (var i = 0; i < fieldMeta.length; i++) {
    var meta = fieldMeta[i];
    var $field = $("[name='" + escapeCssAttr(meta.form_name) + "']");
    if ($field.length) {
      $field.attr("data-iso-path", meta.iso_path || "");
      $field.attr("data-form-name", meta.form_name || "");
    }
  }
}

function applyFieldStateStyles() {
  var config = getRuntimeConfig();
  var styles = config.fieldStateStyles || {};
  // Apply as body data attributes for CSS to pick up
  var $body = $("body");
  for (var state in styles) {
    if (!styles.hasOwnProperty(state)) continue;
    $body.attr("data-state-" + state, styles[state]);
  }
}

function applyFieldStateOverrides() {
  var config = getRuntimeConfig();
  var overrides = config.fieldStateOverrides || [];
  for (var i = 0; i < overrides.length; i++) {
    var rule = overrides[i];
    var target = rule.target || "";
    var state = rule.state || "";
    if (!target || !state) continue;
    var $fields = $(target);
    $fields.each(function() {
      var $el = $(this);
      var $group = $el.closest(".field-group");
      $group.removeClass("field-required field-readonly field-editable field-disabled field-hidden");
      $group.addClass("field-" + state);
      if (state === "readonly" || state === "disabled") {
        $el.prop("readonly", true);
      } else if (state === "hidden") {
        $group.hide();
      } else if (state === "required") {
        $el.attr("data-api-required", "true");
      }
    });
  }
}

// ============================================================
// Module 15: Component Renderer (Lazy)
// ============================================================

var renderState = {};
var componentTemplates = window.COMPONENT_TEMPLATES || {};
var componentInstances = window.COMPONENT_INSTANCES || [];

function renderComponent(pathPrefix, componentType, $container) {
  if (renderState[pathPrefix]) return;
  var template = componentTemplates[componentType];
  if (!template) return;

  // Find instance overrides
  var overrides = null;
  for (var i = 0; i < componentInstances.length; i++) {
    if (componentInstances[i].pathPrefix === pathPrefix) {
      overrides = componentInstances[i].overrides || null;
      break;
    }
  }

  var prefix = pathPrefix.indexOf("AH_") === 0 ? "AH" : "DOC";
  var html = buildComponentHtml(template.fields, pathPrefix, prefix, overrides);
  $container.html(html);
  $container.attr("data-rendered", "true");
  renderState[pathPrefix] = true;

  initComponentAfterRender($container, pathPrefix);
}

function buildComponentHtml(fields, pathPrefix, prefix, overrides) {
  var parts = [];
  var leafBuf = [];

  function flushLeaves() {
    for (var i = 0; i < leafBuf.length; i += 2) {
      var pair = leafBuf.slice(i, i + 2);
      parts.push('<div class="field-grid">\n' + pair.join("\n") + "\n</div>");
    }
    leafBuf = [];
  }

  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    var fieldPath = pathPrefix + "_" + f.tag;
    // Apply overrides to field
    var ef = applyFieldOverrides(f, overrides);
    if (ef.type === "container") {
      flushLeaves();
      parts.push(buildContainerHtml(ef, fieldPath, prefix, overrides));
    } else {
      leafBuf.push(buildLeafHtml(ef, fieldPath, prefix));
    }
  }
  flushLeaves();
  return parts.join("\n");
}

function applyFieldOverrides(f, overrides) {
  if (!overrides) return f;
  var tag = f.tag;
  var result = {};
  for (var k in f) { if (f.hasOwnProperty(k)) result[k] = f[k]; }
  // Apply mandatory override
  if (overrides.mandatory) {
    for (var i = 0; i < overrides.mandatory.length; i++) {
      if (overrides.mandatory[i] === tag) { result.multMin = 1; break; }
    }
  }
  // Apply type changes
  if (overrides.typeChanges && overrides.typeChanges[tag]) {
    var tc = overrides.typeChanges[tag];
    if (tc.maxLen) result.maxLen = tc.maxLen;
    if (tc.type) result.type = tc.type;
  }
  return result;
}

function buildContainerHtml(f, fieldPath, prefix, overrides) {
  var children = f.children || [];
  if (typeof children === "string" && children.charAt(0) === "$") {
    var refName = children.substring(1);
    var refTpl = componentTemplates[refName];
    children = refTpl ? refTpl.fields : [];
  }
  var multMin = f.multMin || 0;
  var multMax = f.multMax || 1;
  var collapseId = "collapse_" + fieldPath;
  var badge = multMin >= 1
    ? '<span class="label label-danger">必填 / Required</span>'
    : '<span class="label label-info">可选 / Optional</span>';
  var collapsedIn = multMin >= 1 ? " in" : "";
  var headingClass = multMin >= 1 ? "" : " collapsed";

  var childHtml = "";
  if (multMax > 1) {
    childHtml = buildRepeatGroupHtml(f, children, fieldPath, prefix, multMin, multMax, overrides);
    return childHtml;
  }

  var innerHtml = buildComponentHtml(children, fieldPath, prefix, overrides);
  return '<div class="panel panel-default">\n' +
    '  <div class="panel-heading' + headingClass + '" data-toggle="collapse" data-target="#' + collapseId + '">\n' +
    '    <h4 class="panel-title">\n' +
    '      ' + escapeHtml(f.nameZh || "") + ' / ' + escapeHtml(f.nameEn || "") + ' ' + badge + '\n' +
    '      <span class="toggle-icon">&#9660;</span>\n' +
    '    </h4>\n' +
    '  </div>\n' +
    '  <div id="' + collapseId + '" class="panel-body collapse' + collapsedIn + '">\n' +
    '    ' + innerHtml + '\n' +
    '  </div>\n' +
    '</div>';
}

function buildRepeatGroupHtml(f, children, fieldPath, prefix, multMin, multMax, overrides) {
  var repeatId = "repeat_" + fieldPath;
  var maxDisp = multMax >= 9999 ? "*" : String(multMax);
  var innerHtml = buildComponentHtml(children, fieldPath, prefix, overrides);
  var hideStyle = multMin === 0 ? ' style="display:none"' : "";
  var tplClass = multMin === 0 ? " repeat-template" : "";
  return '<div class="repeat-group panel panel-default" id="' + repeatId + '" ' +
    'data-repeat-group="' + repeatId + '" data-min="' + multMin + '" data-max="' + multMax + '">\n' +
    '  <div class="panel-heading">\n' +
    '    <h4 class="panel-title" style="display:inline">' + escapeHtml(f.nameZh || "") + ' / ' + escapeHtml(f.nameEn || "") + '</h4>\n' +
    '    <span class="label label-default">[' + multMin + '..' + maxDisp + ']</span>\n' +
    '    <button type="button" class="btn btn-xs btn-primary btn-repeat-add pull-right">+ 添加</button>\n' +
    '  </div>\n' +
    '  <div class="panel-body repeat-items" id="' + repeatId + '_items">\n' +
    '    <div class="repeat-item' + tplClass + '" data-index="1"' + hideStyle + '>\n' +
    '      <span class="repeat-index">第1条</span>\n' +
    '      <button type="button" class="btn btn-xs btn-danger btn-repeat-remove">×</button>\n' +
    '      ' + innerHtml + '\n' +
    '    </div>\n' +
    '  </div>\n' +
    '</div>';
}

function buildLeafHtml(f, fieldPath, prefix) {
  var formName = fieldPath;
  var isoPath = buildIsoPath(prefix, fieldPath);
  var multMin = f.multMin || 0;
  var multMax = f.multMax || 1;

  // Repeatable leaf (e.g., AdrLine [0..2]) → render as repeat-leaf
  if (multMax > 1 && !f.isFixed) {
    return buildRepeatLeafHtml(f, fieldPath, prefix, multMin, multMax);
  }

  var isRequired = multMin >= 1;
  var stateClass = isRequired ? "field-required" : "field-editable";
  if (f.isFixed) stateClass = "field-readonly";
  var reqMark = isRequired ? '<span class="required text-danger">*</span>' : "";
  var maxDisp = multMax >= 9999 ? "*" : String(multMax);

  var inputHtml = buildInputHtml(f, formName, prefix, isoPath);
  var hintHtml = "";
  if (f.pattern) {
    hintHtml = '<div class="hint">格式 / Format: ' + escapeHtml(f.pattern) + '</div>';
  } else if (f.maxLen && f.maxLen > 0) {
    hintHtml = '<div class="hint">最大长度 / Max: ' + f.maxLen + '</div>';
  }

  return '<div class="field-group ' + stateClass + '" ' +
    'data-iso-path="' + escapeHtml(isoPath) + '" ' +
    'data-form-name="' + escapeHtml(formName) + '" ' +
    'data-required="' + (isRequired ? "true" : "false") + '">\n' +
    '  <label class="control-label" for="' + escapeHtml(formName) + '">\n' +
    '    ' + escapeHtml(f.nameZh || "") + ' <span class="en">' + escapeHtml(f.nameEn || "") + ' (' + escapeHtml(f.tag) + ')</span>\n' +
    '    ' + reqMark + '\n' +
    '    <span class="mult-tag">[' + multMin + '..' + maxDisp + ']</span>\n' +
    '  </label>\n' +
    '  ' + inputHtml + '\n' +
    '  ' + hintHtml + '\n' +
    '  <div class="error-msg"></div>\n' +
    '</div>';
}

function buildRepeatLeafHtml(f, fieldPath, prefix, multMin, multMax) {
  var repeatId = "repeat_" + fieldPath;
  var formName = fieldPath;
  var isoPath = buildIsoPath(prefix, fieldPath);
  var maxDisp = multMax >= 9999 ? "*" : String(multMax);
  var inputHtml = buildInputHtml(f, formName, prefix, isoPath);
  var hintHtml = "";
  if (f.pattern) {
    hintHtml = '<div class="hint">格式 / Format: ' + escapeHtml(f.pattern) + '</div>';
  } else if (f.maxLen && f.maxLen > 0) {
    hintHtml = '<div class="hint">最大长度 / Max: ' + f.maxLen + '</div>';
  }
  var itemInner = '<div class="field-group field-editable" ' +
    'data-iso-path="' + escapeHtml(isoPath) + '" ' +
    'data-form-name="' + escapeHtml(formName) + '" data-required="false">\n' +
    '        ' + inputHtml + '\n' +
    '        ' + hintHtml + '\n' +
    '        <div class="error-msg"></div>\n' +
    '      </div>';
  var hideStyle = multMin === 0 ? ' style="display:none"' : "";
  var tplClass = multMin === 0 ? " repeat-template" : "";
  return '<div class="repeat-group repeat-leaf panel panel-default" id="' + repeatId + '" ' +
    'data-repeat-group="' + repeatId + '" data-min="' + multMin + '" data-max="' + multMax + '">\n' +
    '  <div class="panel-heading">\n' +
    '    <h4 class="panel-title" style="display:inline">' + escapeHtml(f.nameZh || "") + ' / ' + escapeHtml(f.nameEn || "") + '</h4>\n' +
    '    <span class="label label-default">[' + multMin + '..' + maxDisp + ']</span>\n' +
    '    <button type="button" class="btn btn-xs btn-primary btn-repeat-add pull-right">+ 添加</button>\n' +
    '  </div>\n' +
    '  <div class="panel-body repeat-items" id="' + repeatId + '_items">\n' +
    '    <div class="repeat-item' + tplClass + '" data-index="1"' + hideStyle + '>\n' +
    '      <span class="repeat-index">第1条</span>\n' +
    '      <button type="button" class="btn btn-xs btn-danger btn-repeat-remove">×</button>\n' +
    '      ' + itemInner + '\n' +
    '    </div>\n' +
    '  </div>\n' +
    '</div>';
}

function buildInputHtml(f, formName, prefix, isoPath) {
  var tag = f.tag;
  var typeCode = f.type || "text";
  var maxLen = f.maxLen || 0;
  var maxAttr = maxLen > 0 ? ' maxlength="' + maxLen + '"' : "";
  var common = 'class="form-control" id="' + escapeHtml(formName) + '" ' +
    'name="' + escapeHtml(formName) + '" ' +
    'data-prefix="' + escapeHtml(prefix) + '" ' +
    'data-tag="' + escapeHtml(tag) + '" ' +
    'data-iso-path="' + escapeHtml(isoPath) + '" ' +
    'data-form-name="' + escapeHtml(formName) + '" ' +
    'data-type-code="' + escapeHtml(typeCode) + '"';

  if (f.isFixed) {
    return '<input type="text" ' + common + maxAttr + ' readonly="readonly" value="' + escapeHtml(f.fixedValue || "") + '">';
  }
  if (f.codeValues && f.codeValues.length > 0) {
    var opts = '<option value="">-- 请选择 / Please select --</option>\n';
    for (var i = 0; i < f.codeValues.length; i++) {
      var cv = f.codeValues[i];
      opts += '    <option value="' + escapeHtml(cv.code || "") + '">' +
        escapeHtml(cv.code || "") + ' - ' + escapeHtml(cv.description_zh || cv.description_en || "") +
        '</option>\n';
    }
    return '<select ' + common + '>\n    ' + opts + '</select>';
  }
  if (typeCode === "date") return '<input type="text" ' + common + maxAttr + ' placeholder="YYYY-MM-DD">';
  if (typeCode === "dateTime") return '<input type="text" ' + common + maxAttr + ' placeholder="YYYY-MM-DDThh:mm:ss">';
  if (typeCode === "time") return '<input type="text" ' + common + maxAttr + ' placeholder="hh:mm:ss">';
  if (typeCode === "decimal") return '<input type="text" ' + common + maxAttr + ' placeholder="0.00">';
  if (typeCode === "boolean") {
    return '<select ' + common + '>\n' +
      '  <option value="">-- 请选择 / Please select --</option>\n' +
      '  <option value="true">是 / Yes (true)</option>\n' +
      '  <option value="false">否 / No (false)</option>\n' +
      '</select>';
  }
  return '<input type="text" ' + common + maxAttr + '>';
}

function buildIsoPath(prefix, fieldPath) {
  var parts = fieldPath.split("_");
  parts.shift();
  var dotPath = parts.join(".");
  if (prefix === "AH") return "AppHdr." + dotPath;
  return "Document." + dotPath;
}

function initComponentAfterRender($container, pathPrefix) {
  $container.find("[data-repeat-group]").each(function() {
    saveRepeatTemplate($(this));
    updateRepeatRemoveState($(this));
    updateRepeatAddState($(this));
  });
  initChoiceGroupsInContainer($container);
  buildTooltipsInContainer($container);
  restoreDraftForComponent(pathPrefix);
  updateProgress();
}

function initChoiceGroupsInContainer($container) {
  var groups = window.CHOICE_GROUPS || [];
  if (!groups.length) return;

  for (var i = 0; i < groups.length; i++) {
    var group = groups[i];
    var options = group.options || [];
    if (options.length < 2) continue;

    var firstTag = options[0].tag;

    // Search for choice groups by leaf field match
    $container.find(".field-group[data-form-name$='_" + firstTag + "']").each(function() {
      var $first = $(this);
      var baseFormName = _getBaseName($first, firstTag);
      if (!baseFormName) return;

      var panelSet = [];
      var allFound = true;
      for (var j = 0; j < options.length; j++) {
        var targetName = baseFormName + options[j].tag;
        var $el = $container.find(".field-group[data-form-name='" + targetName + "']");
        if (!$el.length) {
          $el = $container.find("[id$='" + targetName + "']").filter("[id^='collapse_']").closest(".panel");
        }
        if ($el.length) {
          panelSet.push({ tag: options[j].tag, name: options[j].name, $el: $el });
        } else { allFound = false; break; }
      }
      if (!allFound || panelSet.length !== options.length) return;

      _updateChoiceState(panelSet);
      for (var p = 0; p < panelSet.length; p++) {
        (function(panels) {
          panels[p].$el.on("input change", "input,select,textarea", function() {
            _updateChoiceState(panels);
          });
        })(panelSet);
      }
    });

    // Search for choice groups by container panel match
    $container.find("[id^='collapse_']").each(function() {
      var id = $(this).attr("id");
      if (!_endsWithTag(id, firstTag)) return;
      var $panel = $(this).closest(".panel");
      var baseFormName = _getBaseName($panel, firstTag);
      if (!baseFormName) return;

      var panelSet = [];
      var allFound = true;
      for (var j = 0; j < options.length; j++) {
        var targetName = baseFormName + options[j].tag;
        var $el = $container.find("[id$='" + targetName + "']").filter("[id^='collapse_']").closest(".panel");
        if (!$el.length) {
          $el = $container.find(".field-group[data-form-name='" + targetName + "']");
        }
        if ($el.length) {
          panelSet.push({ tag: options[j].tag, name: options[j].name, $el: $el });
        } else { allFound = false; break; }
      }
      if (!allFound || panelSet.length !== options.length) return;

      _updateChoiceState(panelSet);
      for (var p = 0; p < panelSet.length; p++) {
        (function(panels) {
          panels[p].$el.on("input change", "input,select,textarea", function() {
            _updateChoiceState(panels);
          });
        })(panelSet);
      }
    });
  }
}

function buildTooltipsInContainer($container) {
  $container.find(".field-group").each(function() {
    var $fg = $(this);
    var formName = $fg.attr("data-form-name");
    if (!formName) return;
    var meta = findFieldMetaByFormName(formName);
    if (!meta) return;
    var tipHtml = '<div class="field-tooltip">';
    tipHtml += '<span class="tip-tag">&lt;' + escapeHtml(meta.tag || meta.xml_tag || "") + '&gt;</span>';
    tipHtml += '<div>' + (meta.multMin >= 1 ? '必填' : '可选') + '</div>';
    tipHtml += '</div>';
    $fg.css("position", "relative").append(tipHtml);
  });
}

function findFieldMetaByFormName(formName) {
  var meta = window.FIELD_META || [];
  for (var i = 0; i < meta.length; i++) {
    if (meta[i].form_name === formName) return meta[i];
  }
  // Check in component instances expanded fields
  return null;
}

function restoreDraftForComponent(pathPrefix) {
  for (var name in formData) {
    if (!formData.hasOwnProperty(name)) continue;
    if (name.indexOf(pathPrefix) === 0 && formData[name]) {
      var $field = $("[name='" + escapeCssAttr(name) + "']");
      if ($field.length) $field.val(formData[name]);
    }
  }
}

function searchTemplateFields(fields, query, pathPrefix) {
  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    var nameZh = (f.nameZh || "").toLowerCase();
    var nameEn = (f.nameEn || "").toLowerCase();
    var tag = (f.tag || "").toLowerCase();
    if (nameZh.indexOf(query) !== -1 || nameEn.indexOf(query) !== -1 || tag.indexOf(query) !== -1) {
      return true;
    }
    var children = f.children || [];
    if (typeof children === "string" && children.charAt(0) === "$") {
      var refTpl = componentTemplates[children.substring(1)];
      if (refTpl) children = refTpl.fields;
      else children = [];
    }
    if (children.length > 0 && searchTemplateFields(children, query, pathPrefix + "_" + f.tag)) {
      return true;
    }
  }
  return false;
}

// ============================================================
// Module 14: Initialization & Event Binding
// ============================================================

$(document).ready(function() {
  // --- Load saved preferences ---
  try {
    var savedTheme = localStorage.getItem("iso20022-theme");
    if (savedTheme === "dark") {
      $("body").removeClass("theme-light").addClass("theme-dark");
    }
    var savedLang = localStorage.getItem("iso20022-lang");
    if (savedLang) currentLang = savedLang;
    var savedReqOnly = localStorage.getItem("iso20022-required-only");
    if (savedReqOnly === "1") {
      requiredOnlyMode = true;
      $("body").addClass("required-only");
    }
  } catch(e) {}

  // --- Apply runtime configuration ---
  applyRuntimeConfig();

  // --- Tag field groups ---
  $(".field-group").each(function() {
    var $fg = $(this);
    var $input = $fg.find("input, select, textarea").first();
    if (!$input.length) return;
    var name = $input.attr("name") || "";
    var meta = findFieldMeta(name);
    if (meta && meta.mult_min >= 1) {
      $fg.addClass("field-required").attr("data-required", "true");
    }
  });

  // --- Tag all-optional panels ---
  $(".panel.panel-default").each(function() {
    var $panel = $(this);
    var $body = $panel.find("> .panel-body");
    if (!$body.length) return;
    var hasRequired = $body.find(".field-group.field-required").length > 0;
    if (!hasRequired) {
      $panel.addClass("panel-all-optional");
    }
  });

  // --- Add amount display elements ---
  $("[data-type='decimal']").each(function() {
    var $el = $(this);
    if (!$el.siblings(".amount-display").length) {
      $el.after('<div class="amount-display" style="display:none"></div>');
    }
  });

  // --- Add date format hints ---
  $("[data-type='date']").each(function() {
    var $el = $(this);
    if (!$el.siblings(".date-hint").length) {
      $el.after('<span class="date-hint text-muted">YYYY-MM-DD</span>');
    }
  });
  $("[data-type='dateTime']").each(function() {
    var $el = $(this);
    if (!$el.siblings(".date-hint").length) {
      $el.after('<span class="date-hint text-muted">YYYY-MM-DDThh:mm:ss</span>');
    }
  });

  // --- Initialize repeat group states ---
  $("[data-repeat-group]").each(function() {
    saveRepeatTemplate($(this));
    updateRepeatRemoveState($(this));
    updateRepeatAddState($(this));
  });

  // --- Build field tooltips ---
  $(".field-group").each(function() {
    var $fg = $(this);
    var formName = $fg.attr("data-form-name");
    if (!formName) return;
    var meta = findFieldMeta(formName);
    if (!meta) return;
    var tipHtml = '<div class="field-tooltip">';
    tipHtml += '<span class="tip-tag">&lt;' + escapeHtml(meta.xml_tag) + '&gt;</span>';
    tipHtml += '<div>类型: ' + escapeHtml(meta.type_code) + '</div>';
    if (meta.max_length > 0) {
      tipHtml += '<div>最大长度: ' + meta.max_length + '</div>';
    }
    tipHtml += '<div>' + (meta.mult_min >= 1 ? '必填' : '可选') + ' [' + meta.mult_min + '..' + (meta.mult_max >= 9999 ? '*' : meta.mult_max) + ']</div>';
    if (meta.iso_path) {
      tipHtml += '<div style="font-size:10px;margin-top:3px">' + escapeHtml(meta.iso_path) + '</div>';
    }
    tipHtml += '</div>';
    $fg.css("position", "relative").append(tipHtml);
  });

  // --- Restore quick draft silently ---
  restoreQuickDraft();

  // --- Render required components that are already expanded ---
  $("[data-component][data-rendered='false']").each(function() {
    var $comp = $(this);
    if ($comp.hasClass("in")) {
      var type = $comp.attr("data-component");
      var pathPrefix = $comp.attr("data-path-prefix");
      renderComponent(pathPrefix, type, $comp);
    }
  });

  // --- Initial UI state ---
  switchLang(currentLang);
  initChoiceGroups();
  updateProgress();

  // --- Start auto-save timer (30s) ---
  autoSaveTimer = setInterval(function() {
    autoSave();
    saveDraft();
  }, 30000);

  // ==================== Event Bindings ====================

  // Template buttons
  $(document).on("click", ".template-btn", function() {
    var key = $(this).attr("data-template-key");
    if (key) applyTemplate(key);
  });

  // Search (input + propertychange for IE8 compatibility)
  var lastSearchQuery = "";
  $(document).on("input keyup", "#fieldSearch", function(e) {
    // Skip navigation keys to avoid resetting matches
    if (e.keyCode === 13 || e.keyCode === 27 || e.keyCode === 38 || e.keyCode === 40) return;
    var val = $(this).val();
    if (val !== lastSearchQuery) {
      lastSearchQuery = val;
      searchFields(val);
    }
  });
  $(document).on("keydown", "#fieldSearch", function(e) {
    if (e.keyCode === 13) { // Enter
      e.preventDefault();
      if (e.shiftKey) stepMatch(-1); else stepMatch(1);
    } else if (e.keyCode === 27) { // Escape
      clearSearch();
    }
  });
  $(document).on("click", "#searchPrev", function() { stepMatch(-1); });
  $(document).on("click", "#searchNext", function() { stepMatch(1); });
  $(document).on("click", "#searchClear", function() { clearSearch(); });

  // Ctrl+F override
  $(document).on("keydown", function(e) {
    if ((e.ctrlKey || e.metaKey) && e.keyCode === 70) {
      e.preventDefault();
      $("#fieldSearch").focus();
    }
  });

  // Repeat groups
  $(document).on("click", ".btn-repeat-add", function() {
    var groupId = $(this).closest("[data-repeat-group]").attr("data-repeat-group");
    addRepeatItem(groupId);
  });
  $(document).on("click", ".btn-repeat-remove", function() {
    removeRepeatItem(this);
  });

  // Component lazy rendering: render on panel expand
  $(document).on("show.bs.collapse", "[data-component]", function() {
    var $container = $(this);
    if ($container.attr("data-rendered") === "false") {
      var type = $container.attr("data-component");
      var pathPrefix = $container.attr("data-path-prefix");
      renderComponent(pathPrefix, type, $container);
    }
  });

  // Form field changes (delegated)
  $(document).on("input change", ".field-group input, .field-group select, .field-group textarea", function() {
    var $el = $(this);
    var name = $el.attr("name");
    var value = $el.val() || "";
    if (!name) return;

    var oldValue = formData[name] || "";
    formData[name] = value;

    // Emit change event via API
    if (window.ISO20022_FORM_API && window.ISO20022_FORM_API._emit) {
      window.ISO20022_FORM_API._emit("change", {field: name, value: value, oldValue: oldValue});
    }

    // Validate
    var msg = validateField(name, value);
    setFieldError(name, msg);

    // Business rules
    checkBusinessRules(name, value);

    // At-least-one groups
    checkAtLeastOneGroups(name);

    // Amount display
    if ($el.attr("data-type-code") === "decimal") {
      updateAmountDisplay(name);
    }

    // Currency consistency
    if (name.indexOf("_CCY") !== -1) {
      checkCurrencyConsistency();
    }

    // Update preview and progress
    updateJSONPreview();
    updateProgress();
  });

  // Currency field change listeners
  $(document).on("change", "[name*='_CCY']", function() {
    checkCurrencyConsistency();
    // Update amount displays for related amount fields
    var name = $(this).attr("name") || "";
    var amtName = name.replace("_CCY", "");
    updateAmountDisplay(amtName);
  });
});

// Expose public API functions for form_api.py
window.APP = {
  validateField: validateField,
  validateAll: validateAll,
  findFieldMeta: findFieldMeta,
  buildISO20022JSON: buildISO20022JSON,
  showToast: showToast,
  formData: formData,
  validationErrors: validationErrors,
  setFieldError: setFieldError,
  escapeCssAttr: escapeCssAttr
};

})(jQuery, window);
"""
