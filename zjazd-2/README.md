# Inteligentny Sterownik Ogrzewania

System sterowania ogrzewaniem oparty na logice rozmytej (Fuzzy Logic), implementowany w języku Python.

## 📋 Opis projektu

Projekt implementuje inteligentny system sterowania ogrzewaniem pomieszczenia z wykorzystaniem logiki rozmytej. System analizuje trzy parametry wejściowe i na ich podstawie określa optymalną moc grzewczą:

### Wejścia systemu:
- **Temperatura w pomieszczeniu** (10-30°C)
- **Temperatura na zewnątrz** (-15 do 20°C)
- **Wilgotność w pomieszczeniu** (20-100%)

### Wyjście systemu:
- **Moc ogrzewania** (0-100%)

System wykorzystuje zbiory rozmyte i reguły językowe do podejmowania decyzji, co pozwala na płynne i naturalne sterowanie, podobne do ludzkiego rozumowania. Kod zawiera bardzo szczegółowe komentarze do każdego kroku oraz wizualizację wyników w postaci czterech wykresów.

## 👥 Autorzy

**Michał Małolepszy (s29097),**
**Aleksander Bastek (s27454)**

## 🛠️ Wymagania systemowe

- Python 3.8 lub nowszy
- pip (menedżer pakietów)

## 📦 Instalacja

### Krok 1: Zaktualizuj pip (opcjonalnie, ale zalecane)

```bash
  python.exe -m pip install --upgrade pip
```

### Krok 2: Zainstaluj wymagane pakiety z pliku requirements.txt

```bash
  pip install -r requirements.txt
```

### Zawartość pliku requirements.txt:

```
numpy>=1.20.0
scikit-fuzzy>=0.4.0
packaging>=21.0
networkx>=2.0
matplotlib>=3.5.0
```

Jeśli plik `requirements.txt` nie istnieje w Twoim katalogu, utwórz go z powyższą zawartością.

## 🚀 Uruchomienie

### Uruchomienie programu:

```bash
  python fuzzy_heating.py
```

### Oczekiwany wynik:

Program wyświetli w konsoli szczegółową symulację dla 4 scenariuszy testowych:

```
════════════════════════════════════════════════════════════════════════════════
INTELIGENTNY STEROWNIK OGRZEWANIA - LOGIKA ROZMYTA
════════════════════════════════════════════════════════════════════════════════

[PRZYPADEK 1] MROŹNY DZIEŃ - POMIESZCZENIE ZIMNE
  Opis: Zimno na zewnątrz, w pomieszczeniu zimno, sucho - potrzeba mocnego grzania
  Wejścia:  temp_pom=17°C, temp_zewn=-10°C, wilgotność=30%
  WYJŚCIE:  moc grzania = 84.4%
  Interpretacja: 🔥 MAKSYMALNE GRZANIE

[PRZYPADEK 2] ŁAGODNY DZIEŃ - POMIESZCZENIE KOMFORTOWE
  Opis: Całkiem ciepło na zewnątrz, wewnątrz komfort, ale wilgotno - zmniejsz grzanie
  Wejścia:  temp_pom=22°C, temp_zewn=10°C, wilgotność=80%
  WYJŚCIE:  moc grzania = 38.0%
  Interpretacja: 🔥 GRZANIE ŚREDNIE

[PRZYPADEK 3] CIEPŁY DZIEŃ - POMIESZCZENIE CIEPŁE
  Opis: Umiarkowana wilgotność, pomieszczenie już ciepłe - praktycznie brak grzania
  Wejścia:  temp_pom=25°C, temp_zewn=5°C, wilgotność=60%
  WYJŚCIE:  moc grzania = 15.6%
  Interpretacja: ❄️ MINIMALNE GRZANIE

[PRZYPADEK 4] PRZEJŚCIOWY DZIEŃ - POMIESZCZENIE CHŁODNE
  Opis: Średnie warunki - system powinien grzać na poziomie średnim
  Wejścia:  temp_pom=19°C, temp_zewn=0°C, wilgotność=45%
  WYJŚCIE:  moc grzania = 50.0%
  Interpretacja: 🔥 GRZANIE ŚREDNIE
```

