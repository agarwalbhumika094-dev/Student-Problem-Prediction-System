import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv


# =============== MAIN WINDOW ===============

root = tk.Tk()
root.title("Student Problem Prediction System")
root.geometry("650x650")
root.resizable(False, False)
root.configure(bg="#f4f6f9")


# =============== SCROLLABLE AREA ===============

canvas = tk.Canvas(root, bg="#f4f6f9", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

main_frame = tk.Frame(canvas, bg="#f4f6f9")
window_id = canvas.create_window((0, 0), window=main_frame, anchor="nw")


def update_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_frame(event):
    canvas.itemconfig(window_id, width=event.width)


main_frame.bind("<Configure>", update_scroll)
canvas.bind("<Configure>", resize_frame)


def mouse_scroll(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


canvas.bind_all("<MouseWheel>", mouse_scroll)


# =============== HEADING ===============

heading = tk.Label(
    main_frame,
    text="STUDENT PROBLEM PREDICTION SYSTEM",
    font=("Arial", 19, "bold"),
    bg="#f4f6f9",
    fg="#154360"
)
heading.pack(pady=20)


tk.Label(
    main_frame,
    text="STUDENT DETAILS",
    font=("Arial", 14, "bold"),
    bg="#f4f6f9",
    fg="#2874a6"
).pack(pady=10)


# =============== INPUT FIELDS ===============

def add_field(label):
    tk.Label(
        main_frame,
        text=label,
        font=("Arial", 11, "bold"),
        bg="#f4f6f9",
        fg="#34495e"
    ).pack(pady=(6, 2))

    entry = tk.Entry(
        main_frame,
        font=("Arial", 12),
        width=30,
        justify="center",
        relief="solid",
        bd=1
    )
    entry.pack(pady=3)

    return entry


name_entry = add_field("Student Name")

fields = [
    "Study Hours",
    "Sleep Hours",
    "Attendance (%)",
    "Previous Marks",
    "Test 1 Marks",
    "Test 2 Marks",
    "Test 3 Marks"
]

entries = [add_field(field) for field in fields]


# =============== NEWTON INTERPOLATION ===============

def newton_interpolation(x, y, value):
    n = len(x)
    table = [y.copy()]

    for j in range(1, n):
        column = []

        for i in range(n - j):
            result = (
                table[j-1][i+1] - table[j-1][i]
            ) / (x[i+j] - x[i])

            column.append(result)

        table.append(column)

    result = table[0][0]
    product = 1

    for j in range(1, n):
        product *= (value - x[j-1])
        result += table[j][0] * product

    return result


# =============== LAGRANGE INTERPOLATION ===============

def lagrange_interpolation(x, y, value):
    result = 0
    n = len(x)

    for i in range(n):
        term = y[i]

        for j in range(n):
            if i != j:
                term *= (value - x[j]) / (x[i] - x[j])

        result += term

    return result


# =============== GAUSSIAN ELIMINATION ===============

def gaussian_elimination(A, B):
    n = len(B)

    for i in range(n):
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]

            for k in range(i, n):
                A[j][k] -= factor * A[i][k]

            B[j] -= factor * B[i]

    x = [0] * n

    for i in range(n - 1, -1, -1):
        total = B[i]

        for j in range(i + 1, n):
            total -= A[i][j] * x[j]

        x[i] = total / A[i][i]

    return x


# =============== TRAPEZOIDAL RULE ===============

def trapezoidal_rule(x, y):
    n = len(x) - 1
    h = x[1] - x[0]

    result = y[0] + y[n]

    for i in range(1, n):
        result += 2 * y[i]

    return (h / 2) * result


# =============== GRAPH ===============

last_graph_data = None


def show_graph():
    if last_graph_data is None:
        messagebox.showwarning(
            "Warning",
            "Please predict first."
        )
        return

    test1, test2, test3, predicted = last_graph_data

    tests = [
        "Test 1",
        "Test 2",
        "Test 3",
        "Predicted Test 4"
    ]

    marks = [test1, test2, test3, predicted]

    plt.figure(figsize=(8, 5))
    plt.plot(tests, marks, marker="o")
    plt.title("Student Performance Prediction")
    plt.xlabel("Tests")
    plt.ylabel("Marks")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# =============== PREDICTION ===============

def predict():
    global last_graph_data

    try:
        name = name_entry.get().strip()

        study = float(entries[0].get())
        sleep = float(entries[1].get())
        attendance = float(entries[2].get())
        previous = float(entries[3].get())

        test1 = float(entries[4].get())
        test2 = float(entries[5].get())
        test3 = float(entries[6].get())

        if not name:
            messagebox.showerror("Error", "Enter student name.")
            return

        if not (0 <= study <= 24 and 0 <= sleep <= 24):
            messagebox.showerror(
                "Error",
                "Study and sleep hours must be between 0 and 24."
            )
            return

        all_marks = [
            attendance, previous, test1, test2, test3
        ]

        if any(mark < 0 or mark > 100 for mark in all_marks):
            messagebox.showerror(
                "Error",
                "Attendance and marks must be between 0 and 100."
            )
            return

        x = [1, 2, 3]
        y = [test1, test2, test3]

        # Newton Interpolation
        predicted = newton_interpolation(x, y, 4)

        # Lagrange Interpolation
        lagrange = lagrange_interpolation(x, y, 2.5)

        # Trapezoidal Rule
        trapezoidal = trapezoidal_rule(x, y)

        # Gaussian Elimination
        A = [
            [2, 7, 6],
            [4, 8, 7],
            [3, 9, 8]
        ]

        B = [54, 71, 73]

        weights = gaussian_elimination(A, B)

        score = (
            weights[0] * study
            + weights[1] * (attendance / 10)
            + weights[2] * (previous / 10)
        )

        # Problem Analysis
        problems = []

        if study < 3:
            problems.append("Low Study Hours")

        if sleep < 7:
            problems.append("Insufficient Sleep")

        if attendance < 75:
            problems.append("Low Attendance")

        if previous < 50:
            problems.append("Low Academic Marks")

        if problems:
            problem_text = "\n".join(
                "- " + problem for problem in problems
            )
        else:
            problem_text = "No major problem detected."

        last_graph_data = (
            test1, test2, test3, predicted
        )

        result = (
            f"Student: {name}\n\n"
            f"PROBLEM ANALYSIS\n"
            f"{problem_text}\n\n"
            f"NUMERICAL ANALYSIS RESULTS\n"
            f"Newton Predicted Test 4: {predicted:.2f}\n"
            f"Lagrange Estimate at Test 2.5: {lagrange:.2f}\n"
            f"Gaussian Elimination Score: {score:.2f}\n"
            f"Trapezoidal Rule Result: {trapezoidal:.2f}"
        )

        messagebox.showinfo("Prediction Result", result)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please fill all fields with valid numbers."
        )

    except ZeroDivisionError:
        messagebox.showerror(
            "Error",
            "Numerical calculation could not be completed."
        )


