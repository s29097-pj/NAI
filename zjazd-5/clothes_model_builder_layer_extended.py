# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za tworzenie modelu i zapisanie go do pliku
# Do sieci neuronowej została dodana kolejna warstwa

# Opis problemu:
# Na podstawie zbioru 60000 zdjęć ciuchów, próbujemy przewidzieć rodzaj ubrania na podstawie jego obrazu

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# Zalando fashion mnist zawierające 10 klas: "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa pełnopołączeniowa z pakietu tensorflow

# Uruchomienie:
# python clothes_model_builder_layer_extended.py

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def main():
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    dense_model = keras.Sequential(
        [
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(256, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )

    dense_model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    dense_model.fit(train_images, train_labels, epochs=7)

    dense_model.save("clothes_model.keras")

    test_loss, test_acc = dense_model.evaluate(test_images, test_labels)
    print(f"Model Accuracy: {test_acc * 100}%")

    predictions = dense_model.predict(test_images)

    y_pred = np.argmax(predictions, axis=1)
    cm = confusion_matrix(test_labels, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    plt.figure(figsize=(10, 10))
    disp.plot()
    plt.title("Dense (Fully Connected) Neural Network - Confusion Matrix")
    plt.savefig("clothes_confusion_matrix.png")
    plt.close()


if __name__ == "__main__":
    main()
