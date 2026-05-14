"""Generate app.css for the v4 form (IE8+ compatible, dual theme).

All CSS uses only CSS2.1 features: no var(), no flex, no grid, no sticky.
Theme switching is done via body.theme-light / body.theme-dark classes.
"""

from __future__ import annotations


def get_app_css() -> str:
    return _BASE_CSS + _LIGHT_THEME + _DARK_THEME + _FIELD_STATES + _COMPONENTS + _PRINT


_BASE_CSS = """
/* ===== Base Reset & Layout ===== */
body {
  font-family: "Microsoft YaHei", "Segoe UI", "PingFang SC", Arial, sans-serif;
  font-size: 13px;
  line-height: 1.5;
}

#page-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 15px 20px;
  position: relative;
}

.main-panel {
  min-height: 600px;
}

/* ===== Page Header ===== */
.page-header-bar {
  padding: 16px 24px;
  margin-bottom: 15px;
  border-radius: 6px;
}

.page-header-bar h1 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 2px;
  letter-spacing: 0.2px;
}

.page-header-bar .subtitle {
  font-size: 12px;
  margin: 0;
}

.page-header-bar .msg-id {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-family: Consolas, monospace;
  font-size: 12px;
  margin-top: 6px;
}

/* ===== Command Bar ===== */
.command-bar {
  margin-bottom: 12px;
  padding: 10px 15px;
  border-radius: 4px;
}

.command-bar .btn {
  margin-right: 5px;
  margin-bottom: 5px;
}

/* ===== Progress Bar ===== */
.progress-container {
  display: inline-block;
  *display: inline;
  *zoom: 1;
  width: 100%;
  margin-bottom: 12px;
  padding: 10px 15px;
  border-radius: 4px;
}

.progress-container .progress-label {
  float: left;
  font-size: 12px;
  font-weight: 600;
  line-height: 8px;
  margin-right: 12px;
}

.progress-container .progress {
  overflow: hidden;
  margin-bottom: 0;
  height: 8px;
  margin-right: 100px;
}

.progress-text {
  float: right;
  font-size: 12px;
  font-weight: 600;
  line-height: 8px;
  margin-top: -8px;
}

/* ===== Template Bar ===== */
.template-bar {
  margin-bottom: 12px;
  padding: 10px 15px;
  border-radius: 4px;
}

.template-bar .label-text {
  font-size: 12px;
  font-weight: 600;
  margin-right: 10px;
}

.template-btn {
  padding: 5px 12px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 11px;
  cursor: pointer;
  margin-right: 5px;
  margin-bottom: 5px;
}

.template-btn:hover {
  border-color: #337ab7;
  background: #e8f0fe;
}

.template-btn.active {
  border-color: #337ab7;
  background: #337ab7;
  color: white;
  font-weight: bold;
}

/* ===== Search Bar ===== */
.search-bar {
  position: sticky;
  top: 10px;
  z-index: 450;
  padding: 8px 14px;
  margin-bottom: 12px;
  border-radius: 4px;
}


.search-bar .form-control {
  font-size: 13px;
}

.search-count {
  font-size: 11px;
  line-height: 34px;
  padding-left: 10px;
}

/* ===== Section Divider ===== */
.section-divider {
  margin: 18px 0 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  line-height: 0;
}

.section-divider span {
  padding: 0 12px;
  font-size: 12px;
  font-weight: 600;
}

/* ===== Field Groups ===== */
.field-group {
  margin-bottom: 6px;
  padding: 4px 0 4px 8px;
  border: none;
  border-left: 3px solid transparent;
}

.field-group.field-required {
  border-left-color: #337ab7;
}

.field-group.field-readonly {
  border-left-color: #ccc;
}

.field-group .form-control {
  font-size: 12px;
  padding: 5px 8px;
  height: auto;
}

.field-group .control-label {
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 3px;
  display: block;
}

.field-group .control-label .en {
  font-weight: 400;
  font-size: 11px;
}

.field-group .control-label .required {
  font-weight: 700;
}

.field-group .control-label .mult-tag {
  font-size: 9px;
  padding: 0 4px;
  border-radius: 2px;
  font-family: monospace;
}

.field-group .hint {
  font-size: 11px;
  margin-top: 1px;
}

.field-group .error-msg {
  font-size: 11px;
  margin-top: 2px;
  display: none;
}

.field-group .error-msg.show {
  display: block;
}

.field-group .biz-warn {
  font-size: 11px;
  margin-top: 2px;
  padding: 3px 6px;
  border-radius: 2px;
  display: none;
}

.field-group .biz-warn.show {
  display: block;
}

.amount-row {
  overflow: hidden;
}

.amount-row .ccy-select {
  float: left;
  width: 90px;
  height: 30px;
  margin-right: 8px;
  padding: 4px 6px;
  font-size: 12px;
  display: block;
}

.amount-row .amt-input {
  display: block;
  overflow: hidden;
}

.amount-row .amt-input .form-control {
  width: 100%;
  height: 30px;
}

.field-group .amount-display {
  font-size: 11px;
  margin-top: 1px;
  font-weight: 600;
  display: none;
}

.field-group .amount-display.show {
  display: block;
}

/* ===== Field Grid (2-column float) ===== */
.field-grid:after {
  content: "";
  display: table;
  clear: both;
}

.field-grid .field-group {
  float: left;
  width: 49%;
  margin: 0 0.5% 10px;
  min-height: 60px;
}

@media (max-width: 992px) {
  .field-grid .field-group {
    width: 100%;
    margin: 0 0 10px;
    float: none;
  }
}

/* ===== Repeat Groups ===== */
.repeat-group {
  margin-bottom: 10px;
}

.repeat-group .panel-heading {
  padding: 8px 12px;
}

.repeat-leaf .repeat-item {
  padding: 6px 10px;
  margin-bottom: 4px;
}

.repeat-leaf .repeat-item .field-group {
  margin-bottom: 0;
  padding: 0;
}

.repeat-leaf .repeat-item .btn-repeat-remove {
  top: 8px;
}

.repeat-item {
  position: relative;
  border: 1px solid #ddd;
  border-radius: 3px;
  padding: 10px;
  margin-bottom: 8px;
}

.repeat-index {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  padding: 1px 8px;
  border-radius: 2px;
  margin-bottom: 6px;
}

.btn-repeat-remove {
  position: absolute;
  top: 6px;
  right: 6px;
}

/* ===== JSON Preview Panel ===== */
.json-panel .panel {
  margin-bottom: 0;
  height: 100%;
}

.json-panel .panel-body {
  overflow-y: auto;
  max-height: calc(100vh - 180px);
  max-height: 600px;
}

#jsonPreview {
  font-family: Consolas, "SF Mono", monospace;
  font-size: 11px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-all;
  border: none;
  background: transparent;
  width: 100%;
  min-height: 300px;
  resize: vertical;
}

/* ===== Summary View ===== */
.summary-view .summary-item {
  padding: 6px 0;
  border-bottom: 1px solid #eee;
  font-size: 12px;
}

.summary-view .summary-item:after {
  content: "";
  display: table;
  clear: both;
}

.summary-label {
  float: left;
  font-weight: 500;
  width: 80px;
}

.summary-value {
  margin-left: 90px;
  font-weight: 600;
  word-break: break-all;
}

/* ===== Toast ===== */
.toast-msg {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  z-index: 9999;
  display: none;
}

.toast-msg.show {
  display: block;
}

/* ===== Quick Fill Panel ===== */
.quick-panel {
  position: fixed;
  bottom: 80px;
  left: 20px;
  width: 420px;
  z-index: 500;
  display: none;
  max-height: 500px;
  overflow-y: auto;
}

.quick-panel.show {
  display: block;
}

.quick-panel-toggle {
  position: fixed;
  bottom: 24px;
  left: 24px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  font-size: 18px;
  z-index: 500;
  cursor: pointer;
}

/* ===== Validation Summary ===== */
.validation-summary {
  padding: 8px 14px;
  font-size: 12px;
  display: none;
  border-top: 1px solid #ddd;
}

.validation-summary.show {
  display: block;
}

/* ===== Search Highlight ===== */
.search-highlight {
  background: #fff3cd;
  padding: 1px 2px;
  border-radius: 2px;
}

.field-locate {
  outline: 1px dashed #2563a8;
  outline-offset: 2px;
}

.field-locate-active {
  outline: 3px solid #2563a8;
  outline-offset: 2px;
}

.panel-heading.field-locate,
.panel-heading.field-locate-active {
  outline-offset: -2px;
}

/* ===== Audit Mode ===== */
body.audit-mode input,
body.audit-mode select,
body.audit-mode textarea {
  pointer-events: none;
}

body.audit-mode .btn-repeat-add,
body.audit-mode .btn-repeat-remove,
body.audit-mode .template-btn {
  pointer-events: none;
  opacity: 0.5;
}

.audit-badge {
  display: none;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 3px;
  margin-left: 8px;
}

body.audit-mode .audit-badge {
  display: inline-block;
}

/* ===== Required-only Filter ===== */
body.required-only .panel-all-optional {
  display: none;
}

body.required-only .field-group[data-required="false"] {
  display: none;
}

/* ===== Confirm Modal ===== */
#confirmModal .modal-body p {
  font-size: 13px;
}

/* ===== Import Modal ===== */
#importModal textarea {
  width: 100%;
  min-height: 200px;
  font-family: Consolas, monospace;
  font-size: 11px;
}

/* PLACEHOLDER_THEMES */
"""

