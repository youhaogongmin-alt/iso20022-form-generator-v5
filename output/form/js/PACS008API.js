// ===== PACS008API registration =====
(function(window) {
  'use strict';
  var factory = window.ISO20022_FORM_API_FACTORY;
  if (!factory || !factory.create) return;
  var api = factory.create({
    messageId: 'pacs.008.001.08',
    dataKey: 'PACS008',
    rootId: 'PACS008_PAGE',
    apiName: 'PACS008API',
    formApiName: 'PACS008_FORM_API'
  });
  window.ISO20022_FORM_APIS = window.ISO20022_FORM_APIS || {};
  window.ISO20022_FORM_APIS['PACS008'] = api;
  window['PACS008API'] = api;
  window['PACS008_FORM_API'] = api;
  window.ISO20022_FORM_API = api;
})(window);
