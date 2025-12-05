# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Opis problemu:
# Dane dotyczą pacjentek chorych na raka piersi,
# na których przeprowadzono operacje w celu wyleczenia
# Celem jest przewidywanie, czy pacjentka przeyżyje w przeciągu 5 lat

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# 1. Kąt nachylenia miednicy (Pelvic Incidence)
# 2. Kąt przechylenia miednicy (Pelvic Tilt)
# 3. Krzywizna lędźwiowa (Lumbar Lordosis Angle)
# 4. Kąt nachylenia kręgu krzyżowego (Sacral Slope)
# 5. Odchylenie kątowe (Pelvic Radius)
# 6. Stopień przemieszczenia kręgu (Degree Spondylolisthesis)

# Klasy wyjściowe:
# 1. Normalny (Normal - NO)
# 2. Patologiczny (Abnormal - AB)

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

file_path = 'vertebral.dat'

df = pd.read_csv(file_path, sep=r'\s+', header=None)
df.columns = [
    'pelvic_incidence',
    'pelvic_tilt',
    'lumbar_lordosis_angle',
    'sacral_slope',
    'pelvic_radius',
    'degree_spondylolisthesis',
    'class_label'
]

shuffled_df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

X = shuffled_df.drop(columns=['class_label'])
y = shuffled_df['class_label']

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

feature_names = X.columns

print("\nEnter example vertebral measurements to get predictions.")
try:
    pelvic_incidence = float(input("pelvic_incidence: "))
    pelvic_tilt = float(input("pelvic_tilt: "))
    lumbar_lordosis_angle = float(input("lumbar_lordosis_angle: "))
    sacral_slope = float(input("sacral_slope: "))
    pelvic_radius = float(input("pelvic_radius: "))
    degree_spondylolisthesis = float(input("degree_spondylolisthesis: "))

    user_sample = pd.DataFrame(
        [[pelvic_incidence,
          pelvic_tilt,
          lumbar_lordosis_angle,
          sacral_slope,
          pelvic_radius,
          degree_spondylolisthesis]],
        columns=[
            'pelvic_incidence',
            'pelvic_tilt',
            'lumbar_lordosis_angle',
            'sacral_slope',
            'pelvic_radius',
            'degree_spondylolisthesis'
        ]
    )

    dt_user_pred = dt_classifier.predict(user_sample)[0]
    svm_user_pred = svm_classifier.predict(user_sample)[0]

    print("\nPredictions for the entered vertebral sample:")
    print(f"  Decision Tree predicted class_label: {dt_user_pred}")
    print(f"  SVM predicted class_label: {svm_user_pred}")
except Exception as e:
    print(f"Could not compute prediction due to input/processing error: {e}")
