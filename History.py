import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


# ==========================================
# FETCH PATIENT HISTORY FROM MYSQL
# ==========================================

def fetch_history(search_text=""):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                p.patient_id,
                p.name,
                p.age,
                p.gender,
                p.phone,
                pr.symptoms,
                pr.predicted_disease,
                pr.prediction_date
            FROM patients p
            INNER JOIN predictions pr
            ON p.patient_id = pr.patient_id
            WHERE p.name LIKE %s
            ORDER BY pr.prediction_date DESC
        """

        cursor.execute(query, (f"%{search_text}%",))

        records = cursor.fetchall()

        return records

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to fetch patient history:\n{e}"
        )
        return []

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# OPEN PATIENT HISTORY WINDOW
# ==========================================

def open_history_window(parent=None):

    if parent is None:
        parent = tk._default_root

    if parent is None:
        raise RuntimeError(
            "Please run the main application first."
        )

    history_window = tk.Toplevel(parent)

    history_window.title("Patient History")
    history_window.geometry("1150x650")
    history_window.configure(bg="#F4F7FB")

    # ======================================
    # TITLE
    # ======================================

    title = tk.Label(
        history_window,
        text="PATIENT HISTORY",
        font=("Arial", 24, "bold"),
        bg="#F4F7FB",
        fg="#17365D"
    )
    title.pack(pady=20)

    subtitle = tk.Label(
        history_window,
        text="View and manage previous disease predictions",
        font=("Arial", 11),
        bg="#F4F7FB",
        fg="#555555"
    )
    subtitle.pack(pady=2)

    # ======================================
    # SEARCH SECTION
    # ======================================

    search_frame = tk.Frame(
        history_window,
        bg="#F4F7FB"
    )
    search_frame.pack(fill="x", padx=25, pady=20)

    tk.Label(
        search_frame,
        text="Search Patient:",
        font=("Arial", 12, "bold"),
        bg="#F4F7FB"
    ).pack(side="left", padx=5)

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=("Arial", 12),
        width=30
    )
    search_entry.pack(side="left", padx=10)

    # ======================================
    # TABLE FRAME
    # ======================================

    table_frame = tk.Frame(
        history_window,
        bg="white"
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    columns = (
        "patient_id",
        "name",
        "age",
        "gender",
        "phone",
        "symptoms",
        "predicted_disease",
        "prediction_date"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "patient_id": "Patient ID",
        "name": "Patient Name",
        "age": "Age",
        "gender": "Gender",
        "phone": "Phone",
        "symptoms": "Symptoms",
        "predicted_disease": "Predicted Disease",
        "prediction_date": "Prediction Date"
    }

    widths = {
        "patient_id": 80,
        "name": 130,
        "age": 55,
        "gender": 80,
        "phone": 120,
        "symptoms": 230,
        "predicted_disease": 150,
        "prediction_date": 180
    }

    for column in columns:

        tree.heading(
            column,
            text=headings[column]
        )

        tree.column(
            column,
            width=widths[column],
            anchor="center",
            minwidth=60
        )

    # ======================================
    # SCROLLBARS
    # ======================================

    vertical_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    horizontal_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=vertical_scroll.set,
        xscrollcommand=horizontal_scroll.set
    )

    tree.grid(row=0, column=0, sticky="nsew")

    vertical_scroll.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scroll.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    # ======================================
    # LOAD HISTORY RECORDS
    # ======================================

    def load_history(search_text=""):

        for item in tree.get_children():
            tree.delete(item)

        records = fetch_history(search_text)

        for record in records:

            tree.insert(
                "",
                "end",
                values=record
            )

    # ======================================
    # SEARCH FUNCTION
    # ======================================

    def search_history():

        search_text = search_var.get().strip()

        load_history(search_text)

    # ======================================
    # REFRESH FUNCTION
    # ======================================

    def refresh_history():

        search_var.set("")
        load_history()

    # ======================================
    # BUTTON SECTION
    # ======================================

    button_frame = tk.Frame(
        history_window,
        bg="#F4F7FB"
    )

    button_frame.pack(pady=15)

    search_button = tk.Button(
        button_frame,
        text="Search",
        font=("Arial", 11, "bold"),
        bg="#2196F3",
        fg="white",
        width=12,
        command=search_history,
        cursor="hand2"
    )

    search_button.pack(side="left", padx=10)

    refresh_button = tk.Button(
        button_frame,
        text="Refresh",
        font=("Arial", 11, "bold"),
        bg="#4CAF50",
        fg="white",
        width=12,
        command=refresh_history,
        cursor="hand2"
    )

    refresh_button.pack(side="left", padx=10)

    close_button = tk.Button(
        button_frame,
        text="Close",
        font=("Arial", 11, "bold"),
        bg="#E53935",
        fg="white",
        width=12,
        command=history_window.destroy,
        cursor="hand2"
    )

    close_button.pack(side="left", padx=10)

    # Search using Enter key
    search_entry.bind(
        "<Return>",
        lambda event: search_history()
    )

    # Load all records when window opens
    load_history()

    search_entry.focus_set()