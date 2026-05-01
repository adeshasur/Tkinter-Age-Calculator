import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime
from PIL import Image, ImageTk, ImageDraw

# --- Theme Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HyperModernAgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - Hyper Modern")
        self.geometry("450x850")
        self.resizable(False, False)

        self.setup_background()
        self.setup_ui()

    def setup_background(self):
        try:
            # Load the generated gradient background
            bg_img = Image.open("bg.png")
            # Using CTkImage for proper scaling
            self.bg_image = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(450, 850))
            
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background error: {e}")
            self.configure(fg_color="#0f172a")

    def setup_ui(self):
        # Main Container (Glass Frame)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Evolution Hero (Small & Sleek)
        try:
            evo_img = Image.open("Age.png")
            self.evo_photo = ctk.CTkImage(light_image=evo_img, dark_image=evo_img, size=(350, 100))
            self.evo_label = ctk.CTkLabel(self.main_frame, image=self.evo_photo, text="")
            self.evo_label.pack(pady=(30, 10))
        except: pass

        # Title Section
        self.title_label = ctk.CTkLabel(self.main_frame, text="AGE PRO", 
                                       font=ctk.CTkFont(family="Inter", size=36, weight="bold"),
                                       text_color="white")
        self.title_label.pack()
        
        self.subtitle = ctk.CTkLabel(self.main_frame, text="වයස ගණකය | Advanced Analytics", 
                                    font=ctk.CTkFont(family="Inter", size=12),
                                    text_color="#cbd5e1")
        self.subtitle.pack(pady=(0, 30))

        # Input Section (Glass Card)
        self.input_card = ctk.CTkFrame(self.main_frame, corner_radius=25, 
                                       fg_color=("#e2e8f0", "#1e293b"),
                                       border_width=1, border_color="#475569")
        self.input_card.pack(fill="x", padx=10, pady=10)

        self.name_entry = ctk.CTkEntry(self.input_card, placeholder_text="Name", 
                                       height=50, corner_radius=15, border_width=0,
                                       fg_color=("#f1f5f9", "#0f172a"), text_color=("black", "white"))
        self.name_entry.pack(pady=(25, 10), padx=25, fill="x")

        # Date Row
        self.date_row = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.date_row.pack(pady=10, padx=25, fill="x")
        
        entry_style = {"height": 50, "corner_radius": 15, "border_width": 0, "fg_color": ("#f1f5f9", "#0f172a"), "text_color": ("black", "white")}
        
        self.year_entry = ctk.CTkEntry(self.date_row, placeholder_text="Year", **entry_style)
        self.year_entry.pack(side="left", expand=True, padx=(0, 5))
        
        self.month_entry = ctk.CTkEntry(self.date_row, placeholder_text="Mon", **entry_style)
        self.month_entry.pack(side="left", expand=True, padx=5)
        
        self.day_entry = ctk.CTkEntry(self.date_row, placeholder_text="Day", **entry_style)
        self.day_entry.pack(side="left", expand=True, padx=(5, 0))

        # Action Button (Neon Gradient feel)
        self.calc_btn = ctk.CTkButton(self.input_card, text="GENERATE INSIGHTS", 
                                      height=55, corner_radius=15, 
                                      fg_color="#3b82f6", hover_color="#2563eb",
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      command=self.calculate)
        self.calc_btn.pack(pady=(20, 25), padx=25, fill="x")

        # Results Dashboard (Initially Hidden)
        self.results_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # Result Card
        self.res_card = ctk.CTkFrame(self.results_frame, corner_radius=25,
                                     fg_color=("#ffffff", "#1e293b"), border_width=2, border_color="#3b82f6")
        self.res_card.pack(fill="x", pady=10)

        self.res_title = ctk.CTkLabel(self.res_card, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.res_title.pack(pady=(20, 5))

        self.res_age = ctk.CTkLabel(self.res_card, text="", font=ctk.CTkFont(size=40, weight="bold"), text_color="#38bdf8")
        self.res_age.pack()

        # Progress Bar (Life Progress)
        self.progress_label = ctk.CTkLabel(self.res_card, text="Life Cycle Progress", font=ctk.CTkFont(size=10))
        self.progress_label.pack(pady=(10, 0))
        self.progress_bar = ctk.CTkProgressBar(self.res_card, height=10, corner_radius=5)
        self.progress_bar.pack(pady=(5, 20), padx=40, fill="x")

        # Stats Grid
        self.stats_grid = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.stats_grid.pack(fill="x")
        self.stats_grid.columnconfigure((0, 1), weight=1)

        self.stat_zodiac = self.create_stat_box(self.stats_grid, "Zodiac", 0, 0)
        self.stat_bday = self.create_stat_box(self.stats_grid, "Next B-Day", 0, 1)
        self.stat_days = self.create_stat_box(self.stats_grid, "Days Lived", 1, 0)
        self.stat_hearts = self.create_stat_box(self.stats_grid, "Heartbeats", 1, 1)

    def create_stat_box(self, parent, label, row, col):
        box = ctk.CTkFrame(parent, corner_radius=15, fg_color=("#f8fafc", "#1e293b"), height=80)
        box.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(box, text=label, font=ctk.CTkFont(size=10), text_color="#94a3b8").pack(pady=(10, 0))
        val = ctk.CTkLabel(box, text="", font=ctk.CTkFont(size=13, weight="bold"))
        val.pack(pady=(0, 10))
        return val

    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            y, m, d = int(self.year_entry.get()), int(self.month_entry.get()), int(self.day_entry.get())
            birth_date = date(y, m, d)
            today = date.today()

            age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            total_days = (today - birth_date).days
            
            # Progress (Assume 85 years life expectancy)
            progress = min(1.0, age_years / 85)
            self.progress_bar.set(progress)

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
            self.res_title.configure(text=f"Welcome, {name}")
            self.res_age.configure(text=f"{age_years} YRS")
            self.stat_zodiac.configure(text=sign)
            self.stat_bday.configure(text=f"{days_to} Days")
            self.stat_days.configure(text=f"{total_days:,}")
            self.stat_hearts.configure(text=f"{total_days * 24 * 60 * 72:,}")

            self.results_frame.pack(fill="x", pady=10)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")

if __name__ == "__main__":
    app = HyperModernAgeApp()
    app.mainloop()
