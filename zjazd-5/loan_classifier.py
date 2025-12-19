# Autorzy:  Aleksander Bastek, Michał Małolepszy

# Plik odpowiedzialny jest za predykcje, czy osobie zostanie przyznany kredyt na podstawie danych

# Opis problemu:
# Na podstawie danych wejściowych o osobie zostanie przewidziane, czy zostanie przyznany kredyt

# ---------------------------------------------------------
# Dane na, których przewidywane były rezultaty
# age,occupation_status,years_employed,annual_income,credit_score,credit_history_years,savings_assets,current_debt,defaults_on_file,delinquencies_last_2yrs,derogatory_marks,product_type,loan_intent,loan_amount,interest_rate,debt_to_income_ratio,loan_to_income_ratio,payment_to_income_ratio,loan_status

# ---------------------------------------------------------
# Metoda przewidywania:
# Sieć neuronowa oparta o warstwy w pełni połączone z pakietu tensorflow

# Uruchomienie:
# python3 loan_classifier.py --age 30 --years_employed 5.5 --annual_income 60000 --credit_score 720 --history_years 10 --savings 15000 --debt 2000 --loan_amount 5000 --interest_rate 8.5 --defaults 0 --delinquencies 0 --derogatory 0 --occupation Employed --product "Personal Loan" --intent Personal

import argparse
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import StandardScaler


def main():
    parser = argparse.ArgumentParser(description="Predict loan approval status based on applicant data.")

    # Numerical inputs
    parser.add_argument("--age", type=int, required=True)
    parser.add_argument("--years_employed", type=float, required=True)
    parser.add_argument("--annual_income", type=int, required=True)
    parser.add_argument("--credit_score", type=int, required=True)
    parser.add_argument("--history_years", type=float, required=True)
    parser.add_argument("--savings", type=int, required=True)
    parser.add_argument("--debt", type=int, required=True)
    parser.add_argument("--loan_amount", type=int, required=True)
    parser.add_argument("--interest_rate", type=float, required=True)
    parser.add_argument("--defaults", type=int, choices=[0, 1], required=True, help="0 for No, 1 for Yes")
    parser.add_argument("--delinquencies", type=int, required=True)
    parser.add_argument("--derogatory", type=int, required=True)

    parser.add_argument("--occupation", type=str, choices=['Employed', 'Self-Employed', 'Student', 'Unemployed'],
                        required=True)
    parser.add_argument("--product", type=str, choices=['Credit Card', 'Personal Loan', 'Line of Credit'],
                        required=True)
    parser.add_argument("--intent", type=str,
                        choices=['Business', 'Home Improvement', 'Education', 'Debt Consolidation', 'Medical',
                                 'Personal'], required=True)

    args = parser.parse_args()

    try:
        model = keras.models.load_model("loan_model.keras")

        df_original = pd.read_csv('loan_approval.csv').drop(columns=['customer_id', 'loan_status'])

        user_data = pd.DataFrame([{
            'age': args.age,
            'years_employed': args.years_employed,
            'annual_income': args.annual_income,
            'credit_score': args.credit_score,
            'credit_history_years': args.history_years,
            'savings_assets': args.savings,
            'current_debt': args.debt,
            'loan_amount': args.loan_amount,
            'interest_rate': args.interest_rate,
            'defaults_on_file': args.defaults,
            'delinquencies_last_2yrs': args.delinquencies,
            'derogatory_marks': args.derogatory,
            'occupation_status': args.occupation,
            'product_type': args.product,
            'loan_intent': args.intent,
            # Calculated ratios
            'debt_to_income_ratio': args.debt / max(args.annual_income, 1),
            'loan_to_income_ratio': args.loan_amount / max(args.annual_income, 1),
            'payment_to_income_ratio': (args.loan_amount / 12) / max(args.annual_income, 1)
        }])

        combined = pd.concat([df_original, user_data], ignore_index=True)
        combined_encoded = pd.get_dummies(combined, columns=['occupation_status', 'product_type', 'loan_intent'])

        user_row = combined_encoded.iloc[[-1]]

        df_encoded_orig = pd.get_dummies(df_original, columns=['occupation_status', 'product_type', 'loan_intent'])
        scaler = StandardScaler()
        scaler.fit(df_encoded_orig)

        user_scaled = scaler.transform(user_row)

        prediction = model.predict(user_scaled, verbose=0)
        result_class = np.argmax(prediction)
        confidence = prediction[0][result_class] * 100

        status = "APPROVED" if result_class == 1 else "REJECTED"

        print("-" * 30)
        print(f"LOAN STATUS: {status}")
        print(f"Confidence: {confidence:.2f}%")
        print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
