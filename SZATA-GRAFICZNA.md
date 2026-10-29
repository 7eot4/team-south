# TEAM SOUTH — korekta szaty graficznej

Ten dokument opisuje poprzedni etap. Aktualny układ i kanały kontaktu: `UKLAD-I-KONTAKT.md`. Paleta bieli, czerni i grafitu pozostaje w użyciu.

29.10.2026. Zmiana zgodna z dyspozycją zachowania kolorystyki wcześniejszej strony https://teamsouth.pl/.

## Punkty odniesienia

Sprawdzono aktualny kod źródłowy oryginalnej strony i jej oryginalne logo. W kodzie dominują biel `rgb(255,255,255)`, czerń `rgb(0,0,0)` oraz grafit marki `rgb(35,31,32)` = `#231f20`. Kolorów przypadkowych przycisków dostawcy i domyślnych komponentów platformy nie traktowano jako identyfikacji firmy. Oryginalna witryna używa też fotografii w odcieniach szarości na pierwszym ekranie.

## Wdrożenie

- Usunięto zieleń i limonkę z całego interfejsu, także z aktywnych stanów, formularza, mapy, obramowań, okien, ikon, paska kontaktowego i efektów najechania. Grafit `#231f20`, biel i neutralne szarości zastępują poprzednią paletę.
- Zastosowano biały nagłówek z oryginalnym czarno-białym logo, grafitowe przyciski i neutralne tła sekcji. Pomiędzy ofertą, galerią, publikacjami, zapytaniem i kontaktem zachowano czytelne rozdzielenie powierzchni białych, jasnoszarych i grafitowych.
- Pierwszy ekran wykorzystuje zdjęcie prac przy obiekcie przemysłowym z dotychczasowej galerii firmy; czarno-biały efekt i neutralne przyciemnienie realizuje CSS. Fotografia nie jest przypisywana do konkretnego klienta ani lokalizacji.
- Zmieniono wąskie nagłówki na szerszą typografię Manrope, dopasowano rozmiary, łamanie tekstu i odstępy do komputera i telefonu. Poprawiono czytelność małego podpisu na zdjęciu przez ciemny podkład.
- Zdjęcia w galerii zachowują naturalne kolory, aby pokazywać rzeczywisty wygląd nawierzchni i zieleni. Sekcja sprzętu otrzymała czarno-białą fotografię dopasowaną do grafitowego tła.
- Podgląd udostępnianego linku wskazuje oryginalne czarno-białe logo firmy. Kolor interfejsu przeglądarki to grafit marki.
- Zachowano wszystkie istniejące funkcje, treści oraz oryginalne pliki zdjęć. Nie zmieniono danych firmy ani adresu publikacji.
- Build dodaje identyfikator zawartości do adresów CSS i JavaScript, aby nowe dokumenty nie korzystały ze starszej wersji tych plików zachowanej w pamięci przeglądarki.

## Weryfikacja

`python build.py`, `python verify.py`, `node --check dist/app.js` oraz kontrola palety CSS. Sprawdzono brak dawnych zmiennych zieleni i limonki oraz brak nasyconych kolorów interfejsu poza bliskim czerni grafitem marki.

Testy Edge obejmują sześć szerokości 1440/1024/768/540/390/320 px oraz wszystkie wcześniej wdrożone interakcje. Oceniono zrzuty komputera, telefonu, pierwszego ekranu, całej strony i kontaktu. Materiały lokalne: `.local/restyle/` oraz `.local/qa-v2/`.

Publikacja: https://7eot4.github.io/team-south/ . Po wdrożeniu kontrolowane są wynik GitHub Actions, zgodność zdalnego commitu i pliki dostępne publicznie.
