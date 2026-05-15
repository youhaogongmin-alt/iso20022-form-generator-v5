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

  function assignNested(root, path, value) {
    var parts = String(path || '').split('.');
    var current = root;
    var start = 0;
    if (parts[0] === 'AppHdr' || parts[0] === 'Document') start = 1;
    for (var i = start; i < parts.length; i++) {
      var key = parts[i];
      if (!key) continue;
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
        var path = $(el).attr('data-iso-path') || '';
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
      $(el).val(value == null ? '' : String(value)).trigger('change');
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
        var path = $(this).attr('data-iso-path');
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
      var validationErrors = (window.APP && window.APP.validationErrors) || {};
      for (var name in validationErrors) {
        if (validationErrors.hasOwnProperty(name) && validationErrors[name]) {
          var el = findElementByIdInRoot(name) || findByName(name)[0] || null;
          if (el) errors.push({ field: name, message: validationErrors[name], element: el });
        }
      }
      $find('.has-error [data-form-name]').each(function() {
        var name = this.name || $(this).attr('data-form-name') || '';
        if (!name || validationErrors[name]) return;
        var msg = $(this).closest('.field-group').find('.error-msg').text() || 'invalid field';
        errors.push({ field: name, message: msg, element: this });
      });
      return errors;
    }

    function validate() {
      if (window.APP && window.APP.validateAll) {
        window.APP.validateAll();
      }
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
      on: onEvent,
      off: offEvent,
      _emit: emitEvent
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
