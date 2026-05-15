"""Generate the ES5 ISO20022 form API scripts (jQuery-based, IE8+ compatible).

This module produces the public API layer that external systems call.
"""

from __future__ import annotations


def get_api_key(message_id: str, variant: str = "") -> str:
    """Return a business-readable API key such as PACS008 or PACS008STP."""
    parts = (message_id or "iso.000").split(".")
    family = parts[0].upper() if parts else "ISO"
    number = parts[1] if len(parts) > 1 else "000"
    base = family + "".join(ch for ch in number if ch.isalnum())
    suffix = "".join(ch for ch in (variant or "").upper() if ch.isalnum())
    return base + suffix


def get_api_file_name(message_id: str, variant: str = "") -> str:
    """Return the per-message API filename, e.g. PACS008API.js."""
    return get_api_key(message_id, variant) + "API.js"


def get_form_api_global_name(message_id: str, variant: str = "") -> str:
    """Return the long compatibility global name, e.g. PACS008_FORM_API."""
    parts = (message_id or "iso.000").split(".")
    family = parts[0].upper() if parts else "ISO"
    number = "".join(ch for ch in (parts[1] if len(parts) > 1 else "000") if ch.isalnum())
    suffix = "".join(ch for ch in (variant or "").upper() if ch.isalnum())
    if suffix:
        return f"{family}{number}_{suffix}_FORM_API"
    return f"{family}{number}_FORM_API"


def get_form_api_script() -> str:
    """Return the shared API factory JavaScript as a string."""
    return _API_SCRIPT


def get_form_api_registration_script(message_id: str, variant: str = "") -> str:
    """Return the thin per-message API registration JavaScript."""
    api_key = get_api_key(message_id, variant)
    api_var = api_key + "API"
    global_name = get_form_api_global_name(message_id, variant)
    root_id = api_key + "_PAGE"
    return (
        "// ===== " + api_var + " registration =====\n"
        "(function(window) {\n"
        "  'use strict';\n"
        "  var factory = window.ISO20022_FORM_API_FACTORY;\n"
        "  if (!factory || !factory.create) return;\n"
        "  var api = factory.create({\n"
        f"    messageId: {message_id!r},\n"
        f"    dataKey: {api_key!r},\n"
        f"    rootId: {root_id!r},\n"
        f"    apiName: {api_var!r},\n"
        f"    formApiName: {global_name!r}\n"
        "  });\n"
        "  window.ISO20022_FORM_APIS = window.ISO20022_FORM_APIS || {};\n"
        f"  window.ISO20022_FORM_APIS[{api_key!r}] = api;\n"
        f"  window[{api_var!r}] = api;\n"
        f"  window[{global_name!r}] = api;\n"
        "  window.ISO20022_FORM_API = api;\n"
        "})(window);\n"
    )


