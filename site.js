'use strict';
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
const activeMotions = new Set();
const elementMotions = new WeakMap();
let revealObserver;
function playMotion(element, frames, options = {}) {
  if (!element || motionPreference.matches || typeof element.animate !== 'function') return;
  elementMotions.get(element)?.cancel();
  const animation = element.animate(frames, { duration: 480, easing: 'cubic-bezier(.22,1,.36,1)', ...options });
  activeMotions.add(animation); elementMotions.set(element, animation);
  animation.finished.catch(() => {}).finally(() => activeMotions.delete(animation));
}
function enterMotion(element, delay = 0, distance = 14) {
  playMotion(element, [{ opacity: .12, transform: `translateY(${distance}px)` }, { opacity: 1, transform: 'translateY(0)' }], { duration: 620, delay, fill: 'backwards' });
}
motionPreference.addEventListener('change', () => {
  if (!motionPreference.matches) return;
  activeMotions.forEach(animation => animation.cancel());
  activeMotions.clear(); revealObserver?.disconnect();
});
const wellFormed = text => typeof text.toWellFormed === 'function' ? text.toWellFormed() : text.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]|[\uD800-\uDFFF]/g, token => token.length === 2 ? token : '\uFFFD');
const menu = $('.menu');
const navigation = $('#navigation');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('open'); }
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open);
  if (open) playMotion(navigation, [{ opacity: .3, transform: 'translateY(-8px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 240 });
});
navigation.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);

