# Weryfikacja — 29.10.2026

## Rozbudowa interaktywna v2

- `python build.py`, `python verify.py`, `node --check dist/app.js`: PASS.
- Kontrola statyczna: 62 unikalne identyfikatory HTML, 46 lokalnych odwołań do zasobów, poprawne kotwice, brak automatycznej wysyłki i trwałego zapisu danych.
- Testy `tests/browser_check.py` w zainstalowanym Edge: wszystkie pięć usług; cztery filtry galerii; paginacja 6/12/16; okno zdjęć, klawisze strzałek i Esc, fokus modalny i powrót do miniatury.
- Kreator: puste i białe pola, wybór usługi, podsumowanie, bezpieczne wyświetlanie tekstu użytkownika, zgodna treść mailto, zawartość schowka, plik TXT, długa wiadomość, cofanie i reset.
- Pomocnik: powierzchnia 10 × 5 = 50 m² i objętość 10 × 5 × 0,3 = 15 m³; odrzucenie ujemnych danych; przekazanie do kreatora bez omijania wyboru usługi.
- FAQ, plik vCard, kopiowanie e-mail, zapasowe udostępnianie linku i okno informacji o prywatności: PASS.
- Brak zapytań do stron trzecich przed kliknięciem mapy. Test mapy sprawdza wstawienie iframe po kliknięciu; zewnętrzna odpowiedź Google jest zastąpiona lokalną odpowiedzią testową. Nie dowodzi to dokładności punktu ani dostępności usługi Google.
- Szerokości 1440/1024/768/540/390/320 px, menu mobilne, obrazy, ograniczone animacje oraz kontakt i galeria bez JavaScript: PASS. Osobno sprawdzono podsumowanie kreatora przy 320 px.
- Brak błędów JavaScript, błędnych odpowiedzi HTTP oraz wpisów localStorage/sessionStorage w sprawdzonych ścieżkach. Po odświeżeniu dane kreatora nie są odtwarzane.
- Oceniono zrzuty pulpitu, telefonu, sekcji oferty i podsumowania. Lokalne materiały: `.local/qa-v2/`, wyłączone z Git.

Wbudowana przeglądarka nadal nie uruchamia się z powodu brakującego modułu dostawcy. Kontrolę wykonano przez Playwright i lokalny Edge, bez użycia prywatnego profilu przeglądarki. Skrypt pozwala powtórzyć te same sprawdzenia na adresie publicznym.

Aktualny adres: https://7eot4.github.io/team-south/ . Wynik publikacji i zgodność zdalnego commitu sprawdzane są po push; poniżej zachowano historyczny zapis pierwszej wersji.

Wdrożenie v2: GitHub Actions `40910131087`, commit `842f105203430123fe5890ae2019a808157f3d2c`, wynik `success`. Pełny skrypt `tests/browser_check.py` wykonano także na publicznym URL. Końcowa korekta dodaje wymagane pole `N` wizytówki vCard 3.0; treść danych firmy pozostaje bez zmian. Dla tej korekty ponownie sprawdzany jest plik kontaktu, zgodność publicznych zasobów oraz wynik wdrożenia.

## Pierwsza wersja — zapis historyczny

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
