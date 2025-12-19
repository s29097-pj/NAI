# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za predykcje klasy na podstawie obrazu

# Opis problemu:
# Na podstawie zdjęć z projektu cifar próbujemy przewidzieć klasę podanego obrazu

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# cifar 10 zawierające 10 klas: "airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa oparta o warstwy splotowe z pakietu tensorflow

# Uruchomienie:
# python cifar_animal_classifier.py images/horse.png

import argparse
import numpy as np
from tensorflow import keras
from PIL import Image

def load_and_prep_image(image_path):
    img = Image.open(image_path)
    img = img.resize((32, 32))
    
    img_array = np.array(img) / 255.0
    
    # Add batch dimension: (32, 32, 3) -> (1, 32, 32, 3)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def main():
    parser = argparse.ArgumentParser(description="Predict the animal in an image using a trained CIFAR-10 model.")
    parser.add_argument("image", help="Path to the image file to classify.")
    args = parser.parse_args()

    class_names = [
        "airplane", "automobile", "bird", "cat", "deer",
        "dog", "frog", "horse", "ship", "truck"
    ]

    try:
        model = keras.models.load_model("animal_model.keras")
        
        processed_image = load_and_prep_image(args.image)
        
        predictions = model.predict(processed_image)

        predicted_class_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_class_index]
        confidence = 100 * np.max(predictions[0])

        print(f"Prediction: {predicted_class}")
        print(f"Confidence: {confidence:.2f}%")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
