import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from database import get_connection


# =========================================================
# LOAD DATASET
# =========================================================

try:
    data = pd.read_csv("dataset.csv")

except Exception as e:
    print("Error loading dataset:", e)
    data = None


# =========================================================
# TRAIN MACHINE LEARNING MODEL
# =========================================================

symptoms = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "vomiting",
    "diarrhea",
    "body_pain",
    "sore_throat",
    "breathing_difficulty"
]

model = None

if data is not None:

    X = data[symptoms]
    y = data["disease"]

    model = DecisionTreeClassifier(
        random_state=42
    )

    model.fit(X, y)


# =========================================================
# OPEN PREDICTION WINDOW
# =========================================================

def open_prediction_window():

    if model is None:
        messagebox.showerror(
            "Error",
            "Dataset could not be loaded."
        )
        return

    window = tk.Toplevel()

    window.title("Disease Prediction")

    window.geometry("700x650")

    window.resizable(False, False)


    # =====================================================
    # TITLE
    # =====================================================

    title = tk.Label(
        window,
        text="Disease Prediction",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)


    subtitle = tk.Label(
        window,
        text="Select the symptoms reported by the patient",
        font=("Arial", 12)
    )

    subtitle.pack(pady=5)


    # =====================================================
    # PATIENT SELECTION
    # =====================================================

    patient_frame = tk.Frame(window)

    patient_frame.pack(pady=15)


    tk.Label(
        patient_frame,
        text="Select Patient:",
        font=("Arial", 12, "bold")
    ).grid(
        row=0,
        column=0,
        padx=10
    )


    patient_combo = ttk.Combobox(
        patient_frame,
        width=35,
        state="readonly"
    )

    patient_combo.grid(
        row=0,
        column=1,
        padx=10
    )


    # =====================================================
    # LOAD PATIENTS FROM MYSQL
    # =====================================================

    patient_data = []

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT patient_id, name FROM patients ORDER BY patient_id"
        )

        patient_data = cursor.fetchall()

        cursor.close()
        connection.close()


        patient_list = []

        for patient in patient_data:

            patient_id = patient[0]
            patient_name = patient[1]

            patient_list.append(
                f"{patient_id} - {patient_name}"
            )

        patient_combo["values"] = patient_list


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


    # =====================================================
    # SYMPTOMS
    # =====================================================

    symptoms_frame = tk.LabelFrame(
        window,
        text="Symptoms",
        font=("Arial", 13, "bold"),
        padx=20,
        pady=15
    )

    symptoms_frame.pack(
        padx=30,
        pady=15,
        fill="x"
    )


    symptom_vars = {}


    for index, symptom in enumerate(symptoms):

        var = tk.IntVar(value=0)

        symptom_vars[symptom] = var

        checkbox = tk.Checkbutton(
            symptoms_frame,
            text=symptom.replace("_", " ").title(),
            variable=var,
            font=("Arial", 11)
        )

        row = index // 2
        column = index % 2

        checkbox.grid(
            row=row,
            column=column,
            sticky="w",
            padx=25,
            pady=8
        )


    # =====================================================
    # RESULT
    # =====================================================

    result_label = tk.Label(
        window,
        text="",
        font=("Arial", 18, "bold")
    )

    result_label.pack(pady=20)


    # =====================================================
    # PREDICT FUNCTION
    # =====================================================

    def predict_disease():

        # -----------------------------------------------
        # Check patient
        # -----------------------------------------------

        selected_patient = patient_combo.get()

        if selected_patient == "":

            messagebox.showwarning(
                "Select Patient",
                "Please select a patient first."
            )

            return


        # -----------------------------------------------
        # Get patient ID
        # -----------------------------------------------

        patient_id = int(
            selected_patient.split(" - ")[0]
        )


        # -----------------------------------------------
        # Get selected symptoms
        # -----------------------------------------------

        selected_symptoms = []

        input_values = []


        for symptom in symptoms:

            value = symptom_vars[symptom].get()

            input_values.append(value)

            if value == 1:
                selected_symptoms.append(
                    symptom.replace("_", " ")
                )


        # -----------------------------------------------
        # Check symptom selection
        # -----------------------------------------------

        if len(selected_symptoms) == 0:

            messagebox.showwarning(
                "Select Symptoms",
                "Please select at least one symptom."
            )

            return


        # -----------------------------------------------
        # ML Prediction
        # -----------------------------------------------

        prediction = model.predict(
            [input_values]
        )

        disease = prediction[0]


        # -----------------------------------------------
        # Display result
        # -----------------------------------------------

        result_label.config(
            text=f"Predicted Disease: {disease}"
        )


        # -----------------------------------------------
        # Symptoms as text
        # -----------------------------------------------

        symptoms_text = ", ".join(
            selected_symptoms
        )


        # -----------------------------------------------
        # Save prediction to MySQL
        # -----------------------------------------------

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO predictions
            (
                patient_id,
                symptoms,
                predicted_disease
            )
            VALUES (%s, %s, %s)
            """

            values = (
                patient_id,
                symptoms_text,
                disease
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            cursor.close()
            connection.close()


            messagebox.showinfo(
                "Prediction Saved",
                f"Prediction: {disease}\n\n"
                "Prediction has been saved successfully."
            )


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # =====================================================
    # BUTTONS
    # =====================================================

    button_frame = tk.Frame(window)

    button_frame.pack(pady=10)


    predict_button = tk.Button(
        button_frame,
        text="🩺 Predict Disease",
        command=predict_disease,
        width=22,
        font=("Arial", 12, "bold"),
        bg="#1976D2",
        fg="white"
    )

    predict_button.grid(
        row=0,
        column=0,
        padx=10
    )


    clear_button = tk.Button(
        button_frame,
        text="Clear Symptoms",
        command=lambda: clear_symptoms(),
        width=18,
        font=("Arial", 11)
    )

    clear_button.grid(
        row=0,
        column=1,
        padx=10
    )


    # =====================================================
    # CLEAR FUNCTION
    # =====================================================

    def clear_symptoms():

        for symptom in symptoms:

            symptom_vars[symptom].set(0)

        result_label.config(
            text=""
        )


    # =====================================================
    # DISCLAIMER
    # =====================================================

    disclaimer = tk.Label(
        window,
        text=(
            "Note: This is an educational project and the "
            "prediction is not a medical diagnosis."
        ),
        font=("Arial", 9),
        fg="gray"
    )

    disclaimer.pack(
        side="bottom",
        pady=15
    )