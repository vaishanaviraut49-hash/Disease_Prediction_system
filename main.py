
import tkinter as tk
from tkinter import messagebox
from database import get_connection
from datetime import datetime
from Disease_prediction import open_prediction_window
from History import open_history_window
from analytics import open_reports_window

# =========================================================
# SETTINGS
# =========================================================

root = tk.Tk()
root.title("Disease Prediction System")
root.geometry("1100x700")
root.minsize(900, 600)

# Base font size
FONT_SIZE = 12


# =========================================================
# THEME
# =========================================================

themes = {
    "Blue": {
        "bg": "#EAF4FF",
        "header": "#1976D2",
        "nav": "#FFFFFF",
        "card": "#FFFFFF",
        "text": "#172B4D",
        "button": "#1976D2",
        "button_text": "#FFFFFF",
        "accent": "#42A5F5"
    },

    "Green": {
        "bg": "#EAF7F0",
        "header": "#198754",
        "nav": "#FFFFFF",
        "card": "#FFFFFF",
        "text": "#18392B",
        "button": "#198754",
        "button_text": "#FFFFFF",
        "accent": "#43A047"
    },

    "Purple": {
        "bg": "#F3EEFF",
        "header": "#673AB7",
        "nav": "#FFFFFF",
        "card": "#FFFFFF",
        "text": "#30204D",
        "button": "#673AB7",
        "button_text": "#FFFFFF",
        "accent": "#9575CD"
    }
}

current_theme = "Blue"


# =========================================================
# FONT
# =========================================================

def get_font(size=12, bold=False):
    weight = "bold" if bold else "normal"
    return ("Arial", size, weight)


# =========================================================
# UPDATE CLOCK
# =========================================================

def update_clock():
    now = datetime.now().strftime("%d-%m-%Y   %I:%M:%S %p")
    clock_label.config(text=now)
    root.after(1000, update_clock)


# =========================================================
# CLEAR CONTENT
# =========================================================

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


# =========================================================
# APPLY THEME
# =========================================================

def apply_theme():

    colors = themes[current_theme]

    root.configure(bg=colors["bg"])
    header.configure(bg=colors["header"])
    navigation.configure(bg=colors["nav"])
    content_frame.configure(bg=colors["bg"])

    logo.config(
        bg=colors["header"],
        fg="white"
    )

    clock_label.config(
        bg=colors["header"],
        fg="white"
    )

    apply_button_colors(navigation)

    show_home()


def apply_button_colors(parent):

    colors = themes[current_theme]

    for widget in parent.winfo_children():

        if isinstance(widget, tk.Button):
            widget.config(
                bg=colors["button"],
                fg=colors["button_text"],
                activebackground=colors["accent"],
                activeforeground="white",
                font=get_font(10, True)
            )


# =========================================================
# ZOOM FUNCTIONS
# =========================================================

def zoom_in():

    global FONT_SIZE

    if FONT_SIZE < 20:
        FONT_SIZE += 1
        show_home()


def zoom_out():

    global FONT_SIZE

    if FONT_SIZE > 9:
        FONT_SIZE -= 1
        show_home()


# =========================================================
# CODE-CREATED MEDICAL ICON
# =========================================================

def create_medical_icon(parent):

    canvas = tk.Canvas(
        parent,
        width=180,
        height=130,
        bg=themes[current_theme]["bg"],
        highlightthickness=0
    )

    canvas.pack(pady=10)

    # Circle
    canvas.create_oval(
        25, 10, 155, 140,
        outline=themes[current_theme]["button"],
        width=5
    )

    # Heart shape using lines
    canvas.create_line(
        90, 95,
        70, 70,
        55, 55,
        50, 40,
        55, 28,
        70, 25,
        90, 45,
        110, 25,
        125, 28,
        130, 40,
        125, 55,
        110, 70,
        90, 95,
        fill=themes[current_theme]["accent"],
        width=5,
        smooth=True
    )

    # Medical plus
    canvas.create_rectangle(
        82, 50, 98, 82,
        fill=themes[current_theme]["button"],
        outline=""
    )

    canvas.create_rectangle(
        70, 62, 110, 70,
        fill=themes[current_theme]["button"],
        outline=""
    )

    return canvas


# =========================================================
# HOME PAGE
# =========================================================