_LIGHT_THEME = """
/* ===== Light Theme ===== */
body, body.theme-light {
  background-color: #f0f1f3;
  color: #1c1e21;
}

body.theme-light .page-header-bar {
  background-color: #1b3a5c;
  color: #ffffff;
  border: 1px solid #15304d;
}

body.theme-light .page-header-bar .subtitle {
  color: rgba(255,255,255,0.7);
}

body.theme-light .page-header-bar .msg-id {
  background: rgba(255,255,255,0.12);
  color: #ffffff;
}

body.theme-light .command-bar,
body.theme-light .progress-container,
body.theme-light .template-bar,
body.theme-light .search-bar {
  background-color: #ffffff;
  border: 1px solid #d0d3d8;
}

body.theme-light .section-divider {
  border-bottom-color: #d0d3d8;
}

body.theme-light .section-divider span {
  background-color: #f0f1f3;
  color: #5a5f6b;
}

body.theme-light .panel-default > .panel-heading {
  background-color: #ebedf0;
  border-color: #d0d3d8;
  color: #1c1e21;
}

body.theme-light .panel-default {
  border-color: #d0d3d8;
}

body.theme-light .field-group {
  background-color: transparent;
}

body.theme-light .field-group .hint {
  color: #7b8794;
}

body.theme-light .field-group .error-msg {
  color: #c62828;
}

body.theme-light .field-group .biz-warn {
  color: #b45309;
  background-color: #fef3c7;
}

body.theme-light .field-group .hint {
  color: #5a5f6b;
}

body.theme-light .field-group .amount-display {
  color: #2563a8;
}

body.theme-light .field-group .control-label .en {
  color: #5a5f6b;
}

body.theme-light .field-group .control-label .required {
  color: #c62828;
}

body.theme-light .field-group .control-label .mult-tag {
  color: #5a5f6b;
  background-color: #f5f6f8;
}

body.theme-light .repeat-index {
  color: #2563a8;
  background-color: #e8eff8;
}

body.theme-light .search-highlight {
  background-color: #fef08a;
  color: #1c1e21;
}

body.theme-light .toast-msg {
  background-color: #1c1e21;
  color: #ffffff;
}

body.theme-light .quick-panel-toggle {
  background-color: #2563a8;
  color: #ffffff;
}

body.theme-light .audit-badge {
  background-color: #fef3c7;
  color: #b45309;
}

body.theme-light .template-btn.active {
  background-color: #2563a8;
  border-color: #2563a8;
  color: #ffffff;
}

body.theme-light .json-panel .panel {
  background-color: #ffffff;
}

body.theme-light .summary-item {
  border-bottom-color: #ebedf0;
}

body.theme-light .summary-label {
  color: #5a5f6b;
}

body.theme-light .summary-value {
  color: #1c1e21;
}

body.theme-light .validation-summary.valid {
  background-color: #e6f4ea;
  color: #1a7f37;
}

body.theme-light .validation-summary.error {
  background-color: #fde8e8;
  color: #c62828;
}
"""