const services = {
  ziemne: { kicker: 'ROBOTY ZIEMNE', title: 'Wykopy i niwelacja terenu', description: 'Zanim pojawi się kostka, trawnik czy chodnik, trzeba przygotować grunt. Wykonujemy wykopy i niwelację — na działkach i przy większych inwestycjach.', items: ['Wykopy i przygotowanie gruntu', 'Wyrównanie i niwelacja terenu', 'Prace z użyciem koparek i minikoparek'], tip: 'Przygotuj lokalizację, orientacyjne wymiary oraz informacje o dojeździe do działki.', image: '07', alt: 'Minikoparka podczas prac terenowych' },
  bruk: { kicker: 'BRUKARSTWO', title: 'Podjazdy, chodniki i nawierzchnie', description: 'Podjazd, który prowadzi pod dom. Ścieżka przez ogród. Plac przy hali. Układamy kostkę i płyty tam, gdzie potrzebna jest nawierzchnia do codziennego użytku.', items: ['Podjazdy i ciągi piesze', 'Kostka brukowa i płyty betonowe', 'Nawierzchnie przy obiektach przemysłowych'], tip: 'Podaj przybliżoną powierzchnię, rodzaj istniejącego podłoża i planowane przeznaczenie nawierzchni.', image: '08', alt: 'Gotowa nawierzchnia z kostki brukowej' },
  drogi: { kicker: 'INFRASTRUKTURA DROGOWA', title: 'Drogi i ciągi komunikacyjne', description: 'Chodnik do szkoły, ścieżka rowerowa, droga dojazdowa. Budujemy ciągi komunikacyjne, które łączą miejsca i służą ludziom każdego dnia.', items: ['Budowa chodników', 'Ścieżki rowerowe', 'Nawierzchnie dróg i ciągów komunikacyjnych'], tip: 'Przygotuj lokalizację, długość i szerokość odcinka oraz informację o dostępnej dokumentacji.', image: '01', alt: 'Chodnik wzdłuż drogi — galeria firmy' },
  rekreacja: { kicker: 'REKREACJA', title: 'Place zabaw i tereny rekreacyjne', description: 'Miejsce na zabawę, ruch i chwilę na zewnątrz. Budujemy place zabaw i zagospodarowujemy otoczenie obiektów sportowych — razem z nawierzchniami.', items: ['Place zabaw', 'Otoczenie obiektów sportowych', 'Nawierzchnie i przestrzenie rekreacyjne'], tip: 'Opisz przeznaczenie terenu, jego powierzchnię i zakres projektu. Przekaż dokumentację, jeśli jest dostępna.', image: '26', alt: 'Kolorowa przestrzeń rekreacyjna — galeria firmy' },
  zielen: { kicker: 'TERENY ZIELONE', title: 'Parki, ogrody i otoczenie budynków', description: 'Po budowie przychodzi czas na otoczenie. Przygotowujemy teren i urządzamy zieleń przy domach, firmach i w przestrzeni publicznej.', items: ['Zagospodarowanie terenów zielonych', 'Przestrzenie parkowe', 'Otoczenie inwestycji prywatnych i publicznych'], tip: 'Przygotuj zdjęcia, orientacyjną powierzchnię i opis planowanych zmian. Zaznacz, które elementy mają pozostać.', image: '09', alt: 'Zagospodarowany ogród z zielenią i ścieżkami' }
};
$$('[data-service]').forEach(button => button.addEventListener('click', () => {
  const key = button.dataset.service, service = services[key];
  $$('[data-service]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  $('#service-kicker').textContent = service.kicker;
  $('#service-title').textContent = service.title;
  $('#service-description').textContent = service.description;
  $('#service-tip').textContent = service.tip;
  $('#service-list').replaceChildren(...service.items.map(text => { const li = document.createElement('li'); li.textContent = text; return li; }));
  $('#service-image').srcset = `assets/work-${service.image}-600.webp 600w, assets/work-${service.image}-1400.webp 1400w`;
  $('#service-image').src = `assets/work-${service.image}-1400.webp`;
  $('#service-image').alt = service.alt;
  $('.choose-service').dataset.selectService = key;
  enterMotion($('.service-copy'), 0, 8);
}));
$('#service-image').addEventListener('load', () => playMotion($('#service-image'), [{ opacity: .55 }, { opacity: 1 }], { duration: 360 }));

const galleryCards = $$('.gallery-card');
let filter = 'all', galleryLimit = 6, photoIndex = 0, lightboxTrigger;
const matchingCards = () => galleryCards.filter(card => filter === 'all' || card.dataset.category === filter);
function filterGallery(animate = false) {
  const matches = matchingCards();
  galleryCards.forEach(card => { const index = matches.indexOf(card); card.hidden = index < 0 || index >= galleryLimit; });
  $('#gallery-status').textContent = `${Math.min(galleryLimit, matches.length)} / ${matches.length} zdjęć`;
  $('#gallery-more').hidden = matches.length <= galleryLimit;
  if (animate) matches.slice(0, galleryLimit).forEach((card, index) => {
    const box = card.getBoundingClientRect();
    if (box.top < innerHeight && box.bottom > 0) enterMotion(card, (index % 3) * 55, 10);
  });
}
$$('[data-filter]').forEach(button => button.addEventListener('click', () => {
  filter = button.dataset.filter; galleryLimit = 6;
  $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  filterGallery(true);
}));
$('#gallery-more').addEventListener('click', () => {
  const matches = matchingCards(); const firstNew = matches[galleryLimit];
  galleryLimit += 6; filterGallery(true);
  if (firstNew) firstNew.querySelector('a').focus({ preventScroll: true });
});
filterGallery();
const lightbox = $('#lightbox');
const lightboxImage = $('#lightbox-image');
function loadPhoto(url) {
  lightboxImage.hidden = true;
  $('#lightbox-feedback').hidden = false;
  $('#lightbox-status').textContent = 'Ładowanie zdjęcia…';
  $('#lightbox-retry').hidden = true;
  lightboxImage.src = url;
}
lightboxImage.addEventListener('load', () => {
  lightboxImage.hidden = false;
  $('#lightbox-feedback').hidden = true;
  playMotion(lightboxImage, [{ opacity: .35 }, { opacity: 1 }], { duration: 300 });
});
lightboxImage.addEventListener('error', () => {
  lightboxImage.hidden = true;
  $('#lightbox-feedback').hidden = false;
  $('#lightbox-status').textContent = 'Nie udało się wczytać zdjęcia. Spróbuj ponownie lub wybierz inne.';
  $('#lightbox-retry').hidden = false;
});
$('#lightbox-retry').addEventListener('click', () => {
  const url = new URL(matchingCards()[photoIndex].querySelector('a').href);
  url.searchParams.set('retry', String(Date.now()));
  loadPhoto(url.href);
});
function showPhoto(index) {
  const cards = matchingCards(); photoIndex = (index + cards.length) % cards.length;
  const card = cards[photoIndex], link = card.querySelector('a'), img = card.querySelector('img');
  loadPhoto(link.href); lightboxImage.alt = img.alt;
  $('#lightbox-caption').textContent = card.querySelector('strong').textContent;
  $('#lightbox-count').textContent = `${photoIndex + 1} / ${cards.length}`;
}
galleryCards.forEach(card => card.querySelector('a').addEventListener('click', e => {
  e.preventDefault(); lightboxTrigger = e.currentTarget;
  showPhoto(matchingCards().indexOf(card)); lightbox.showModal(); document.body.classList.add('modal-open');
}));
$('#lightbox-prev').addEventListener('click', () => showPhoto(photoIndex - 1));
$('#lightbox-next').addEventListener('click', () => showPhoto(photoIndex + 1));
$('#lightbox-close').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); showPhoto(photoIndex + (e.key === 'ArrowRight' ? 1 : -1)); }
});
lightbox.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  // A photo beyond the first six can be reached with arrows; return to the original visible thumbnail.
  lightboxTrigger?.focus({ preventScroll: true });
});
lightbox.addEventListener('click', e => { if (e.target === lightbox && (e.clientX < lightbox.getBoundingClientRect().left || e.clientY < lightbox.getBoundingClientRect().top || e.clientX > lightbox.getBoundingClientRect().right || e.clientY > lightbox.getBoundingClientRect().bottom)) lightbox.close(); });

