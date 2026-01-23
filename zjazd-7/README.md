# Lunar Lander PPO Agent 🚀

**Rozwiązanie zadania z przedmiotu NAI.**

Realizacja Opcji 4: 

*Zaproponuj własne użycie algorytmu RL* (na bazie środowiska klasycznego sterowania).

## 👤 Autorzy
**Autorzy:** Michał Małolepszy (s29097), Aleksander Bastek (s27454)

## 📄 Opis Problemu
Celem projektu było stworzenie autonomicznego agenta, który nauczy się sterować lądownikiem księżycowym w środowisku o ograniczonej grawitacji.

**Zadania agenta:**
1.  Stabilizacja lotu (utrzymanie pionu).
2.  Oszczędne gospodarowanie paliwem (kary za ciągłe używanie silników).
3.  Precyzyjne lądowanie w wyznaczonej strefie (pomiędzy dwiema flagami na współrzędnych 0,0).
4.  Bezpieczne przyziemienie (prędkość bliska zeru w momencie kontaktu z gruntem).

Wybrano środowisko `LunarLander-v3` z biblioteki **Gymnasium**, ponieważ stanowi ono klasyczny problem sterowania ciągłego (*continuous control*), wymagający znacznie bardziej zaawansowanej strategii niż proste gry zręcznościowe.

## 🧠 Zastosowana Technologia
W projekcie zdecydowano się na użycie algorytmu **PPO (Proximal Policy Optimization)** zamiast popularnego DQN.

**Dlaczego PPO?**
Algorytm DQN działa na dyskretnej przestrzeni akcji i często ma problemy z płynnością ruchów w symulacjach fizycznych. PPO (algorytm typu *on-policy*) pozwala na stabilniejszą naukę zachowań wymagających precyzji, takich jak delikatne dozowanie ciągu silnika tuż nad ziemią.

**Parametry modelu:**
* **Język:** Python 3.13
* **Środowisko:** Gymnasium (LunarLander-v3)
* **Framework RL:** Stable-Baselines3
* **Polityka sieci:** MlpPolicy (Multi-Layer Perceptron)
* **Czas treningu:** 300,000 kroków symulacji (ok. 15 minut na CPU).

## 🎥 Wynik Działania
Model osiągnął pełną zbieżność (*explained_variance* > 0.9).
Agent potrafi bezpiecznie wylądować, wyłączyć silniki i ustabilizować pojazd na powierzchni.

**Plik wideo:**
W folderze `wideo_lunar` znajduje się plik `.mp4` prezentujący przykładowe lądowanie wytrenowanego agenta.

## ⚙️ Instrukcja Uruchomienia

### 1. Instalacja zależności
Upewnij się, że posiadasz Python 3.x. Zainstaluj biblioteki:
```bash
pip install gymnasium[box2d] stable-baselines3 moviepy shimmy
```
### 2. Trening i Generowanie Wideo (Główny skrypt)
Uruchomienie tego skryptu spowoduje wytrenowanie modelu od zera (300k kroków), 
zapisanie go oraz wygenerowanie pliku wideo z rezultatem.

```bash
python lunar_lander.py
```

### 3. Podgląd na żywo (Live Demo)
Aby zobaczyć, jak wytrenowany agent gra w czasie rzeczywistym (w oknie graficznym), uruchom:

```bash
python watch_game.py
```

(Wymaga wcześniejszego wytrenowania modelu i obecności pliku ppo_lunar_lander.zip)

## 📚 Referencje
1. [Gymnasium Documentation](https://gymnasium.farama.org/environments/box2d/lunar_lander/)
2. [Stable-Baselines3 Documentation](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)
3. OpenAI Gym/Box2D: Silnik fizyczny wykorzystywany do symulacji lądownika.
