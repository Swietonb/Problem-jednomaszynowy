from ortools.sat.python import cp_model

#odkomentować dla danych 1/ zakomentowac dla innych
# from dane import pobierz_czasy_przetwarzania, pobierz_terminy_realizacji, pobierz_czasy_przezbrojen

#odkomanetować dla danych 2/ zakomentowac dla innych
# from dane2 import pobierz_czasy_przetwarzania, pobierz_terminy_realizacji, pobierz_czasy_przezbrojen
from dane3 import sprawdz_dane

from wizualizacja import rysuj_wykres
import time

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

def rozwiaz_cp_sat():
    # odkomentować dla danych 3/ zakomentowac dla innych
    plik_danych = 'dane_testowe.json'
    sprawdz_dane(plik_danych)
    czasy_przetwarzania, terminy_realizacji, czasy_przezbrojen = wczytaj_dane(plik_danych)

    # odkomentować dla danych 1,2/ zakomentowac dla innych
    # czasy_przetwarzania = pobierz_czasy_przetwarzania()
    # terminy_realizacji = pobierz_terminy_realizacji()
    # czasy_przezbrojen = pobierz_czasy_przezbrojen()

    zadania = list(czasy_przetwarzania.keys())
    num_zadan = len(zadania)

    # Tworzenie modelu CP-SAT
    model = cp_model.CpModel()

    # przedział czasu dla każdego zadania
    task_starts = []
    task_ends = []
    task_intervals = []
    for zadanie in zadania:
        start = model.NewIntVar(0, 200, f'start_{zadanie}')
        duration = czasy_przetwarzania[zadanie]
        end = model.NewIntVar(0, 200, f'end_{zadanie}')
        interval = model.NewIntervalVar(start, duration, end, f'interval_{zadanie}')
        task_starts.append(start)
        task_ends.append(end)
        task_intervals.append(interval)

    # Ograniczenie, że zadania nie nakładają się na siebie
    model.AddNoOverlap(task_intervals)

    # Dodanie czasów przezbrojenia
    for i in range(num_zadan):
        for j in range(num_zadan):
            if i == j:
                continue
            zadanie_i = zadania[i]
            zadanie_j = zadania[j]
            lit = model.NewBoolVar(f'precede_{zadanie_i}_{zadanie_j}')
            # Jeśli zadanie i jest przed zadaniem j
            model.Add(task_starts[j] >= task_ends[i] + czasy_przezbrojen[(zadanie_i, zadanie_j)]).OnlyEnforceIf(lit)
            # Jeśli zadanie j jest przed zadaniem i
            model.Add(task_starts[i] >= task_ends[j] + czasy_przezbrojen[(zadanie_j, zadanie_i)]).OnlyEnforceIf(lit.Not())
            # Jedno z nich musi być prawdziwe
            model.Add(lit + lit.Not() == 1)

    # Ograniczenia na opóźnienia
    opoznienia = []
    for i, zadanie in enumerate(zadania):
        opoznienie = model.NewIntVar(0, 200, f'opoznienie_{zadanie}')
        model.Add(opoznienie >= task_ends[i] - terminy_realizacji[zadanie])
        opoznienia.append(opoznienie)

    # Funkcja celu: minimalizacja sumy opóźnień
    model.Minimize(sum(opoznienia))

    # Ustawienia solvera
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0  # limit czasu

    # Mierzenie czasu rozpoczęcia
    start_time = time.time()

    # Rozwiązywanie problemu
    status = solver.Solve(model)

    # Mierzenie czasu zakończenia
    end_time = time.time()
    solving_time = end_time - start_time

    # Sprawdzanie wyników
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        wyniki = {}
        suma_opoznien = 0  # Zmienna do sumy opóźnień
        for i, zadanie in enumerate(zadania):
            opoznienie_wartosc = solver.Value(opoznienia[i])
            wyniki[zadanie] = {
                "Czas rozpoczęcia": solver.Value(task_starts[i]),
                "Czas zakończenia": solver.Value(task_ends[i]),
                "Opóźnienie": opoznienie_wartosc
            }
            suma_opoznien += opoznienie_wartosc  # Dodawanie opóźnienia do sumy
        # Dodajemy czas rozwiązania i sumę opóźnień do wyników
        wyniki["Czas rozwiązania (s)"] = solving_time
        wyniki["Suma opóźnień"] = suma_opoznien
        return wyniki, czasy_przezbrojen, terminy_realizacji
    else:
        print("Nie znaleziono optymalnego rozwiązania.")
        print(f"Status: {solver.StatusName(status)}")
        return None


if __name__ == "__main__":
    wyniki, czasy_przezbrojen, terminy_realizacji = rozwiaz_cp_sat()
    if wyniki:
        print("Wyniki CP-SAT:")
        for zadanie, wynik in wyniki.items():
            if zadanie not in ["Czas rozwiązania (s)", "Suma opóźnień"]:
                print(f"{zadanie}: Czas rozpoczęcia = {wynik['Czas rozpoczęcia']}, "
                      f"Czas zakończenia = {wynik['Czas zakończenia']}, "
                      f"Opóźnienie = {wynik['Opóźnienie']}")
        print(f"\nSuma opóźnień: {wyniki['Suma opóźnień']}")
        print(f"Czas rozwiązania: {wyniki['Czas rozwiązania (s)']:.4f} sekund")

    rysuj_wykres(wyniki, terminy_realizacji, czasy_przezbrojen)