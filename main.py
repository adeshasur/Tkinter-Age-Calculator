import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from PIL import Image, ImageTk

# --- Logic Functions ---

def get_zodiac(month, day):
    zodiac_signs = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"),
        (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
        (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
        (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
        (12, 31, "Capricorn")
    ]
    for m, d, sign in zodiac_signs:
        if month < m or (month == m and day <= d):
            return sign
    return "Unknown"

def calculate_age():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter your name")
        return

    try:
        b_year = int(year_entry.get())
        b_month = int(month_entry.get())
        b_day = int(day_entry.get())

        today = date.today()
        birth_date = date(b_year, b_month, b_day)
        
        if birth_date > today:
            messagebox.showerror("Error", "Birth date cannot be in the future")
            return

        # Age Calculation
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Next Birthday
        next_bday = date(today.year, b_month, b_day)
        if next_bday < today:
            next_bday = date(today.year + 1, b_month, b_day)
        days_to_bday = (next_bday - today).days

        # Stats
        delta = today - birth_date
        total_days = delta.days
        heartbeats = total_days * 24 * 60 * 72 # 72 bpm
        
        # Update UI
        result_name.config(text=f"Hello, {name}!")
        result_age.config(text=f"{age_years} Years Old")
        result_zodiac.config(text=f"Zodiac: {get_zodiac(b_month, b_day)}")
        
        if days_to_bday == 0:
            result_countdown.config(text="🎉 It's your Birthday! 🎉", fg="#e11d48")
        else:
            result_countdown.config(text=f"Next birthday in {days_to_bday} days")

        stat_days.config(text=f"{total_days:,}")
        stat_hearts.config(text=f"{heartbeats:,}")

        # Reveal results
        result_container.pack(pady=20, fill="x", padx=30)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric date values")

def reset():
    name_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    month_entry.delete(0, tk.END)
    day_entry.delete(0, tk.END)
    result_container.pack_forget()
    name_entry.focus()

# --- UI Setup ---

root = tk.Tk()
root.title("Age Pro - Modern Analytics")
root.geometry("500x950")
root.configure(bg="#f8fafc") # Clean Slate BG

# Styles
style = ttk.Style()
style.theme_use('clam')
style.configure("TEntry", fieldbackground="#ffffff", borderwidth=0)

# Colors
accent = "#2563eb"     # Electric Blue
text_dark = "#1e293b"  # Deep Slate
text_light = "#64748b" # Muted Blue

# Header & Image
header_frame = tk.Frame(root, bg="#f8fafc")
header_frame.pack(pady=(40, 10))

try:
    img_orig = Image.open("Age.png")
    # Resize keeping aspect ratio
    w, h = img_orig.size
    new_w = 350
    new_h = int(h * (new_w / w))
    img_res = img_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img_res)
    img_label = tk.Label(header_frame, image=photo, bg="#f8fafc")
    img_label.image = photo
    img_label.pack()
except Exception as e:
    print(f"Image error: {e}")

tk.Label(header_frame, text="AGE CALCULATOR", font=("Inter", 24, "bold"), 
         fg=accent, bg="#f8fafc").pack(pady=(10, 0))
tk.Label(header_frame, text="Discover your life progress and insights", font=("Inter", 10), 
         fg=text_light, bg="#f8fafc").pack()

# Input Card
input_card = tk.Frame(root, bg="#ffffff", highlightthickness=1, highlightbackground="#e2e8f0", padx=30, pady=30)
input_card.pack(pady=20, padx=30, fill="x")

def add_label(text, row):
    tk.Label(input_card, text=text, font=("Inter", 9, "bold"), 
             fg=text_light, bg="#ffffff").grid(row=row, column=0, sticky="w", pady=(10, 2))

add_label("FULL NAME", 0)
name_entry = tk.Entry(input_card, font=("Inter", 12), bg="#f1f5f9", fg=text_dark, bd=0, insertbackground=accent)
name_entry.grid(row=1, column=0, sticky="ew", ipady=8)

# Date Grid
date_grid = tk.Frame(input_card, bg="#ffffff")
date_grid.grid(row=2, column=0, sticky="ew", pady=(15, 0))
date_grid.columnconfigure((0,1,2), weight=1)

tk.Label(date_grid, text="YEAR", font=("Inter", 8, "bold"), fg=text_light, bg="#ffffff").grid(row=0, column=0, sticky="w")
year_entry = tk.Entry(date_grid, font=("Inter", 11), bg="#f1f5f9", fg=text_dark, bd=0, justify="center")
year_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5), ipady=8)

tk.Label(date_grid, text="MONTH", font=("Inter", 8, "bold"), fg=text_light, bg="#ffffff").grid(row=0, column=1, sticky="w")
month_entry = tk.Entry(date_grid, font=("Inter", 11), bg="#f1f5f9", fg=text_dark, bd=0, justify="center")
month_entry.grid(row=1, column=1, sticky="ew", padx=5, ipady=8)

tk.Label(date_grid, text="DAY", font=("Inter", 8, "bold"), fg=text_light, bg="#ffffff").grid(row=0, column=2, sticky="w")
day_entry = tk.Entry(date_grid, font=("Inter", 11), bg="#f1f5f9", fg=text_dark, bd=0, justify="center")
day_entry.grid(row=1, column=2, sticky="ew", padx=(5, 0), ipady=8)

# Buttons
btn_frame = tk.Frame(root, bg="#f8fafc")
btn_frame.pack(pady=10)

calc_btn = tk.Button(btn_frame, text="Analyze My Life", font=("Inter", 12, "bold"), 
                     bg=accent, fg="white", bd=0, cursor="hand2", padx=40, pady=12,
                     command=calculate_age)
calc_btn.pack(side="left", padx=10)

tk.Button(btn_frame, text="Reset", font=("Inter", 10), bg="#e2e8f0", fg=text_dark, 
          bd=0, cursor="hand2", padx=20, pady=12, command=reset).pack(side="left", padx=10)

# Result Container (Hidden)
result_container = tk.Frame(root, bg="#ffffff", highlightthickness=2, highlightbackground=accent, padx=25, pady=25)

result_name = tk.Label(result_container, text="", font=("Inter", 16, "bold"), fg=text_dark, bg="#ffffff")
result_name.pack()
result_age = tk.Label(result_container, text="", font=("Inter", 24, "bold"), fg=accent, bg="#ffffff")
result_age.pack(pady=5)
result_zodiac = tk.Label(result_container, text="", font=("Inter", 10, "bold"), fg=text_light, bg="#ffffff")
result_zodiac.pack()
result_countdown = tk.Label(result_container, text="", font=("Inter", 10, "italic"), fg=accent, bg="#ffffff")
result_countdown.pack(pady=(10, 0))

# Stats Row
stats_row = tk.Frame(result_container, bg="#ffffff")
stats_row.pack(fill="x", pady=(20, 0))
stats_row.columnconfigure((0,1), weight=1)

def add_stat_box(label, row, col):
    box = tk.Frame(stats_row, bg="#f8fafc", padx=10, pady=10)
    box.grid(row=row, column=col, sticky="ew", padx=5)
    tk.Label(box, text=label, font=("Inter", 8, "bold"), fg=text_light, bg="#f8fafc").pack()
    val_label = tk.Label(box, text="", font=("Inter", 11, "bold"), fg=text_dark, bg="#f8fafc")
    val_label.pack()
    return val_label

stat_days = add_stat_box("TOTAL DAYS", 0, 0)
stat_hearts = add_stat_box("HEARTBEATS", 0, 1)

name_entry.focus()
root.mainloop()
