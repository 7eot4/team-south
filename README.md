# TEAM SOUTH

Autorska wersja poglądowa przebudowy https://teamsouth.pl/.

Aktualna analiza strony, obecności w sieci i zakres wdrożenia: `AUDYT-V2.md`.

Testy i utwardzenie bezpieczeństwa: `AUDYT-BEZPIECZENSTWA.md`. Bramka statyczna jest uruchamiana przy każdej publikacji. Dodatkowe skrypty w `tests/` obejmują kontrolowane ataki na formularz i CSP, podmianę skryptu, błędy sieciowe, 57 układów w trzech silnikach i powtarzane pomiary laboratoryjne. Ograniczenia hostingu i znana regresja WebKit są opisane w raporcie.

Środowisko testów przeglądarkowych: `python -m pip install -r requirements-dev.txt`, następnie `python -m playwright install firefox webkit`; wymagany zainstalowany Edge. Test trzech silników uruchamiaj pod HTTPS. Wersja Playwright przypięta dla powtarzalności testów; nie jest zależnością strony produkcyjnej.

Aktualny układ i kontakt: `UKLAD-I-KONTAKT.md` — kompozycja oparta na zdjęciach, zwarte usługi, ikony w nawigacji i WhatsApp z gotową wiadomością. Biel, grafit `#231f20` i szarości zachowują kierunek oryginalnej strony. `SZATA-GRAFICZNA.md` opisuje poprzedni etap doboru palety.

Budowanie: `python build.py`. Kontrola plików: `python verify.py` oraz `node --check dist/app.js`.

Podgląd: `python -m http.server 8178 --bind 127.0.0.1 --directory dist`, następnie http://127.0.0.1:8178/.

Publikacja w `.github/workflows/pages.yml`: zbudowanie i weryfikacja strony, katalog `dist`, gałąź `main`, GitHub Pages przez GitHub Actions. Repozytorium: `7eot4/team-south`.

Adres publikacji: https://7eot4.github.io/team-south/

Kalkulator orientacyjnego budżetu jest w sekcji `#kalkulator`: kostka (sama robocizna albo materiał z ułożeniem), praca z masami ziemi i godziny minikoparki. Ilość można podać bezpośrednio lub obliczyć z wymiarów. Opcjonalnie dolicza podbudowę, znane koszty dodatkowe i własną rezerwę. Kwoty netto pochodzą z jawnych referencji, nie z potwierdzonego cennika TEAM SOUTH. Źródła, zakres i wzory: `KALKULATOR-WYCENY.md`. Wynik można dołączyć do zapytania; zmiana danych odłącza nieaktualną kalkulację. Test trzech silników: `python tests/estimate_check.py https://7eot4.github.io/team-south/`.

Animacje zachowują czarno-biały styl: wejścia sekcji podczas przewijania, stopniowe wejście nagłówka, reakcje przycisków i zdjęć, zmiany galerii, kroki formularza, menu, rozwijane odpowiedzi i okna podglądu. Cienka linia postępu czytania korzysta z obsługiwanej przez przeglądarkę osi przewijania; w pozostałych silnikach jest pomijana. Bez bibliotek i pętli ruchu w tle. Treść pozostaje widoczna bez animacji; systemowe `prefers-reduced-motion` wyłącza efekty, również po zmianie ustawienia w trakcie wizyty. Test: `python tests/motion_check.py https://7eot4.github.io/team-south/`.

Źródła strony: `site.html`, `site.css`, `site.js`, `estimate.js`; katalog galerii w `build.py`. Nie edytuj ręcznie wygenerowanych `dist/index.html`, `dist/style.css`, `dist/app.js` ani `dist/estimate.js`. Zasoby zdjęć i logo są w `dist/assets`, a ich pochodzenie w `dist/assets/sources.json`.

Opcjonalne odtworzenie zoptymalizowanych zasobów: `python build_assets.py` (wymaga Pillow i dostępu do źródeł). Hosting i zwykły build nie pobierają materiałów z sieci ani nie wymagają Pillow. Fonty zawierają licencje OFL.

Ikony Facebook/Instagram/LinkedIn/WhatsApp są lokalnymi grafikami Bootstrap Icons z licencją MIT. Facebook/Instagram/LinkedIn (`data-social`) otwierają informację o niepodłączonym profilu; nagłówek i stopka korzystają z tej samej obsługi. WhatsApp jest odnośnikiem `wa.me` z numerem firmy i wiadomością początkową generowanym przez `build.py`. Kreator tworzy odnośnik z podsumowaniem w `site.js`. Nie wysyła automatycznie wiadomości; wymaga aktywnego konta odbiorcy na numerze firmy.

Kontrola przeglądarkowa: `python tests/browser_check.py http://127.0.0.1:8178/` (Playwright i zainstalowany Edge; `python -m pip install playwright`). Ten sam skrypt obsługuje publiczny URL. Artefakty QA są zapisywane w ignorowanym `.local/qa-v2`.

Kreator nie zapisuje i nie wysyła danych. Generuje treść, link do poczty, plik TXT lub zawartość schowka. Długi tekst ma alternatywę kopiowania/pobrania. Mapa Google ładuje się dopiero po kliknięciu. Brak analityki i zewnętrznych fontów. Nie zmienia oryginalnej domeny.
