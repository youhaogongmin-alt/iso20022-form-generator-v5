const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('output/form/index.html', 'utf-8');
const htmlNoScripts = html.replace(/<script[\s\S]*?<\/script>/gi, '');
const fieldMeta = JSON.parse(fs.readFileSync('output/fieldMeta_v4.json', 'utf-8'));
const aloGroups = JSON.parse(fs.readFileSync('output/alo_v4.json', 'utf-8'));

const dom = new JSDOM(htmlNoScripts);
const document = dom.window.document;

function sectionHasValue(section) {
  const inputs = section.querySelectorAll('input[name], select[name], textarea[name]');
  for (const input of inputs) {
    if (input.disabled || input.readOnly) continue;
    if (input.value && input.value.trim()) return true;
  }
  return false;
}

function isEffectivelyRequired(el) {
  let node = el.closest('.panel');
  while (node) {
    const heading = Array.from(node.children).find(child => child.classList && child.classList.contains('panel-heading'));
    if (heading && heading.querySelector('.label-info') && !sectionHasValue(node)) {
      return false;
    }
    const parent = node.parentElement;
    node = parent ? parent.closest('.panel') : null;
  }
  return true;
}

function findFieldMeta(name) {
  return fieldMeta.find(m => m.form_name === name);
}

let total = 0;
let counted = [];
const inputs = document.querySelectorAll('input[name], select[name], textarea[name]');
inputs.forEach(el => {
  const name = el.getAttribute('name');
  const meta = findFieldMeta(name);
  const apiRequired = el.getAttribute('data-api-required') === 'true';
  if (!((meta && meta.mult_min >= 1) || apiRequired)) return;
  if (!el.readOnly && !isEffectivelyRequired(el)) return;
  total++;
  counted.push(name);
});

console.log('Individual required fields counted:', total);
console.log('AT_LEAST_ONE_GROUPS:', aloGroups.length);
console.log('Total:', total + aloGroups.length);
console.log();
console.log('Counted fields:');
counted.forEach(f => console.log('  ' + f));
