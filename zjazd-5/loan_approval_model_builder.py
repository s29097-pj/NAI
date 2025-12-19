# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest stworzenie i zapisanie modelu

# Opis problemu:
# Na podstawie danych wejściowych o osobie zostanie przewidziane, czy zostanie przyznany kredyt

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# age,occupation_status,years_employed,annual_income,credit_score,credit_history_years,savings_assets,current_debt,defaults_on_file,delinquencies_last_2yrs,derogatory_marks,product_type,loan_intent,loan_amount,interest_rate,debt_to_income_ratio,loan_to_income_ratio,payment_to_income_ratio,loan_status

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa oparta o warstwy w pełni połączone z pakietu tensorflow

# Uruchomienie:
# python loan_approval_model_builder.py


import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

def main():
    file_path = 'loan_approval.csv'
    df = pd.read_csv(file_path)

    # 1. Select exactly which columns we want to use as features
    numerical_cols = [
        'age', 'years_employed', 'annual_income', 'credit_score', 
        'credit_history_years', 'savings_assets', 'current_debt', 
        'loan_amount', 'interest_rate', 'debt_to_income_ratio', 
        'loan_to_income_ratio', 'payment_to_income_ratio',
        'defaults_on_file', 'delinquencies_last_2yrs', 'derogatory_marks'
    ]
    
    categorical_cols = [
        'occupation_status', 'product_type', 'loan_intent'
    ]

    # 2. Preprocess Categorical data into numbers (One-Hot Encoding)
    # This creates new columns for each category (e.g., occupation_status_Employed)
    df_encoded = pd.get_dummies(df, columns=categorical_cols)

    # 3. Define X (Features) and y (Target)
    # Filter columns to only include our numerical list + the new encoded categorical columns
    feature_cols = [col for col in df_encoded.columns if col not in ['customer_id', 'loan_status']]
    X = df_encoded[feature_cols]
    y_labels = df_encoded['loan_status']

    # 4. Target Encoding: Convert 0/1 to categorical probability arrays
    y = tf.one_hot(y_labels, depth=2).numpy()

    # 5. Split and Shuffle
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 6. Scaling (Crucial for Dense layers with large values like 'annual_income')
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 7. Build Model
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.BatchNormalization(), # Stabilizes training
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(2, activation='softmax')
    ])

    model.compile(
        optimizer="adam", 
        loss="categorical_crossentropy", 
        metrics=["accuracy"]
    )

    # 8. Train
    print(f"Training on {X_train.shape[1]} features (including all encoded columns)...")
    model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1, verbose=1)

    # 9. Save and Evaluate
    model.save("loan_model.keras")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nFinal Test Accuracy: {test_acc * 100:.2f}%")

if __name__ == "__main__":
    main()