_API_SCRIPT = r"""
// ===== ISO20022_FORM_API_FACTORY (ES5 + jQuery, IE8+ compatible) =====
(function($, window, document) {
  'use strict';

  function trim(s) {
    return String(s == null ? '' : s).replace(/^\s+|\s+$/g, '');
  }

  function normalizeIsoPath(path) {
    return String(path || '')
      .replace(/^\/+/, '')
      .replace(/\//g, '.')
      .replace(/_/g, '.')
      .replace(/\.+/g, '.')
      .replace(/^\.+|\.+$/g, '');
  }

  function escapeXml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
  }

  function isArray(value) {
    return Object.prototype.toString.call(value) === '[object Array]';
  }

  function parseIndexedPart(part) {
    var match = /^([^\[]+)(?:\[(\d+)\])?$/.exec(String(part || ''));
    if (!match) return { key: part, index: 0 };
    return {
      key: match[1],
      index: match[2] ? parseInt(match[2], 10) : 0
    };
  }

  function assignNested(root, path, value) {
    var parts = String(path || '').split('.');
    var current = root;
    var start = 0;
    if (parts[0] === 'AppHdr' || parts[0] === 'Document') start = 1;
    for (var i = start; i < parts.length; i++) {
      var parsed = parseIndexedPart(parts[i]);
      var key = parsed.key;
      var index = parsed.index;
      if (!key) continue;
      if (index > 0) {
        if (!current[key]) current[key] = [];
        if (!isArray(current[key])) current[key] = [current[key]];
        while (current[key].length < index) current[key].push({});
        if (i === parts.length - 1) {
          current[key][index - 1] = value;
        } else {
          if (!current[key][index - 1] || typeof current[key][index - 1] !== 'object') {
            current[key][index - 1] = {};
          }
          current = current[key][index - 1];
        }
        continue;
      }
      if (i === parts.length - 1) {
        current[key] = value;
      } else {
        if (!current[key]) current[key] = {};
        current = current[key];
      }
    }
  }

  function objectToXml(obj, tagName) {
    var xml = '';
    if (isArray(obj)) {
      for (var i = 0; i < obj.length; i++) {
        if (obj[i] !== undefined && obj[i] !== null) xml += objectToXml(obj[i], tagName);
      }
      return xml;
    }
    if (typeof obj !== 'object' || obj == null) {
      return '<' + tagName + '>' + escapeXml(obj) + '</' + tagName + '>';
    }
    if (tagName) xml += '<' + tagName + '>';
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        xml += objectToXml(obj[key], key);
      }
    }
    if (tagName) xml += '</' + tagName + '>';
    return xml;
  }

  function jsonToXml(json) {
    var xml = '<?xml version="1.0" encoding="UTF-8"?>';
    xml += objectToXml(json.AppHdr || {}, 'AppHdr');
    xml += objectToXml(json.Document || {}, 'Document');
    return xml;
  }

  function getData(dataKey) {
    var dataStore = window.ISO20022_FORM_DATA || {};
    return dataStore[dataKey] || {};
  }

  function contains(root, el) {
    if (!root || !el) return false;
    if (root === document) return true;
    if (root === el) return true;
    return $.contains(root, el);
  }

  function firstMessageId(config) {
    var messages = config.messages || {};
    for (var k in messages) {
      if (messages.hasOwnProperty(k)) return k;
    }
    return 'unknown';
  }

  function findApiByElement(el) {
    var apis = window.ISO20022_FORM_APIS || {};
    for (var key in apis) {
      if (apis.hasOwnProperty(key) && apis[key] &&
          apis[key].containsElement && apis[key].containsElement(el)) {
        return apis[key];
      }
    }
    return window.ISO20022_FORM_API || null;
  }

  function createApi(options) {
    options = options || {};
    var dataKey = options.dataKey || 'default';
    var data = getData(dataKey);
    var appConfig = data.appConfig || window.ISO20022_APP_CONFIG || {};
    var MESSAGE_ID = options.messageId || firstMessageId(appConfig);
    var fieldMeta = data.fieldMeta || window.FIELD_META || [];
    var apiEvents = {};
    var formMode = 'create';
    var initialValues = {};
    var rootId = options.rootId || '';
    var suppressDomChange = false;
    var customValidators = [];
    var apiValidationErrors = {};
    var formErrorSeq = 0;

    function getRoot() {
      var root = rootId ? document.getElementById(rootId) : null;
      return root || document;
    }

    function $find(selector) {
      var root = getRoot();
      if (root === document) return $(selector);
      var $items = $(root).find(selector);
      if ($(root).is(selector)) $items = $items.add(root);
      return $items;
    }

    function findByName(name) {
      return $find('[name="' + String(name).replace(/"/g, '\\"') + '"]');
    }

    function findByFormName(formName) {
      var safe = String(formName || '').replace(/"/g, '\\"');
      var $fieldGroup = $find('.field-group[data-form-name="' + safe + '"]');
      if ($fieldGroup.length) return $fieldGroup;
      var $input = findByName(formName);
      if ($input.length) return $input.closest('.field-group');
      var $collapse = $find('[id="collapse_' + safe + '"]');
      if ($collapse.length) return $collapse.closest('.panel');
      return $();
    }

    function getRuntimeConfig() {
      var messages = appConfig.messages || {};
      return messages[MESSAGE_ID] || messages['default'] || {};
    }

    function getAliasTarget(key) {
      var cfg = getRuntimeConfig();
      var aliases = cfg.fieldAliases || {};
      var mappings = cfg.valueMappings || {};
      return aliases[key] || mappings[key] || null;
    }

    function findFieldMetaByKey(key) {
      var normalized = normalizeIsoPath(key);
      for (var i = 0; i < fieldMeta.length; i++) {
        var meta = fieldMeta[i];
        if (meta.form_name === key || meta.iso_path === key ||
            normalizeIsoPath(meta.iso_path) === normalized) {
          return meta;
        }
      }
      return null;
    }

    function splitFormNameWithRepeatSuffix(formName) {
      var name = String(formName || '');
      var best = null;
      for (var i = 0; i < fieldMeta.length; i++) {
        var base = fieldMeta[i].form_name || '';
        if (!base) continue;
        if (name === base || name.indexOf(base + '_') === 0) {
          var suffix = name.substring(base.length);
          var ok = true;
          if (suffix) {
            var parts = suffix.substring(1).split('_');
            for (var p = 0; p < parts.length; p++) {
              if (!/^\d+$/.test(parts[p])) { ok = false; break; }
            }
          }
          if (ok && (!best || base.length > best.base.length)) {
            best = { base: base, suffix: suffix };
          }
        }
      }
      if (best) return best;
      return { base: name.replace(/(?:_\d+)+$/, ''), suffix: name.match(/(?:_\d+)+$/) ? name.match(/(?:_\d+)+$/)[0] : '' };
    }

    function normalizeIsoPathForParse(path) {
      return String(path || '')
        .replace(/^\/+/, '')
        .replace(/\//g, '.')
        .replace(/\.+/g, '.')
        .replace(/^\.+|\.+$/g, '');
    }

    function stripPathIndexes(path) {
      return String(path || '').replace(/\[(?:\d+|\*)\]/g, '');
    }

    function formNameToIsoPath(formName) {
      var name = String(formName || '');
      var parts = name.split('_');
      if (parts[0] === 'AH') {
        parts.shift();
        if (parts[0] === 'AppHdr') parts.shift();
        return parts.length ? 'AppHdr.' + parts.join('.') : 'AppHdr';
      }
      if (parts[0] === 'DOC') {
        parts.shift();
        return parts.length ? 'Document.' + parts.join('.') : 'Document';
      }
      return name.replace(/_/g, '.');
    }

    function isMetaRepeatable(meta) {
      if (!meta) return false;
      var max = meta.mult_max;
      return max === Infinity || max === 'Infinity' || parseInt(max, 10) > 1;
    }

    function parsePath(path) {
      var raw = String(path || '');
      if (raw.indexOf('AH_') === 0 || raw.indexOf('DOC_') === 0) {
        return { isFormName: true, formName: raw, targetName: raw, repeatSteps: [] };
      }

      var normalized = normalizeIsoPathForParse(raw);
      var tokens = normalized ? normalized.split('.') : [];
      var prefix = 'DOC';
      var start = 0;
      if (tokens[0] === 'AppHdr') {
        prefix = 'AH';
        start = tokens[1] === 'AppHdr' ? 1 : 0;
      } else if (tokens[0] === 'Document') {
        prefix = 'DOC';
        start = 1;
      }

      var segments = [];
      var suffixes = [];
      var repeatSteps = [];
      for (var i = start; i < tokens.length; i++) {
        var token = tokens[i];
        if (!token) continue;
        var match = /^([^\[]+)(?:\[(\d+|\*)\])?$/.exec(token);
        if (!match) continue;
        var tag = match[1];
        var indexText = match[2] || '';
        segments.push(tag);

        if (indexText && indexText !== '*') {
          var index = parseInt(indexText, 10);
          if (index < 1) index = 1;
          var baseName = prefix + '_' + segments.join('_');
          var suffixBefore = suffixes.join('');
          repeatSteps.push({
            formName: baseName + suffixBefore,
            groupId: 'repeat_' + baseName + suffixBefore,
            index: index
          });
          if (index > 1) suffixes.push('_' + index);
        }
      }

      var targetBase = prefix + '_' + segments.join('_');
      var targetMeta = findFieldMetaByKey(stripPathIndexes(normalized));
      if (targetMeta && targetMeta.form_name) targetBase = targetMeta.form_name;
      return {
        isFormName: false,
        formName: targetBase,
        targetName: targetBase + suffixes.join(''),
        repeatSteps: repeatSteps
      };
    }

    function getRepeatContextsForElement(el, isoPath) {
      var contexts = [];
      var $groups = $(el).parents('[data-repeat-group]');
      for (var i = $groups.length - 1; i >= 0; i--) {
        var $group = $($groups[i]);
        var groupName = String($group.attr('data-repeat-group') || '').replace(/^repeat_/, '');
        var split = splitFormNameWithRepeatSuffix(groupName);
        var meta = findFieldMetaByKey(split.base);
        var groupIsoPath = meta && meta.iso_path ? meta.iso_path : formNameToIsoPath(split.base);
        var $items = $group.children('.repeat-items').children('.repeat-item').not('.repeat-template');
        var itemIndex = 0;
        $items.each(function(idx) {
          if (this === el || $.contains(this, el)) {
            itemIndex = idx + 1;
            return false;
          }
        });
        if (groupIsoPath && itemIndex > 0) {
          contexts.push({ isoPath: normalizeIsoPathForParse(groupIsoPath), index: itemIndex });
        }
      }

      if (!contexts.length && el && el.name) {
        var nameSplit = splitFormNameWithRepeatSuffix(el.name);
        var suffixParts = nameSplit.suffix ? nameSplit.suffix.substring(1).split('_') : [];
        if (suffixParts.length) {
          var parts = normalizeIsoPathForParse(isoPath).split('.');
          var prefixParts = [];
          var suffixIdx = 0;
          for (var p = 0; p < parts.length && suffixIdx < suffixParts.length; p++) {
            prefixParts.push(parts[p]);
            var prefixPath = prefixParts.join('.');
            var prefixMeta = findFieldMetaByKey(prefixPath);
            if (isMetaRepeatable(prefixMeta)) {
              contexts.push({ isoPath: normalizeIsoPathForParse(prefixPath), index: parseInt(suffixParts[suffixIdx], 10) || 1 });
              suffixIdx++;
            }
          }
        }
      }
      return contexts;
    }

    function applyRepeatContextsToIsoPath(isoPath, contexts) {
      var parts = normalizeIsoPathForParse(isoPath).split('.');
      var out = [];
      var prefix = [];
      for (var i = 0; i < parts.length; i++) {
        if (!parts[i]) continue;
        prefix.push(parts[i]);
        var prefixPath = normalizeIsoPathForParse(prefix.join('.'));
        var token = parts[i];
        for (var j = 0; j < contexts.length; j++) {
          if (contexts[j].isoPath === prefixPath) {
            token += '[' + contexts[j].index + ']';
            break;
          }
        }
        out.push(token);
      }
      return out.join('.');
    }

    function getElementIsoPath(el, indexed) {
      var isoPath = $(el).attr('data-iso-path') || '';
      if (!isoPath || indexed === false) return isoPath;
      return applyRepeatContextsToIsoPath(isoPath, getRepeatContextsForElement(el, isoPath));
    }

    function openPath(path) {
      var parsed = parsePath(path);
      var formName = parsed.targetName || parsed.formName;
      if (window.APP && window.APP.openPathByFormName) {
        window.APP.openPathByFormName(formName, getRoot(), data);
      }
      var el = resolveFieldElement(formName);
      if (el && window.APP && window.APP.openPathByFormName) {
        window.APP.openPathByFormName(el.name || formName, getRoot(), data);
      }
      return { ok: !!el, name: formName, element: el || null };
    }

    function ensureRepeatGroup(groupId, count) {
      if (!window.APP || !window.APP.getRepeatItemCount || !window.APP.addRepeatItem) {
        return { ok: false, groupId: groupId, error: 'repeat API unavailable' };
      }
      var current = window.APP.getRepeatItemCount(groupId, getRoot());
      while (current < count) {
        var before = current;
        window.APP.addRepeatItem(groupId, getRoot());
        current = window.APP.getRepeatItemCount(groupId, getRoot());
        if (current <= before) {
          return { ok: false, groupId: groupId, count: current, error: 'repeat item not added' };
        }
      }
      return { ok: true, groupId: groupId, count: current };
    }

    function ensurePath(path, options) {
      options = options || {};
      var parsed = parsePath(path);
      for (var i = 0; i < parsed.repeatSteps.length; i++) {
        var step = parsed.repeatSteps[i];
        if (options.autoOpen !== false && window.APP && window.APP.openPathByFormName) {
          window.APP.openPathByFormName(step.formName, getRoot(), data);
        }
        if (options.autoRepeat === false) {
          var current = window.APP && window.APP.getRepeatItemCount
            ? window.APP.getRepeatItemCount(step.groupId, getRoot())
            : 0;
          if (current < step.index) {
            return { ok: false, groupId: step.groupId, count: current, error: 'repeat item missing' };
          }
          continue;
        }
        var ensured = ensureRepeatGroup(step.groupId, step.index);
        if (!ensured.ok) return ensured;
      }
      if (options.autoOpen !== false) openPath(parsed.targetName);
      return { ok: true, name: parsed.targetName, formName: parsed.formName, repeatSteps: parsed.repeatSteps };
    }

    function setChoiceElementState($el, active, clearValue) {
      if (!$el || !$el.length) return;
      $el.toggleClass('choice-disabled', !active);
      $el.find('.field-group').toggleClass('field-disabled', !active);
      if (active) {
        $el.find('.field-group').removeClass('field-disabled').addClass('field-required');
        if ($el.hasClass('field-group')) $el.removeClass('field-disabled').addClass('field-required');
      } else {
        $el.find('.field-group').addClass('field-disabled').removeClass('field-required');
        if ($el.hasClass('field-group')) $el.addClass('field-disabled').removeClass('field-required');
      }
      $el.find('input,select,textarea').each(function() {
        if (!active && clearValue) $(this).val('');
        $(this).prop('disabled', !active).prop('readonly', !active);
      });
      if ($el.hasClass('field-group')) {
        $el.find('input,select,textarea').each(function() {
          if (!active && clearValue) $(this).val('');
          $(this).prop('disabled', !active).prop('readonly', !active);
        });
      }
    }

    function activateChoice(reference, options) {
      options = options || {};
      var parsed = parsePath(reference);
      var targetName = parsed.targetName || String(reference || '');
      var split = splitFormNameWithRepeatSuffix(targetName);
      var baseName = split.base;
      var suffix = split.suffix || '';
      var lastUnderscore = baseName.lastIndexOf('_');
      if (lastUnderscore === -1) return { ok: false, name: targetName, error: 'choice base not found' };
      var basePrefix = baseName.substring(0, lastUnderscore + 1);
      var targetTag = baseName.substring(lastUnderscore + 1);
      var groups = data.choiceGroups || window.CHOICE_GROUPS || [];

      for (var i = 0; i < groups.length; i++) {
        var optionsList = groups[i].options || [];
        var targetIdx = -1;
        for (var j = 0; j < optionsList.length; j++) {
          if (optionsList[j].tag === targetTag) targetIdx = j;
        }
        if (targetIdx === -1) continue;

        var panelSet = [];
        var foundCount = 0;
        for (var k = 0; k < optionsList.length; k++) {
          var optionName = basePrefix + optionsList[k].tag + suffix;
          var $option = findByFormName(optionName);
          panelSet.push({ name: optionName, $el: $option });
          if ($option.length) foundCount++;
        }
        if (!foundCount) continue;

        for (var p = 0; p < panelSet.length; p++) {
          setChoiceElementState(
            panelSet[p].$el,
            p === targetIdx,
            p !== targetIdx && options.clearInactiveChoice !== false
          );
        }
        return { ok: true, name: targetName, choiceTag: targetTag };
      }
      return { ok: false, name: targetName, error: 'choice group not found' };
    }

    function setPathValue(path, value, options) {
      options = options || {};
      var ensured = ensurePath(path, options);
      if (!ensured.ok) return ensured;
      if (options.autoChoice !== false) activateChoice(ensured.name, options);
      if (options.autoOpen !== false) openPath(ensured.name);
      return setField(ensured.name, value, options);
    }

    function setPathValues(values, options) {
      var results = [];
      if (!values) return results;
      for (var path in values) {
        if (values.hasOwnProperty(path)) {
          results.push(setPathValue(path, values[path], options));
        }
      }
      return results;
    }

    function getPathValue(path, options) {
      options = options || {};
      var parsed = parsePath(path);
      var el = resolveFieldElement(parsed.targetName);
      if (!el && options.autoOpen) {
        ensurePath(path, { autoOpen: true, autoRepeat: false });
        el = resolveFieldElement(parsed.targetName);
      }
      return el ? el.value : null;
    }

    function getPathValues(options) {
      options = options || {};
      var includeEmpty = options.includeEmpty;
      var indexed = options.indexed !== false;
      var out = {};
      $find('[data-iso-path]').each(function() {
        var path = getElementIsoPath(this, indexed);
        if (path && this.name && (includeEmpty || this.value !== '')) {
          out[path] = this.value;
        }
      });
      return out;
    }

    function ensureErrorBox($group) {
      var $err = $group.find('.error-msg:first');
      if (!$err.length) {
        $err = $('<div class="error-msg text-danger" style="display:none"></div>');
        $group.append($err);
      }
      return $err;
    }

    function setElementError(el, message) {
      if (!el) return false;
      var $group = $(el).closest('.field-group');
      if (!$group.length) $group = $(el);
      var $err = ensureErrorBox($group);
      if (message) {
        $group.addClass('has-error');
        $err.text(message).show();
      } else {
        $group.removeClass('has-error');
        $err.text('').hide();
      }
      return true;
    }

    function resolvePathElement(path, options) {
      options = options || {};
      var parsed = parsePath(path);
      var name = parsed.targetName;
      if (options.ensure !== false) {
        var ensured = ensurePath(path, {
          autoOpen: options.autoOpen !== false,
          autoRepeat: options.autoRepeat === true
        });
        if (ensured && ensured.ok) {
          name = ensured.name;
          if (options.autoChoice === true) activateChoice(name, options);
        }
      } else if (options.autoOpen !== false) {
        openPath(name);
      }
      if (options.autoOpen !== false) openPath(name);
      return resolveFieldElement(name);
    }

    function rememberApiError(el, path, message, source) {
      var name = el ? el.name : '';
      var actualPath = el ? getElementIsoPath(el, true) : path;
      var key = name || actualPath || ('_form_' + (++formErrorSeq));
      apiValidationErrors[key] = {
        field: name,
        path: actualPath || '',
        message: message,
        element: el || null,
        source: source || 'manual'
      };
      return apiValidationErrors[key];
    }

    function clearStoredErrorByPath(path, el) {
      var parsed = parsePath(path);
      var targetName = el ? el.name : parsed.targetName;
      var normalizedPath = normalizeIsoPathForParse(path);
      for (var key in apiValidationErrors) {
        if (!apiValidationErrors.hasOwnProperty(key)) continue;
        var err = apiValidationErrors[key];
        if (key === targetName || err.field === targetName ||
            normalizeIsoPathForParse(err.path) === normalizedPath) {
          delete apiValidationErrors[key];
        }
      }
    }

    function setPathError(path, message, options) {
      options = options || {};
      var msg = trim(message);
      var el = resolvePathElement(path, {
        ensure: options.ensure !== false,
        autoOpen: options.autoOpen !== false,
        autoRepeat: options.autoRepeat === true,
        autoChoice: options.autoChoice === true
      });
      if (!el) return { ok: false, path: path, error: 'field not found' };
      if (!msg) return clearPathError(path, options);
      setElementError(el, msg);
      var err = rememberApiError(el, path, msg, options.source || 'manual');
      return {
        ok: true,
        name: err.field,
        path: err.path,
        message: err.message,
        element: el
      };
    }

    function clearPathError(path, options) {
      options = options || {};
      var el = resolvePathElement(path, { ensure: false, autoOpen: false });
      if (el) setElementError(el, '');
      clearStoredErrorByPath(path, el);
      return { ok: true, path: path, name: el ? el.name : parsePath(path).targetName, element: el || null };
    }

    function clearApiErrorsBySource(source) {
      for (var key in apiValidationErrors) {
        if (!apiValidationErrors.hasOwnProperty(key)) continue;
        var err = apiValidationErrors[key];
        if (source && err.source !== source) continue;
        if (err.element) setElementError(err.element, '');
        delete apiValidationErrors[key];
      }
    }

    function clearErrors(options) {
      options = options || {};
      clearApiErrorsBySource('');
      if (options.visible !== false) {
        $find('.field-group.has-error').each(function() {
          var $field = $(this).find('[data-form-name]:first');
          setElementError($field.length ? $field[0] : this, '');
        });
      }
      var appErrors = (window.APP && window.APP.validationErrors) || {};
      $find('[data-form-name]').each(function() {
        if (this.name && appErrors.hasOwnProperty(this.name)) delete appErrors[this.name];
      });
      return { ok: true };
    }

    function extractIndexesFromPath(path) {
      var indexes = [];
      String(path || '').replace(/\[(\d+)\]/g, function(all, indexText) {
        indexes.push(indexText);
        return all;
      });
      return indexes;
    }

    function makeFieldInfo(el) {
      var indexedPath = getElementIsoPath(el, true);
      return {
        name: el.name || '',
        isoPath: $(el).attr('data-iso-path') || '',
        path: indexedPath,
        value: el.value,
        element: el,
        meta: findFieldMetaByKey(el.name),
        indexes: extractIndexesFromPath(indexedPath)
      };
    }

    function escapeRegExp(text) {
      return String(text || '').replace(/[-\/\\^$+?.()|[\]{}]/g, '\\$&');
    }

    function pathPatternMatches(pattern, path, isoPath) {
      var normalizedPattern = normalizeIsoPathForParse(pattern);
      var normalizedPath = normalizeIsoPathForParse(path);
      if (normalizedPattern.indexOf('[*]') !== -1) {
        var regex = '^' + escapeRegExp(normalizedPattern).replace(/\\\[\\\*\\\]/g, '\\[\\d+\\]') + '$';
        return new RegExp(regex).test(normalizedPath);
      }
      if (normalizedPattern === normalizedPath) return true;
      return normalizeIsoPath(normalizedPattern) === normalizeIsoPath(isoPath);
    }

    function findFieldsByPathPattern(pattern) {
      var out = [];
      $find('[data-iso-path]').each(function() {
        var info = makeFieldInfo(this);
        if (pathPatternMatches(pattern, info.path, info.isoPath)) out.push(info);
      });
      return out;
    }

    function makeValidationContext(rule, fieldInfo) {
      fieldInfo = fieldInfo || {};
      return {
        api: api,
        rule: rule,
        name: fieldInfo.name || '',
        path: fieldInfo.path || rule.path || '',
        isoPath: fieldInfo.isoPath || '',
        field: fieldInfo,
        element: fieldInfo.element || null,
        value: fieldInfo.value,
        indexes: fieldInfo.indexes || [],
        getField: getField,
        getPathValue: getPathValue,
        getPathValues: getPathValues,
        getJson: buildJson,
        setPathError: setPathError,
        clearPathError: clearPathError
      };
    }

    function getValidationContexts(rule) {
      var contexts = [];
      if (rule.path) {
        var fields = findFieldsByPathPattern(rule.path);
        if (!fields.length && String(rule.path).indexOf('[*]') === -1) {
          var el = resolvePathElement(rule.path, { ensure: false, autoOpen: false });
          if (el) fields.push(makeFieldInfo(el));
        }
        for (var i = 0; i < fields.length; i++) contexts.push(makeValidationContext(rule, fields[i]));
      } else {
        contexts.push(makeValidationContext(rule, null));
      }
      return contexts;
    }

    function normalizeValidationErrors(result, rule, ctx, out) {
      if (result === true || result === undefined || result === null) return;
      if (isArray(result)) {
        for (var i = 0; i < result.length; i++) normalizeValidationErrors(result[i], rule, ctx, out);
        return;
      }
      if (result === false) {
        result = { message: rule.message || 'invalid field' };
      } else if (typeof result === 'string') {
        result = { message: result };
      }
      if (typeof result !== 'object') return;
      if (result.valid === true || result.ok === true) return;
      if (result.valid === false || result.ok === false || result.message || result.msg) {
        out.push({
          path: result.path || result.isoPath || result.field || ctx.path || rule.path || '',
          message: result.message || result.msg || rule.message || 'invalid field'
        });
      }
    }

    function runCustomValidators() {
      var collected = [];
      clearApiErrorsBySource('validator');
      for (var i = 0; i < customValidators.length; i++) {
        var rule = customValidators[i];
        if (!rule || typeof rule.validate !== 'function') continue;
        var contexts = getValidationContexts(rule);
        for (var c = 0; c < contexts.length; c++) {
          var ctx = contexts[c];
          try {
            normalizeValidationErrors(rule.validate.call(api, ctx), rule, ctx, collected);
          } catch (err) {
            collected.push({
              path: ctx.path || rule.path || '',
              message: (rule.message || rule.name || 'custom validation failed') + ': ' + (err && err.message ? err.message : err)
            });
          }
        }
      }
      for (var e = 0; e < collected.length; e++) {
        if (collected[e].path) {
          setPathError(collected[e].path, collected[e].message, {
            source: 'validator',
            autoOpen: true,
            autoRepeat: false,
            autoChoice: false
          });
        } else {
          rememberApiError(null, '', collected[e].message, 'validator');
        }
      }
      for (var key in apiValidationErrors) {
        if (apiValidationErrors.hasOwnProperty(key) && apiValidationErrors[key].element) {
          setElementError(apiValidationErrors[key].element, apiValidationErrors[key].message);
        }
      }
      return collected;
    }

    function registerValidator(rule) {
      if (typeof rule === 'function') rule = { validate: rule };
      rule = rule || {};
      if (typeof rule.validate !== 'function') return function() {};
      customValidators.push(rule);
      return function() {
        for (var i = customValidators.length - 1; i >= 0; i--) {
          if (customValidators[i] === rule) customValidators.splice(i, 1);
        }
      };
    }

    function stripWildcardIndexes(path) {
      return stripPathIndexes(path);
    }

    function patternBaseFormName(pattern) {
      return parsePath(stripWildcardIndexes(pattern)).formName;
    }

    function extractIndexesFromFieldName(pattern, actualName) {
      var base = patternBaseFormName(pattern);
      var suffix = '';
      if (actualName && actualName.indexOf(base + '_') === 0) {
        suffix = actualName.substring(base.length + 1);
      }
      var suffixParts = suffix ? suffix.split('_') : [];
      var indexes = [];
      var wildcardCount = (String(pattern || '').match(/\[\*\]/g) || []).length;
      for (var i = 0; i < wildcardCount; i++) {
        indexes.push(suffixParts[i] || '1');
      }
      return indexes;
    }

    function sourceMatches(pattern, field) {
      if (!pattern || !field) return false;
      if (String(pattern).indexOf('[*]') !== -1) {
        var base = patternBaseFormName(pattern);
        return field.name === base || field.name.indexOf(base + '_') === 0;
      }
      if (pattern === field.name || pattern === field.isoPath) return true;
      return normalizeIsoPath(pattern) === normalizeIsoPath(field.isoPath);
    }

    function applyWildcardIndexes(target, indexes) {
      var idx = 0;
      return String(target || '').replace(/\[\*\]/g, function() {
        var val = indexes[idx] || '1';
        idx++;
        return '[' + val + ']';
      });
    }

    function registerLinkage(rule) {
      rule = rule || {};
      if (!rule.source || !rule.target) {
        return function() {};
      }
      var busy = false;
      var off = onEvent('change', function(event) {
        if (busy) return;
        var field = getField(event.field);
        if (!field || !sourceMatches(rule.source, field)) return;

        var indexes = extractIndexesFromFieldName(rule.source, field.name);
        var target = typeof rule.target === 'function'
          ? rule.target(event.value, { event: event, field: field, indexes: indexes })
          : applyWildcardIndexes(rule.target, indexes);
        var nextValue = event.value;
        if (typeof rule.transform === 'function') {
          nextValue = rule.transform(event.value, { event: event, field: field, indexes: indexes, target: target });
        }

        busy = true;
        try {
          setPathValue(target, nextValue, {
            autoOpen: rule.autoOpen !== false,
            autoChoice: rule.autoChoice !== false,
            autoRepeat: rule.autoRepeat !== false,
            clearInactiveChoice: rule.clearInactiveChoice !== false,
            emit: rule.emit === true
          });
        } finally {
          busy = false;
        }
      });
      return off;
    }

    function findElementByIdInRoot(id) {
      var root = getRoot();
      var el = document.getElementById(id);
      if (el && contains(root, el)) return el;
      var $found = $find('[id="' + String(id).replace(/"/g, '\\"') + '"]');
      return $found.length ? $found[0] : null;
    }

    function resolveFieldElement(reference) {
      if (!reference) return null;
      if (reference.nodeType === 1) return contains(getRoot(), reference) ? reference : null;
      if (reference.jquery) return reference[0] && contains(getRoot(), reference[0]) ? reference[0] : null;

      var key = String(reference);
      var alias = getAliasTarget(key);
      if (alias) {
        if (typeof alias === 'string') return resolveFieldElement(alias);
        if (alias.name) return resolveFieldElement(alias.name);
        if (alias.isoPath) return resolveFieldElement(alias.isoPath);
        if (alias.target) return resolveFieldElement(alias.target);
      }

      if (key.indexOf('[name="') === 0 || key.indexOf("[name='") === 0) {
        key = key.substring(7, key.length - 2);
      }

      var meta = findFieldMetaByKey(key);
      if (meta && meta.form_name) {
        var el = findElementByIdInRoot(meta.form_name);
        if (el) return el;
      }

      var el2 = findElementByIdInRoot(key);
      if (el2) return el2;

      var $found = findByName(key);
      return $found.length ? $found[0] : null;
    }

    function buildJson() {
      var json = { AppHdr: {}, Document: {} };
      $find('[data-iso-path]').each(function() {
        var el = this;
        if (!el.name || !el.value || trim(el.value) === '') return;
        var path = getElementIsoPath(el, true);
        if (path.indexOf('AppHdr') === 0) assignNested(json.AppHdr, path, el.value);
        else if (path.indexOf('Document') === 0) assignNested(json.Document, path, el.value);
      });
      return json;
    }

    function emitEvent(type, payload) {
      var handlers = apiEvents[type] || [];
      var event = $.extend({ type: type, messageId: MESSAGE_ID, mode: formMode }, payload || {});
      for (var i = 0; i < handlers.length; i++) {
        try { handlers[i](event); } catch (e) {}
      }
      return event;
    }

    function emitFromDom(type, payload) {
      if (suppressDomChange && type === 'change') return null;
      return emitEvent(type, payload);
    }

    function onEvent(type, handler) {
      if (!apiEvents[type]) apiEvents[type] = [];
      apiEvents[type].push(handler);
      return function() { offEvent(type, handler); };
    }

    function offEvent(type, handler) {
      var handlers = apiEvents[type];
      if (!handlers) return;
      for (var i = handlers.length - 1; i >= 0; i--) {
        if (handlers[i] === handler) handlers.splice(i, 1);
      }
    }

    function setField(key, value, options) {
      var el = resolveFieldElement(key);
      if (!el) return { ok: false, key: key, error: 'field not found' };
      var oldValue = el.value;
      suppressDomChange = true;
      try {
        $(el).val(value == null ? '' : String(value)).trigger('change');
      } finally {
        suppressDomChange = false;
      }
      if (!options || options.emit !== false) {
        emitEvent('change', { field: el.name, value: el.value, oldValue: oldValue, element: el });
      }
      return {
        ok: true,
        name: el.name,
        isoPath: $(el).attr('data-iso-path') || '',
        value: el.value,
        element: el
      };
    }

    function getField(key) {
      var el = resolveFieldElement(key);
      if (!el) return null;
      return {
        name: el.name,
        isoPath: $(el).attr('data-iso-path') || '',
        value: el.value,
        element: el,
        meta: findFieldMetaByKey(el.name)
      };
    }

    function setValues(values, options) {
      var results = [];
      if (!values) return results;
      for (var key in values) {
        if (values.hasOwnProperty(key)) {
          results.push(setField(key, values[key], { emit: options ? options.emit : true }));
        }
      }
      return results;
    }

    function getValues(options) {
      var includeEmpty = options && options.includeEmpty;
      var out = {};
      $find('[data-form-name]').each(function() {
        if (this.name && (includeEmpty || this.value !== '')) {
          out[this.name] = this.value;
        }
      });
      return out;
    }

    function getIsoPathValues(options) {
      var includeEmpty = options && options.includeEmpty;
      var out = {};
      $find('[data-iso-path]').each(function() {
        var path = getElementIsoPath(this, false);
        if (path && this.name && (includeEmpty || this.value !== '')) {
          out[path] = this.value;
        }
      });
      return out;
    }

    function clearValues(options) {
      $find('[data-form-name]').each(function() {
        if (!this.readOnly && !this.disabled) {
          $(this).val('').trigger('change');
        }
      });
      emitEvent('clear', {});
    }

    function importNested(obj, prefix) {
      for (var key in obj) {
        if (!obj.hasOwnProperty(key)) continue;
        var value = obj[key];
        if (value && typeof value === 'object' && value['#text'] !== undefined) {
          var fieldName = prefix + '_' + key;
          var $el = findByName(fieldName);
          if ($el.length) $el.val(value['#text']).trigger('change');
          var ccy = value['@Ccy'] || value.Ccy;
          if (ccy) {
            var $ccyEl = findByName(fieldName + '_CCY');
            if ($ccyEl.length) $ccyEl.val(ccy).trigger('change');
          }
        } else if (typeof value === 'object' && value !== null) {
          importNested(value, prefix + '_' + key);
        } else {
          var fn = prefix + '_' + key;
          var $field = findByName(fn);
          if ($field.length) $field.val(String(value)).trigger('change');
        }
      }
    }

    function loadJson(json) {
      if (!json) return;
      if (json.AppHdr) importNested(json.AppHdr, 'AH_AppHdr');
      if (json.Document) {
        var docKey = null;
        for (var k in json.Document) { if (json.Document.hasOwnProperty(k)) { docKey = k; break; } }
        if (docKey) importNested(json.Document[docKey], 'DOC_' + docKey);
      }
      snapshotInitialValues();
      emitEvent('load', { json: json, fieldCount: $find('[data-form-name]').length });
    }

    function getErrors() {
      var errors = [];
      var seen = {};
      var validationErrors = (window.APP && window.APP.validationErrors) || {};
      for (var name in validationErrors) {
        if (validationErrors.hasOwnProperty(name) && validationErrors[name]) {
          var el = findElementByIdInRoot(name) || findByName(name)[0] || null;
          if (el) {
            seen[name] = true;
            errors.push({ field: name, path: getElementIsoPath(el, true), message: validationErrors[name], element: el, source: 'builtin' });
          }
        }
      }
      $find('.has-error [data-form-name]').each(function() {
        var name = this.name || $(this).attr('data-form-name') || '';
        if (!name || validationErrors[name]) return;
        var msg = $(this).closest('.field-group').find('.error-msg').text() || 'invalid field';
        if (seen[name]) return;
        seen[name] = true;
        errors.push({ field: name, path: getElementIsoPath(this, true), message: msg, element: this, source: 'dom' });
      });
      for (var key in apiValidationErrors) {
        if (!apiValidationErrors.hasOwnProperty(key)) continue;
        var err = apiValidationErrors[key];
        var errKey = err.field || err.path || key;
        if (seen[errKey]) continue;
        seen[errKey] = true;
        errors.push({
          field: err.field,
          path: err.path,
          message: err.message,
          element: err.element,
          source: err.source || 'api'
        });
      }
      return errors;
    }

    function validate() {
      if (window.APP && window.APP.validateAll) {
        window.APP.validateAll();
      }
      runCustomValidators();
      var errors = getErrors();
      var result = { valid: errors.length === 0, errorCount: errors.length, errors: errors };
      emitEvent('validate', result);
      return result;
    }

    function submit(options) {
      var json = buildJson();
      var xml = jsonToXml(json);
      var evt = emitEvent('beforeSubmit', { json: json, xml: xml, cancel: false });
      if (evt.cancel) return { cancelled: true };

      var valResult = validate();
      var result = {
        valid: valResult.valid,
        mode: formMode,
        values: getValues({ includeEmpty: false }),
        json: json,
        xml: xml,
        errors: valResult.errors
      };
      if (options && options.focusFirstError && !valResult.valid) {
        focusFirstError();
      }
      emitEvent('submit', result);
      return result;
    }

    function snapshotInitialValues() {
      initialValues = {};
      $find('[data-form-name]').each(function() {
        if (this.name) initialValues[this.name] = this.value || '';
      });
    }

    function getDirtyFields() {
      var dirty = [];
      $find('[data-form-name]').each(function() {
        if (!this.name) return;
        var init = initialValues.hasOwnProperty(this.name) ? initialValues[this.name] : '';
        if (this.value !== init) dirty.push(this.name);
      });
      return dirty;
    }

    function reset() {
      for (var name in initialValues) {
        if (!initialValues.hasOwnProperty(name)) continue;
        var $el = findByName(name);
        if ($el.length) $el.val(initialValues[name]).trigger('change');
      }
    }

    function setFieldState(key, state, options) {
      var el = resolveFieldElement(key);
      if (!el) return { ok: false, key: key, error: 'field not found' };
      var $group = $(el).closest('.field-group');
      if ($group.length) {
        $group.removeClass('field-required field-editable field-readonly field-disabled field-hidden');
        if (state === 'hidden') $group.addClass('field-hidden');
        if (state === 'required') $group.addClass('field-required');
        if (state === 'readonly') $group.addClass('field-readonly');
        if (state === 'disabled') $group.addClass('field-disabled');
        if (state === 'editable') $group.addClass('field-editable');
      }
      if (state === 'required') $(el).attr('data-required', 'true');
      if (state === 'editable' || state === 'visible') {
        el.readOnly = false;
        el.disabled = false;
      }
      if (state === 'readonly') el.readOnly = true;
      if (state === 'disabled') el.disabled = true;
      return { ok: true, name: el.name, state: state, element: el };
    }

    function setFieldsState(stateMap, options) {
      var results = [];
      for (var key in stateMap) {
        if (stateMap.hasOwnProperty(key)) {
          results.push(setFieldState(key, stateMap[key], options));
        }
      }
      return results;
    }

    function findFieldsByIsoPathPrefix(prefix) {
      var normalized = normalizeIsoPath(prefix);
      var out = [];
      $find('[data-iso-path]').each(function() {
        var path = normalizeIsoPath($(this).attr('data-iso-path'));
        if (path === normalized || path.indexOf(normalized + '.') === 0) {
          out.push(this);
        }
      });
      return out;
    }

    function setPathState(prefix, state, options) {
      var fields = findFieldsByIsoPathPrefix(prefix);
      var results = [];
      for (var i = 0; i < fields.length; i++) {
        results.push(setFieldState(fields[i], state, options));
      }
      return results;
    }

    function setMode(mode, options) {
      var previousMode = formMode;
      formMode = mode || 'create';
      if (formMode === 'review' || formMode === 'readonly') {
        setPathState('AppHdr', 'readonly', { refresh: false });
        setPathState('Document', 'readonly', { refresh: false });
      }
      if (!options || options.emit !== false) {
        emitEvent('modeChange', { mode: formMode, previousMode: previousMode });
      }
      return formMode;
    }

    function focusFirstError() {
      var $first = $find('.has-error [data-form-name]:first');
      if ($first.length) {
        $first.focus();
        $('html, body').animate({ scrollTop: $first.offset().top - 100 }, 300);
      }
    }

    function containsElement(el) {
      return contains(getRoot(), el);
    }

    function destroy() {
      apiEvents = {};
      initialValues = {};
      customValidators = [];
      apiValidationErrors = {};
      if (window.ISO20022_FORM_APIS && window.ISO20022_FORM_APIS[dataKey]) {
        delete window.ISO20022_FORM_APIS[dataKey];
      }
      if (options.apiName && window[options.apiName]) delete window[options.apiName];
      if (options.formApiName && window[options.formApiName]) delete window[options.formApiName];
    }

    var api = {
      messageId: MESSAGE_ID,
      dataKey: dataKey,
      rootId: rootId,
      setField: setField,
      getField: getField,
      setValues: setValues,
      setPathValue: setPathValue,
      setPathValues: setPathValues,
      getPathValue: getPathValue,
      getPathValues: getPathValues,
      ensurePath: ensurePath,
      openPath: openPath,
      activateChoice: activateChoice,
      setPathError: setPathError,
      clearPathError: clearPathError,
      clearErrors: clearErrors,
      getValues: getValues,
      getIsoPathValues: getIsoPathValues,
      clear: clearValues,
      loadJson: loadJson,
      importJson: loadJson,
      getJson: buildJson,
      getXml: function() { return jsonToXml(buildJson()); },
      validate: validate,
      submit: submit,
      getErrors: getErrors,
      getDirtyFields: getDirtyFields,
      reset: reset,
      destroy: destroy,
      setFieldState: setFieldState,
      setFieldsState: setFieldsState,
      setPathState: setPathState,
      findFieldsByIsoPathPrefix: findFieldsByIsoPathPrefix,
      setMode: setMode,
      getMode: function() { return formMode; },
      focusFirstError: focusFirstError,
      containsElement: containsElement,
      registerLinkage: registerLinkage,
      registerValidator: registerValidator,
      on: onEvent,
      off: offEvent,
      _emit: emitFromDom
    };

    $(function() {
      snapshotInitialValues();
      emitEvent('ready', { messageId: MESSAGE_ID, fieldCount: $find('[data-form-name]').length });
    });

    return api;
  }

  window.ISO20022_FORM_API_FACTORY = {
    create: createApi,
    findByElement: findApiByElement
  };

})(jQuery, window, document);
"""
