# TEAM SOUTH — testy bezpieczeństwa, stabilności i wydajności

Data: 29.10.2026. Zakres: kod i podgląd `7eot4/team-south`, https://7eot4.github.io/team-south/ . Testy dotyczą statycznej strony, nie infrastruktury GitHub, systemów firmy ani oryginalnej domeny teamsouth.pl. Nie wysyłano wiadomości, nie testowano cudzych kont i nie wykonywano testów przeciążeniowych.

## Wynik i poprawki

Nie potwierdzono wykonania kodu z badanych pól formularza ani wycieku wpisywanych danych w sprawdzonych ścieżkach. Wynik opisuje zbadany zakres, a nie gwarancję braku wszystkich podatności. Szczegóły ograniczeń są poniżej.

| Obszar | Ustalenie | Zmiana / wynik |
|---|---|---|
| Stabilność pierwszego ekranu | W pomiarze wersji publicznej CLS wynosił ok. 0,170. Mobilny nagłówek przechodził ze 179 do 81 px podczas inicjalizacji; mniejszy udział miała zmiana fontu. | Oddzielna nawigacja `noscript`, rezerwowanie miejsca na kontrolki i końcowe ujawnienie aplikacji. Lokalne próby po zmianie: CLS 0. |
| Rozmiar zasobów mobilnych | Pomiar początkowy: 755 495 B zasobów poza dokumentem HTML. Zdjęcie usługi było pobierane w zbyt dużym wariancie. | Responsywne źródło zdjęć również po zmianie usługi. Lokalny zwykły profil: mediana 377 430 B. Porównanie wielkości orientacyjne, warunki sieci przed/po różnią się. |
| Uruchamiany kod | Brak polityki CSP i kontroli integralności w dokumencie wersji początkowej. Nie było to samo w sobie dowodem wykorzystanej podatności. | CSP z hashem jedynego skryptu; SRI dla skryptu, CSS i CSS fontów; brak `unsafe-inline` i `unsafe-eval`. |
| Awaria lub podmiana skryptu | Potrzebne bezpieczne zachowanie przy braku inicjalizacji. | Kontrolki są ujawniane po pełnym uruchomieniu. Zmieniony plik jest blokowany, formularz pozostaje niedostępny, kontakt i komunikat zastępczy działają. CSP zabrania natywnej wysyłki formularza. |
| Dane formularza | HTML/XSS i fragmenty nagłówków/URL mogą trafiać do pola tekstowego. | Wynik jest wyświetlany przez `textContent`, a treść linków kodowana. Odbiorcy i schematy są stałe. Testy korpusu nie wykonały kodu ani nie zmieniły odbiorcy. |
| Nietypowy Unicode i limity | Nieprawidłowa para znaków UTF-16 mogła powodować wyjątek kodowania URI. | Naprawienie niesparowanych znaków przed kodowaniem, kontrola maksymalnych długości również dla wartości programowych, czyszczenie błędów walidacji po resecie. |
| Błąd ładowania fotografii | Przy nieudanym żądaniu brakowało jasnej informacji i ponowienia. | Stan ładowania, komunikat błędu, przycisk ponowienia i potwierdzony powrót do poprawnego zdjęcia. |
| Publikacja | Bezpośrednie akcje wskazywały zmienne tagi starszych wersji. | Akcje zaktualizowane i przypięte do commitów, tokeny publikacji ograniczone do zadania wdrożenia, wyłączone zachowanie poświadczeń checkout, limit czasu i statyczna bramka bezpieczeństwa w CI. |

## Sprawdzenia bezpieczeństwa

1. Kontrola aktualnych śledzonych plików pod kątem wybranych wzorców tokenów i kluczy; kontrola zakresu artefaktu publikacji. Nie jest to pełny skan historii Git ani całego konta.
2. Brak niebezpiecznych miejsc interpretacji HTML w kodzie aplikacji, brak inline handlerów i stylów w HTML; kontrola lokalnych SVG pod kątem aktywnego kodu i zewnętrznych odwołań.
3. Zgodność sum SHA-384 wszystkich głównych plików ze znacznikami `integrity`, zgodność hasha skryptu z CSP, polityka ustawiona przed zasobami.
4. Kontrolowany korpus ośmiu rodzajów danych: znaczniki HTML, zdarzenia, zamknięcie pola tekstowego, schemat `javascript:`, próby dołączenia Bcc/subject, CRLF, polskie znaki i emoji. Oddzielnie nieprawidłowy UTF-16 i 801 znaków.
5. Aktywne próby dołączenia inline skryptu, obcego skryptu, niezatwierdzonego skryptu z tego samego originu, obrazka i ramki z obcej domeny, żądania `fetch`, zmiany `base` oraz natywnej wysyłki formularza. Polityka blokuje próby przed wysłaniem testowych danych. Cele `.invalid` są dodatkowo przechwytywane przez test; nie atakowano zewnętrznych serwisów.
6. Test zmienionych bajtów aplikacji — skrypt odrzucony. Test niedostępnej fotografii — komunikat i udane ponowienie. Kontrola poprawnego zamknięcia okna i blokady przewijania.
7. Brak automatycznej wysyłki danych i trwałego zapisu przez aplikację. Zasoby własne; mapa łączy z Google dopiero po kliknięciu. Mapa została także otwarta bez zastępowania odpowiedzi Google i wyrenderowała się przy nowej CSP; nie jest to weryfikacja geodezyjna punktu.
8. HTTPS wymuszone w konfiguracji Pages; poprawna walidacja certyfikatu i negocjacja TLS 1.3. HSTS w odpowiedzi serwera. Kontrolowane adresy `.env`, `.git/config`, `.local/security/headers-before.json`, `site.html`, `tests/browser_check.py` zwracają HTTP 404.
9. Linki zewnętrzne mają `noopener noreferrer`, a dokument ustawia `no-referrer`. WhatsApp i poczta są testowane jako przygotowanie treści, bez rzeczywistej wysyłki.

