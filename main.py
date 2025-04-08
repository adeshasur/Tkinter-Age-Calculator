from tkinter import *
from datetime import date, timedelta
from tkinter import messagebox

def calculate_age():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Input Error", "Please enter your name")
        return

    try:
        birth_year = int(year_entry.get())
        birth_month = int(month_entry.get())
        birth_day = int(day_entry.get())

        if not (1 <= birth_month <= 12):
            messagebox.showerror("Invalid Month", "Month should be between 1 and 12")
            return
        if not (1 <= birth_day <= 31):
            messagebox.showerror("Invalid Day", "Day should be between 1 and 31")
            return

        today = date.today()

        try:
            birth_date = date(birth_year, birth_month, birth_day)
        except ValueError as e:
            messagebox.showerror("Invalid Date", str(e))
            return

        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        delta = today - birth_date
        total_days = delta.days
        total_seconds = total_days * 86400
        total_minutes = total_seconds // 60
        total_hours = total_minutes // 60

        months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        if today.day < birth_date.day:
            months -= 1
            days = (today - (birth_date.replace(year=today.year, month=today.month) - timedelta(days=1))).days
        else:
            days = today.day - birth_date.day
        months %= 12

        result_var.set(f"Hello {name}!")
        age_var.set(f"You are {age_years} years, {months} months, and {days} days old.")
        days_var.set(f"Total days: {total_days:,}")
        hours_var.set(f"Total hours: {total_hours:,}")
        minutes_var.set(f"Total minutes: {total_minutes:,}")
        seconds_var.set(f"Total seconds: {total_seconds:,}")
        result_frame.pack(pady=10, fill="x", padx=20)

    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numbers for year, month, and day")

def reset_entries():
    name_entry.delete(0, END)
    year_entry.delete(0, END)
    month_entry.delete(0, END)
    day_entry.delete(0, END)
    result_var.set("")
    age_var.set("")
    days_var.set("")
    hours_var.set("")
    minutes_var.set("")
    seconds_var.set("")
    result_frame.pack_forget()
    name_entry.focus()

def validate_numeric_input(P):
    return P.isdigit() or P == ""

# Setup
root = Tk()
root.title("Age Calculator")
window_width, window_height = 550, 890
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# Colors
bg_color = "#f0f4f8"
accent_color = "#4a86e8"
result_bg = "#e8f0ff"

root.configure(bg=bg_color)

# Variables
result_var = StringVar()
age_var = StringVar()
days_var = StringVar()
hours_var = StringVar()
minutes_var = StringVar()
seconds_var = StringVar()
validate_numeric = root.register(validate_numeric_input)

# Header
header_frame = Frame(root, bg=bg_color)
header_frame.pack(pady=(15, 5))

Label(header_frame, text="AGE CALCULATOR", font=("Arial", 24, "bold"), fg=accent_color, bg=bg_color).pack()
Label(header_frame, text="Find out your exact age down to the second", font=("Arial", 12), bg=bg_color).pack()

# Load image
try:
    image = PhotoImage(file="Age.png")
    image_label = Label(header_frame, image=image, bg=bg_color)
    image_label.image = image  # Keep reference to prevent garbage collection
    image_label.pack(pady=10)
except Exception as e:
    print("Image load error:", e)
    Label(header_frame, text="[Age Image Missing]", font=("Arial", 12), bg="#ddd", width=40, height=5).pack(pady=10)

# Input Frame
input_frame = Frame(root, bg=bg_color)
input_frame.pack(pady=10, padx=30, fill="x")

def add_field(label_text, row):
    Label(input_frame, text=label_text, font=("Arial", 12, "bold"), bg=bg_color).grid(row=row, column=0, sticky="e", pady=8)
    entry = Entry(input_frame, font=("Arial", 12), validate="key", validatecommand=(validate_numeric, '%P'))
    entry.grid(row=row, column=1, sticky="ew", padx=10)
    return entry

input_frame.columnconfigure(1, weight=1)
name_entry = Entry(input_frame, font=("Arial", 12))
Label(input_frame, text="Name:", font=("Arial", 12, "bold"), bg=bg_color).grid(row=0, column=0, sticky="e", pady=8)
name_entry.grid(row=0, column=1, sticky="ew", padx=10)
year_entry = add_field("Year:", 1)
month_entry = add_field("Month (1-12):", 2)
day_entry = add_field("Day (1-31):", 3)

# Buttons
button_frame = Frame(root, bg=bg_color)
button_frame.pack(pady=15)
Button(button_frame, text="Calculate Age", font=("Arial", 12, "bold"), bg=accent_color, fg="white",
       padx=15, pady=8, command=calculate_age).pack(side=LEFT, padx=15)
Button(button_frame, text="Reset", font=("Arial", 12), bg="#f44336", fg="white",
       padx=15, pady=8, command=reset_entries).pack(side=RIGHT, padx=15)

# Result Frame
result_frame = Frame(root, bg=result_bg, bd=2, relief=GROOVE)
Label(result_frame, textvariable=result_var, font=("Arial", 16, "bold"), bg=result_bg, fg=accent_color).pack(pady=10)
Label(result_frame, textvariable=age_var, font=("Arial", 14), bg=result_bg).pack()
Label(result_frame, text="Your age in other units:", font=("Arial", 13, "bold"),
      bg=result_bg, fg=accent_color).pack(pady=(10, 5))
Label(result_frame, textvariable=days_var, font=("Arial", 12), bg=result_bg).pack()
Label(result_frame, textvariable=hours_var, font=("Arial", 12), bg=result_bg).pack()
Label(result_frame, textvariable=minutes_var, font=("Arial", 12), bg=result_bg).pack()
Label(result_frame, textvariable=seconds_var, font=("Arial", 12), bg=result_bg).pack(pady=(0, 10))

name_entry.focus()
root.mainloop()
