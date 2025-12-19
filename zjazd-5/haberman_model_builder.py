# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za tworzenie modelu i zapisanie go do pliku

# Opis problemu:
# Dane dotyczą pacjentek chorych na raka piersi,
# na których przeprowadzono operacje w celu wyleczenia
# Celem jest przewidywanie, czy pacjentka przeyżyje w przeciągu 5 lat

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# Informacje o atrybutach:
#   1. Wiek pacjenta w momencie operacji (wartości liczbowe)
#   2. Rok operacji pacjenta (rok - 1900, wartości liczbowe)
#   3. Liczba dodatnich węzłów pachowych wykrytych (wartości liczbowe)
#   4. Status przeżycia (atrybut klasy)
#         1 = pacjent przeżył 5 lat lub dłużej
#         2 = pacjent zmarł w ciągu 5 lat

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa w pełni połączona z pakietu tensorflow

# Uruchomienie:
# python haberman_model_builder.py

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras

def main():
    file_path = 'haberman.data'

    df = pd.read_csv(file_path, header=None)
    df.columns = [
        'age',
        'year',
        'positive_nodes',
        'survival_status'
    ]

    shuffled_df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

    shuffled_df['survival_status'] = shuffled_df['survival_status'].map({1: 0, 2: 1})

    survival_statuses = shuffled_df['survival_status']
    X = shuffled_df.drop(columns=['survival_status'])
    y = tf.one_hot(survival_statuses, depth=2).numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = keras.Sequential(
        [
            keras.layers.Dense(3, activation=tf.nn.relu),
            keras.layers.Dense(4, activation=tf.nn.relu),
            keras.layers.Dense(2, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    model.fit(X_train, y_train, epochs=7)

    model.save("haberman_model.keras")

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Model Accuracy: {test_acc * 100}%")

if __name__ == "__main__":
    main()
