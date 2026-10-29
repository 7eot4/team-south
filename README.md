# TEAM SOUTH

Autorska wersja poglądowa przebudowy https://teamsouth.pl/.

Aktualna analiza strony, obecności w sieci i zakres wdrożenia: `AUDYT-V2.md`.

Aktualny układ i kontakt: `UKLAD-I-KONTAKT.md` — kompozycja oparta na zdjęciach, zwarte usługi, ikony w nawigacji i WhatsApp z gotową wiadomością. Biel, grafit `#231f20` i szarości zachowują kierunek oryginalnej strony. `SZATA-GRAFICZNA.md` opisuje poprzedni etap doboru palety.

Budowanie: `python build.py`. Kontrola plików: `python verify.py` oraz `node --check dist/app.js`.

Podgląd: `python -m http.server 8178 --bind 127.0.0.1 --directory dist`, następnie http://127.0.0.1:8178/.

Publikacja w `.github/workflows/pages.yml`: zbudowanie i weryfikacja strony, katalog `dist`, gałąź `main`, GitHub Pages przez GitHub Actions. Repozytorium: `7eot4/team-south`.

Adres publikacji: https://7eot4.github.io/team-south/

Źródła strony: `site.html`, `site.css`, `site.js`; katalog galerii w `build.py`. Nie edytuj ręcznie wygenerowanych `dist/index.html`, `dist/style.css` ani `dist/app.js`. Zasoby zdjęć i logo są w `dist/assets`, a ich pochodzenie w `dist/assets/sources.json`.

Opcjonalne odtworzenie zoptymalizowanych zasobów: `python build_assets.py` (wymaga Pillow i dostępu do źródeł). Hosting i zwykły build nie pobierają materiałów z sieci ani nie wymagają Pillow. Fonty zawierają licencje OFL.

Ikony Facebook/Instagram/LinkedIn/WhatsApp są lokalnymi grafikami Bootstrap Icons z licencją MIT. Facebook/Instagram/LinkedIn (`data-social`) otwierają informację o niepodłączonym profilu; nagłówek i stopka korzystają z tej samej obsługi. WhatsApp jest odnośnikiem `wa.me` z numerem firmy i wiadomością początkową generowanym przez `build.py`. Kreator tworzy odnośnik z podsumowaniem w `site.js`. Nie wysyła automatycznie wiadomości; wymaga aktywnego konta odbiorcy na numerze firmy.

Kontrola przeglądarkowa: `python tests/browser_check.py http://127.0.0.1:8178/` (Playwright i zainstalowany Edge; `python -m pip install playwright`). Ten sam skrypt obsługuje publiczny URL. Artefakty QA są zapisywane w ignorowanym `.local/qa-v2`.

Kreator nie zapisuje i nie wysyła danych. Generuje treść, link do poczty, plik TXT lub zawartość schowka. Długi tekst ma alternatywę kopiowania/pobrania. Mapa Google ładuje się dopiero po kliknięciu. Brak analityki i zewnętrznych fontów. Nie zmienia oryginalnej domeny.
