import pandas as pd

def pobierz_czasy_przetwarzania():
    return {
        "Zadanie 1": 5,
        "Zadanie 2": 3,
        "Zadanie 3": 4,
        "Zadanie 4": 6,
        "Zadanie 5": 2
    }

def pobierz_terminy_realizacji():
    return {
        "Zadanie 1": 10,
        "Zadanie 2": 8,
        "Zadanie 3": 9,
        "Zadanie 4": 12,
        "Zadanie 5": 7
    }

def pobierz_czasy_przezbrojen():
    return {
        ("Zadanie 1", "Zadanie 1"): 0, ("Zadanie 1", "Zadanie 2"): 1, ("Zadanie 1", "Zadanie 3"): 2,
        ("Zadanie 1", "Zadanie 4"): 3, ("Zadanie 1", "Zadanie 5"): 1,
        ("Zadanie 2", "Zadanie 1"): 1, ("Zadanie 2", "Zadanie 2"): 0, ("Zadanie 2", "Zadanie 3"): 1,
        ("Zadanie 2", "Zadanie 4"): 2,("Zadanie 2", "Zadanie 5"): 1,
        ("Zadanie 3", "Zadanie 1"): 2,("Zadanie 3", "Zadanie 2"): 1,("Zadanie 3", "Zadanie 3"): 0,
        ("Zadanie 3", "Zadanie 4"): 1,("Zadanie 3", "Zadanie 5"): 2,
        ("Zadanie 4", "Zadanie 1"): 3,("Zadanie 4", "Zadanie 2"): 2,("Zadanie 4", "Zadanie 3"): 1,
        ("Zadanie 4", "Zadanie 4"): 0,("Zadanie 4", "Zadanie 5"): 1,
        ("Zadanie 5", "Zadanie 1"): 1,("Zadanie 5", "Zadanie 2"): 1,("Zadanie 5", "Zadanie 3"): 2,
        ("Zadanie 5", "Zadanie 4"): 1,("Zadanie 5", "Zadanie 5"): 0}

def przygotuj_tabele_danych():
    czasy_przetwarzania = pobierz_czasy_przetwarzania()
    terminy_realizacji = pobierz_terminy_realizacji()
    czas_przezbrojenia = pobierz_czasy_przezbrojen()

    czasy_przetwarzania_df = pd.DataFrame(list(czasy_przetwarzania.items()), columns=["Zadanie", "Czas przetwarzania (h)"])
    terminy_realizacji_df = pd.DataFrame(list(terminy_realizacji.items()), columns=["Zadanie", "Termin realizacji (h)"])

    return czasy_przetwarzania_df, terminy_realizacji_df

def sprawdz_dane():
    czasy_przetwarzania = pobierz_czasy_przetwarzania()
    terminy_realizacji = pobierz_terminy_realizacji()
    czas_przezbrojenia = pobierz_czasy_przezbrojen()

    print("Czasy przetwarzania zadań:")
    for zadanie, czas in czasy_przetwarzania.items():
        print(f"{zadanie}: {czas} godzin")

    print("\nTerminy realizacji zadań:")
    for zadanie, termin in terminy_realizacji.items():
        print(f"{zadanie}: {termin} godzin")

    print(f"\nStały czas przezbrojenia między zadaniami: {czas_przezbrojenia} godzin")