const form = $('#inquiry-form'), steps = $$('.form-step');
let formStep = 0;
let attachedEstimate = '';
form.noValidate = true;
function setStep(next, focus = true) {
  formStep = next;
  steps.forEach((step, index) => { step.hidden = index !== next; step.disabled = index !== next; });
  $$('.form-progress li').forEach((item, index) => { if (index === next) item.setAttribute('aria-current', 'step'); else item.removeAttribute('aria-current'); });
  $('#form-back').hidden = next === 0; $('#form-next').hidden = next === 2;
  $('#long-message-note').hidden = next !== 2 || !$('#mail-inquiry').hidden || !$('#whatsapp-inquiry').hidden;
  $('#form-next').textContent = next === 1 ? 'Przygotuj treść →' : 'Dalej →';
  $('#form-status').textContent = '';
  if (focus) {
    form.scrollIntoView({ block: 'start', behavior: 'instant' });
    const legend = steps[next].querySelector('legend'); legend.tabIndex = -1; legend.focus({ preventScroll: true });
    enterMotion(steps[next], 0, 8);
  }
}
function generateSummary() {
  const service = $('#inquiry-service').selectedOptions[0].textContent;
  const text = wellFormed(['Dzień dobry,', '', 'Proszę o kontakt w sprawie inwestycji:', `Zakres: ${service}`, `Inwestor: ${$('#investor').value}`, `Miejscowość: ${$('#location').value.trim()}`, `Orientacyjny zakres: ${$('#scope').value.trim() || 'do ustalenia'}`, `Planowany termin: ${$('#timing').value}`, `Dokumentacja / zdjęcia: ${$('#documentation').checked ? 'mam do przekazania w wiadomości' : 'do uzgodnienia'}`, '', $('#description').value.trim() ? `Opis:\n${$('#description').value.trim()}` : 'Szczegóły do omówienia podczas rozmowy.', ...(attachedEstimate ? ['', attachedEstimate] : []), '', 'Proszę o informację o możliwości realizacji i dalszych krokach.'].join('\n'));
  $('#inquiry-summary').textContent = text;
  const href = `mailto:biuro@teamsouth.pl?subject=${encodeURIComponent('Zapytanie — ' + service)}&body=${encodeURIComponent(text)}`;
  $('#mail-inquiry').href = href;
  $('#mail-inquiry').hidden = href.length > 1900;
  const whatsappHref = `https://wa.me/48797559814?text=${encodeURIComponent(text)}`;
  $('#whatsapp-inquiry').href = whatsappHref;
  $('#whatsapp-inquiry').hidden = whatsappHref.length > 1900;
  $('#long-message-note').hidden = !$('#mail-inquiry').hidden || !$('#whatsapp-inquiry').hidden;
  return text;
}
form.addEventListener('submit', e => {
  e.preventDefault();
  if (formStep === 2) return;
  if (formStep === 1) $('#location').setCustomValidity($('#location').value.trim().length < 2 ? 'Podaj miejscowość (co najmniej 2 znaki).' : '');
  steps[formStep].querySelectorAll('[maxlength]').forEach(field => {
    if (field.value.length > field.maxLength) field.setCustomValidity(`Maksymalnie ${field.maxLength} znaków.`);
  });
  const invalid = [...steps[formStep].querySelectorAll('input, select, textarea')].find(field => !field.checkValidity());
  if (invalid) { invalid.reportValidity(); return; }
  if (formStep === 1) generateSummary();
  setStep(formStep + 1);
});
$('#location').addEventListener('input', () => $('#location').setCustomValidity(''));
form.querySelectorAll('[maxlength]').forEach(field => field.addEventListener('input', () => field.setCustomValidity('')));
$('#form-back').addEventListener('click', () => setStep(Math.max(0, formStep - 1)));
$('#form-reset').addEventListener('click', () => {
  detachEstimate();
  form.reset(); $('#location').setCustomValidity(''); $('#inquiry-summary').textContent = '';
  form.querySelectorAll('[maxlength]').forEach(field => field.setCustomValidity(''));
  $('#mail-inquiry').href = 'mailto:biuro@teamsouth.pl'; $('#whatsapp-inquiry').href = $('.whatsapp-link').href; $('#description-count').textContent = '0 / 800'; setStep(0);
});
$('#description').addEventListener('input', () => { $('#description-count').textContent = `${$('#description').value.length} / 800`; });
$('.choose-service').addEventListener('click', e => { $('#inquiry-service').value = e.currentTarget.dataset.selectService; setStep(0, false); });
async function copyText(text, status, fallback) {
  try { await navigator.clipboard.writeText(text); status.textContent = 'Skopiowano.'; }
  catch {
    status.textContent = fallback || 'Kopiowanie niedostępne. Zaznacz tekst i skopiuj ręcznie lub pobierz plik.';
    if (status === $('#form-status')) { const range = document.createRange(); range.selectNodeContents($('#inquiry-summary')); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); }
  }
}
$('#copy-inquiry').addEventListener('click', () => copyText($('#inquiry-summary').textContent, $('#form-status')));
$('#download-inquiry').addEventListener('click', () => {
  const blob = new Blob(['\ufeff' + $('#inquiry-summary').textContent], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob), link = document.createElement('a');
  link.href = url; link.download = 'zapytanie-team-south.txt'; document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  $('#form-status').textContent = 'Przygotowano plik zapytania do pobrania. Nic nie zostało wysłane.';
});
setStep(0, false);

