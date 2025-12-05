# Autorzy:  Aleksander Bastek, Michał Małolepszy

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
# Do przewidywania klasy wyjściowej (status przeżycia) wykorzystaliśmy dwie metody:
#   - drzewo decyzyjne (Decision Tree)
#   - SVM (Support Vector Machine) w implementacji klasowej (SVC)

# Analiza wyników przedstawia dokładność z jaką każda z metod przewidywała klasę wyjściową
# oraz macierze pomyłek, które przedstawiają liczbę trafionych i nietrafionych przewidywań

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'haberman.data'

df = pd.read_csv(file_path, header=None)
df.columns = [
    'age',
    'year',
    'positive_nodes',
    'survival_status'
]

shuffled_df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

X = shuffled_df.drop(columns=['survival_status'])
y = shuffled_df['survival_status']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)

svm_classifier = SVC(random_state=42)
svm_classifier.fit(X_train, y_train)

dt_pred = dt_classifier.predict(X_test)
svm_pred = svm_classifier.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_pred)
svm_accuracy = accuracy_score(y_test, svm_pred)

print(f"Decision Tree Accuracy: {dt_accuracy:.2f}")
print(f"SVM Accuracy: {svm_accuracy:.2f}")

dt_cm = confusion_matrix(y_test, dt_pred)
svm_cm = confusion_matrix(y_test, svm_pred)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

class_labels = y.unique()
sns.heatmap(dt_cm, annot=True, fmt='d', cmap='Blues', ax=ax1,
            xticklabels=class_labels, yticklabels=class_labels)
ax1.set_title('Decision Tree Confusion Matrix')
ax1.set_ylabel('True Label')
ax1.set_xlabel('Predicted Label')

sns.heatmap(svm_cm, annot=True, fmt='d', cmap='Blues', ax=ax2,
            xticklabels=class_labels, yticklabels=class_labels)
ax2.set_title('SVM Confusion Matrix')
ax2.set_ylabel('True Label')
ax2.set_xlabel('Predicted Label')

plt.tight_layout()
plt.show()

print("\nEnter example Haberman patient data to get predictions.")
try:
    age = int(input("Age of patient at time of operation (years): "))
    year = int(input("Year of operation (e.g. 64 = 1964): "))
    positive_nodes = int(input("Number of positive axillary nodes detected: "))

    user_sample = pd.DataFrame(
        [[age, year, positive_nodes]],
        columns=['age', 'year', 'positive_nodes']
    )

    dt_user_pred = dt_classifier.predict(user_sample)[0]
    svm_user_pred = svm_classifier.predict(user_sample)[0]

    print("\nPredictions for the entered patient:")
    print(f"  Decision Tree predicted survival_status: {dt_user_pred}")
    print(f"  SVM predicted survival_status: {svm_user_pred}")
except Exception as e:
    print(f"Could not compute prediction due to input/processing error: {e}")