def show_home():

    clear_content()

    colors = themes[current_theme]

    # Welcome title
    title = tk.Label(
        content_frame,
        text="Welcome to Disease Prediction System",
        font=get_font(FONT_SIZE + 10, True),
        bg=colors["bg"],
        fg=colors["text"]
    )

    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        content_frame,
        text="Smart • Simple • Patient Friendly",
        font=get_font(FONT_SIZE, False),
        bg=colors["bg"],
        fg=colors["text"]
    )

    subtitle.pack()

    # Medical illustration
    create_medical_icon(content_frame)

    # Dashboard cards
    cards_frame = tk.Frame(
        content_frame,
        bg=colors["bg"]
    )

    cards_frame.pack(pady=5)

    create_card(
        cards_frame,
        "👤",
        "Patient Management",
        "Add and manage patients",
        0,
        0,
        show_patient
    )

    create_card(
        cards_frame,
        "🩺",
        "Disease Prediction",
        "Predict from symptoms",
        0,
        1,
        show_prediction
    )

    create_card(
        cards_frame,
        "📋",
        "Patient History",
        "View patient records",
        1,
        0,
        show_history
    )

    create_card(
        cards_frame,
        "📊",
        "Reports",
        "View reports and charts",
        1,
        1,
        show_reports
    )


# =========================================================
# DASHBOARD CARD
# =========================================================

def create_card(
        parent,
        icon,
        title,
        description,
        row,
        column,
        command):

    colors = themes[current_theme]

    card = tk.Frame(
        parent,
        width=330,
        height=120,
        bg=colors["card"],
        highlightbackground=colors["accent"],
        highlightthickness=2
    )

    card.grid(
        row=row,
        column=column,
        padx=12,
        pady=8
    )

    card.grid_propagate(False)

    icon_label = tk.Label(
        card,
        text=icon,
        font=get_font(FONT_SIZE + 8),
        bg=colors["card"]
    )

    icon_label.pack(pady=(8, 0))

    title_label = tk.Label(
        card,
        text=title,
        font=get_font(FONT_SIZE + 1, True),
        bg=colors["card"],
        fg=colors["text"]
    )

    title_label.pack()

    description_label = tk.Label(
        card,
        text=description,
        font=get_font(FONT_SIZE - 2),
        bg=colors["card"],
        fg=colors["text"]
    )

    description_label.pack()

    button = tk.Button(
        card,
        text="Open",
        command=command,
        width=10,
        bg=colors["button"],
        fg=colors["button_text"],
        activebackground=colors["accent"],
        activeforeground="white"
    )

    button.pack(pady=4)


# =========================================================
# PATIENT MANAGEMENT
# =========================================================

