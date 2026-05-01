import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from PIL import Image

# --- iOS Theme Configuration ---
ctk.set_appearance_mode("Light")  # iOS look is iconic in Light mode
ctk.set_default_color_theme("blue")

class IOSAgeCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Calculator")
        self.geometry("400x800")
        self.resizable(False, False)
        self.configure(fg_color="#F2F2F7") # iOS System Secondary Background

        self.setup_ui()

    def setup_ui(self):
        # Header Section
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(pady=(60, 20), padx=30, fill="x")

        # Apple-style Icon/Image
        try:
            img = Image.open("Age.png")
            self.icon_image = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
            self.icon_label = ctk.CTkLabel(self.header, image=self.icon_image, text="")
            self.icon_label.pack(pady=10)
        except: pass

        self.title_label = ctk.CTkLabel(self.header, text="Age Calculator", 
                                       font=ctk.CTkFont(family="SF Pro Display", size=32, weight="bold"),
                                       text_color="#000000")
        self.title_label.pack()
        
        self.subtitle = ctk.CTkLabel(self.header, text="Track your life milestones", 
                                    font=ctk.CTkFont(family="SF Pro Text", size=15),
                                    text_color="#8E8E93")
        self.subtitle.pack()

        # Input Group (iOS Form Style)
        self.form_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        self.form_card.pack(pady=10, padx=20, fill="x")

        # Helper to create iOS style rows
        def create_input(placeholder, pady=(0, 0)):
            entry = ctk.CTkEntry(self.form_card, placeholder_text=placeholder, 
                                 height=50, corner_radius=10, border_width=0,
                                 fg_color="#F2F2F7", text_color="#000000",
                                 font=ctk.CTkFont(family="SF Pro Text", size=14))
            entry.pack(pady=pady, padx=20, fill="x")
            return entry

        self.name_entry = create_input("Name", pady=(20, 10))
        
        # Date Row
        self.date_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.date_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        self.year_entry = ctk.CTkEntry(self.date_frame, placeholder_text="Year", width=100, height=50, corner_radius=10, border_width=0, fg_color="#F2F2F7", text_color="#000000")
        self.year_entry.pack(side="left", expand=True, padx=(0, 5))
        
        self.month_entry = ctk.CTkEntry(self.date_frame, placeholder_text="Month", width=80, height=50, corner_radius=10, border_width=0, fg_color="#F2F2F7", text_color="#000000")
        self.month_entry.pack(side="left", expand=True, padx=5)
        
        self.day_entry = ctk.CTkEntry(self.date_frame, placeholder_text="Day", width=80, height=50, corner_radius=10, border_width=0, fg_color="#F2F2F7", text_color="#000000")
        self.day_entry.pack(side="left", expand=True, padx=(5, 0))

        # Main Action Button (iOS Blue)
        self.calc_btn = ctk.CTkButton(self, text="Calculate Age", 
                                      height=55, corner_radius=15, 
                                      fg_color="#007AFF", hover_color="#0051D5",
                                      font=ctk.CTkFont(family="SF Pro Display", size=17, weight="bold"),
                                      command=self.calculate)
        self.calc_btn.pack(pady=20, padx=20, fill="x")

        # Results Area (iOS Card Style)
        self.result_area = ctk.CTkFrame(self, fg_color="transparent")
        
        self.main_res_card = ctk.CTkFrame(self.result_area, fg_color="#FFFFFF", corner_radius=20)
        self.main_res_card.pack(fill="x", padx=20, pady=10)

        self.res_label = ctk.CTkLabel(self.main_res_card, text="", font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"), text_color="#000000")
        self.res_label.pack(pady=(25, 5))

        self.age_display = ctk.CTkLabel(self.main_res_card, text="", font=ctk.CTkFont(family="SF Pro Display", size=48, weight="bold"), text_color="#007AFF")
        self.age_display.pack(pady=(0, 25))

        # Stats Grid (iOS Style)
        self.stats_grid = ctk.CTkFrame(self.result_area, fg_color="transparent")
        self.stats_grid.pack(fill="x", padx=15)
        self.stats_grid.columnconfigure((0, 1), weight=1)

        self.stat_zodiac = self.create_ios_box(self.stats_grid, "ZODIAC", 0, 0)
        self.stat_bday = self.create_ios_box(self.stats_grid, "NEXT BIRTHDAY", 0, 1)

    def create_ios_box(self, parent, label, row, col):
        box = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        box.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(box, text=label, font=ctk.CTkFont(family="SF Pro Text", size=10, weight="bold"), text_color="#8E8E93").pack(pady=(12, 0))
        val = ctk.CTkLabel(box, text="", font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"), text_color="#000000")
        val.pack(pady=(0, 12))
        return val

    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            y, m, d = int(self.year_entry.get()), int(self.month_entry.get()), int(self.day_entry.get())
            birth_date = date(y, m, d)
            today = date.today()

            age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            # Next Bday
            next_b = date(today.year, m, d)
            if next_b < today: next_b = date(today.year + 1, m, d)
            days_to = (next_b - today).days

            # Zodiac
            zodiac_signs = [(1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"), (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"), (12, 31, "Capricorn")]
            sign = "Unknown"
            for mz, dz, sz in zodiac_signs:
                if m < mz or (m == mz and d <= dz):
                    sign = sz
                    break

            # Update UI
            self.res_label.configure(text=f"Hello, {name}")
            self.age_display.configure(text=f"{age_years} Years")
            self.stat_zodiac.configure(text=sign)
            self.stat_bday.configure(text=f"{days_to} Days")

            self.result_area.pack(fill="x", expand=True)
        except Exception as e:
            messagebox.showerror("Input Error", "Please check your birth date details.")

if __name__ == "__main__":
    app = IOSAgeCalculator()
    app.mainloop()
