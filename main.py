from tkinter import *
from datetime import date, datetime, timedelta
from tkinter import messagebox

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
            if birth_date > today:
                messagebox.showerror("Invalid Date", "Birth date cannot be in the future!")
                return
        except ValueError as e:
            messagebox.showerror("Invalid Date", str(e))
            return

        # Basic Age
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Months and Days
        months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        if today.day < birth_date.day:
            months -= 1
            # Calculate days in previous month
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days_in_prev = (date(today.year, today.month, 1) - timedelta(days=1)).day
            days = days_in_prev - birth_date.day + today.day
        else:
            days = today.day - birth_date.day
        months %= 12

        # Next Birthday
        next_bday = date(today.year, birth_month, birth_day)
        if next_bday < today:
            next_bday = date(today.year + 1, birth_month, birth_day)
        days_to_bday = (next_bday - today).days

        # Detailed Stats
        delta = today - birth_date
        total_days = delta.days
        total_hours = total_days * 24
        total_minutes = total_hours * 60
        total_seconds = total_minutes * 60
        
        # Fun Stats (Estimates)
        heartbeats = total_minutes * 72 # Avg 72 bpm
        breaths = total_minutes * 16    # Avg 16 bpm

        # Update UI Variables
        result_var.set(f"Hello, {name}!")
        zodiac_var.set(f"Zodiac: {get_zodiac(birth_month, birth_day)}")
        age_var.set(f"{age_years} Years, {months} Months, {days} Days")
        
        if days_to_bday == 0:
            next_bday_var.set("🎉 HAPPY BIRTHDAY! 🎉")
        else:
            next_bday_var.set(f"Next Birthday in: {days_to_bday} Days")

        days_var.set(f"{total_days:,} Days")
        hours_var.set(f"{total_hours:,} Hours")
        heart_var.set(f"{heartbeats:,} Heartbeats")
        breath_var.set(f"{breaths:,} Breaths")

        # Show result frame
        result_frame.pack(pady=20, fill="x", padx=25)
        
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numbers for date fields")

def reset_entries():
    name_entry.delete(0, END)
    year_entry.delete(0, END)
    month_entry.delete(0, END)
    day_entry.delete(0, END)
    result_frame.pack_forget()
    name_entry.focus()

# --- UI Setup ---

root = Tk()
root.title("Premium Age Pro")

# Window Geometry
window_width, window_height = 500, 920
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# Modern Dark Theme Palette
bg_dark = "#0f172a"        # Deep Slate
card_bg = "#1e293b"        # Lighter Slate
accent_blue = "#38bdf8"    # Sky Blue
accent_cyan = "#22d3ee"    # Cyan
text_main = "#f8fafc"      # Near White
text_dim = "#94a3b8"       # Muted Slate
btn_primary = "#0284c7"    # Ocean Blue
btn_hover = "#0369a1"      # Darker Ocean

root.configure(bg=bg_dark)

# --- Components ---

def on_enter(e):
    e.widget['background'] = btn_hover

def on_leave(e):
    if "Reset" in e.widget['text']:
        e.widget['background'] = "#ef4444"
    else:
        e.widget['background'] = btn_primary

# Variables
result_var = StringVar()
zodiac_var = StringVar()
age_var = StringVar()
next_bday_var = StringVar()
days_var = StringVar()
hours_var = StringVar()
heart_var = StringVar()
breath_var = StringVar()

# Header
header_frame = Frame(root, bg=bg_dark)
header_frame.pack(pady=(30, 10))

Label(header_frame, text="AGE CALCULATOR", font=("Segoe UI", 28, "bold"), 
      fg=accent_blue, bg=bg_dark).pack()
Label(header_frame, text="Advanced Life Analytics & Insights", font=("Segoe UI", 11), 
      fg=text_dim, bg=bg_dark).pack()

# Input Card
input_card = Frame(root, bg=card_bg, padx=25, pady=25, highlightthickness=1, highlightbackground="#334155")
input_card.pack(pady=10, padx=25, fill="x")

def create_input_row(label, row):
    Label(input_card, text=label, font=("Segoe UI", 10, "bold"), 
          fg=text_dim, bg=card_bg).grid(row=row, column=0, sticky="w", pady=10)
    entry = Entry(input_card, font=("Segoe UI", 12), bg="#0f172a", fg="white", 
                  insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#475569")
    entry.grid(row=row, column=1, sticky="ew", padx=(15, 0), ipady=5)
    return entry

input_card.columnconfigure(1, weight=1)
name_entry = create_input_row("NAME", 0)
year_entry = create_input_row("BIRTH YEAR", 1)
month_entry = create_input_row("MONTH (1-12)", 2)
day_entry = create_input_row("DAY (1-31)", 3)

# Buttons
btn_frame = Frame(root, bg=bg_dark)
btn_frame.pack(pady=20)

calc_btn = Button(btn_frame, text="Calculate My Age", font=("Segoe UI", 12, "bold"), 
                  bg=btn_primary, fg="white", bd=0, cursor="hand2",
                  padx=30, pady=12, command=calculate_age)
calc_btn.pack(side=LEFT, padx=10)
calc_btn.bind("<Enter>", on_enter)
calc_btn.bind("<Leave>", on_leave)

reset_btn = Button(btn_frame, text="Reset", font=("Segoe UI", 11), 
                   bg="#ef4444", fg="white", bd=0, cursor="hand2",
                   padx=20, pady=12, command=reset_entries)
reset_btn.pack(side=LEFT, padx=10)
reset_btn.bind("<Enter>", lambda e: e.widget.config(bg="#dc2626"))
reset_btn.bind("<Leave>", lambda e: e.widget.config(bg="#ef4444"))

# Result Card (Hidden initially)
result_frame = Frame(root, bg=card_bg, padx=20, pady=20, highlightthickness=1, highlightbackground=accent_blue)

Label(result_frame, textvariable=result_var, font=("Segoe UI", 18, "bold"), 
      bg=card_bg, fg=accent_cyan).pack()
Label(result_frame, textvariable=zodiac_var, font=("Segoe UI", 11, "bold"), 
      bg=card_bg, fg=text_dim).pack(pady=(0, 10))

# Age Badge
age_label = Label(result_frame, textvariable=age_var, font=("Segoe UI", 16), 
                  bg="#0f172a", fg="white", padx=15, pady=10)
age_label.pack(fill="x", pady=5)

Label(result_frame, textvariable=next_bday_var, font=("Segoe UI", 11, "italic"), 
      bg=card_bg, fg=accent_blue).pack(pady=10)

# Stats Grid
stats_frame = Frame(result_frame, bg=card_bg)
stats_frame.pack(fill="x", pady=10)
stats_frame.columnconfigure((0, 1), weight=1)

def add_stat(label, var, row, col):
    f = Frame(stats_frame, bg=card_bg, pady=5)
    f.grid(row=row, column=col, sticky="nsew")
    Label(f, text=label, font=("Segoe UI", 9, "bold"), fg=text_dim, bg=card_bg).pack()
    Label(f, textvariable=var, font=("Segoe UI", 11), fg="white", bg=card_bg).pack()

add_stat("TOTAL DAYS", days_var, 0, 0)
add_stat("TOTAL HOURS", hours_var, 0, 1)
add_stat("EST. HEARTBEATS", heart_var, 1, 0)
add_stat("EST. BREATHS", breath_var, 1, 1)

name_entry.focus()
root.mainloop()
