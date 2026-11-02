import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =====================================================
# FETCH REPORT DATA FROM MYSQL
# =====================================================

def fetch_report_data():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Total patients
        cursor.execute(
            "SELECT COUNT(*) FROM patients"
        )
        total_patients = cursor.fetchone()[0]

        # Total predictions
        cursor.execute(
            "SELECT COUNT(*) FROM predictions"
        )
        total_predictions = cursor.fetchone()[0]

        # Disease-wise count
        cursor.execute("""
            SELECT predicted_disease, COUNT(*)
            FROM predictions
            WHERE predicted_disease IS NOT NULL
            AND predicted_disease != ''
            GROUP BY predicted_disease
            ORDER BY COUNT(*) DESC
        """)

        disease_data = cursor.fetchall()

        # Daily prediction count
        cursor.execute("""
            SELECT DATE(prediction_date), COUNT(*)
            FROM predictions
            GROUP BY DATE(prediction_date)
            ORDER BY DATE(prediction_date)
        """)

        daily_data = cursor.fetchall()

        return (
            total_patients,
            total_predictions,
            disease_data,
            daily_data
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =====================================================
# OPEN REPORTS WINDOW
# =====================================================

def open_reports_window(parent=None):

    if parent is None:
        parent = tk._default_root

    if parent is None:
        raise RuntimeError(
            "Please run the main application first."
        )

    report_window = tk.Toplevel(parent)

    report_window.title("Reports and Analytics")
    report_window.geometry("1150x750")
    report_window.minsize(900, 600)
    report_window.configure(bg="#F4F7FB")

    # =================================================
    # TITLE
    # =================================================

    title = tk.Label(
        report_window,
        text="REPORTS & ANALYTICS",
        font=("Arial", 24, "bold"),
        bg="#F4F7FB",
        fg="#17365D"
    )

    title.pack(pady=(20, 5))

    subtitle = tk.Label(
        report_window,
        text="Disease Prediction System - Statistical Reports",
        font=("Arial", 11),
        bg="#F4F7FB",
        fg="#555555"
    )

    subtitle.pack(pady=5)

    # =================================================
    # SUMMARY CARDS
    # =================================================

    summary_frame = tk.Frame(
        report_window,
        bg="#F4F7FB"
    )

    summary_frame.pack(
        fill="x",
        padx=25,
        pady=15
    )

    def create_summary_card(parent, title_text):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#D5DFEA",
            highlightthickness=1,
            padx=25,
            pady=15
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=10
        )

        tk.Label(
            card,
            text=title_text,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#555555"
        ).pack()

        value_label = tk.Label(
            card,
            text="0",
            font=("Arial", 25, "bold"),
            bg="white",
            fg="#1976D2"
        )

        value_label.pack(pady=5)

        return value_label

    patient_count_label = create_summary_card(
        summary_frame,
        "Total Patients"
    )

    prediction_count_label = create_summary_card(
        summary_frame,
        "Total Predictions"
    )

    disease_count_label = create_summary_card(
        summary_frame,
        "Different Diseases"
    )

    # =================================================
    # CHART FRAME
    # =================================================

    chart_frame = tk.Frame(
        report_window,
        bg="#F4F7FB"
    )

    chart_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # =================================================
    # LOAD REPORTS AND DRAW CHARTS
    # =================================================

    def load_reports():

        try:

            (
                total_patients,
                total_predictions,
                disease_data,
                daily_data
            ) = fetch_report_data()

            patient_count_label.config(
                text=str(total_patients)
            )

            prediction_count_label.config(
                text=str(total_predictions)
            )

            disease_count_label.config(
                text=str(len(disease_data))
            )

            # Remove old charts
            for widget in chart_frame.winfo_children():
                widget.destroy()

            # Create chart
            figure = Figure(
                figsize=(10, 6),
                dpi=100
            )

            # Disease bar chart
            ax1 = figure.add_subplot(221)

            if disease_data:

                diseases = [
                    str(row[0]) for row in disease_data
                ]

                counts = [
                    row[1] for row in disease_data
                ]

                ax1.bar(
                    diseases,
                    counts
                )

                ax1.set_title(
                    "Disease-wise Prediction Count",
                    fontsize=11,
                    fontweight="bold"
                )

                ax1.set_xlabel("Disease")
                ax1.set_ylabel("Predictions")
                ax1.tick_params(
                    axis="x",
                    labelrotation=20,
                    labelsize=8
                )

            else:

                ax1.text(
                    0.5, 0.5,
                    "No prediction data available",
                    ha="center",
                    va="center"
                )

                ax1.set_title("Disease Distribution")

            # Disease pie chart
            ax2 = figure.add_subplot(222)

            if disease_data:

                diseases = [
                    str(row[0]) for row in disease_data
                ]

                counts = [
                    row[1] for row in disease_data
                ]

                ax2.pie(
                    counts,
                    labels=diseases,
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax2.set_title(
                    "Disease Percentage",
                    fontsize=11,
                    fontweight="bold"
                )

            else:

                ax2.text(
                    0.5, 0.5,
                    "No data available",
                    ha="center",
                    va="center"
                )

                ax2.set_title("Disease Percentage")

            # Daily prediction trend
            ax3 = figure.add_subplot(212)

            if daily_data:

                dates = [
                    str(row[0]) for row in daily_data
                ]

                counts = [
                    row[1] for row in daily_data
                ]

                ax3.plot(
                    dates,
                    counts,
                    marker="o"
                )

                ax3.set_title(
                    "Daily Prediction Trend",
                    fontsize=11,
                    fontweight="bold"
                )

                ax3.set_xlabel("Date")
                ax3.set_ylabel("Number of Predictions")

                ax3.tick_params(
                    axis="x",
                    labelrotation=25,
                    labelsize=8
                )

            else:

                ax3.text(
                    0.5, 0.5,
                    "No daily prediction data available",
                    ha="center",
                    va="center"
                )

                ax3.set_title("Daily Prediction Trend")

            figure.tight_layout(pad=3)

            # Display charts inside Tkinter
            chart_canvas = FigureCanvasTkAgg(
                figure,
                master=chart_frame
            )

            chart_canvas.draw()

            chart_canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                f"Unable to load reports:\n{e}",
                parent=report_window
            )

    # =================================================
    # BUTTON SECTION
    # =================================================

    button_frame = tk.Frame(
        report_window,
        bg="#F4F7FB"
    )

    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="Refresh Reports",
        command=load_reports,
        font=("Arial", 11, "bold"),
        bg="#1976D2",
        fg="white",
        width=18,
        cursor="hand2"
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Close",
        command=report_window.destroy,
        font=("Arial", 11, "bold"),
        bg="#E53935",
        fg="white",
        width=12,
        cursor="hand2"
    ).pack(side="left", padx=10)

    # Load reports when window opens
    load_reports()