def show_patient():

    clear_content()

    colors = themes[current_theme]

    title = tk.Label(
        content_frame,
        text="Patient Registration",
        font=get_font(FONT_SIZE + 8, True),
        bg=colors["bg"],
        fg=colors["text"]
    )

    title.pack(pady=25)

    form = tk.Frame(
        content_frame,
        bg=colors["bg"]
    )

    form.pack()

    # Name
    tk.Label(
        form,
        text="Patient Name:",
        font=get_font(FONT_SIZE),
        bg=colors["bg"],
        fg=colors["text"]
    ).grid(row=0, column=0, padx=15, pady=12, sticky="w")

    name_entry = tk.Entry(
        form,
        width=35,
        font=get_font(FONT_SIZE)
    )

    name_entry.grid(row=0, column=1, padx=15, pady=12)

    # Age
    tk.Label(
        form,
        text="Age:",
        font=get_font(FONT_SIZE),
        bg=colors["bg"],
        fg=colors["text"]
    ).grid(row=1, column=0, padx=15, pady=12, sticky="w")

    age_entry = tk.Entry(
        form,
        width=35,
        font=get_font(FONT_SIZE)
    )

    age_entry.grid(row=1, column=1, padx=15, pady=12)

    # Gender
    tk.Label(
        form,
        text="Gender:",
        font=get_font(FONT_SIZE),
        bg=colors["bg"],
        fg=colors["text"]
    ).grid(row=2, column=0, padx=15, pady=12, sticky="w")

    gender_entry = tk.Entry(
        form,
        width=35,
        font=get_font(FONT_SIZE)
    )

    gender_entry.grid(row=2, column=1, padx=15, pady=12)

    # Phone
    tk.Label(
        form,
        text="Phone:",
        font=get_font(FONT_SIZE),
        bg=colors["bg"],
        fg=colors["text"]
    ).grid(row=3, column=0, padx=15, pady=12, sticky="w")

    phone_entry = tk.Entry(
        form,
        width=35,
        font=get_font(FONT_SIZE)
    )

    phone_entry.grid(row=3, column=1, padx=15, pady=12)

    # SAVE
    def save_patient():

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_entry.get().strip()
        phone = phone_entry.get().strip()

        if name == "" or age == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter patient name and age."
            )
            return

        try:

            age_value = int(age)

            if age_value <= 0:
                messagebox.showwarning(
                    "Invalid Age",
                    "Please enter a valid age."
                )
                return

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO patients
            (name, age, gender, phone)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                name,
                age_value,
                gender,
                phone
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Patient saved successfully!"
            )

            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)
            gender_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)

        except ValueError:

            messagebox.showerror(
                "Invalid Age",
                "Age must be a number."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    button_frame = tk.Frame(
        content_frame,
        bg=colors["bg"]
    )

    button_frame.pack(pady=25)

    tk.Button(
        button_frame,
        text="Save Patient",
        command=save_patient,
        width=18,
        bg=colors["button"],
        fg="white",
        font=get_font(FONT_SIZE, True)
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        button_frame,
        text="Back to Home",
        command=show_home,
        width=18,
        bg=colors["button"],
        fg="white",
        font=get_font(FONT_SIZE, True)
    ).grid(row=0, column=1, padx=10)


# =========================================================
# PREDICTION
# =========================================================

def show_prediction():
     open_prediction_window()

# =========================================================
# HISTORY
# =========================================================

def show_history():

    try:
        open_history_window(root)

    except Exception as e:

        messagebox.showerror(
            "History Error",
            f"Unable to open Patient History:\n{e}"
        )

# =========================================================
# REPORTS
# =========================================================

def show_reports():

    try:
        open_reports_window(root)

    except Exception as e:

        messagebox.showerror(
            "Reports Error",
            f"Unable to open Reports:\n{e}"
        )
# =========================================================
# ABOUT PROJECT
# =========================================================

def show_about():

    clear_content()

    colors = themes[current_theme]

    # Main heading
    tk.Label(
        content_frame,
        text="ABOUT DISEASE PREDICTION SYSTEM",
        font=get_font(FONT_SIZE + 10, True),
        bg=colors["bg"],
        fg=colors["text"]
    ).pack(pady=(25, 10))

    # Introduction card
    card = tk.Frame(
        content_frame,
        bg=colors["card"],
        highlightbackground=colors["accent"],
        highlightthickness=2
    )

    card.pack(padx=50, pady=10, fill="x")

    tk.Label(
        card,
        text="🩺 Disease Prediction System",
        font=get_font(FONT_SIZE + 5, True),
        bg=colors["card"],
        fg=colors["button"]
    ).pack(pady=(20, 10))

    tk.Label(
        card,
        text=(
            "Disease Prediction System is a Python-based application "
            "that uses Machine Learning to predict possible diseases "
            "based on symptoms entered by patients.\n\n"
            "It also stores patient information, maintains prediction "
            "history and provides statistical reports."
        ),
        font=get_font(FONT_SIZE),
        bg=colors["card"],
        fg=colors["text"],
        justify="center",
        wraplength=750
    ).pack(padx=20, pady=10)

    # Project objective
    tk.Label(
        content_frame,
        text="PROJECT OBJECTIVE",
        font=get_font(FONT_SIZE + 3, True),
        bg=colors["bg"],
        fg=colors["text"]
    ).pack(pady=(15, 5))

    tk.Label(
        content_frame,
        text=(
            "To provide a simple system for symptom-based disease "
            "prediction and patient record management."
        ),
        font=get_font(FONT_SIZE),
        bg=colors["bg"],
        fg=colors["text"],
        wraplength=800
    ).pack(pady=5)

    # Technologies
    tk.Label(
        content_frame,
        text="TECHNOLOGIES USED",
        font=get_font(FONT_SIZE + 3, True),
        bg=colors["bg"],
        fg=colors["text"]
    ).pack(pady=(15, 5))

    tk.Label(
        content_frame,
        text=(
            "Python  |  Tkinter  |  MySQL  |  Pandas  |  "
            "Scikit-learn  |  Matplotlib"
        ),
        font=get_font(FONT_SIZE, True),
        bg=colors["bg"],
        fg=colors["button"],
        wraplength=800
    ).pack(pady=5)

    # Features
    tk.Label(
        content_frame,
        text="KEY FEATURES",
        font=get_font(FONT_SIZE + 3, True),
        bg=colors["bg"],
        fg=colors["text"]
    ).pack(pady=(15, 5))

    features = (
        "✔ Patient Registration\n"
        "✔ Symptom-Based Disease Prediction\n"
        "✔ Patient History Management\n"
        "✔ Reports and Data Visualization\n"
        "✔ MySQL Database Connectivity"
    )

    tk.Label(
        content_frame,
        text=features,
        font=get_font(FONT_SIZE),
        bg=colors["bg"],
        fg=colors["text"],
        justify="left"
    ).pack(pady=5)

    # Disclaimer
    tk.Label(
        content_frame,
        text=(
            "Medical Disclaimer: This application is an educational "
            "project. Its predictions are not a substitute for "
            "professional medical advice or diagnosis."
        ),
        font=get_font(FONT_SIZE - 1),
        bg=colors["bg"],
        fg="#B03A2E",
        wraplength=850,
        justify="center"
    ).pack(pady=15)

    # Back button
    tk.Button(
        content_frame,
        text="Back to Home",
        command=show_home,
        width=20,
        bg=colors["button"],
        fg="white",
        font=get_font(FONT_SIZE, True)
    ).pack(pady=10)


# =========================================================
# EXIT
# =========================================================

def exit_application():

    answer = messagebox.askyesno(
        "Exit",
        "Do you want to exit the application?"
    )

    if answer:
        root.destroy()


# =========================================================
# HEADER
# =========================================================

colors = themes[current_theme]

header = tk.Frame(
    root,
    height=75,
    bg=colors["header"]
)

header.pack(
    side="top",
    fill="x"
)

header.pack_propagate(False)


logo = tk.Label(
    header,
    text="🩺  Disease Prediction System",
    font=("Arial", 20, "bold"),
    bg=colors["header"],
    fg="white"
)

logo.pack(
    side="left",
    padx=25
)


clock_label = tk.Label(
    header,
    text="",
    font=("Arial", 10, "bold"),
    bg=colors["header"],
    fg="white"
)

clock_label.pack(
    side="right",
    padx=20
)


# =========================================================
# NAVIGATION
# =========================================================

navigation = tk.Frame(
    root,
    height=55,
    bg="white",
    relief="solid",
    borderwidth=1
)

navigation.pack(
    side="top",
    fill="x"
)

navigation.pack_propagate(False)


def nav_button(text, command):

    button = tk.Button(
        navigation,
        text=text,
        command=command,
        width=11,
        bg=colors["button"],
        fg="white",
        activebackground=colors["accent"],
        activeforeground="white",
        font=("Arial", 10, "bold")
    )

    button.pack(
        side="left",
        padx=4,
        pady=9
    )

    return button


nav_button("Home", show_home)
nav_button("Patients", show_patient)
nav_button("Prediction", show_prediction)
nav_button("History", show_history)
nav_button("Reports", show_reports)
nav_button("About", show_about)


# =========================================================
# THEME BUTTON
# =========================================================

def change_theme():

    global current_theme

    if current_theme == "Blue":
        current_theme = "Green"

    elif current_theme == "Green":
        current_theme = "Purple"

    else:
        current_theme = "Blue"

    apply_theme()


tk.Button(
    navigation,
    text="🎨 Theme",
    command=change_theme,
    width=10
).pack(
    side="right",
    padx=3,
    pady=9
)


# =========================================================
# ZOOM BUTTONS
# =========================================================

tk.Button(
    navigation,
    text="🔍 +",
    command=zoom_in,
    width=6
).pack(
    side="right",
    padx=2,
    pady=9
)

tk.Button(
    navigation,
    text="🔍 −",
    command=zoom_out,
    width=6
).pack(
    side="right",
    padx=2,
    pady=9
)


# =========================================================
# EXIT BUTTON
# =========================================================

tk.Button(
    navigation,
    text="Exit",
    command=exit_application,
    width=8
).pack(
    side="right",
    padx=5,
    pady=9
)


# =========================================================
# CONTENT
# =========================================================

content_frame = tk.Frame(
    root,
    bg=colors["bg"]
)

content_frame.pack(
    fill="both",
    expand=True
)


# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    root,
    text="Disease Prediction System  |  Python + Tkinter + MySQL",
    font=("Arial", 9),
    bg=colors["header"],
    fg="white"
)

footer.pack(
    side="bottom",
    fill="x"
)


# =========================================================
# START
# =========================================================

update_clock()
show_home()

root.mainloop()