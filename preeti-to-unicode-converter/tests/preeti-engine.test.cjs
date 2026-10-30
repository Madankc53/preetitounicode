const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

function section(startMarker, endMarker) {
  const start = html.indexOf(startMarker);
  const end = html.indexOf(endMarker, start);
  assert.notEqual(start, -1, `Missing source marker: ${startMarker}`);
  assert.notEqual(end, -1, `Missing source marker: ${endMarker}`);
  return html.slice(start, end);
}

const mapsSource = section('const MAPS = {', '// ═══════════════════════════════════════════════════\n// STATE');
const engineSource = section('function applyRules(t,rules){', 'function revConvert(t,font){');
const keyboardSource = section('function getKeyboardKeys(font){', 'function buildKeyboard(font){');

const sandbox = {};
vm.runInNewContext(`
  ${mapsSource}
  ${engineSource}
  ${keyboardSource}
  this.api = { MAPS, applyRules, fwdConvert, getKeyboardKeys };
`, sandbox);

const { MAPS, applyRules, fwdConvert, getKeyboardKeys } = sandbox.api;

test('Preeti single-key mappings match the embedded map', () => {
  for (const [key, expected] of Object.entries(MAPS.preeti.fwd)) {
    if (key.length === 1 && !MAPS.preeti.rules.some(rule => rule.f.startsWith(key))) {
      assert.equal(fwdConvert(key, 'preeti'), expected, `Preeti key ${JSON.stringify(key)}`);
    }
  }
});

test('longest Preeti sequences take precedence over shorter overlapping rules', () => {
  assert.equal(fwdConvert('cf]', 'preeti'), 'ओ');
  assert.equal(fwdConvert('cfW', 'preeti'), 'औ');
  assert.equal(fwdConvert('cf', 'preeti'), 'आ');
});

test('special Preeti sequences are converted before single-character mapping', () => {
  assert.equal(fwdConvert('if', 'preeti'), 'ष');
  assert.equal(fwdConvert('em', 'preeti'), 'झ');
});

test('short-i matra is reordered after its consonant', () => {
  assert.equal(fwdConvert('ls', 'preeti'), 'कि');
});

test('unknown symbols and line breaks are preserved', () => {
  assert.equal(fwdConvert('s🙂\n?\t', 'preeti'), 'क🙂\nरु\t');
});

test('rule matching is single-pass and does not remap replacement text', () => {
  const result = applyRules('ab', [
    { f: 'a', r: 'b' },
    { f: 'b', r: 'c' }
  ]);
  assert.equal(result, 'bc');
});

test('on-screen keyboard labels are generated from the selected font map', () => {
  const keys = getKeyboardKeys('preeti');
  const labels = new Map(keys);
  for (const [key, value] of Object.entries(MAPS.preeti.fwd)) {
    if (key.length === 1 && !/\\s/.test(key) && /[\\u0900-\\u097F]/.test(value)) {
      assert.equal(labels.get(key), value, `Keyboard label for key ${JSON.stringify(key)}`);
    }
  }
  for (const rule of MAPS.preeti.rules) {
    assert.equal(labels.get(rule.f), rule.r, `Keyboard label for sequence ${rule.f}`);
  }
});
