# TEAM SOUTH — układ strony i kanały kontaktu

29.10.2026. Aktualny etap zastępuje układ opisany we wcześniejszych materiałach. Paleta nadal odpowiada pierwotnej stronie firmy: biel, grafit `#231f20` i neutralne szarości.

## Zmiana kompozycji

- Zamiast pełnoekranowego tła i trzech haseł: krótki nagłówek opisujący działalność, kontakt telefoniczny i zestaw dwóch zdjęć prac.
- Zwarty nagłówek z oryginalnym logo, numerem telefonu, e-mailem i ikonami kanałów kontaktu; na telefonie widoczne ikony obok przycisku menu.
- Zakres usług jako lista po lewej i powiązane zdjęcie z konkretnym opisem po prawej. Usunięto metaforyczne tytuły usług i numery sekcji.
- Fotograficzna galeria z zachowaniem proporcji zdjęć, zamiast jednakowych kart. Pozostały filtry, kolejne zdjęcia, powiększenie i obsługa klawiatury. Rozmiary znane przed załadowaniem fotografii ograniczają przestawianie układu.
- Opisy konkretnych realizacji i publikacje samorządowe są dostępne w rozwijanej części pod galerią; nie konkurują z podstawową ofertą.
- Opis firmy i sprzętu w jednym bloku. Formularz sąsiaduje z danymi kontaktowymi, zamiast osobnej sekcji z kolejnym dużym hasłem i powtarzanym numerem telefonu.
- FAQ jest krótką częścią pomocniczą, a ikony są powtórzone w stopce. Usunięto oddzielną dużą sekcję z ikonami i zbędny pasek postępu przewijania.
- Zachowano wszystkie istotne funkcje: zapytanie, obmiar, galerię, FAQ, mapę na żądanie, udostępnianie i pobieranie kontaktu. Strona nadal jest oznaczona jako poglądowa.

## Ikony społecznościowe

Facebook, Instagram i LinkedIn znajdują się w nagłówku oraz stopce. Nie ma potwierdzonych adresów profili; kliknięcie otwiera informację o niepodłączonym profilu. Przyciski mają nazwy dostępne dla czytników ekranu, działają klawiaturą i oddają fokus po zamknięciu okna.

## WhatsApp

Dodano rzeczywiste odnośniki WhatsApp w nagłówku, stopce, kontakcie oraz mobilnym pasku. Wskazują publiczny telefon firmy w formacie międzynarodowym: `48797559814`.

Wiadomość początkowa:

> Dzień dobry, chciałbym zapytać o ofertę TEAM SOUTH.
>
> Zakres prac:
> Miejscowość:
> Planowany termin:

Odnośnik używa oficjalnego mechanizmu `https://wa.me/NUMER?text=ZAKODOWANA_TREŚĆ`. Na urządzeniu z zainstalowaną aplikacją WhatsApp obsługuje przejście do aplikacji; na komputerze lub bez aplikacji może pojawić się strona pośrednia lub WhatsApp Web. Odbiorca musi mieć aktywne konto WhatsApp na tym numerze — nie zostało to niezależnie potwierdzone i nie wysyłano wiadomości testowych.

Źródło mechanizmu: https://faq.whatsapp.com/5913398998672934 i https://faq.whatsapp.com/425247423114725/ . Ikona pochodzi z Bootstrap Icons z licencją MIT znajdującą się w `dist/assets/icons/LICENSE.txt`.

Kreator przekazuje pełne podsumowanie inwestycji do osobnego przycisku WhatsApp. Treść można zmienić przed wysłaniem; samo kliknięcie nie wysyła wiadomości. Dla długiego opisu dostępne są kopiowanie i plik TXT zamiast zawodnego długiego linku. Formularz nie zapisuje danych i nie przesyła ich automatycznie.

## Kontrola

Sprawdzane są build i zasoby, działanie istniejących funkcji oraz nagłówek i ikony przy sześciu szerokościach. Test WhatsApp sprawdza numer, zakodowaną polską treść, zgodność podsumowania oraz otwarcie właściwego URL w nowej karcie. Odpowiedź WhatsApp jest zastępowana odpowiedzią testową — test nie uruchamia prywatnej aplikacji i nie wysyła wiadomości. Nie jest dowodem rejestracji konta odbiorcy ani testem konkretnego telefonu.

Podglądy kontroli wizualnej znajdują się w ignorowanych `.local/layout-v3/` i `.local/qa-v2/`. Po publikacji weryfikowane są: zgodność lokalnego i zdalnego commitu, wynik GitHub Actions i działająca wersja pod adresem https://7eot4.github.io/team-south/ .
