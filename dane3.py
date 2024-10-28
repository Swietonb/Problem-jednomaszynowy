import json
import random
import pandas as pd

liczba_zadan = 15                   # Liczba zadań
min_przetw = 1                      # minimalny czas przetwarzania
max_przetw = 8                      # maksymalny czas przetwarzania
min_termin = liczba_zadan + 30      # minimalny termin
max_termin = liczba_zadan + 80      # maksymalny termin
min_przezb = 1                      # minimalny czas przezbrojenia
max_przezb = 5                      # maksymalny czas przezbrojenia

def generuj_czasy_przetwarzania(liczba_zadan):
    return {f"Zadanie {i}": random.randint(min_przetw, max_przetw) for i in range(1, liczba_zadan + 1)}

def generuj_terminy_realizacji(liczba_zadan):
    return {f"Zadanie {i}": random.randint(min_termin, max_termin) for i in range(1, liczba_zadan + 1)}

def generuj_czasy_przezbrojen(liczba_zadan):
    zadania = [f"Zadanie {i}" for i in range(1, liczba_zadan + 1)]
    czasy_przezbrojenia = {}
    for zadanie1 in zadania:
        for zadanie2 in zadania:
            if zadanie1 == zadanie2:
                czas = 0
            else:
                czas = random.randint(min_przezb, max_przezb)
            czasy_przezbrojenia[(zadanie1, zadanie2)] = czas
    return czasy_przezbrojenia

def zapisz_dane_do_pliku(liczba_zadan, plik_wyjscia):
    dane = {
        "czasy_przetwarzania": generuj_czasy_przetwarzania(liczba_zadan),
        "terminy_realizacji": generuj_terminy_realizacji(liczba_zadan),
        # Zamiana krotek na stringi
        "czasy_przezbrojen": {f"{zadanie1} -> {zadanie2}": czas for (zadanie1, zadanie2), czas in generuj_czasy_przezbrojen(liczba_zadan).items()}
    }
    with open(plik_wyjscia, 'w') as f:
        json.dump(dane, f, indent=4)
    print(f"Dane zapisane do pliku {plik_wyjscia}")

def naturalna_kolejnosc(zadanie):
    return int(zadanie[1:])

def sprawdz_dane(plik_wejsciowy):
    with open(plik_wejsciowy, 'r') as f:
        dane = json.load(f)

    print("Czasy przetwarzania zadań:")
    for zadanie, czas in dane["czasy_przetwarzania"].items():
        print(f"{zadanie}: {czas} godzin")

    print("\nTerminy realizacji zadań:")
    for zadanie, termin in dane["terminy_realizacji"].items():
        print(f"{zadanie}: {termin} godzin")

    # wworzenie tabeli z czasami przezbrojeń
    zadania = sorted([f"Z{i}" for i in range(1, len(dane["czasy_przetwarzania"]) + 1)], key=naturalna_kolejnosc)
    przezbrojenia_df = pd.DataFrame(index=zadania, columns=zadania)

    for klucz, czas in dane["czasy_przezbrojen"].items():
        zadanie1, zadanie2 = klucz.replace("Zadanie ", "Z").split(" -> ")
        przezbrojenia_df.loc[zadanie1, zadanie2] = czas

    # wyswietlanie pelnej tabeli
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print("\nCzasy przezbrojeń między zadaniami (w godzinach):")
    print(przezbrojenia_df)

if __name__ == "__main__":
    # Generowanie danych dla wybranej liczby zadań i zapis do pliku
    plik_wyjscia = 'dane_testowe.json'
    zapisz_dane_do_pliku(liczba_zadan, plik_wyjscia)
    sprawdz_dane(plik_wyjscia)