# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Opis problemu:
# Sprawdzamy różne jądra SVM wybierając te, które daje najwyższą dokładność
# Jednocześnie testujemy parametry jądra "C" i "class_weight" oraz ich wpływ na wyniki
# svm_kernel_analysis_pl.md zawiera opis analizy

import pandas as pd
from sklearn.model_selection import train_test_split
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


def train_and_evaluate(classifier, X_train, X_test, y_train, y_test):
    classifier.fit(X_train, y_train)
    predictions = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)
    return accuracy, conf_matrix

svm_kernels = ['linear', 'poly', 'rbf', 'sigmoid']

best_kernel = None
best_accuracy = 0.0
best_conf_matrix = None
best_classifier = None
kernel_results = {}

for kernel in svm_kernels:
    svm_classifier = SVC(kernel=kernel, random_state=42)
    accuracy, conf_matrix = train_and_evaluate(
        svm_classifier, X_train, X_test, y_train, y_test
    )

    kernel_results[kernel] = {
        'accuracy': accuracy,
        'conf_matrix': conf_matrix,
        'classifier': svm_classifier
    }

    print(f"\nKernel: {kernel}")
    print(f"Accuracy: {accuracy:.2f}")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_kernel = kernel
        best_conf_matrix = conf_matrix
        best_classifier = svm_classifier

print("\nBest kernel based on accuracy on the test set:")
print(f"Best kernel: {best_kernel}")
print(f"Best kernel accuracy: {best_accuracy:.2f}")

tuned_params = {
    "kernel": best_kernel,
    "C": 20,
    "class_weight": {"AB": 10, "NO": 1},
    "random_state": 42,
}

svm_best_tuned = SVC(**tuned_params)
tuned_accuracy, tuned_conf_matrix = train_and_evaluate(
    svm_best_tuned, X_train, X_test, y_train, y_test
)

print(f"\nBest kernel (tuned): {best_kernel}")
print(f"Tuned SVM accuracy: {tuned_accuracy:.2f}")
print("Tuned SVM confusion matrix:")
print(tuned_conf_matrix)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

class_labels = y.unique()

sns.heatmap(
    best_conf_matrix,
    annot=True,
    fmt='d',
    cmap='Blues',
    ax=ax1,
    xticklabels=class_labels,
    yticklabels=class_labels
)
ax1.set_title(f'Best Kernel SVM ({best_kernel}) - Default Params')
ax1.set_ylabel('True Label')
ax1.set_xlabel('Predicted Label')

sns.heatmap(
    tuned_conf_matrix,
    annot=True,
    fmt='d',
    cmap='Blues',
    ax=ax2,
    xticklabels=class_labels,
    yticklabels=class_labels
)
ax2.set_title(f'Best Kernel SVM ({best_kernel}) - Tuned Params')
ax2.set_ylabel('True Label')
ax2.set_xlabel('Predicted Label')

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(15, 15))
class_labels = y.unique()

for (kernel, results), ax in zip(kernel_results.items(), axes.ravel()):
    sns.heatmap(
        results['conf_matrix'],
        annot=True,
        fmt='d',
        cmap='Blues',
        ax=ax,
        xticklabels=class_labels,
        yticklabels=class_labels
    )
    ax.set_title(f'{kernel.capitalize()} Kernel\nAccuracy: {results["accuracy"]:.2f}')
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')

plt.tight_layout()
plt.show()
