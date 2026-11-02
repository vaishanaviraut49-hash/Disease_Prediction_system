import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import get_connection
import csv


def open_report_window(parent=None):

    if parent is None:
        window = tk.Tk()
    else:
        window = tk.Toplevel(parent)

    window.title("Disease Prediction - Report")
    window.geometry("1100x650")
    window.configure(bg="#F0F4F8")

    # TITLE
    tk.Label(
        window,
        text="DISEASE PREDICTION REPORT",
        font=("Arial", 22, "bold"),
        bg="#F0F4F8",
        fg="#17365D"
    ).pack(pady=15)

    # TOTAL PREDICTIONS
    total_label = tk.Label(
        window,
        text="Total Predictions: 0",
        font=("Arial", 15, "bold"),
        bg="#D9EAF7",
        fg="#17365D"
    )
    total_label.pack(pady=10)

    # DISEASE SUMMARY
    summary_frame = tk.LabelFrame(
        window,
        text="Disease-wise Summary",
        font=("Arial", 12, "bold"),
        bg="#F0F4F8"
    )
    summary_frame.pack(fill="x", padx=15, pady=10)

    summary_tree = ttk.Treeview(
        summary_frame,
        columns=("Disease", "Count"),
        show="headings",
        height=4
    )

    summary_tree.heading("Disease", text="Predicted Disease")
    summary_tree.heading("Count", text="Total Cases")

    summary_tree.column("Disease", width=350)
    summary_tree.column("Count", width=150)

    summary_tree.pack(fill="x", padx=5, pady=5)

    # PATIENT REPORT
    report_frame = tk.LabelFrame(
        window,
        text="Patient Prediction Records",
        font=("Arial", 12, "bold"),
        bg="#F0F4F8"
    )
    report_frame.pack(fill="both", expand=True, padx=15, pady=10)

    columns = (
        "ID",
        "Patient Name",
        "Symptoms",
        "Predicted Disease",
        "Prediction Date"
    )

    report_tree = ttk.Treeview(
        report_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        report_tree.heading(column, text=column)

    report_tree.column("ID", width=50, anchor="center")
    report_tree.column("Patient Name", width=140)
    report_tree.column("Symptoms", width=300)
    report_tree.column("Predicted Disease", width=180)
    report_tree.column("Prediction Date", width=180)

    scrollbar = ttk.Scrollbar(
        report_frame,
        orient="vertical",
        command=report_tree.yview
    )

    report_tree.configure(yscrollcommand=scrollbar.set)

    report_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # LOAD REPORT
    def load_report():

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM predictions"
            )
            total = cursor.fetchone()[0]

            total_label.config(
                text=f"Total Predictions: {total}"
            )

            for item in summary_tree.get_children():
                summary_tree.delete(item)

            cursor.execute("""
                SELECT predicted_disease, COUNT(*)
                FROM predictions
                GROUP BY predicted_disease
                ORDER BY predicted_disease
            """)

            for disease, count in cursor.fetchall():
                summary_tree.insert(
                    "",
                    "end",
                    values=(disease, count)
                )

            for item in report_tree.get_children():
                report_tree.delete(item)

            cursor.execute("""
                SELECT
                    p.patient_id,
                    p.name,
                    pr.symptoms,
                    pr.predicted_disease,
                    pr.prediction_date
                FROM patients AS p
                INNER JOIN predictions AS pr
                    ON p.patient_id = pr.patient_id
                ORDER BY pr.prediction_date DESC
            """)

            records = cursor.fetchall()

            for record in records:
                report_tree.insert(
                    "",
                    "end",
                    values=record
                )

        except Exception as error:
            messagebox.showerror(
                "Report Error",
                str(error),
                parent=window
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

    # EXPORT CSV
    def export_report():

        records = [
            report_tree.item(item, "values")
            for item in report_tree.get_children()
        ]

        if not records:
            messagebox.showwarning(
                "No Data",
                "No patient records available to export.",
                parent=window
            )
            return

        file_path = filedialog.asksaveasfilename(
            parent=window,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="Disease_Prediction_Report.csv"
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(records)

            messagebox.showinfo(
                "Success",
                "Report exported successfully!",
                parent=window
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                str(error),
                parent=window
            )

    # BUTTONS
    button_frame = tk.Frame(window, bg="#F0F4F8")
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Refresh Report",
        command=load_report,
        bg="#198754",
        fg="white",
        width=16
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Export CSV",
        command=export_report,
        bg="#0D6EFD",
        fg="white",
        width=16
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Close",
        command=window.destroy,
        bg="#DC3545",
        fg="white",
        width=12
    ).pack(side="left", padx=10)

    load_report()

    if parent is None:
        window.mainloop()


if __name__ == "__main__":
    open_report_window()