## Responsywność i zgodność

Sprawdzono 19 układów na każdy silnik: Edge 156.0.4314.50, Firefox 157.0 i WebKit 27.2 — łącznie 57 kombinacji. Rozmiary obejmują 320–2560 px szerokości oraz niski ekran poziomy 568×320 i 667×375. Nie wykryto poziomego przepełnienia ani zasłaniania ikon przez menu w tej matrycy. Sprawdzono formularz, bezpieczny tekst, usługi, filtry i galerię, okna modalne, klawiaturę, fokus i FAQ.

WebKit 27.2 zgłasza trzy znane ostrzeżenia `style-src-attr` przy trzech natywnych polach `select`. Zjawisko odtworzono na minimalnej stronie bez stylów i potwierdzono w zgłoszeniu dostawcy: https://github.com/microsoft/playwright/issues/43497 (regresja upstream). Strona nie ma atrybutów `style`, a funkcje działają. Test kwalifikuje wyłącznie ten konkretny przypadek i nadal odrzuca inne naruszenia. Nie wyłączono CSP. To zastrzeżenie do narzędzia/silnika, nie dowód sprawdzenia każdego modelu iPhone ani rzeczywistego Safari.

Pełny test funkcjonalny Edge dodatkowo sprawdza schowek wraz z odmową dostępu, TXT, vCard, poprawne linki WhatsApp/mailto, długi opis, wyczyszczenie formularza, kalkulator, podgląd bez JavaScript i mapę na żądanie.

## Wydajność — laboratorium lokalne

Trzy świeże konteksty na profil, viewport 390×844, wyłączona pamięć podręczna. Wyniki nie są statystykami rzeczywistych odwiedzających.

| Profil | Mediana LCP | Maks. CLS | Mediana transferu zasobów bez HTML |
|---|---:|---:|---:|
| Zwykłe połączenie lokalne | 152 ms | 0 | 377 430 B |
| Opóźnienie 150 ms, pobieranie 200 000 B/s, CPU ×4 | 1436 ms | 0 | 482 548 B |

Nie zarejestrowano zadania blokującego ponad 300 ms w badanym okresie początkowego ładowania. W profilu zwykłym największe zmierzone zadanie miało 77 ms. Pomiary LCP i transferu na adresie publicznym będą wykonane ponownie po publikacji; nie należy porównywać lokalnego czasu wprost z czasem przez internet. Nie mierzono rzeczywistego INP ani płynności GPU na fizycznych telefonach.

## Ograniczenia hostingu i zakresu

- W sprawdzonej odpowiedzi HTTP nie ma nagłówków CSP, X-Frame-Options, X-Content-Type-Options ani Permissions-Policy. CSP została wdrożona w HTML tam, gdzie jest skuteczna. `frame-ancestors` i X-Frame-Options nie działają przez meta, więc nie deklarujemy ochrony przed osadzeniem strony przez inną witrynę. Pełne sterowanie nagłówkami wymaga obsługi po stronie hostingu lub dodatkowej warstwy serwera; nie zmieniano hostingu, domen ani kont użytkownika.
- SRI i CSP nie chronią przed przejęciem repozytorium i jednoczesną zmianą całego HTML wraz z polityką. Nie audytowano 2FA, ról całego konta ani prywatnych repozytoriów.
- Strona nie ma logowania, bazy i własnego serwera aplikacji. Testy SQLi, sesji i autoryzacji takiego zaplecza nie mają tutaj zastosowania. Nie wykonywano skanowania portów, testów przeciążeniowych, testów infrastruktury CDN ani testów serwisów Google/Meta.
- Aktywne konto WhatsApp odbiorcy i działanie konkretnego urządzenia nadal wymagają sprawdzenia przez firmę; testy nie wysyłają wiadomości.

## Powtarzanie

```
python build.py
python verify.py
node --check dist/app.js
python tests/security_static.py
python tests/browser_check.py https://7eot4.github.io/team-south/
python tests/security_browser.py https://7eot4.github.io/team-south/
python tests/cross_browser.py https://7eot4.github.io/team-south/
python tests/performance_check.py https://7eot4.github.io/team-south/
```

Testy przeglądarkowe wymagają Playwright i przeglądarek. WebKit z `upgrade-insecure-requests` testujemy po HTTPS, zgodnie z produkcją. W lokalnym HTTPS używano wyłącznie deweloperskiego certyfikatu w ignorowanym `.local/`; jego akceptacja w testach nie dotyczy publicznego adresu. Pliki kluczy i materiały testowe nie są publikowane.

Surowe lokalne wyniki: `.local/security/` — pomiary, wyniki przeglądarek, blokady CSP i materiały wizualne. Po wdrożeniu sprawdzane są zgodność zdalnego commitu, wynik Actions, integralność publicznych plików oraz testy publicznego adresu. Ten audyt nie jest certyfikacją ani obietnicą całkowitego braku błędów.

Źródła techniczne: [CSP i hashe — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy), [ograniczenie frame-ancestors — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors), [DOM XSS — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html), [HTTPS — GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https), [CLS — web.dev](https://web.dev/articles/cls), [fonty opcjonalne — web.dev](https://web.dev/articles/preload-optional-fonts).
