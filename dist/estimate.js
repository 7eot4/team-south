'use strict';
// The calculator stays unavailable if the core application failed integrity checks.
function initializeEstimate() {
if (document.documentElement.classList.contains('no-js')) return;
// Reference prices, not TEAM SOUTH's price list. Keep rates and scope in this one catalogue.
// Sources and assumptions: KALKULATOR-WYCENY.md, checked 2026-10-30.
const estimateCatalogue = {
  bruk: { label: 'Ułożenie kostki betonowej', unit: 'm²', inquiry: 'bruk', low: 50, high: 80, foundation: true, scope: 'Samo ułożenie kostki betonowej. Kostka i podbudowa nie są częścią stawki podstawowej.', exclusions: 'Poza podstawą: kostka, podbudowa, obrzeża, roboty ziemne, odwodnienie, transport, wywóz i VAT.' },
  'bruk-material': { label: 'Kostka betonowa z ułożeniem', unit: 'm²', inquiry: 'bruk', low: 130, high: 160, foundation: true, scope: 'Standardowa kostka betonowa z jej ułożeniem. Podbudowa jest osobną, opcjonalną pozycją.', exclusions: 'Poza podstawą: podbudowa, obrzeża, roboty ziemne, odwodnienie, transport, wywóz i VAT.' },
  ziemne: { label: 'Przesuwanie i niwelacja ziemi', unit: 'm³', inquiry: 'ziemne', low: 40, high: 100, foundation: false, scope: 'Praca z masami ziemi na terenie. Przy wymiarach liczymy objętość prostokątnej warstwy, bez skarp i spulchnienia.', exclusions: 'Poza kalkulacją: zakup ziemi, transport, wywóz, utylizacja, odwodnienie i VAT. Trudny grunt wymaga indywidualnej oceny.' },
  minikoparka: { label: 'Minikoparka 3,5 t z operatorem', unit: 'h', inquiry: 'ziemne', low: 120, high: 120, foundation: false, scope: 'Referencyjna stawka godzinowa minikoparki 3,5 t z operatorem. Czas pracy podajesz samodzielnie.', exclusions: 'Poza kalkulacją: transport maszyny, materiały, wywóz, utylizacja i VAT. Dobór sprzętu oraz minimalny czas rozliczenia ustala firma.' }
};
const estimateFoundationRate = { low: 30, high: 50 };
let estimateMoneyFormatter;
const estimateMoney = value => {
  estimateMoneyFormatter ??= new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN', minimumFractionDigits: 0, maximumFractionDigits: 2 });
  return estimateMoneyFormatter.format(value / 100);
};
const estimateRange = range => range.low === range.high ? estimateMoney(range.low) : `${estimateMoney(range.low)} – ${estimateMoney(range.high)}`;
const estimateNumber = (input, max, digits = 3, optional = false) => {
  const text = input.value.trim();
  if (!text && optional) { input.removeAttribute('aria-invalid'); return 0; }
  const validSyntax = new RegExp(`^\\d{1,7}(?:[.,]\\d{1,${digits}})?$`).test(text);
  const number = validSyntax ? Number(text.replace(',', '.')) : NaN;
  const valid = Number.isFinite(number) && number <= max && (optional ? number >= 0 : number > 0);
  if (text && !valid) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid');
  return valid ? number : null;
};
let currentEstimate = null;
function estimateInputsChanged() {
  detachEstimate('Kalkulacja została zmieniona. Dołącz aktualny wynik ponownie.');
  calculateEstimate();
}
function calculateEstimate() {
  const key = $('#estimate-service').value;
  if (!Object.hasOwn(estimateCatalogue, key)) {
    currentEstimate = null; $('#estimate-use').disabled = true; $('#estimate-total').textContent = '—';
    $('#estimate-validation').textContent = 'Wybierz jeden z dostępnych rodzajów prac.';
    return;
  }
  const model = estimateCatalogue[key];
  const dimensions = model.unit !== 'h' && $('#estimate-mode').value === 'dimensions';
  $('#estimate-mode-field').hidden = model.unit === 'h';
  $('#estimate-direct').hidden = dimensions;
  $('#estimate-dimensions').hidden = !dimensions;
  $('#estimate-depth-field').hidden = model.unit !== 'm³';
  $('#estimate-foundation-field').hidden = !model.foundation;
  $('#estimate-scope').textContent = model.scope;
  const exclusions = model.foundation && $('#estimate-foundation').checked ? model.exclusions.replace('podbudowa, ', '') : model.exclusions;
  $('#estimate-exclusions').textContent = exclusions;
  $('#estimate-quantity-label').textContent = model.unit === 'h' ? 'Czas pracy (godziny)' : model.unit === 'm³' ? 'Objętość (m³)' : 'Powierzchnia (m²)';
  const modelRange = { low: Math.round(model.low * 100), high: Math.round(model.high * 100) };
  let quantity;
  if (dimensions) {
    const length = estimateNumber($('#estimate-length'), 1000);
    const width = estimateNumber($('#estimate-width'), 1000);
    const depth = model.unit === 'm³' ? estimateNumber($('#estimate-depth'), 20) : 1;
    quantity = [length, width, depth].some(value => value === null) ? null : length * width * depth;
  } else quantity = estimateNumber($('#estimate-quantity'), model.unit === 'h' ? 1000 : 1000000);
  const extra = estimateNumber($('#estimate-extra'), 1000000, 2, true);
  const reserve = Number($('#estimate-reserve').value);
  const valid = quantity !== null && quantity >= .001 && quantity <= 1000000 && extra !== null && [0, 10, 15, 20].includes(reserve);
  currentEstimate = null;
  $('#estimate-use').disabled = !valid;
  $('#estimate-foundation-row').hidden = !model.foundation || !$('#estimate-foundation').checked;
  if (!valid) {
    ['#estimate-total', '#estimate-used-quantity', '#estimate-rate', '#estimate-base', '#estimate-foundation-cost', '#estimate-extra-cost', '#estimate-reserve-cost'].forEach(selector => { $(selector).textContent = '—'; });
    const hasValues = $$('#kalkulator input:not([type=checkbox])').some(input => input.value.trim());
    $('#estimate-validation').textContent = hasValues ? 'Sprawdź liczby. Ilość musi być dodatnia (do 1 000 000 jednostek lub 1000 h); koszty dodatkowe do 1 000 000 zł, z dokładnością do grosza.' : 'Podaj ilość lub wymiary, aby zobaczyć wynik. Możesz użyć przecinka lub kropki.';
    return;
  }
  const base = { low: Math.round(quantity * modelRange.low), high: Math.round(quantity * modelRange.high) };
  const foundation = { low: 0, high: 0 };
  if (model.foundation && $('#estimate-foundation').checked) {
    foundation.low = Math.round(quantity * estimateFoundationRate.low * 100);
    foundation.high = Math.round(quantity * estimateFoundationRate.high * 100);
  }
  const additional = Math.round(extra * 100);
  const subtotal = { low: base.low + foundation.low + additional, high: base.high + foundation.high + additional };
  const reserveCost = { low: Math.round(subtotal.low * reserve / 100), high: Math.round(subtotal.high * reserve / 100) };
  const total = { low: subtotal.low + reserveCost.low, high: subtotal.high + reserveCost.high };
  const quantityText = `${plNumber(Number(quantity.toFixed(6)))} ${model.unit}`;
  $('#estimate-rate').textContent = `${estimateRange(modelRange)} / ${model.unit}`;
  $('#estimate-total').textContent = estimateRange(total);
  $('#estimate-used-quantity').textContent = quantityText;
  $('#estimate-base').textContent = estimateRange(base);
  $('#estimate-foundation-cost').textContent = estimateRange(foundation);
  $('#estimate-extra-cost').textContent = estimateMoney(additional);
  $('#estimate-reserve-cost').textContent = `${estimateRange(reserveCost)} (${reserve}%)`;
  $('#estimate-validation').textContent = 'Wynik jest gotowy. Kwoty są netto i obejmują tylko wybrane pozycje.';
  currentEstimate = {
    inquiry: model.inquiry,
    scope: `${model.label}: ${quantityText}`,
    text: [
      'SZACUNEK RYNKOWY — nie oferta TEAM SOUTH.',
      `${model.label}: ${quantityText}; stawka ${estimateRange(modelRange)} / ${model.unit} netto.`,
      `Prace: ${estimateRange(base)} netto.`,
      foundation.high ? `Podbudowa: ${estimateRange(foundation)} netto.` : '',
      additional ? `Dodatkowe koszty: ${estimateMoney(additional)} netto.` : '',
      reserve ? `Rezerwa budżetowa ${reserve}%: ${estimateRange(reserveCost)}.` : '',
      `Razem: ${estimateRange(total)} netto.`,
      exclusions,
      'Proszę o indywidualną wycenę; stawki referencyjne sprawdzone 30.10.2026.'
    ].filter(Boolean).join('\n')
  };
}
$('#estimate-service').addEventListener('change', () => {
  $('#estimate-quantity').value = '';
  $('#estimate-foundation').checked = false;
  if ($('#estimate-service').value === 'minikoparka') $('#estimate-mode').value = 'quantity';
  estimateInputsChanged();
});
$$('#kalkulator input').forEach(input => input.addEventListener('input', estimateInputsChanged));
['#estimate-mode', '#estimate-reserve'].forEach(selector => $(selector).addEventListener('change', estimateInputsChanged));
$('#estimate-use').addEventListener('click', () => {
  calculateEstimate();
  if (!currentEstimate) return;
  attachedEstimate = currentEstimate.text;
  attachedEstimateScope = currentEstimate.scope;
  $('#inquiry-service').value = currentEstimate.inquiry;
  $('#scope').value = attachedEstimateScope;
  $('#estimate-attached').hidden = false;
  $('#estimate-status').textContent = 'Kalkulacja dołączona. Uzupełnij miejscowość i sprawdź wiadomość.';
  setStep(1);
  $('#location').focus({ preventScroll: true });
});
$('#remove-estimate').addEventListener('click', () => detachEstimate('Kalkulacja odłączona od zapytania.'));
$('#estimate-reset').addEventListener('click', () => {
  $$('#kalkulator input').forEach(input => { input.value = ''; input.checked = false; input.removeAttribute('aria-invalid'); });
  $('#estimate-service').value = 'bruk'; $('#estimate-mode').value = 'quantity'; $('#estimate-reserve').value = '0';
  estimateInputsChanged();
});
calculateEstimate();
$('#scope').addEventListener('input', () => detachEstimate('Zakres został zmieniony. Dołącz aktualną kalkulację ponownie.'));
$('#inquiry-service').addEventListener('change', () => {
  if (attachedEstimate && $('#inquiry-service').value !== currentEstimate?.inquiry) detachEstimate('Zakres został zmieniony. Kalkulacja odłączona.');
});
$('.choose-service').addEventListener('click', e => {
  if (attachedEstimate && e.currentTarget.dataset.selectService !== currentEstimate?.inquiry) detachEstimate('Wybrano inny zakres prac. Kalkulacja odłączona.');
});


$('#kalkulator').classList.remove('estimate-pending');
}
// Let the initial page paint before introducing calculator controls and their layout.
requestAnimationFrame(() => requestAnimationFrame(initializeEstimate));
