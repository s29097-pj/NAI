"""
================================================================================
INTELIGENTNY STEROWNIK OGRZEWANIA Z WYKORZYSTANIEM LOGIKI ROZMYTEJ
================================================================================

OPIS PROBLEMU:
    System steruje ogrzewaniem pomieszczenia w oparciu o logikę rozmytą (fuzzy logic).
    Na wejściu przyjmuje trzy parametry (temperatura wewnątrz, temperatura na zewnątrz, 
    wilgotność), a na wyjściu generuje moc grzania (w procentach).
    
    Problem tradycyjnego sterowania: ostre progi temperatur prowadzą do niestabilności.
    Rozwiązanie: logika rozmyta pozwala na płynne przejścia i naturalne reguły podobne 
    do ludzkiego rozumowania.

AUTORZY ROZWIĄZANIA:
    Autorzy: Michał Małolepszy (s29097), Aleksander Bastek (s27454)

INSTRUKCJA PRZYGOTOWANIA ŚRODOWISKA:
    1. Zainstaluj Pythona 3.8+: https://www.python.org/
    2. Zaktualizuj pip: python.exe -m pip install --upgrade pip
    3. Zainstaluj zależności: pip install -r requirements.txt
    
    Wymagane pakiety (requirements.txt):
    - numpy>=1.20.0
    - scikit-fuzzy>=0.4.0
    - packaging>=21.0
    - networkx>=2.0
    - matplotlib>=3.5.0

================================================================================
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ============================================================================
# KROK 1: DEFINIOWANIE ZMIENNYCH WEJŚCIOWYCH (ANTECEDENTY)
# ============================================================================
# Antecedenty to zmienne, które podajemy systemowi (pomiary czujników)

# Temperatura wewnątrz pomieszczenia: zakres 10-30°C
# Dzielimy ten zakres na 21 wartości (co 1°C)
temp_room = ctrl.Antecedent(np.arange(10, 31, 1), 'temp_room')

# Temperatura na zewnątrz: zakres -15 do 20°C
# Dzielimy na 36 wartości (co 1°C)
temp_outside = ctrl.Antecedent(np.arange(-15, 21, 1), 'temp_outside')

# Wilgotność pomieszczenia: zakres 20-100%
# Dzielimy na 81 wartości (co 1%)
humidity = ctrl.Antecedent(np.arange(20, 101, 1), 'humidity')

# ============================================================================
# KROK 2: DEFINIOWANIE ZMIENNEJ WYJŚCIOWEJ (CONSEQUENT)
# ============================================================================
# Consequent to wyjście systemu - to co system ma wygenerować

# Moc grzania: zakres 0-100%
# Dzielimy na 101 wartości (co 1%)
heating_power = ctrl.Consequent(np.arange(0, 101, 1), 'heating_power')

# ============================================================================
# KROK 3: DEFINIOWANIE FUNKCJI PRZYNALEŻNOŚCI (ZBIORY ROZMYTE)
# ============================================================================
# Funkcje przynależności opisują jak wartości zmiennych należą do zbiorów rozmytych
# Używamy funkcji trójkątnych (trimf): każda ma formę trójkąta

# --- TEMPERATURA W POMIESZCZENIU ---
# Zdefiniujemy trzy rozmyte zbiory: zimno, komfort, ciepło
temp_room['zimno'] = fuzz.trimf(temp_room.universe, [10, 10, 18])    # Pik na 10°C
temp_room['komfort'] = fuzz.trimf(temp_room.universe, [16, 21, 25])  # Pik na 21°C
temp_room['cieplo'] = fuzz.trimf(temp_room.universe, [22, 28, 30])   # Pik na 28°C

# --- TEMPERATURA NA ZEWNĄTRZ ---
# Zdefiniujemy trzy rozmyte zbiory: bardzo_zimno, zimno, ciepło
temp_outside['bardzo_zimno'] = fuzz.trimf(temp_outside.universe, [-15, -15, 0])   # Pik na -15°C
temp_outside['zimno'] = fuzz.trimf(temp_outside.universe, [-5, 5, 15])            # Pik na 5°C
temp_outside['ciepło'] = fuzz.trimf(temp_outside.universe, [10, 20, 20])          # Pik na 20°C

# --- WILGOTNOŚĆ W POMIESZCZENIU ---
# Zdefiniujemy trzy rozmyte zbiory: niska, umiarkowana, wysoka
humidity['nisko'] = fuzz.trimf(humidity.universe, [20, 20, 40])       # Pik na 20%
humidity['umiarkowana'] = fuzz.trimf(humidity.universe, [35, 60, 80]) # Pik na 60%
humidity['wysoko'] = fuzz.trimf(humidity.universe, [70, 100, 100])    # Pik na 100%

# --- MOC GRZANIA (WYJŚCIE) ---
# Zdefiniujemy trzy rozmyte zbiory: niska, średnia, wysoka
heating_power['niska'] = fuzz.trimf(heating_power.universe, [0, 0, 40])     # Pik na 0%
heating_power['średnia'] = fuzz.trimf(heating_power.universe, [25, 50, 75]) # Pik na 50%
heating_power['wysoka'] = fuzz.trimf(heating_power.universe, [60, 100, 100])# Pik na 100%

# ============================================================================
# KROK 4: DEFINIOWANIE REGUŁ ROZMYTYCH (IF-THEN)
# ============================================================================
# Reguły opisują logikę sterowania w języku naturalnym
# Format: IF (warunki) THEN (wyjście)

# Reguła 1: Jeśli zimno WEWNĄTRZ i bardzo zimno NA ZEWNĄTRZ → grzej maksymalnie
rule1 = ctrl.Rule(temp_room['zimno'] & temp_outside['bardzo_zimno'], heating_power['wysoka'])

# Reguła 2: Jeśli zimno WEWNĄTRZ i zimno NA ZEWNĄTRZ → grzej maksymalnie
rule2 = ctrl.Rule(temp_room['zimno'] & temp_outside['zimno'], heating_power['wysoka'])

# Reguła 3: Jeśli zimno WEWNĄTRZ i ciepło NA ZEWNĄTRZ → grzej średnio
rule3 = ctrl.Rule(temp_room['zimno'] & temp_outside['ciepło'], heating_power['średnia'])

# Reguła 4: Jeśli KOMFORTOWO WEWNĄTRZ i bardzo zimno NA ZEWNĄTRZ → grzej aby utrzymać
rule4 = ctrl.Rule(temp_room['komfort'] & temp_outside['bardzo_zimno'], heating_power['wysoka'])

# Reguła 5: Jeśli KOMFORTOWO WEWNĄTRZ i zimno NA ZEWNĄTRZ → grzej trochę
rule5 = ctrl.Rule(temp_room['komfort'] & temp_outside['zimno'], heating_power['średnia'])

# Reguła 6: Jeśli KOMFORTOWO WEWNĄTRZ i ciepło NA ZEWNĄTRZ → grzej mało
rule6 = ctrl.Rule(temp_room['komfort'] & temp_outside['ciepło'], heating_power['niska'])

# Reguła 7: Jeśli CIEPŁO WEWNĄTRZ → nie grzej
rule7 = ctrl.Rule(temp_room['cieplo'], heating_power['niska'])

# Reguła 8: Jeśli wilgotność NISKA → możesz grzać mocniej (para pomaga)
rule8 = ctrl.Rule(humidity['nisko'], heating_power['wysoka'])

# Reguła 9: Jeśli wilgotność WYSOKA i KOMFORTOWO → nie przegrzewaj (zbyt sucho)
rule9 = ctrl.Rule(humidity['wysoko'] & temp_room['komfort'], heating_power['niska'])

# ============================================================================
# KROK 5: STWORZENIE SYSTEMU STERUJĄCEGO
# ============================================================================
# Łączymy wszystkie reguły w jeden system fuzzy

# Tworzymy system ze wszystkimi 9 regułami
heating_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, 
    rule6, rule7, rule8, rule9
])

# Tworzymy symulację (instancję) systemu sterującego
heating_sim = ctrl.ControlSystemSimulation(heating_ctrl)

# ============================================================================
# KROK 6: FUNKCJA OBLICZAJĄCĄ MOC GRZANIA
# ============================================================================

def calculate_heating(temp_r, temp_o, humid):
    """
    Oblicza moc grzania dla podanych parametrów.
    
    Args:
        temp_r: temperatura pomieszczenia (°C)
        temp_o: temperatura zewnętrzna (°C)
        humid: wilgotność (%)
    
    Returns:
        moc grzania (%)
    """
    try:
        # Podajemy wartości wejściowe do systemu fuzzy
        heating_sim.input['temp_room'] = temp_r
        heating_sim.input['temp_outside'] = temp_o
        heating_sim.input['humidity'] = humid
        
        # Obliczamy wyjście
        heating_sim.compute()
        
        # Zwracamy obliczoną moc grzania
        # Ochrona przed błędem: jeśli output nie istnieje, zwróć 0
        if 'heating_power' in heating_sim.output:
            return heating_sim.output['heating_power']
        else:
            return 0.0
    except Exception as e:
        print(f"Błąd w calculate_heating: {e}")
        return 0.0

# ============================================================================
# KROK 7: FUNKCJA DEMONSTRACYJNA - TESTOWANIE SYSTEMU
# ============================================================================

def demo_real_time():
    """
    Demonstracja działania algorytmu na 4 przykładowych scenariuszach.
    
    Każdy scenariusz symuluje różne warunki pogodowe i wnętrza,
    pokazując jak system reaguje na różne kombinacje wejść.
    """
    import time
    
    # Lista przykładowych scenariuszy testowych
    # Każdy scenariusz zawiera: temp w pomieszczeniu, temp na zewnątrz, wilgotność
    przykłady = [
        {
            "nazwa": "MROŹNY DZIEŃ - POMIESZCZENIE ZIMNE",
            "temp_room": 17, 
            "temp_outside": -10, 
            "humidity": 30,
            "opis": "Zimno na zewnątrz, w pomieszczeniu zimno, sucho - potrzeba mocnego grzania"
        },
        {
            "nazwa": "ŁAGODNY DZIEŃ - POMIESZCZENIE KOMFORTOWE",
            "temp_room": 22, 
            "temp_outside": 10, 
            "humidity": 80,
            "opis": "Całkiem ciepło na zewnątrz, wewnątrz komfort, ale wilgotno - zmniejsz grzanie"
        },
        {
            "nazwa": "CIEPŁY DZIEŃ - POMIESZCZENIE CIEPŁE",
            "temp_room": 25, 
            "temp_outside": 5, 
            "humidity": 60,
            "opis": "Umiarkowana wilgotność, pomieszczenie już ciepłe - praktycznie brak grzania"
        },
        {
            "nazwa": "PRZEJŚCIOWY DZIEŃ - POMIESZCZENIE CHŁODNE",
            "temp_room": 19, 
            "temp_outside": 0, 
            "humidity": 45,
            "opis": "Średnie warunki - system powinien grzać na poziomie średnim"
        },
    ]
    
    print("\n" + "="*80)
    print("SYMULACJA STEROWANIA OGRZEWANIEM - LOGIKA ROZMYTA")
    print("="*80)
    
    # Lista do przechowywania wyników (później do wizualizacji)
    wyniki = []
    
    # Przetwarzamy każdy scenariusz
    for i, dane in enumerate(przykłady, 1):
        print(f"\n[PRZYPADEK {i}] {dane['nazwa']}")
        print(f"  Opis: {dane['opis']}")
        
        # Obliczamy moc grzania używając dedykowanej funkcji
        moc_grzania = calculate_heating(
            dane["temp_room"], 
            dane["temp_outside"], 
            dane["humidity"]
        )
        
        # Wyświetlamy wynik
        print(f"  Wejścia:  temp_pom={dane['temp_room']}°C, "
              f"temp_zewn={dane['temp_outside']}°C, "
              f"wilgotność={dane['humidity']}%")
        print(f"  WYJŚCIE:  moc grzania = {moc_grzania:.1f}%")
        
        # Interpretacja wyniku
        if moc_grzania >= 70:
            interpretacja = "🔥 MAKSYMALNE GRZANIE"
        elif moc_grzania >= 40:
            interpretacja = "🔥 GRZANIE ŚREDNIE"
        else:
            interpretacja = "❄️ MINIMALNE GRZANIE"
        print(f"  Interpretacja: {interpretacja}")
        
        # Zapisujemy wynik do listy
        wyniki.append({
            'przypadek': f"Przypadek {i}",
            'temp_room': dane["temp_room"],
            'temp_outside': dane["temp_outside"],
            'humidity': dane["humidity"],
            'heating_power': moc_grzania
        })
        
        time.sleep(1)  # Opóźnienie dla czytelności
    
    print("\n" + "="*80)
    return wyniki

# ============================================================================
# KROK 8: FUNKCJA WIZUALIZACJI - WYKRESY ZAPISYWANE DO PLIKU
# ============================================================================

def visualize_results(wyniki):
    """
    Tworzy ładne wykresy pokazujące wyniki symulacji.
    Wykresy są zapisywane do pliku PNG zamiast wyświetlania okna.
    
    Wykresy pokazują:
    1. Porównanie mocy grzania dla każdego scenariusza (wykres słupkowy)
    2. Wpływ temperatury wewnątrz na moc grzania (z parametrami stałymi)
    3. Wpływ temperatury zewnątrz na moc grzania (z parametrami stałymi)
    4. Wpływ wilgotności na moc grzania (z parametrami stałymi)
    """
    
    # Przygotowanie danych do pierwszego wykresu
    przypadki = [w['przypadek'] for w in wyniki]
    moce_grzania = [w['heating_power'] for w in wyniki]
    
    # Stworzenie figury z 4 podwykresy (2x2)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Inteligentny Sterownik Ogrzewania - Analiza Wyników', 
                 fontsize=16, fontweight='bold')
    
    # ===== WYKRES 1: MOŚĆ GRZANIA DLA KAŻDEGO SCENARIUSZA =====
    ax1 = axes[0, 0]
    kolory = ['#ff6b6b' if m >= 70 else '#ffd93d' if m >= 40 else '#6bcf7f' 
              for m in moce_grzania]
    
    bars = ax1.bar(range(len(przypadki)), moce_grzania, color=kolory, 
                    edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Moc Grzania (%)', fontweight='bold')
    ax1.set_title('Moc Grzania dla Każdego Scenariusza', fontweight='bold')
    ax1.set_xticks(range(len(przypadki)))
    ax1.set_xticklabels([f'Poz.{i+1}' for i in range(len(przypadki))])
    ax1.set_ylim([0, 100])
    ax1.grid(axis='y', alpha=0.3)
    
    # Dodaj wartości na słupkach
    for bar, moc in zip(bars, moce_grzania):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{moc:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # ===== WYKRES 2: WPŁYW TEMPERATURY WEWNĄTRZ =====
    ax2 = axes[0, 1]
    
    # Symulujemy jak zmienia się moc przy zmieniającej się temp wewnątrz
    # Pozostałe parametry: temp_zewn=0°C, wilgotność=50%
    temperatury_wew = np.arange(10, 31, 1)
    moce_temp_wew = []
    
    print("Generowanie wykresu 2/4: Wpływ temperatury wewnątrz...", end='', flush=True)
    for t_wew in temperatury_wew:
        # Używamy dedykowanej funkcji do obliczenia mocy
        moc = calculate_heating(t_wew, 0, 50)
        moce_temp_wew.append(moc)
    print(" OK")
    
    ax2.plot(temperatury_wew, moce_temp_wew, 'b-', linewidth=2.5, marker='o')
    ax2.fill_between(temperatury_wew, moce_temp_wew, alpha=0.3, color='blue')
    ax2.set_xlabel('Temperatura Pomieszczenia (°C)', fontweight='bold')
    ax2.set_ylabel('Moc Grzania (%)', fontweight='bold')
    ax2.set_title('Wpływ Temperatury Wewnątrz', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # ===== WYKRES 3: WPŁYW TEMPERATURY ZEWNĄTRZ =====
    ax3 = axes[1, 0]
    
    # Symulujemy jak zmienia się moc przy zmieniającej się temp zewnątrz
    # Pozostałe parametry: temp_wew=20°C, wilgotność=50%
    temperatury_zew = np.arange(-15, 21, 1)
    moce_temp_zew = []
    
    print("Generowanie wykresu 3/4: Wpływ temperatury zewnętrznej...", end='', flush=True)
    for t_zew in temperatury_zew:
        # Używamy dedykowanej funkcji do obliczenia mocy
        moc = calculate_heating(20, t_zew, 50)
        moce_temp_zew.append(moc)
    print(" OK")
    
    ax3.plot(temperatury_zew, moce_temp_zew, 'r-', linewidth=2.5, marker='s')
    ax3.fill_between(temperatury_zew, moce_temp_zew, alpha=0.3, color='red')
    ax3.set_xlabel('Temperatura Zewnętrzna (°C)', fontweight='bold')
    ax3.set_ylabel('Moc Grzania (%)', fontweight='bold')
    ax3.set_title('Wpływ Temperatury Zewnętrznej', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # ===== WYKRES 4: WPŁYW WILGOTNOŚCI =====
    ax4 = axes[1, 1]
    
    # Symulujemy jak zmienia się moc przy zmieniającej się wilgotności
    # Pozostałe parametry: temp_wew=20°C, temp_zewn=0°C
    wilgotnosci = np.arange(20, 101, 2)
    moce_wilg = []
    
    print("Generowanie wykresu 4/4: Wpływ wilgotności...", end='', flush=True)
    for wilg in wilgotnosci:
        # Używamy dedykowanej funkcji do obliczenia mocy
        moc = calculate_heating(20, 0, wilg)
        moce_wilg.append(moc)
    print(" OK")
    
    ax4.plot(wilgotnosci, moce_wilg, 'g-', linewidth=2.5, marker='^')
    ax4.fill_between(wilgotnosci, moce_wilg, alpha=0.3, color='green')
    ax4.set_xlabel('Wilgotność Pomieszczenia (%)', fontweight='bold')
    ax4.set_ylabel('Moc Grzania (%)', fontweight='bold')
    ax4.set_title('Wpływ Wilgotności', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Dopasowanie układu
    plt.tight_layout()
    
    # ZAPISUJEMY WYKRES DO PLIKU zamiast wyświetlania okna
    # To pozwala programowi działać bez problemów w terminalu
    filename = 'fuzzy_heating_results.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n✓ Wykresy zapisane do pliku: {filename}")
    
    # Zamknij figurę aby zwolnić pamięć
    plt.close(fig)
    
    print("\n" + "="*80)
    print("WYKRESY ZOSTAŁY WYGENEROWANE")
    print("="*80)

# ============================================================================
# KROK 9: GŁÓWNA FUNKCJA - URUCHOMIENIE CAŁEGO SYSTEMU
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "INTELIGENTNY STEROWNIK OGRZEWANIA" + " "*30 + "║")
    print("║" + " "*16 + "System z Logiki Rozmytej (Fuzzy Logic)" + " "*24 + "║")
    print("╚" + "="*78 + "╝")
    
    # Uruchamiamy demonstrację i zbieramy wyniki
    wyniki = demo_real_time()
    
    # Wyświetlamy wykresy (zapisane do pliku)
    print("\nGenerowanie wykresów...")
    visualize_results(wyniki)
    
    print("\n✓ Program zakończył się pomyślnie!")
    print("  Wszystkie scenariusze zostały przetestowane.")
    print("  Wykresy zostały wygenerowane i zapisane do pliku PNG.")
    print("  Otwórz plik 'fuzzy_heating_results.png' aby zobaczyć wykresy.")