### Wizualizacja wyników:

Po wyświetleniu scenariuszy testowych system automatycznie wygeneruje 4 profesjonalne wykresy:

1. **Moc Grzania dla Każdego Scenariusza** - wykres słupkowy pokazujący porównanie mocy
2. **Wpływ Temperatury Wewnątrz** - jak zmiana temperatury pomieszczenia wpływa na moc grzania
3. **Wpływ Temperatury Zewnętrznej** - jak zmiana temperatury na zewnątrz wpływa na moc grzania
4. **Wpływ Wilgotności** - jak zmiana wilgotności wpływa na moc grzania

Wykresy pomogą zrozumieć zależności między wejściami a wyjściem systemu.

### Użycie w własnym kodzie:

```python
from fuzzy_heating import heating_sim

# Podaj wartości wejściowe
heating_sim.input['temp_room'] = 18
heating_sim.input['temp_outside'] = -5
heating_sim.input['humidity'] = 45

# Oblicz wynik
heating_sim.compute()

# Odczytaj moc ogrzewania
print(f"Zalecana moc grzania: {heating_sim.output['heating_power']:.1f}%")
```

## 🧠 Logika systemu

System wykorzystuje **9 reguł rozmytych**:

1. Zimno w pomieszczeniu + bardzo zimno na zewnątrz → Wysoka moc
2. Zimno w pomieszczeniu + zimno na zewnątrz → Wysoka moc
3. Zimno w pomieszczeniu + ciepło na zewnątrz → Średnia moc
4. Komfortowo w pomieszczeniu + bardzo zimno na zewnątrz → Wysoka moc
5. Komfortowo w pomieszczeniu + zimno na zewnątrz → Średnia moc
6. Komfortowo w pomieszczeniu + ciepło na zewnątrz → Niska moc
7. Ciepło w pomieszczeniu → Niska moc
8. Niska wilgotność → Można grzać mocniej
9. Wysoka wilgotność + komfort → Nie przegrzewać

### Funkcje przynależności

Każda zmienna wejściowa i wyjściowa posiada zdefiniowane funkcje przynależności (trójkątne), które reprezentują rozmyte zbiory językowe:

- **Temperatura pomieszczenia:** zimno, komfort, ciepło
- **Temperatura zewnętrzna:** bardzo_zimno, zimno, ciepło
- **Wilgotność:** niska, umiarkowana, wysoka
- **Moc grzania (wyjście):** niska, średnia, wysoka

## 📁 Struktura projektu

```
fuzzy-heating-controller/
├── fuzzy_heating.py       # Główny plik z całą implementacją
├── README.md              # Ten plik - dokumentacja projektu
└── requirements.txt       # Lista wszystkich zależności
```

## 📝 Dokumentacja kodu

Kod zawiera:
- **Pełną dokumentację** na początku pliku (opis problemu, autorzy, instrukcja)
- **Bardzo szczegółowe komentarze** do każdego kroku (8 sekcji logiczne)
- **Docstringi** dla każdej funkcji wyjaśniające jej działanie
- **Nazwy zmiennych** zgodne z konwencją PEP 8
- **Formatowanie** ułatwiające czytanie i zrozumienie kodu

Każdy element kodu ma wyjaśnienie, dzięki czemu łatwo zrozumieć:
- Dlaczego tę zmienną tworzymy
- Jaki jest jej zakres i jednostka
- Jak funkcjonuje logika rozmyta
- Jak działają poszczególne reguły
- Jak obliczany jest wynik

## 🔧 Rozbudowa projektu

- Integracja z czujnikami IoT (Raspberry Pi, Arduino, ESP32)
- Interfejs graficzny (GUI) do monitorowania w czasie rzeczywistym
- Logowanie danych historycznych i analiza zużycia energii
- Optymalizacja reguł rozmytych na podstawie preferencji użytkownika
- Uczenie maszynowe do polepszenia decyzji systemu
- Zdalny dostęp przez aplikację mobilną
- Dodanie kolejnych wejść (pora dnia, obecność osób, przewidywana pogoda)

---

**Projekt realizowany w ramach przedmiotu:
Narzędzia sztucznej inteligencji**

Data utworzenia: Październik 2025