# =============== SAVE STUDENT RECORD ===============

def save_record():
    try:
        name = name_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Enter student name first.")
            return

        values = [entry.get().strip() for entry in entries]

        if any(value == "" for value in values):
            messagebox.showerror("Error", "Fill all fields first.")
            return

        numeric_values = [float(value) for value in values]

        with open("student_records.csv", "a", newline="") as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow([
                    "Name", "Study Hours", "Sleep Hours",
                    "Attendance", "Previous Marks",
                    "Test 1", "Test 2", "Test 3"
                ])

            writer.writerow([name] + numeric_values)

        messagebox.showinfo(
            "Success",
            "Student record saved successfully!"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers in all fields."
        )

# =============== BUTTONS ===============

button_style = {
    "font": ("Arial", 11, "bold"),
    "width": 25,
    "relief": "flat",
    "pady": 7
}

predict_button = tk.Button(
    main_frame,
    text="PREDICT STUDENT PROBLEMS",
    command=predict,
    bg="#2874a6",
    fg="white",
    **button_style
)
predict_button.pack(pady=(18, 7))

save_button = tk.Button(
    main_frame,
    text="SAVE STUDENT RECORD",
    command=save_record,
    bg="#8e44ad",
    fg="white",
    **button_style
)
save_button.pack(pady=7)

graph_button = tk.Button(
    main_frame,
    text="SHOW PERFORMANCE GRAPH",
    command=show_graph,
    bg="#148f77",
    fg="white",
    **button_style
)
graph_button.pack(pady=7)


def reset_fields():
    name_entry.delete(0, tk.END)

    for entry in entries:
        entry.delete(0, tk.END)

    global last_graph_data
    last_graph_data = None


reset_button = tk.Button(
    main_frame,
    text="RESET ALL FIELDS",
    command=reset_fields,
    bg="#7f8c8d",
    fg="white",
    **button_style
)
reset_button.pack(pady=(7, 20))


# =============== RUN APPLICATION ===============

root.mainloop()