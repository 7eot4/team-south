# Kalkulator orientacyjnego budżetu

Wdrożenie przygotowane 30.10.2026. Użytkownik zlecił kalkulacje wyceny; cennika TEAM SOUTH nie dostarczono. Kalkulator jawnie używa referencji zewnętrznych. Nie przedstawia ich jako stawek, oferty, potwierdzonej dostępności maszyn ani gwarantowanego kosztu TEAM SOUTH.

## Dane i zakres

Jedno źródło danych w aplikacji: `estimateCatalogue` i `estimateFoundationRate` w `estimate.js`. Ceny nie są pobierane z sieci podczas wizyty. Brak zapisywania danych klienta. Kalkulator i główna obsługa strony są osobnymi skryptami `defer`, aby nie przetwarzać całego kodu jako jednego dużego zadania. Oba mają własne hashe CSP i SRI. Przy niedostępnym kalkulatorze pozostaje komunikat z kontaktem; niesprawny skrypt podstawowy blokuje również uruchomienie kalkulatora.

| Model | Jednostka | Przyjęta cena netto | Źródło i ograniczenie |
|---|---|---|---|
| Ułożenie kostki betonowej | m² | 50–80 zł | [Oferteo](https://www.oferteo.pl/artykuly/ukladanie-kostki-brukowej-cena-za-metr), tabela „Cena netto za m² / mb”, pozycja robocizny dla betonu. Bez materiału i oddzielnej podbudowy. |
| Standardowa kostka wraz z ułożeniem | m² | 130–160 zł | To samo zestawienie Oferteo, pozycja materiału z robocizną. Podbudowa jest odrębną pozycją modelu; nie dodajemy do tego wariantu ponownie stawki za samo ułożenie. |
| Opcjonalna podbudowa | m² | 30–50 zł | Oddzielna pozycja tego samego zestawienia. Wybór użytkownika; bez automatycznego doliczania do każdego zakresu. Szczegóły warstw i materiałów wymagają potwierdzenia w indywidualnej ofercie. |
| Przesuwanie i niwelacja mas ziemi | m³ | 40–100 zł | [Odcienie Zieleni](https://odcieniezieleni.com/cennik/), własny cennik prac w ziemi w Lublinie. Referencja z innego regionu, nie cena dla każdej klasy gruntu ani dowolnego wykopu. Bez dostawy ziemi, wywozu i utylizacji. |
| Minikoparka 3,5 t z operatorem | h | 120 zł | [SMTeam](https://kontenery.smteam.pl/cennik/), JCB 8035 ZTS; cena godzinowa, transport dodatkowo. Nie używamy ceny dobowej 600 zł jako odpowiednika ośmiu godzin. Paliwo, dobór maszyny, dojazd oraz minimalny czas należy potwierdzić w ofercie. |

Źródła odczytano 30.10.2026. Zestawienie Oferteo oznacza aktualizację 04.05.2026; data odczytu pozostałych stron nie jest deklaracją daty zmiany cennika. Widełki nie są badaniem pełnego rynku ani regionalną taryfą TEAM SOUTH. Nie użyto cen z demonstracyjnych firm ani historycznego cennika REVT, którego adres zwracał błąd.

## Obliczenia

- Ilość można podać bezpośrednio; przy m² również jako długość × szerokość, przy m³ jako długość × szerokość × średnią grubość warstwy. Godziny podaje użytkownik; program nie wymyśla wydajności koparki.
- Każdą pozycję liczymy osobno dla dolnej i górnej stawki. Kwoty poszczególnych pozycji zaokrąglamy do całkowitej liczby groszy. Opcjonalne koszty użytkownika są kwotą netto.
- Rezerwa 0/10/15/20% obejmuje prace, opcjonalną podbudowę i dodatkowe koszty. Jest osobną pozycją budżetu, nie opłatą wykonawcy.
- Wynik nie obejmuje VAT. Aplikacja nie kwalifikuje inwestycji podatkowo ani nie przypisuje domyślnej stawki podatku.
- Górny koniec przedziału nie jest wiążącym maksimum. Małe zlecenia, minimalne rozliczenie, grunt, odwodnienie, obrzeża, transport i wywóz wymagają wyceny indywidualnej, chyba że użytkownik sam wpisał już uzgodnioną kwotę w kosztach dodatkowych.
- Drogi i place zabaw wymagają konkretnego zakresu i dokumentacji; nie generujemy arbitralnej ceny za metr dla takich inwestycji.

## Przekazanie do zapytania

Przycisk dołącza kopię wyniku do kreatora i wybiera pasującą kategorię prac. Użytkownik uzupełnia miejscowość, następnie sam otwiera pocztę lub WhatsApp, kopiuje tekst albo pobiera TXT. Nie jest wysyłane żadne zgłoszenie w tle.

Zmiana danych kalkulatora, ręczna zmiana zakresu lub zmiana kategorii prac odłącza nieaktualne obliczenie. Czyszczenie zapytania również je odłącza. Brak JavaScript lub blokada integralności skryptu pozostawia kontakt do firmy, a nie aktywne kontrolki z niepoliczonymi kwotami.

## Weryfikacja

`python tests/estimate_check.py [adres-strony]` sprawdza konkretne rachunki dla wszystkich modeli, przecinek/kropkę, zaokrąglenia, podbudowę, rezerwę, błędne dane, przekazanie do wiadomości i odłączanie nieaktualnej kalkulacji. Testy nie wysyłają wiadomości do firmy.
