# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za tworzenie modelu i zapisanie go do pliku

# Opis problemu:
# Na podstawie zdjęć z projektu cifar próbujemy przewidzieć klasę podanego obrazu

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# cifar 10 zawierające 10 klas: "airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa oparta o warstwy splotowe z pakietu tensorflow

# Uruchomienie:
# python cifar_model_builder.py

import tensorflow as tf
from tensorflow import keras

def main():
    cifar10 = tf.keras.datasets.cifar10
    (train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    model = keras.Sequential(
        [
            keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.2),

            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.3),

            keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.4),

            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    model.fit(train_images, train_labels, epochs=10, batch_size=64, validation_split=0.1)

    model.save("animal_model.keras")

    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(f"Model Accuracy: {test_acc * 100}%")

if __name__ == "__main__":
    main()
