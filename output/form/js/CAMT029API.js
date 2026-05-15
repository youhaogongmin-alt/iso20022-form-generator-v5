// ===== CAMT029API registration =====
(function(window) {
  'use strict';
  var factory = window.ISO20022_FORM_API_FACTORY;
  if (!factory || !factory.create) return;
  var api = factory.create({
    messageId: 'camt.029.001.09',
    dataKey: 'CAMT029',
    rootId: 'CAMT029_PAGE',
    apiName: 'CAMT029API',
    formApiName: 'CAMT029_FORM_API'
  });
  window.ISO20022_FORM_APIS = window.ISO20022_FORM_APIS || {};
  window.ISO20022_FORM_APIS['CAMT029'] = api;
  window['CAMT029API'] = api;
  window['CAMT029_FORM_API'] = api;
  window.ISO20022_FORM_API = api;
})(window);
