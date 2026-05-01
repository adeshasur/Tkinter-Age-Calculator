import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk

# --- Theme Setup ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class AppleUltimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - Apple Edition")
        self.geometry("450x880")
        self.resizable(False, False)

        self.setup_background()
        self.setup_ui()

    def setup_background(self):
        try:
            bg_img = Image.open("apple_bg.png")
            self.bg_image = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(450, 880))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.configure(fg_color="#FBFBFD") # Apple White fallback

    def setup_ui(self):
        # Main Scrollable / Stacked Frame
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=25, pady=25)

        # Hero Image (Evolution)
        try:
            hero = Image.open("Age.png")
            self.hero_photo = ctk.CTkImage(light_image=hero, dark_image=hero, size=(380, 100))
            self.hero_label = ctk.CTkLabel(self.container, image=self.hero_photo, text="")
            self.hero_label.pack(pady=(40, 5))
        except: pass

        # Title
        self.title_label = ctk.CTkLabel(self.container, text="Age Pro", 
                                       font=ctk.CTkFont(family="SF Pro Display", size=42, weight="bold"),
                                       text_color="#1D1D1F") # Apple Dark Gray
        self.title_label.pack()
        
        self.subtitle = ctk.CTkLabel(self.container, text="The art of growing up.", 
                                    font=ctk.CTkFont(family="SF Pro Text", size=17),
                                    text_color="#86868B") # Apple Muted Gray
        self.subtitle.pack(pady=(0, 40))

        # Input Section (Apple Glass Card)
        self.card = ctk.CTkFrame(self.container, corner_radius=28, 
                                 fg_color="#FFFFFF", 
                                 border_width=1, border_color="#E5E5E7")
        self.card.pack(fill="x", pady=10)

        # Custom Styled Input
        def add_ios_input(placeholder, pady=(0, 0)):
            e = ctk.CTkEntry(self.card, placeholder_text=placeholder, 
                             height=55, corner_radius=18, border_width=0,
                             fg_color="#F5F5F7", text_color="#1D1D1F",
                             font=ctk.CTkFont(family="SF Pro Text", size=15))
            e.pack(pady=pady, padx=25, fill="x")
            return e

        self.name_entry = add_ios_input("Your Name", pady=(30, 15))
        
        # Date Grid
        self.date_grid = ctk.CTkFrame(self.card, fg_color="transparent")
        self.date_grid.pack(fill="x", padx=25, pady=(0, 30))
        
        entry_cfg = {"height": 55, "corner_radius": 18, "border_width": 0, "fg_color": "#F5F5F7", "text_color": "#1D1D1F", "font": ("SF Pro Text", 14)}
        
        self.year_e = ctk.CTkEntry(self.date_grid, placeholder_text="Year", width=100, **entry_cfg)
        self.year_e.pack(side="left", expand=True, padx=(0, 5))
        
        self.month_e = ctk.CTkEntry(self.date_grid, placeholder_text="Mon", width=80, **entry_cfg)
        self.month_e.pack(side="left", expand=True, padx=5)
        
        self.day_e = ctk.CTkEntry(self.date_grid, placeholder_text="Day", width=80, **entry_cfg)
        self.day_e.pack(side="left", expand=True, padx=(5, 0))

        # Main Button
        self.action_btn = ctk.CTkButton(self.container, text="Generate Analytics", 
                                        height=65, corner_radius=30, 
                                        fg_color="#007AFF", hover_color="#0066CC",
                                        font=ctk.CTkFont(family="SF Pro Display", size=18, weight="bold"),
                                        command=self.calculate)
        self.action_btn.pack(pady=25, fill="x")

        # Results Dashboard
        self.dashboard = ctk.CTkFrame(self.container, fg_color="transparent")
        
        # Age Summary Card
        self.summary_card = ctk.CTkFrame(self.dashboard, corner_radius=28, fg_color="#FFFFFF", 
                                         border_width=1, border_color="#E5E5E7")
        self.summary_card.pack(fill="x", pady=10)

        self.res_name = ctk.CTkLabel(self.summary_card, text="", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1D1D1F")
        self.res_name.pack(pady=(25, 5))

        self.res_age = ctk.CTkLabel(self.summary_card, text="", font=ctk.CTkFont(size=54, weight="bold"), text_color="#007AFF")
        self.res_age.pack()

        self.res_tag = ctk.CTkLabel(self.summary_card, text="", font=ctk.CTkFont(size=14), text_color="#86868B")
        self.res_tag.pack(pady=(0, 25))

        # Stats Row
        self.stats_row = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        self.stats_row.pack(fill="x")
        self.stats_row.columnconfigure((0, 1), weight=1)

        self.stat_zodiac = self.create_apple_stat(self.stats_row, "Zodiac", 0, 0)
        self.stat_next = self.create_apple_stat(self.stats_row, "Birthday", 0, 1)

    def create_apple_stat(self, parent, label, row, col):
        f = ctk.CTkFrame(parent, corner_radius=20, fg_color="#FFFFFF", border_width=1, border_color="#E5E5E7", height=90)
        f.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11, weight="bold"), text_color="#86868B").pack(pady=(15, 0))
        val = ctk.CTkLabel(f, text="", font=ctk.CTkFont(size=15, weight="bold"), text_color="#1D1D1F")
        val.pack(pady=(0, 15))
        return val

    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            y, m, d = int(self.year_e.get()), int(self.month_e.get()), int(self.day_e.get())
            birth = date(y, m, d)
            today = date.today()

            age_years = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            
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

            self.res_name.configure(text=f"Welcome, {name}")
            self.res_age.configure(text=f"{age_years}")
            self.res_tag.configure(text=f"Years of experiences")
            self.stat_zodiac.configure(text=sign)
            self.stat_next.configure(text=f"{days_to} Days Left")

            self.dashboard.pack(fill="x", expand=True)
        except Exception as e:
            messagebox.showerror("Error", "Invalid date format")

if __name__ == "__main__":
    app = AppleUltimateApp()
    app.mainloop()
