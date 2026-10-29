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

Nie sprawdzono publikacji, zdalnego repozytorium ani GitHub Actions: oczekują potwierdzenia użytkownika dla nowego publicznego repozytorium i wdrożenia. Sprawdzenie lokalne nie dowodzi poprawnego wdrożenia.
