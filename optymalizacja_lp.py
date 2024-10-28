import pulp

#odkomentować dla danych 1/ zakomentowac dla innych
# from dane import pobierz_czasy_przetwarzania, pobierz_terminy_realizacji, pobierz_czasy_przezbrojen

#odkomanetować dla danych 2/ zakomentowac dla innych
# from dane2 import pobierz_czasy_przetwarzania, pobierz_terminy_realizacji, pobierz_czasy_przezbrojen

from dane3 import sprawdz_dane
from wizualizacja import rysuj_wykres
import json

def wczytaj_dane(plik_wejsciowy):
    with open(plik_wejsciowy, 'r') as f:
        dane = json.load(f)

    czasy_przetwarzania = dane["czasy_przetwarzania"]
    terminy_realizacji = dane["terminy_realizacji"]

    # Zamiana stringów z powrotem na krotki
    czasy_przezbrojen = {
        tuple(key.split(" -> ")): value for key, value in dane["czasy_przezbrojen"].items()
    }

    return czasy_przetwarzania, terminy_realizacji, czasy_przezbrojen



def rozwiaz_lp():
    #odkomentować dla danych 3/ zakomentowac dla innych
    plik_danych = 'dane_testowe.json'
    sprawdz_dane(plik_danych)
    czasy_przetwarzania, terminy_realizacji, czasy_przezbrojen = wczytaj_dane(plik_danych)

    # odkomentować dla danych 1,2/ zakomentowac dla innych
    # czasy_przetwarzania = pobierz_czasy_przetwarzania()
    # terminy_realizacji = pobierz_terminy_realizacji()
    # czasy_przezbrojen = {k: v for k, v in pobierz_czasy_przezbrojen().items() if k[0] != k[1]}

    zadania = list(czasy_przetwarzania.keys())

    # Model PuLP
    model = pulp.LpProblem("Jednomaszynowy_problem_z_przezbrojeniami", pulp.LpMinimize)

    # Zmienna decyzyjna: czas rozpoczęcia dla każdego zadania
    czasy_rozpoczecia = pulp.LpVariable.dicts("CzasRozpoczecia", zadania, lowBound=0, cat="Continuous")

    # Zmienna decyzyjna: opóźnienie dla każdego zadania
    opoznienia = pulp.LpVariable.dicts("Opoznienie", zadania, lowBound=0, cat="Continuous")

    # Zmienne binarne: ustalanie kolejności między zadaniami
    kolejność = pulp.LpVariable.dicts(
        "Kolejnosc",
        [(zadanie1, zadanie2) for zadanie1 in zadania for zadanie2 in zadania if zadanie1 != zadanie2],
        cat="Binary"
    )

    # Funkcja celu: minimalizacja sumy opóźnień (tardiness)
    model += pulp.lpSum([opoznienia[zadanie] for zadanie in zadania]), "Suma_opoznien"

    # Ograniczenia na opóźnienia:
    for zadanie in zadania:
        model += (
            opoznienia[zadanie] >= czasy_rozpoczecia[zadanie] + czasy_przetwarzania[zadanie] - terminy_realizacji[
                zadanie],
            f"Opoznienie_dla_{zadanie}"
        )

    # Ograniczenia na kolejność zadań i przezbrojeń:
    M = 1000  # Wartość dużej liczby do wymuszenia ograniczeń binarnych (tzw. Big M method)
    for (zadanie1, zadanie2), czas_przezbrojenia in czasy_przezbrojen.items():
        if zadanie1 != zadanie2:  # Ignorowanie porównywania tego samego zadania
            id_kolejnosc = f"{zadanie1}_{zadanie2}"

            # Gdy zadanie1 jest przed zadaniem2
            model += (
                czasy_rozpoczecia[zadanie2] >= czasy_rozpoczecia[zadanie1] + czasy_przetwarzania[
                    zadanie1] + czas_przezbrojenia - M * (1 - kolejność[(zadanie1, zadanie2)]),
                f"Kolejnosc_{id_kolejnosc}_1"
            )

            # Gdy zadanie2 jest przed zadanie1
            model += (
                czasy_rozpoczecia[zadanie1] >= czasy_rozpoczecia[zadanie2] + czasy_przetwarzania[
                    zadanie2] + czas_przezbrojenia - M * (1 - kolejność[(zadanie2, zadanie1)]),
                f"Kolejnosc_{id_kolejnosc}_2"
            )

    # Ograniczenie na jednoznaczność kolejności: jedno zadanie musi być albo przed, albo po drugim
    for zadanie1 in zadania:
        for zadanie2 in zadania:
            if zadanie1 != zadanie2:
                model += (
                    kolejność[(zadanie1, zadanie2)] + kolejność[(zadanie2, zadanie1)] == 1,
                    f"Unikniecie_sprzecznosci_{zadanie1}_i_{zadanie2}"
                )

    # Rozwiązanie modelu
    #model.solve()
    model.solve(pulp.PULP_CBC_CMD(timeLimit=300))  # Limit czasu 300 sekund

    # Sprawdzanie statusu rozwiązania
    if pulp.LpStatus[model.status] != 'Optimal':
        print(f"Ostrzeżenie: Problem nie ma optymalnego rozwiązania. Status: {pulp.LpStatus[model.status]}")

    # Wyniki
    wyniki = {}
    for zadanie in zadania:
        start = czasy_rozpoczecia[zadanie].varValue
        end = start + czasy_przetwarzania[zadanie]
        opoznienie = opoznienia[zadanie].varValue
        wyniki[zadanie] = {
            "Czas rozpoczęcia": start,
            "Czas zakończenia": end,
            "Opóźnienie": opoznienie
        }

    return wyniki, czasy_przezbrojen, terminy_realizacji


if __name__ == "__main__":
    wyniki, czasy_przezbrojen, terminy_realizacji = rozwiaz_lp()
    print("Wyniki:")
    for zadanie, wynik in wyniki.items():
        print(
            f"{zadanie}: Czas rozpoczęcia = {wynik['Czas rozpoczęcia']}, Czas zakończenia = {wynik['Czas zakończenia']}, Opóźnienie = {wynik['Opóźnienie']}")
    rysuj_wykres(wyniki, terminy_realizacji, czasy_przezbrojen)