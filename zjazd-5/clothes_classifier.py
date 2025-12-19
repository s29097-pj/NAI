# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za predykcje klasy na podstawie obrazu

# Opis problemu:
# Na podstawie zbioru 60000 zdjęć ciuchów, próbujemy przewidzieć rodzaj ubrania na podstawie jego obrazu

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# Zalando fashion mnist zawierające 10 klas: "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa w pełni połączona z pakietu tensorflow

# Uruchomienie:
# python clothes_classifier.py images/shoe.png

import argparse
import tensorflow as tf
from PIL import Image
import numpy as np
import os

def convert_to_negative(image_array: np.ndarray) -> np.ndarray:
    return 255 - image_array


def preprocess_image(image_path: str) -> np.ndarray:
    img = Image.open(image_path).convert("L")
    img = img.resize((28, 28))  # Resize to match training data

    img_array = np.array(img).astype("float32")
    img_array = convert_to_negative(img_array)  # Convert to negative

    img_array /= 255.0

    img_array = img_array.reshape(1, 28, 28, 1)
    return img_array


def validate_files(image_path: str) -> None:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not os.path.exists("clothes_model.keras"):
        raise FileNotFoundError("Clothes model file not found: clothes_model.keras")

def main():
    parser = argparse.ArgumentParser(description="Predict clothing class from image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()

    validate_files(args.image_path)
    clothes_model = tf.keras.models.load_model("clothes_model.keras")
    processed_image = preprocess_image(args.image_path)
    clothes_input = processed_image.squeeze(-1)
    clothes_prediction = clothes_model.predict(clothes_input)

    class_names = [
        "T-shirt/top",
        "Trouser",
        "Pullover",
        "Dress",
        "Coat",
        "Sandal",
        "Shirt",
        "Sneaker",
        "Bag",
        "Ankle boot",
    ]

    cloth_class = class_names[int(np.argmax(clothes_prediction))]

    print(f"Image path: {args.image_path}")
    print(f"Cloth model prediction: {cloth_class}")

if __name__ == "__main__":
    main()
