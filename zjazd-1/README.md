# 🎮 Gra Wythoffa

## 🧩 Zasady gry

Gra **Wythoffa** to dwuosobowa, turowa gra o **sumie zerowej**.  
Na początku są **dwa stosy** (np. zapałek).  
Gracze na zmianę wykonują ruchy według następujących zasad:

- W swoim ruchu gracz może:
  - zabrać **dowolną liczbę zapałek z jednego stosu**, **lub**
  - zabrać **taką samą liczbę zapałek z obu stosów** jednocześnie.
- Nie można pominąć ruchu.
- Przegrywa gracz, który **nie może wykonać ruchu** (oba stosy są puste).

📚 Więcej informacji: [Wikipedia – Wythoff's game](https://en.wikipedia.org/wiki/Wythoff%27s_game)

## ⚙️ Instrukcja uruchomienia

1. Zainstaluj **Python 3.10+**.  
2. Zainstaluj wymagane moduły:

    ```bash
    pip install easyAI
    pip install pygame
    ```
3. Uruchom grę:

    ```bash
    python wythoff.py
    ```

## 🧠 Opis gry

**Wythoff's Game** to **dwuosobowa gra strategiczna** o sumie zerowej,  
w której gracze na zmianę zabierają zapałki z dwóch stosów.  
Celem jest **zabranie ostatniej zapałki**, co oznacza zwycięstwo.  

Gra jest **deterministyczna**, tzn. wynik zależy tylko od decyzji graczy —  
brak elementów losowych.

## 🎯 Zasady rozgrywki

- Gra rozpoczyna się z dwoma stosami zapałek (domyślnie **[5, 7]**).  
- W swojej turze gracz może:
  - zabrać **dowolną liczbę zapałek (≥1)** z jednego stosu, lub
  - zabrać **taką samą liczbę zapałek z obu stosów**.
- Gracz, który zabierze **ostatnią zapałkę**, **wygrywa**.
- Gra kończy się, gdy oba stosy są puste.

💡 Niektóre pozycje początkowe są **wygrane**, inne **przegrane**  
dla pierwszego gracza (np. `[5,7]` to pozycja wygrana przy optymalnej grze).

## 🧱 Opis implementacji

Implementacja została napisana w **Pythonie**  
z użyciem bibliotek **easyAI** (logika gry) i **Pygame** (interfejs graficzny).

### 🔹 Klasa `WythoffGame`

Dziedziczy po `TwoPlayerGame` z `easyAI`.

#### Atrybuty:
- `players` – lista graczy (człowiek i AI)  
- `heaps` – lista z liczbą zapałek w dwóch stosach (domyślnie `[5,7]`)  
- `current_player` – indeks aktualnego gracza (1: człowiek, 2: AI)  
- `selected` – lista zbiorów zaznaczonych zapałek w każdym stosie  
- `last_move` – ostatni wykonany ruch (string)

### 🔹 Metody klasy

| Metoda | Opis |
|:-------|:-----|
| `__init__(players, heaps=None)` | Inicjalizuje grę z graczami i opcjonalnymi stosami. |
| `possible_moves()` | Zwraca listę możliwych ruchów w formacie `"a,b"`. |
| `make_move(move)` | Wykonuje ruch, aktualizując stosy i przełączając gracza. |
| `win()` | Sprawdza, czy gra została wygrana (oba stosy puste). |
| `is_over()` | Alias dla `win()`. |
| `scoring()` | Zwraca ocenę pozycji (100 dla wygranej, 0 inaczej). |
| `show()` | Wypisuje stan gry w konsoli (debug). |
| `draw(screen)` | Rysuje stan gry w oknie Pygame. |

## 🔄 Główna pętla gry

W części `__main__`:

1. Inicjalizowany jest moduł **Pygame**.
2. Tworzony jest obiekt gry z graczem i **AI (algorytm Negamax, głębokość 6)**.
3. Obsługiwane są zdarzenia myszki:
   - zaznaczanie zapałek,
   - przycisk **„Zabierz”** do wykonania ruchu,
   - po zakończeniu: **„Zagraj ponownie”** i **„Wyjdź z gry”**.
4. AI automatycznie wykonuje swoje ruchy.
5. Stan gry jest rysowany w czasie rzeczywistym.

## 🧩 Dodatkowe uwagi

- AI gra **optymalnie** – jeśli pozycja jest przegrana, zawsze wygra.  
- Kod jest w pełni zgodny z zasadami z Wikipedii.  
- W kodzie znajdują się komentarze ułatwiające zrozumienie logiki.  

## 👥 Autorzy

**Michał Małolepszy (s29097),**
**Aleksander Bastek (s27454)**
