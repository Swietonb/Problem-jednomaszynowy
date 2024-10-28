import pandas as pd

def pobierz_czasy_przetwarzania():
    return {
        "Zadanie 1": 5,
        "Zadanie 2": 3,
        "Zadanie 3": 4,
        "Zadanie 4": 6,
        "Zadanie 5": 2,
        "Zadanie 6": 7,
        "Zadanie 7": 3,
        "Zadanie 8": 5
    }

def pobierz_terminy_realizacji():
    return {
        "Zadanie 1": 12,
        "Zadanie 2": 24,
        "Zadanie 3": 33,
        "Zadanie 4": 40,
        "Zadanie 5": 22,
        "Zadanie 6": 30,
        "Zadanie 7": 19,
        "Zadanie 8": 28
    }

def pobierz_czasy_przezbrojen():
    czasy_przezbrojenia = {
        # Czasy przezbrojeń z Zadanie 1
        ("Zadanie 1", "Zadanie 1"): 0,  ("Zadanie 1", "Zadanie 2"): 2,
        ("Zadanie 1", "Zadanie 3"): 3,  ("Zadanie 1", "Zadanie 4"): 1,
        ("Zadanie 1", "Zadanie 5"): 2,  ("Zadanie 1", "Zadanie 6"): 4,
        ("Zadanie 1", "Zadanie 7"): 3,  ("Zadanie 1", "Zadanie 8"): 2,

        # Czasy przezbrojeń z Zadanie 2
        ("Zadanie 2", "Zadanie 1"): 2,  ("Zadanie 2", "Zadanie 2"): 0,
        ("Zadanie 2", "Zadanie 3"): 1,  ("Zadanie 2", "Zadanie 4"): 3,
        ("Zadanie 2", "Zadanie 5"): 2,  ("Zadanie 2", "Zadanie 6"): 2,
        ("Zadanie 2", "Zadanie 7"): 4,  ("Zadanie 2", "Zadanie 8"): 3,

        # Czasy przezbrojeń z Zadanie 3
        ("Zadanie 3", "Zadanie 1"): 3,  ("Zadanie 3", "Zadanie 2"): 1,
        ("Zadanie 3", "Zadanie 3"): 0,  ("Zadanie 3", "Zadanie 4"): 2,
        ("Zadanie 3", "Zadanie 5"): 3,  ("Zadanie 3", "Zadanie 6"): 1,
        ("Zadanie 3", "Zadanie 7"): 2,  ("Zadanie 3", "Zadanie 8"): 4,

        # Czasy przezbrojeń z Zadanie 4
        ("Zadanie 4", "Zadanie 1"): 1,  ("Zadanie 4", "Zadanie 2"): 3,
        ("Zadanie 4", "Zadanie 3"): 2,  ("Zadanie 4", "Zadanie 4"): 0,
        ("Zadanie 4", "Zadanie 5"): 4,  ("Zadanie 4", "Zadanie 6"): 2,
        ("Zadanie 4", "Zadanie 7"): 1,  ("Zadanie 4", "Zadanie 8"): 3,

        # Czasy przezbrojeń z Zadanie 5
        ("Zadanie 5", "Zadanie 1"): 2,  ("Zadanie 5", "Zadanie 2"): 2,
        ("Zadanie 5", "Zadanie 3"): 3,  ("Zadanie 5", "Zadanie 4"): 4,
        ("Zadanie 5", "Zadanie 5"): 0,  ("Zadanie 5", "Zadanie 6"): 1,
        ("Zadanie 5", "Zadanie 7"): 3,  ("Zadanie 5", "Zadanie 8"): 2,

        # Czasy przezbrojeń z Zadanie 6
        ("Zadanie 6", "Zadanie 1"): 4,  ("Zadanie 6", "Zadanie 2"): 2,
        ("Zadanie 6", "Zadanie 3"): 1,  ("Zadanie 6", "Zadanie 4"): 2,
        ("Zadanie 6", "Zadanie 5"): 1,  ("Zadanie 6", "Zadanie 6"): 0,
        ("Zadanie 6", "Zadanie 7"): 3,  ("Zadanie 6", "Zadanie 8"): 2,

        # Czasy przezbrojeń z Zadanie 7
        ("Zadanie 7", "Zadanie 1"): 3,  ("Zadanie 7", "Zadanie 2"): 4,
        ("Zadanie 7", "Zadanie 3"): 2,  ("Zadanie 7", "Zadanie 4"): 1,
        ("Zadanie 7", "Zadanie 5"): 3,  ("Zadanie 7", "Zadanie 6"): 3,
        ("Zadanie 7", "Zadanie 7"): 0,  ("Zadanie 7", "Zadanie 8"): 1,

        # Czasy przezbrojeń z Zadanie 8
        ("Zadanie 8", "Zadanie 1"): 2,  ("Zadanie 8", "Zadanie 2"): 3,
        ("Zadanie 8", "Zadanie 3"): 4,  ("Zadanie 8", "Zadanie 4"): 3,
        ("Zadanie 8", "Zadanie 5"): 2,  ("Zadanie 8", "Zadanie 6"): 2,
        ("Zadanie 8", "Zadanie 7"): 1,  ("Zadanie 8", "Zadanie 8"): 0,
    }

    return czasy_przezbrojenia

def przygotuj_tabele_danych():
    czasy_przetwarzania = pobierz_czasy_przetwarzania()
    terminy_realizacji = pobierz_terminy_realizacji()

    czasy_przetwarzania_df = pd.DataFrame(list(czasy_przetwarzania.items()), columns=["Zadanie", "Czas przetwarzania (h)"])
    terminy_realizacji_df = pd.DataFrame(list(terminy_realizacji.items()), columns=["Zadanie", "Termin realizacji (h)"])

    return czasy_przetwarzania_df, terminy_realizacji_df

def sprawdz_dane():
    czasy_przetwarzania = pobierz_czasy_przetwarzania()
    terminy_realizacji = pobierz_terminy_realizacji()
    czasy_przezbrojenia = pobierz_czasy_przezbrojen()

    print("Czasy przetwarzania zadań:")
    for zadanie, czas in czasy_przetwarzania.items():
        print(f"{zadanie}: {czas} godzin")

    print("\nTerminy realizacji zadań:")
    for zadanie, termin in terminy_realizacji.items():
        print(f"{zadanie}: {termin} godzin")

    print("\nCzasy przezbrojeń między zadaniami:")
    for (zadanie1, zadanie2), czas in czasy_przezbrojenia.items():
        print(f"{zadanie1} -> {zadanie2}: {czas} godzin")

if __name__ == "__main__":
    sprawdz_dane()
