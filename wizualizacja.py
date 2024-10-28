import matplotlib.pyplot as plt

def rysuj_wykres(wyniki, terminy_realizacji, czasy_przezbrojen):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    zadania = [zadanie for zadanie in wyniki if isinstance(wyniki[zadanie], dict)]
    kolory = plt.cm.tab10.colors

    # Sortowanie zadań według czasu rozpoczęcia, aby rysować w odpowiedniej kolejności
    zadania_posortowane = sorted(zadania, key=lambda x: wyniki[x]["Czas rozpoczęcia"])

    # Wykres: Zadania posortowane według czasu rozpoczęcia
    for i, zadanie in enumerate(zadania_posortowane):
        start = wyniki[zadanie]["Czas rozpoczęcia"]
        end = wyniki[zadanie]["Czas zakończenia"]
        opoznienie = wyniki[zadanie]["Opóźnienie"]

        # Rysowanie paska dla zadania
        ax1.barh(i, end - start, left=start, color=kolory[i % len(kolory)], edgecolor='black')

        # Rysowanie tekstu o opóźnieniu
        if opoznienie > 0:
            ax1.text(end + 2, i, f"Opóźnienie: {opoznienie}", va='center')

        # Rysowanie pogrubionych linii przerywanych dla terminów realizacji (ciemny czerwony)
        termin = terminy_realizacji[zadanie]
        ax1.plot([termin, termin], [i - 0.4, i + 0.4], color='darkred', linestyle='--', linewidth=2, label="Termin realizacji" if i == 0 else "")

        # Rysowanie przezbrojenia między zadaniami
        if i < len(zadania_posortowane) - 1:
            zadanie2 = zadania_posortowane[i + 1]
            czas_przezbrojenia = czasy_przezbrojen.get((zadanie, zadanie2), 0)
            ax1.barh(i, czas_przezbrojenia, left=end, height=0.3, color='red', edgecolor='black', label="Przezbrojenie" if i == 0 else "")

    # Opis osi
    ax1.set_xlabel('Czas')
    ax1.set_ylabel('Zadania (wg czasu rozpoczęcia)')
    ax1.set_yticks(range(len(zadania_posortowane)))
    ax1.set_yticklabels(zadania_posortowane)
    ax1.invert_yaxis()

    # Dodanie siatki co 5 jednostek do wykresu
    ax1.xaxis.set_major_locator(plt.MultipleLocator(5))
    ax1.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)

    # Dodanie legendy
    ax1.legend()

    plt.tight_layout()
    plt.show()