_DARK_THEME = """
/* ===== Dark Theme ===== */
body.theme-dark {
  background-color: #18191a;
  color: #e4e6eb;
}

body.theme-dark .navbar-default {
  background-color: #242526;
  border-color: #3a3b3c;
}

body.theme-dark .navbar-default .navbar-brand {
  color: #e4e6eb;
}

body.theme-dark .page-header-bar {
  background-color: #242526;
  color: #e4e6eb;
  border: 1px solid #3a3b3c;
}

body.theme-dark .page-header-bar .subtitle {
  color: #b0b3b8;
}

body.theme-dark .page-header-bar .msg-id {
  background: rgba(255,255,255,0.08);
  color: #e4e6eb;
}

body.theme-dark .command-bar,
body.theme-dark .progress-container,
body.theme-dark .template-bar,
body.theme-dark .search-bar {
  background-color: #242526;
  border: 1px solid #3a3b3c;
}

body.theme-dark .section-divider {
  border-bottom-color: #3a3b3c;
}

body.theme-dark .section-divider span {
  background-color: #18191a;
  color: #b0b3b8;
}

body.theme-dark .panel-default > .panel-heading {
  background-color: #2d2e2f;
  border-color: #3a3b3c;
  color: #e4e6eb;
}

body.theme-dark .panel-default {
  border-color: #3a3b3c;
  background-color: #242526;
}

body.theme-dark .field-group {
  background-color: transparent;
}

body.theme-dark .form-control {
  background-color: #3a3b3c;
  border-color: #4e4f50;
  color: #e4e6eb;
}

body.theme-dark .field-group .hint {
  color: #b0b3b8;
}

body.theme-dark .field-group .error-msg {
  color: #ef5350;
}

body.theme-dark .field-group .biz-warn {
  color: #ffb74d;
  background-color: #3e2723;
}

body.theme-dark .field-group .hint {
  color: #b0b3b8;
}

body.theme-dark .field-group .amount-display {
  color: #5b9bd5;
}

body.theme-dark .field-group .control-label {
  color: #e4e6eb;
}

body.theme-dark .field-group .control-label .en {
  color: #b0b3b8;
}

body.theme-dark .field-group .control-label .required {
  color: #ef5350;
}

body.theme-dark .field-group .control-label .mult-tag {
  color: #b0b3b8;
  background-color: #1a1b1c;
}

body.theme-dark .repeat-index {
  color: #5b9bd5;
  background-color: #1e3a5f;
}

body.theme-dark .search-highlight {
  background-color: #854d0e;
  color: #fef3c7;
}

body.theme-dark .toast-msg {
  background-color: #e4e6eb;
  color: #18191a;
}

body.theme-dark .quick-panel-toggle {
  background-color: #5b9bd5;
  color: #ffffff;
}

body.theme-dark .quick-panel .panel {
  background-color: #242526;
  border-color: #3a3b3c;
}

body.theme-dark .audit-badge {
  background-color: #3e2723;
  color: #ffb74d;
}

body.theme-dark .template-btn.active {
  background-color: #5b9bd5;
  border-color: #5b9bd5;
  color: #ffffff;
}

body.theme-dark .json-panel .panel {
  background-color: #242526;
  border-color: #3a3b3c;
}

body.theme-dark .summary-item {
  border-bottom-color: #3a3b3c;
}

body.theme-dark .summary-label {
  color: #b0b3b8;
}

body.theme-dark .summary-value {
  color: #e4e6eb;
}

body.theme-dark .validation-summary.valid {
  background-color: #1b3a1b;
  color: #4caf50;
}

body.theme-dark .validation-summary.error {
  background-color: #3e1a1a;
  color: #ef5350;
}

body.theme-dark .modal-content {
  background-color: #242526;
  border-color: #3a3b3c;
  color: #e4e6eb;
}

body.theme-dark .btn-default {
  background-color: #3a3b3c;
  border-color: #4e4f50;
  color: #e4e6eb;
}
"""

