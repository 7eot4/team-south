# TEAM SOUTH

Autorska wersja poglądowa przebudowy https://teamsouth.pl/.

Aktualna analiza strony, obecności w sieci i zakres wdrożenia: `AUDYT-V2.md`.

Budowanie: `python build.py`. Kontrola plików: `python verify.py` oraz `node --check dist/app.js`.

Podgląd: `python -m http.server 8178 --bind 127.0.0.1 --directory dist`, następnie http://127.0.0.1:8178/.

Publikacja w `.github/workflows/pages.yml`: zbudowanie i weryfikacja strony, katalog `dist`, gałąź `main`, GitHub Pages przez GitHub Actions. Repozytorium: `7eot4/team-south`.

Adres publikacji: https://7eot4.github.io/team-south/

Źródła strony: `site.html`, `site.css`, `site.js`; katalog galerii w `build.py`. Nie edytuj ręcznie wygenerowanych `dist/index.html`, `dist/style.css` ani `dist/app.js`. Zasoby zdjęć i logo są w `dist/assets`, a ich pochodzenie w `dist/assets/sources.json`.

Opcjonalne odtworzenie zoptymalizowanych zasobów: `python build_assets.py` (wymaga Pillow i dostępu do źródeł). Hosting i zwykły build nie pobierają materiałów z sieci ani nie wymagają Pillow. Fonty zawierają licencje OFL.

Kontrola przeglądarkowa: `python tests/browser_check.py http://127.0.0.1:8178/` (Playwright i zainstalowany Edge; `python -m pip install playwright`). Ten sam skrypt obsługuje publiczny URL. Artefakty QA są zapisywane w ignorowanym `.local/qa-v2`.

Kreator nie zapisuje i nie wysyła danych. Generuje treść, link do poczty, plik TXT lub zawartość schowka. Długi tekst ma alternatywę kopiowania/pobrania. Mapa Google ładuje się dopiero po kliknięciu. Brak analityki i zewnętrznych fontów. Nie zmienia oryginalnej domeny.