let measureText = '';
const plNumber = number => new Intl.NumberFormat('pl-PL', { maximumFractionDigits: 6 }).format(number);
function calculateMeasure() {
  const length = $('#measure-length'), width = $('#measure-width'), depth = $('#measure-depth');
  const valid = [length, width].every(input => input.value !== '' && input.validity.valid && input.valueAsNumber > 0) && (!depth.value || (depth.validity.valid && depth.valueAsNumber > 0));
  $('#use-measure').disabled = !valid; measureText = '';
  if (!valid) { $('#measure-result').textContent = 'Podaj poprawne dodatnie wymiary w metrach.'; return; }
  const area = length.valueAsNumber * width.valueAsNumber;
  const volume = depth.value ? area * depth.valueAsNumber : null;
  measureText = `Powierzchnia: ${plNumber(area)} m²` + (volume !== null ? `; objętość geometryczna: ${plNumber(volume)} m³` : '');
  $('#measure-result').textContent = measureText;
}
$$('.measure-inputs input').forEach(input => input.addEventListener('input', calculateMeasure));
$('#use-measure').addEventListener('click', () => {
  if (!measureText) return;
  $('#scope').value = measureText;
  if ($('#inquiry-service').value) { setStep(1); $('#scope').focus(); }
  else { setStep(0); $('#form-status').textContent = 'Obmiar dodany. Wybierz jeszcze zakres prac.'; $('#inquiry-service').focus(); }
});

