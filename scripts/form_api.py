"""Generate the ES5 PACS008_FORM_API script (jQuery-based, IE8+ compatible).

This module produces the public API layer that external systems call.
The contract is identical to v3.3: same method names, same behavior,
same data-iso-path / data-form-name attributes.
"""

from __future__ import annotations


def get_pacs008_form_api_script() -> str:
    """Return the complete PACS008_FORM_API JavaScript as a string."""
    return _API_SCRIPT


_API_SCRIPT = r"""
// ===== PACS008_FORM_API (ES5 + jQuery, IE8+ compatible) =====
(function($, window) {
  'use strict';

  var MESSAGE_ID = window._PACS008_MESSAGE_ID || 'pacs.008.001.08';
  var fieldMeta = window.FIELD_META || [];
  var apiEvents = {};
  var formMode = 'create';

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

  function getRuntimeConfig() {
    var root = window.ISO20022_APP_CONFIG || {};
    var messages = root.messages || {};
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

  function resolveFieldElement(reference) {
    if (!reference) return null;
    if (reference.nodeType === 1) return reference;
    if (reference.jquery) return reference[0] || null;

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
      var el = document.getElementById(meta.form_name);
      if (el) return el;
    }

    var el2 = document.getElementById(key);
    if (el2) return el2;

    var $found = $('[name="' + key + '"]');
    return $found.length ? $found[0] : null;
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

  function buildJson() {
    var json = { AppHdr: {}, Document: {} };
    $('[data-iso-path]').each(function() {
      var el = this;
      if (!el.name || !el.value || trim(el.value) === '') return;
      var path = $(el).attr('data-iso-path') || '';
      if (path.indexOf('AppHdr') === 0) assignNested(json.AppHdr, path, el.value);
      else if (path.indexOf('Document') === 0) assignNested(json.Document, path, el.value);
    });
    return json;
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

  function emitEvent(type, payload) {
    var handlers = apiEvents[type] || [];
    var event = $.extend({ type: type, messageId: MESSAGE_ID, mode: formMode }, payload || {});
    for (var i = 0; i < handlers.length; i++) {
      try { handlers[i](event); } catch (e) {}
    }
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

  // --- Public API Methods ---

  function setField(key, value, options) {
    var el = resolveFieldElement(key);
    if (!el) return { ok: false, key: key, error: 'field not found' };
    $(el).val(value == null ? '' : String(value)).trigger('change');
    if (options && options.emit === false) { /* skip */ }
    else emitEvent('change', { name: el.name, value: el.value, element: el });
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
    $('[data-form-name]').each(function() {
      if (this.name && (includeEmpty || this.value !== '')) {
        out[this.name] = this.value;
      }
    });
    return out;
  }

  function getIsoPathValues(options) {
    var includeEmpty = options && options.includeEmpty;
    var out = {};
    $('[data-iso-path]').each(function() {
      var path = $(this).attr('data-iso-path');
      if (path && this.name && (includeEmpty || this.value !== '')) {
        out[path] = this.value;
      }
    });
    return out;
  }

  function clearValues(options) {
    $('[data-form-name]').each(function() {
      if (!this.readOnly && !this.disabled) {
        $(this).val('').trigger('change');
      }
    });
    emitEvent('clear', {});
  }

  function loadJson(json) {
    if (!json) return;
    if (json.AppHdr) importNested(json.AppHdr, 'AH_AppHdr');
    if (json.Document) {
      var docKey = null;
      for (var k in json.Document) { if (json.Document.hasOwnProperty(k)) { docKey = k; break; } }
      if (docKey) importNested(json.Document[docKey], 'DOC_' + docKey);
    }
    emitEvent('load', { json: json });
  }

  function importNested(obj, prefix) {
    for (var key in obj) {
      if (!obj.hasOwnProperty(key)) continue;
      var value = obj[key];
      if (value && typeof value === 'object' && value['#text'] !== undefined) {
        var fieldName = prefix + '_' + key;
        var $el = $('[name="' + fieldName + '"]');
        if ($el.length) $el.val(value['#text']).trigger('change');
        var ccy = value['@Ccy'] || value.Ccy;
        if (ccy) {
          var $ccyEl = $('[name="' + fieldName + '_CCY"]');
          if ($ccyEl.length) $ccyEl.val(ccy).trigger('change');
        }
      } else if (typeof value === 'object' && value !== null) {
        importNested(value, prefix + '_' + key);
      } else {
        var fn = prefix + '_' + key;
        var $field = $('[name="' + fn + '"]');
        if ($field.length) $field.val(String(value)).trigger('change');
      }
    }
  }

  function validate() {
    if (window.validateAll) {
      var valid = window.validateAll();
      return { valid: valid, errors: window.getFormErrors ? window.getFormErrors() : [] };
    }
    return { valid: true, errors: [] };
  }

  function submit(options) {
    var errors = validate().errors;
    var json = buildJson();
    var result = {
      valid: errors.length === 0,
      mode: formMode,
      values: getValues({ includeEmpty: false }),
      json: json,
      xml: jsonToXml(json),
      errors: errors
    };
    if (options && options.focusFirstError && errors.length) {
      var firstEl = resolveFieldElement(errors[0].name);
      if (firstEl) $(firstEl).focus();
    }
    emitEvent('submit', result);
    return result;
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
    $('[data-iso-path]').each(function() {
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
    formMode = mode || 'create';
    if (formMode === 'review' || formMode === 'readonly') {
      setPathState('AppHdr', 'readonly', { refresh: false });
      setPathState('Document', 'readonly', { refresh: false });
    }
    if (!options || options.emit !== false) emitEvent('modechange', { mode: formMode });
    return formMode;
  }

  function focusFirstError() {
    var $first = $('.has-error [data-form-name]:first');
    if ($first.length) {
      $first.focus();
      $('html, body').animate({ scrollTop: $first.offset().top - 100 }, 300);
    }
  }

  // --- Expose Public API ---
  window.PACS008_FORM_API = {
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
    setFieldState: setFieldState,
    setFieldsState: setFieldsState,
    setPathState: setPathState,
    findFieldsByIsoPathPrefix: findFieldsByIsoPathPrefix,
    setMode: setMode,
    getMode: function() { return formMode; },
    focusFirstError: focusFirstError,
    on: onEvent,
    off: offEvent
  };

  // Emit ready event when DOM is loaded
  $(function() {
    emitEvent('ready', { fieldCount: $('[data-form-name]').length });
  });

})(jQuery, window);
"""