_FIELD_STATES = """
/* ===== Field States ===== */
.field-required .form-control,
.field-required .ccy-select {
  background-color: #9EB5F9;
  color: #000000;
}

.field-readonly .form-control {
  background-color: #cad1e2;
  color: #000000;
  cursor: not-allowed;
  border-style: dashed;
}

.field-editable .form-control {
  background-color: #ffffff;
  color: #000000;
}

.field-disabled .form-control {
  background-color: #e5e9f0;
  color: #666666;
  cursor: not-allowed;
}

.field-hidden {
  display: none;
}

.has-error .form-control {
  border-color: #c62828;
}

.has-error .error-msg {
  display: block;
}
"""

_COMPONENTS = """
/* ===== JSON Syntax Highlighting ===== */
.json-key { color: #6b21a8; }
.json-string { color: #166534; }
.json-number { color: #9a3412; }
.json-boolean { color: #991b1b; }
.json-null { color: #5a5f6b; }

body.theme-dark .json-key { color: #c084fc; }
body.theme-dark .json-string { color: #86efac; }
body.theme-dark .json-number { color: #fdba74; }
body.theme-dark .json-boolean { color: #fca5a5; }
body.theme-dark .json-null { color: #b0b3b8; }

/* ===== JSON Tabs ===== */
.json-tabs .btn {
  border-radius: 0;
  border-bottom: 2px solid transparent;
}

.json-tabs .btn.active {
  border-bottom-color: #2563a8;
  font-weight: 600;
}

body.theme-dark .json-tabs .btn.active {
  border-bottom-color: #5b9bd5;
}

/* ===== Autosave Indicator ===== */
.autosave-indicator {
  font-size: 11px;
  display: inline-block;
  margin-left: 12px;
}

.autosave-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #1a7f37;
  vertical-align: middle;
  margin-right: 4px;
}

/* ===== Navbar Overrides ===== */
.navbar-brand {
  font-size: 14px;
  font-weight: 600;
}

/* ===== Panel Collapse Toggle ===== */
.panel-heading {
  cursor: pointer;
  padding: 8px 14px;
}

.panel-heading:hover {
  opacity: 0.85;
}

.panel-title {
  font-size: 13px;
  font-weight: 600;
  margin: 0;
}

.panel-heading .toggle-icon {
  float: right;
  font-size: 14px;
  line-height: 20px;
  -ms-transition: transform 0.2s;
  transition: transform 0.2s;
}

.panel-heading.collapsed .toggle-icon {
  -ms-transform: rotate(-90deg);
  transform: rotate(-90deg);
}

/* ===== Tooltip (field info) ===== */
.field-tooltip {
  display: none;
  position: absolute;
  bottom: 100%;
  left: 0;
  padding: 8px 12px;
  font-size: 11px;
  line-height: 1.5;
  border-radius: 3px;
  z-index: 100;
  max-width: 360px;
  min-width: 200px;
}

.field-group:hover .field-tooltip {
  display: block;
}

body.theme-light .field-tooltip {
  background-color: #ffffff;
  border: 1px solid #d0d3d8;
  color: #1c1e21;
}

body.theme-dark .field-tooltip {
  background-color: #3a3b3c;
  border: 1px solid #4e4f50;
  color: #e4e6eb;
}

.field-tooltip .tip-tag {
  font-family: monospace;
  color: #2563a8;
  font-size: 10px;
  display: block;
  margin-bottom: 4px;
}

body.theme-dark .field-tooltip .tip-tag {
  color: #5b9bd5;
}

/* ===== Choice Disabled State ===== */
.choice-disabled {
  opacity: 0.5;
}
.choice-disabled .panel-heading {
  background: #e5e9f0;
}
body.theme-dark .choice-disabled .panel-heading {
  background: #2a2b2c;
}
"""

_PRINT = """
/* ===== Print ===== */
@media print {
  .json-panel { display: none; }
  .command-bar { display: none; }
  .template-bar { display: none; }
  .search-bar { display: none; }
  .progress-container { display: none; }
  .toast-msg { display: none; }
  .quick-panel { display: none; }
  .quick-panel-toggle { display: none; }
  .navbar { display: none; }
  .main-panel { margin-right: 0; }
  body { background: white; color: black; }
  .panel-body.collapse:not(.in) { display: block; height: auto; }
}
"""
