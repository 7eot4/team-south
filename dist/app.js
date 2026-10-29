'use strict';
document.documentElement.classList.remove('no-js');
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const menu = $('.menu');
const navigation = $('#navigation');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('open'); }
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open);
});
navigation.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);

const services = {
  ziemne: { kicker: 'PRZYGOTOWANIE INWESTYCJI', title: 'Zaczynamy od solidnej podstawy.', description: 'Wykopy, niwelacja i przygotowanie terenu. Ustalmy warunki na działce oraz zakres prac ziemnych.', items: ['Wykopy i przygotowanie gruntu', 'Wyrównanie i niwelacja terenu', 'Prace z użyciem koparek i minikoparek'], tip: 'Przygotuj lokalizację, orientacyjne wymiary oraz informacje o dojeździe do działki.', image: '07', alt: 'Minikoparka podczas prac terenowych' },
  bruk: { kicker: 'NAWIERZCHNIE', title: 'Dobrze ułożona codzienność.', description: 'Podjazdy, chodniki i otoczenie budynków. Nawierzchnie z kostki brukowej, płyt betonowych i innych materiałów.', items: ['Podjazdy i ciągi piesze', 'Kostka brukowa i płyty betonowe', 'Nawierzchnie przy obiektach przemysłowych'], tip: 'Podaj przybliżoną powierzchnię, rodzaj istniejącego podłoża i planowane przeznaczenie nawierzchni.', image: '08', alt: 'Gotowa nawierzchnia z kostki brukowej' },
  drogi: { kicker: 'INFRASTRUKTURA DROGOWA', title: 'Łączymy miejsca i ludzi.', description: 'Drogi, chodniki i ścieżki rowerowe. Zakres prac i organizację realizacji dopasowujemy do konkretnej inwestycji.', items: ['Budowa chodników', 'Ścieżki rowerowe', 'Nawierzchnie dróg i ciągów komunikacyjnych'], tip: 'Przygotuj lokalizację, długość i szerokość odcinka oraz informację o dostępnej dokumentacji.', image: '01', alt: 'Chodnik wzdłuż drogi — galeria firmy' },
  rekreacja: { kicker: 'PLACE ZABAW I REKREACJA', title: 'Więcej miejsca na aktywność.', description: 'Przestrzenie dla lokalnych społeczności. Budowa placów zabaw i zagospodarowanie terenów rekreacyjnych.', items: ['Place zabaw', 'Otoczenie obiektów sportowych', 'Nawierzchnie i przestrzenie rekreacyjne'], tip: 'Opisz przeznaczenie terenu, jego powierzchnię i zakres projektu. Przekaż dokumentację, jeśli jest dostępna.', image: '26', alt: 'Kolorowa przestrzeń rekreacyjna — galeria firmy' },
  zielen: { kicker: 'PARKI I TERENY ZIELONE', title: 'Otoczenie, w którym chce się być.', description: 'Parki, ogrody i zielone otoczenie inwestycji. Łączymy przygotowanie terenu z jego zagospodarowaniem.', items: ['Zagospodarowanie terenów zielonych', 'Przestrzenie parkowe', 'Otoczenie inwestycji prywatnych i publicznych'], tip: 'Przygotuj zdjęcia, orientacyjną powierzchnię i opis planowanych zmian. Zaznacz, które elementy mają pozostać.', image: '09', alt: 'Zagospodarowany ogród z zielenią i ścieżkami' }
};
$$('[data-service]').forEach(button => button.addEventListener('click', () => {
  const key = button.dataset.service, service = services[key];
  $$('[data-service]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  $('#service-kicker').textContent = service.kicker;
  $('#service-title').textContent = service.title;
  $('#service-description').textContent = service.description;
  $('#service-tip').textContent = service.tip;
  $('#service-list').replaceChildren(...service.items.map(text => { const li = document.createElement('li'); li.textContent = text; return li; }));
  $('#service-image').src = `assets/work-${service.image}-1400.webp`;
  $('#service-image').alt = service.alt;
  $('.choose-service').dataset.selectService = key;
}));

const galleryCards = $$('.gallery-card');
let filter = 'all', galleryLimit = 6, photoIndex = 0, lightboxTrigger;
const matchingCards = () => galleryCards.filter(card => filter === 'all' || card.dataset.category === filter);
function filterGallery() {
  const matches = matchingCards();
  galleryCards.forEach(card => { const index = matches.indexOf(card); card.hidden = index < 0 || index >= galleryLimit; });
  $('#gallery-status').textContent = `${Math.min(galleryLimit, matches.length)} / ${matches.length} zdjęć`;
  $('#gallery-more').hidden = matches.length <= galleryLimit;
}
$$('[data-filter]').forEach(button => button.addEventListener('click', () => {
  filter = button.dataset.filter; galleryLimit = 6;
  $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  filterGallery();
}));
$('#gallery-more').addEventListener('click', () => {
  const matches = matchingCards(); const firstNew = matches[galleryLimit];
  galleryLimit += 6; filterGallery();
  if (firstNew) firstNew.querySelector('a').focus({ preventScroll: true });
});
filterGallery();
const lightbox = $('#lightbox');
function showPhoto(index) {
  const cards = matchingCards(); photoIndex = (index + cards.length) % cards.length;
  const card = cards[photoIndex], link = card.querySelector('a'), img = card.querySelector('img');
  $('#lightbox-image').src = link.href; $('#lightbox-image').alt = img.alt;
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
form.noValidate = true;
function setStep(next, focus = true) {
  formStep = next;
  steps.forEach((step, index) => { step.hidden = index !== next; step.disabled = index !== next; });
  $$('.form-progress li').forEach((item, index) => { if (index === next) item.setAttribute('aria-current', 'step'); else item.removeAttribute('aria-current'); });
  $('#form-back').hidden = next === 0; $('#form-next').hidden = next === 2;
  $('#long-message-note').hidden = next !== 2 || !$('#mail-inquiry').hidden;
  $('#form-next').textContent = next === 1 ? 'Przygotuj treść →' : 'Dalej →';
  $('#form-status').textContent = '';
  if (focus) {
    form.scrollIntoView({ block: 'start', behavior: 'instant' });
    const legend = steps[next].querySelector('legend'); legend.tabIndex = -1; legend.focus({ preventScroll: true });
  }
}
function generateSummary() {
  const service = $('#inquiry-service').selectedOptions[0].textContent;
  const text = ['Dzień dobry,', '', 'Proszę o kontakt w sprawie inwestycji:', `Zakres: ${service}`, `Inwestor: ${$('#investor').value}`, `Miejscowość: ${$('#location').value.trim()}`, `Orientacyjny zakres: ${$('#scope').value.trim() || 'do ustalenia'}`, `Planowany termin: ${$('#timing').value}`, `Dokumentacja / zdjęcia: ${$('#documentation').checked ? 'mam do przekazania w wiadomości' : 'do uzgodnienia'}`, '', $('#description').value.trim() ? `Opis:\n${$('#description').value.trim()}` : 'Szczegóły do omówienia podczas rozmowy.', '', 'Proszę o informację o możliwości realizacji i dalszych krokach.'].join('\n');
  $('#inquiry-summary').textContent = text;
  const href = `mailto:biuro@teamsouth.pl?subject=${encodeURIComponent('Zapytanie — ' + service)}&body=${encodeURIComponent(text)}`;
  $('#mail-inquiry').href = href;
  $('#mail-inquiry').hidden = href.length > 1900;
  $('#long-message-note').hidden = href.length <= 1900;
  return text;
}
form.addEventListener('submit', e => {
  e.preventDefault();
  if (formStep === 2) return;
  if (formStep === 1) $('#location').setCustomValidity($('#location').value.trim().length < 2 ? 'Podaj miejscowość (co najmniej 2 znaki).' : '');
  const invalid = [...steps[formStep].querySelectorAll('input, select, textarea')].find(field => !field.checkValidity());
  if (invalid) { invalid.reportValidity(); return; }
  if (formStep === 1) generateSummary();
  setStep(formStep + 1);
});
$('#location').addEventListener('input', () => $('#location').setCustomValidity(''));
$('#form-back').addEventListener('click', () => setStep(Math.max(0, formStep - 1)));
$('#form-reset').addEventListener('click', () => {
  form.reset(); $('#location').setCustomValidity(''); $('#inquiry-summary').textContent = '';
  $('#mail-inquiry').href = 'mailto:biuro@teamsouth.pl'; $('#description-count').textContent = '0 / 800'; setStep(0);
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
$$('[data-social]').forEach(button => button.addEventListener('click', () => {
  $('#social-dialog-title').textContent = button.dataset.social;
  socialDialog.showModal(); document.body.classList.add('modal-open');
}));
$('#close-social').addEventListener('click', () => socialDialog.close());
socialDialog.addEventListener('close', () => document.body.classList.remove('modal-open'));

let scrollQueued = false;
function updateProgress() {
  const distance = document.documentElement.scrollHeight - innerHeight;
  $('.scroll-progress').style.width = `${distance > 0 ? Math.min(100, scrollY / distance * 100) : 0}%`;
  scrollQueued = false;
}
document.addEventListener('scroll', () => { if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateProgress); } }, { passive: true });
updateProgress();
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const section = entries.filter(entry => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!section) return;
    $$('#navigation a').forEach(link => { if (link.hash === '#' + section.target.id) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
  }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
  $$('main>section[id]').forEach(section => observer.observe(section));
}
