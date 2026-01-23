"""
ZADANIE: Zaproponuj własne użycie algorytmu RL (Lunar Lander).
PROBLEM: Sterowanie lądownikiem w środowisku o ograniczonej grawitacji.
         Celem jest lądowanie w strefie pomiędzy dwiema flagami (współrzędne 0,0).
         Agent otrzymuje kary za używanie silników (zużycie paliwa) i nagrody za bezpieczne przyziemienie.

AUTORZY: Michał Małolepszy (s29097), Aleksander Bastek (s27454)

INSTRUKCJA UŻYCIA:
    1. Zainstaluj wymagane biblioteki:
       pip install gymnasium[box2d] stable-baselines3 moviepy shimmy
    2. Uruchom skrypt: python rl_lunar_ppo.py
    3. Obserwuj konsolę - zobaczysz postęp treningu (ep_rew_mean rośnie).
    4. Po zakończeniu sprawdź folder 'wideo_lunar' - znajdziesz tam nagranie MP4.

REFERENCJE:
    - Środowisko: https://gymnasium.farama.org/environments/box2d/lunar_lander/
    - Algorytm PPO: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html
"""

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder
from stable_baselines3.common.evaluation import evaluate_policy
import os


def main():
    # NAZWA ŚRODOWISKA
    # LunarLander-v3 to standardowe środowisko z biblioteki Gymnasium (dawniej OpenAI Gym)
    env_id = "LunarLander-v3"

    print(f"--- Inicjalizacja środowiska: {env_id} ---")

    # Tworzymy środowisko treningowe
    # DummyVecEnv optymalizuje działanie środowiska dla biblioteki Stable-Baselines
    env = DummyVecEnv([lambda: gym.make(env_id, render_mode="rgb_array")])

    # KONFIGURACJA MODELU (ALGORYTM PPO)
    # PPO (Proximal Policy Optimization) jest znacznie stabilniejszy niż DQN w tym zadaniu.
    # MlpPolicy oznacza sieć neuronową opartą na liczbach (pozycja, prędkość, kąt), a nie na obrazie.
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        gamma=0.999  # Wysoka gamma, bo zależy nam na długoterminowym celu (lądowanie)
    )

    # TRENING
    print("\n--- Rozpoczynam trening (To potrwa kilka minut...) ---")
    # 100,000 kroków wystarczy, aby model nauczył się unosić i lądować.
    # Dla perfekcyjnego lądowania można zwiększyć do 300,000, ale na zaliczenie 100k wystarczy.
    model.learn(total_timesteps=300000)
    print("--- Trening zakończony ---\n")

    # ZAPISANIE MODELU
    model.save("ppo_lunar_lander")
    print("Model zapisano do pliku ppo_lunar_lander.zip")

    # NAGRYWANIE WIDEO
    print("--- Generowanie wideo z rezultatem ---")
    video_folder = "wideo_lunar"
    video_length = 1000  # Długość nagrania w klatkach

    # Tworzymy osobne środowisko do nagrywania
    eval_env = DummyVecEnv([lambda: gym.make(env_id, render_mode="rgb_array")])

    # Opakowujemy środowisko w rejestrator wideo
    eval_env = VecVideoRecorder(
        eval_env,
        video_folder,
        record_video_trigger=lambda x: x == 0,
        video_length=video_length,
        name_prefix="lunar-lander-agent"
    )

    obs = eval_env.reset()

    # Pętla uruchamiająca model w trybie nagrywania
    for _ in range(video_length + 1):
        # deterministic=True sprawia, że model wykonuje najlepszy znany ruch (nie eksperymentuje)
        action, _ = model.predict(obs, deterministic=True)
        obs, _, _, _ = eval_env.step(action)

    eval_env.close()
    print(f"Gotowe! Sprawdź folder '{video_folder}' i otwórz plik .mp4")


if __name__ == "__main__":
    main()