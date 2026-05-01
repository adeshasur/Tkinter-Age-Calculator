import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk

# --- Theme Setup ---
ctk.set_appearance_mode("Dark")  # Appearance modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AgeCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - Ultra Modern")
        self.geometry("500x950")
        self.resizable(False, False)

        # Logic Vars
        self.name_var = ctk.StringVar()
        self.year_var = ctk.StringVar()
        self.month_var = ctk.StringVar()
        self.day_var = ctk.StringVar()

        self.setup_ui()

    def get_zodiac(self, month, day):
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

    def setup_ui(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(40, 20), padx=20, fill="x")

        # Age Evolution Image
        try:
            img = Image.open("Age.png")
            # Scaling
            w, h = img.size
            ratio = w / h
            new_w = 400
            new_h = int(new_w / ratio)
            self.hero_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            self.img_label = ctk.CTkLabel(self.header_frame, image=self.hero_image, text="")
            self.img_label.pack()
        except Exception as e:
            print(f"Image load error: {e}")

        self.title_label = ctk.CTkLabel(self.header_frame, text="AGE CALCULATOR", 
                                       font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(pady=(15, 0))
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Advanced Personal Analytics", 
                                          text_color="#94a3b8")
        self.subtitle_label.pack()

        # Input Card
        self.input_card = ctk.CTkFrame(self, corner_radius=20)
        self.input_card.pack(pady=20, padx=30, fill="x")

        self.name_entry = ctk.CTkEntry(self.input_card, placeholder_text="Enter Your Name", 
                                       height=45, corner_radius=10)
        self.name_entry.pack(pady=(25, 10), padx=25, fill="x")

        # Date Row
        self.date_frame = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.date_frame.pack(pady=10, padx=25, fill="x")
        
        self.year_entry = ctk.CTkEntry(self.date_frame, placeholder_text="Year", width=100, height=45)
        self.year_entry.pack(side="left", expand=True, padx=(0, 5))
        
        self.month_entry = ctk.CTkEntry(self.date_frame, placeholder_text="Month", width=80, height=45)
        self.month_entry.pack(side="left", expand=True, padx=5)
        
        self.day_entry = ctk.CTkEntry(self.date_frame, placeholder_text="Day", width=80, height=45)
        self.day_entry.pack(side="left", expand=True, padx=(5, 0))

        # Buttons
        self.calc_btn = ctk.CTkButton(self.input_card, text="Calculate My Age", height=50, 
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      command=self.calculate)
        self.calc_btn.pack(pady=(20, 10), padx=25, fill="x")

        self.reset_btn = ctk.CTkButton(self.input_card, text="Reset", height=40, 
                                       fg_color="#334155", hover_color="#475569",
                                       command=self.reset)
        self.reset_btn.pack(pady=(0, 25), padx=25, fill="x")

        # Result Card (Initially Hidden)
        self.result_card = ctk.CTkFrame(self, corner_radius=20, fg_color="#1e293b", border_width=2, border_color="#3b82f6")
        
        self.res_name = ctk.CTkLabel(self.result_card, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.res_name.pack(pady=(20, 5))
        
        self.res_age = ctk.CTkLabel(self.result_card, text="", font=ctk.CTkFont(size=32, weight="bold"), text_color="#3b82f6")
        self.res_age.pack()
        
        self.res_zodiac = ctk.CTkLabel(self.result_card, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#94a3b8")
        self.res_zodiac.pack()

        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=20, padx=20)
        
        self.stat_days = self.create_stat_widget(self.stats_frame, "Total Days", 0, 0)
        self.stat_hearts = self.create_stat_widget(self.stats_frame, "Heartbeats", 0, 1)

    def create_stat_widget(self, parent, label, row, col):
        frame = ctk.CTkFrame(parent, fg_color="#0f172a", corner_radius=10, height=70)
        frame.grid(row=row, column=col, sticky="ew", padx=5)
        parent.grid_columnconfigure(col, weight=1)
        
        lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=10, weight="bold"), text_color="#64748b")
        lbl.pack(pady=(10, 0))
        
        val = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=13, weight="bold"))
        val.pack(pady=(0, 10))
        return val

    def calculate(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return
        
        try:
            y, m, d = int(self.year_entry.get()), int(self.month_entry.get()), int(self.day_entry.get())
            birth_date = date(y, m, d)
            today = date.today()
            
            if birth_date > today:
                messagebox.showerror("Error", "Birth date is in the future")
                return

            age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            total_days = (today - birth_date).days
            heartbeats = total_days * 24 * 60 * 72

            # Update UI
            self.res_name.configure(text=f"Hello, {name}!")
            self.res_age.configure(text=f"{age_years} Years Old")
            self.res_zodiac.configure(text=f"Zodiac: {self.get_zodiac(m, d)}")
            self.stat_days.configure(text=f"{total_days:,}")
            self.stat_hearts.configure(text=f"{heartbeats:,}")

            self.result_card.pack(pady=20, padx=30, fill="x")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def reset(self):
        self.name_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.month_entry.delete(0, 'end')
        self.day_entry.delete(0, 'end')
        self.result_card.pack_forget()

if __name__ == "__main__":
    app = AgeCalculatorApp()
    app.mainloop()
