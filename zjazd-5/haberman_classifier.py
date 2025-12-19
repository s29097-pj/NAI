# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za uruchomienie predykcji na konkretnym przykładzie

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
# python haberman_classifier.py --age 65 --year 64 --nodes 14

import argparse
import numpy as np
from tensorflow import keras


def main():
    parser = argparse.ArgumentParser(description="Predict survival status using the trained Haberman model.")
    parser.add_argument("--age", type=int, required=True, help="Age of patient at time of operation")
    parser.add_argument("--year", type=int, required=True, help="Year of operation (e.g. 64 for 1964)")
    parser.add_argument("--nodes", type=int, required=True, help="Number of positive axillary nodes detected")

    args = parser.parse_args()

    try:
        model = keras.models.load_model("haberman_model.keras")

        input_data = np.array([[args.age, args.year, args.nodes]])

        prediction = model.predict(input_data)
        print(prediction)

        predicted_class_index = np.argmax(prediction, axis=1)[0]

        original_labels = {0: 1, 1: 2}
        final_prediction = original_labels[predicted_class_index]

        description = "patient survived 5 years or longer" if final_prediction == 1 else "patient died within 5 years"

        print(f"\nResults for input: Age={args.age}, Year={args.year}, Nodes={args.nodes}")
        print(f"Predicted survival_status: {final_prediction} ({description})")
        print(f"Confidence: {prediction[0][predicted_class_index] * 100:.2f}%")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure 'haberman_model.keras' exists in the current directory.")


if __name__ == "__main__":
    main()
