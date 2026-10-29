const menu = document.querySelector('.menu');
const navigation = document.querySelector('#navigation');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('open'); }
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open); });
navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
document.querySelector('.copy').addEventListener('click', async () => { const status = document.querySelector('.copy-status'); try { await navigator.clipboard.writeText('biuro@teamsouth.pl'); status.textContent = 'Skopiowano adres e-mail.'; } catch { status.textContent = 'Adres do skopiowania: biuro@teamsouth.pl'; } });
