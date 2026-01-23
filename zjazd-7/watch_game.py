"""
MODUŁ: watch_game.py (Podgląd na żywo)
ZADANIE: Odtwarzanie działania wytrenowanego agenta RL w środowisku graficznym.

OPIS:
    Skrypt ładuje zapisany model (plik .zip) z dysku i uruchamia symulację
    w trybie renderowania 'human' (okienkowym). Pozwala to na wizualną
    ocenę jakości wytrenowanej polityki.

AUTORZY: Michał Małolepszy (s29097), Aleksander Bastek (s27454)

WYMAGANIA:
    - W tym samym folderze musi znajdować się plik 'ppo_lunar_lander.zip'
      (wygenerowany przez skrypt lunar_lander.py).

INSTRUKCJA:
    Uruchom ten skrypt, aby zobaczyć agenta w akcji.
"""

import gymnasium as gym
from stable_baselines3 import PPO
import time
import os


def watch():
    """
    Główna pętla wizualizacji.

    1. Sprawdza istnienie pliku modelu.
    2. Ładuje model PPO.
    3. Uruchamia środowisko LunarLander-v3 w trybie graficznym.
    4. Wyświetla grę w pętli nieskończonej, pauzując po udanym lądowaniu.
    """

    model_path = "ppo_lunar_lander"
    full_path = f"{model_path}.zip"

    # Sprawdzenie czy model istnieje
    if not os.path.exists(full_path):
        print(f"BŁĄD: Nie znaleziono pliku '{full_path}'.")
        print("Najpierw uruchom 'lunar_lander.py', aby wytrenować model!")
        return

    print(f"--- Wczytywanie modelu z pliku: {full_path} ---")
    model = PPO.load(model_path)
    print("Model wczytany pomyślnie!")

    # Inicjalizacja środowiska w trybie "human" (wyświetlanie okna)
    env = gym.make("LunarLander-v3", render_mode="human")

    obs, _ = env.reset()

    print("\n--- ROZPOCZYNAM POKAZ NA ŻYWO ---")
    print("Naciśnij 'Stop' w PyCharm lub zamknij okno gry, aby zakończyć.\n")

    try:
        while True:
            # Model przewiduje akcję (deterministic=True oznacza brak losowości, czysta wiedza)
            action, _ = model.predict(obs, deterministic=True)

            # Wykonanie kroku w symulacji
            obs, reward, terminated, truncated, info = env.step(action)

            # Sprawdzenie warunków końca epizodu
            if terminated or truncated:
                if terminated:
                    print(">>> SUKCES! WYLĄDOWAŁ! (Pauza 2s dla efektu) <<<")
                    # Pauza, żeby nacieszyć oko statkiem stojącym na ziemi
                    time.sleep(2.0)
                else:
                    print("Koniec czasu lub ucieczka poza mapę - Reset.")

                obs, _ = env.reset()

    except KeyboardInterrupt:
        print("\n--- Pokaz zakończony przez użytkownika ---")
    finally:
        env.close()


if __name__ == "__main__":
    watch()