// Reference prices, not TEAM SOUTH's price list. Keep rates and scope in this one catalogue.
// Sources and assumptions: KALKULATOR-WYCENY.md, checked 2026-10-30.
const estimateCatalogue = {
  bruk: { label: 'Ułożenie kostki betonowej', unit: 'm²', inquiry: 'bruk', low: 50, high: 80, foundation: true, scope: 'Samo ułożenie kostki betonowej. Kostka i podbudowa nie są częścią stawki podstawowej.', exclusions: 'Poza podstawą: kostka, podbudowa, obrzeża, roboty ziemne, odwodnienie, transport, wywóz i VAT.' },
  'bruk-material': { label: 'Kostka betonowa z ułożeniem', unit: 'm²', inquiry: 'bruk', low: 130, high: 160, foundation: true, scope: 'Standardowa kostka betonowa z jej ułożeniem. Podbudowa jest osobną, opcjonalną pozycją.', exclusions: 'Poza podstawą: podbudowa, obrzeża, roboty ziemne, odwodnienie, transport, wywóz i VAT.' },
  ziemne: { label: 'Przesuwanie i niwelacja ziemi', unit: 'm³', inquiry: 'ziemne', low: 40, high: 100, foundation: false, scope: 'Praca z masami ziemi na terenie. Przy wymiarach liczymy objętość prostokątnej warstwy, bez skarp i spulchnienia.', exclusions: 'Poza kalkulacją: zakup ziemi, transport, wywóz, utylizacja, odwodnienie i VAT. Trudny grunt wymaga indywidualnej oceny.' },
  minikoparka: { label: 'Minikoparka 3,5 t z operatorem', unit: 'h', inquiry: 'ziemne', low: 120, high: 120, foundation: false, scope: 'Referencyjna stawka godzinowa minikoparki 3,5 t z operatorem. Czas pracy podajesz samodzielnie.', exclusions: 'Poza kalkulacją: transport maszyny, materiały, wywóz, utylizacja i VAT. Dobór sprzętu oraz minimalny czas rozliczenia ustala firma.' }
};
const estimateFoundationRate = { low: 30, high: 50 };
const estimateMoney = value => new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN', minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(value / 100);
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
let attachedEstimateScope = '';
function detachEstimate(message = '') {
  if (!attachedEstimate) return;
  attachedEstimate = '';
  if ($('#scope').value === attachedEstimateScope) $('#scope').value = '';
  attachedEstimateScope = '';
  $('#estimate-attached').hidden = true;
  if (formStep === 2) generateSummary();
  if (message) $('#estimate-status').textContent = message;
}
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
  $('#estimate-rate').textContent = `${estimateRange(modelRange)} / ${model.unit}`;
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
    ['#estimate-total', '#estimate-used-quantity', '#estimate-base', '#estimate-foundation-cost', '#estimate-extra-cost', '#estimate-reserve-cost'].forEach(selector => { $(selector).textContent = '—'; });
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

$('.copy').addEventListener('click', () => copyText('biuro@teamsouth.pl', $('.copy-status'), 'Adres do ręcznego skopiowania: biuro@teamsouth.pl'));
$('#share-site').addEventListener('click', async () => {
  const url = 'https://7eot4.github.io/team-south/';
  if (navigator.share) {
    try { await navigator.share({ title: 'TEAM SOUTH — Budownictwo i infrastruktura', url }); return; }
    catch (error) { if (error.name === 'AbortError') return; }
  }
  await copyText(url, $('.copy-status'), `Link do udostępnienia: ${url}`);
  if ($('.copy-status').textContent === 'Skopiowano.') $('.copy-status').textContent = 'Skopiowano link do strony.';
});
$('#load-map').addEventListener('click', () => {
  const iframe = document.createElement('iframe');
  iframe.title = 'Mapa lokalizacji TEAM SOUTH — Niedźwiedź 145'; iframe.referrerPolicy = 'no-referrer';
  iframe.src = 'https://www.google.com/maps?q=Nied%C5%BAwied%C5%BA%20145%2034-735&output=embed';
  $('#map-container').replaceChildren(iframe);
});
const privacy = $('#privacy-dialog');
$('#open-privacy').addEventListener('click', () => { privacy.showModal(); document.body.classList.add('modal-open'); });
$('#close-privacy').addEventListener('click', () => privacy.close());
privacy.addEventListener('close', () => document.body.classList.remove('modal-open'));

const socialDialog = $('#social-dialog');
let socialTrigger;
$$('[data-social]').forEach(button => button.addEventListener('click', () => {
  socialTrigger = button;
  closeMenu();
  $('#social-dialog-title').textContent = button.dataset.social;
  socialDialog.showModal(); document.body.classList.add('modal-open');
}));
$('#close-social').addEventListener('click', () => socialDialog.close());
socialDialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  if (socialTrigger) (socialTrigger.getClientRects().length ? socialTrigger : menu).focus();
});

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const section = entries.filter(entry => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!section) return;
    $$('#navigation a').forEach(link => { if (link.hash === '#' + section.target.id) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
  }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
  $$('main>section[id]').forEach(section => observer.observe(section));
}
// Reveal script-dependent controls only after the application has initialized.
document.documentElement.classList.remove('no-js');

// Progressive enhancement: content is visible even if motion is unavailable or cancelled.
if (!motionPreference.matches) {
  if ('IntersectionObserver' in window) {
    revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        revealObserver.unobserve(entry.target);
        const delay = entry.target.classList.contains('gallery-card') ? (galleryCards.indexOf(entry.target) % 3) * 60 : 0;
        enterMotion(entry.target, delay, 18);
      });
    }, { rootMargin: '0px 0px -24px 0px', threshold: .06 });
    $$('.section-heading, .service-tabs, .service-view, .gallery-card, .reference-card, .equipment-image, .equipment-copy, .contact-info, .planner, .estimate-controls, .estimate-result, .faq > h2, .faq-list, .footer-main').forEach(element => revealObserver.observe(element));
  }
}
