# Weryfikacja — 29.10.2026

- PASS: `node --check dist/app.js`.
- PASS: `git diff --cached --check` przed zapisem zmian.
- PASS: dokument i pięć lokalnych zasobów zwracają HTTP 200.
- PASS: wszystkie wewnętrzne odnośniki wskazują istniejące identyfikatory.
- PASS: Edge w trybie headless, szerokości 1440, 768, 390 i 320 px: brak przewijania poziomego.
- PASS: mobilne menu rozwija się i zamyka po wybraniu sekcji.
- PASS: kopiowanie e-mail z przyznanym dostępem do schowka: potwierdzenie oraz zgodna zawartość schowka.
- PASS: wszystkie obrazy załadowane, brak błędów JavaScript w konsoli podczas sprawdzonych interakcji.
- Wizualnie sprawdzono zrzuty komputer/telefon. Lokalne materiały QA: `.local/desktop.png`, `.local/mobile.png`, `.local/qa.py` (wyłączone z Git).

Wbudowana przeglądarka nie wystartowała z powodu brakującego `browser-service.mjs`; kontrolę wykonano lokalnie przez Playwright i zainstalowany Edge.

Publikacja autoryzowana globalną zgodą użytkownika 29.10.2026. Repozytorium publiczne: `7eot4/CODEX-17-team-south`, gałąź `main`. Pierwsze wdrożenie GitHub Actions zakończone sukcesem: run `40905806937`. Przed publikacją sprawdzono listę śledzonych plików i brak sekretów w publikowanym zakresie. Zdalny commit zgodny z lokalnym.

Adres strony: https://7eot4.github.io/CODEX-17-team-south/

PASS po publikacji: dokument, CSS, JavaScript, favicon i trzy używane zdjęcia odpowiadają plikom lokalnym (dla tekstu porównano treść po normalizacji CRLF/LF). Powtórzono kontrolę w Edge na publicznym URL: szerokości 1440/768/390/320 px, menu mobilne, kopiowanie e-mail, załadowanie obrazów i brak błędów JavaScript — wynik poprawny.
