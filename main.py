import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime, timedelta
from PIL import Image
import time

# --- Theme Configuration ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class SaasDashboardAgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - SaaS Dashboard")
        self.after(0, lambda: self.state('zoomed'))
        
        # Appearance Mode Toggle logic
        self.is_dark = False

        self.setup_ui()
        self.update_live_counter()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#1e293b")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        try:
            img = Image.open("Age.png")
            self.logo = ctk.CTkImage(light_image=img, dark_image=img, size=(220, 60))
            ctk.CTkLabel(self.sidebar, image=self.logo, text="").grid(row=0, column=0, padx=20, pady=(40, 20))
        except: pass

        ctk.CTkLabel(self.sidebar, text="AGE PRO", font=("SF Pro Display", 24, "bold"), text_color="white").grid(row=1, column=0, padx=20, pady=(0, 30))

        # Input Form in Sidebar
        self.input_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.input_f.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.name_e = ctk.CTkEntry(self.input_f, placeholder_text="Full Name", height=45, corner_radius=10, border_width=0, fg_color="#334155", text_color="white")
        self.name_e.pack(fill="x", pady=5)

        self.date_f = ctk.CTkFrame(self.input_f, fg_color="transparent")
        self.date_f.pack(fill="x", pady=5)
        ec = {"height": 45, "corner_radius": 10, "border_width": 0, "fg_color": "#334155", "text_color": "white", "width": 60}
        self.y_e = ctk.CTkEntry(self.date_f, placeholder_text="YYYY", **ec)
        self.y_e.pack(side="left", expand=True, padx=(0, 2))
        self.m_e = ctk.CTkEntry(self.date_f, placeholder_text="MM", **ec)
        self.m_e.pack(side="left", expand=True, padx=2)
        self.d_e = ctk.CTkEntry(self.date_f, placeholder_text="DD", **ec)
        self.d_e.pack(side="left", expand=True, padx=(2, 0))

        self.calc_btn = ctk.CTkButton(self.sidebar, text="Run Analytics", height=50, corner_radius=10, fg_color="#3b82f6", hover_color="#2563eb", font=("SF Pro Text", 14, "bold"), command=self.calculate)
        self.calc_btn.grid(row=3, column=0, padx=20, pady=30, sticky="ew")

        # Bottom Sidebar
        self.mode_btn = ctk.CTkButton(self.sidebar, text="Switch Theme", height=40, corner_radius=10, fg_color="#475569", command=self.toggle_theme)
        self.mode_btn.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        # --- MAIN AREA ---
        self.main_area = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        self.welcome_lbl = ctk.CTkLabel(self.main_area, text="Welcome to Age Pro Dashboard\nEnter details to generate your life report.", font=("SF Pro Text", 20), text_color="#94a3b8")
        self.welcome_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Dashboard View (Hidden initially)
        self.dashboard = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        
    def toggle_theme(self):
        self.is_dark = not self.is_dark
        ctk.set_appearance_mode("Dark" if self.is_dark else "Light")
        self.main_area.configure(fg_color="#0f172a" if self.is_dark else "#F8FAFC")

    def create_card(self, parent, title, val_var, row, col, span=1):
        c = ctk.CTkFrame(parent, fg_color="#FFFFFF" if not self.is_dark else "#1e293b", corner_radius=20, border_width=1, border_color="#E2E8F0" if not self.is_dark else "#334155")
        c.grid(row=row, column=col, columnspan=span, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(c, text=title, font=("SF Pro Text", 12, "bold"), text_color="#64748b").pack(pady=(20, 0))
        lbl = ctk.CTkLabel(c, text="", font=("SF Pro Display", 28, "bold"), text_color="#3b82f6")
        lbl.pack(pady=(0, 20))
        return lbl

    def calculate(self):
        try:
            name = self.name_e.get().strip()
            y, m, d = int(self.y_e.get()), int(self.m_e.get()), int(self.d_e.get())
            self.birth_date = datetime(y, m, d)
            
            self.welcome_lbl.place_forget()
            self.dashboard.place(relx=0, rely=0, relwidth=1, relheight=1)

            for w in self.dashboard.winfo_children(): w.destroy()

            # Layout Grid
            self.dashboard.grid_columnconfigure((0, 1, 2), weight=1)

            # 1. Age Hero Card
            hero = ctk.CTkFrame(self.dashboard, fg_color="#3b82f6", corner_radius=25)
            hero.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
            
            ctk.CTkLabel(hero, text=f"Life Summary for {name}", font=("SF Pro Display", 18), text_color="white").pack(pady=(30, 5))
            self.live_age_lbl = ctk.CTkLabel(hero, text="", font=("SF Pro Display", 72, "bold"), text_color="white")
            self.live_age_lbl.pack(pady=(0, 30))

            # 2. Stats Grid
            self.card_days = self.create_card(self.dashboard, "TOTAL DAYS LIVED", None, 1, 0)
            self.card_weeks = self.create_card(self.dashboard, "TOTAL WEEKS", None, 1, 1)
            self.card_hearts = self.create_card(self.dashboard, "EST. HEARTBEATS", None, 1, 2)

            self.card_zodiac = self.create_card(self.dashboard, "ZODIAC SIGN", None, 2, 0)
            self.card_stone = self.create_card(self.dashboard, "BIRTH STONE", None, 2, 1)
            self.card_flower = self.create_card(self.dashboard, "BIRTH FLOWER", None, 2, 2)

            # Data update
            today = datetime.now()
            age_yrs = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            diff = today - self.birth_date
            
            self.card_days.configure(text=f"{diff.days:,}")
            self.card_weeks.configure(text=f"{diff.days // 7:,}")
            self.card_hearts.configure(text=f"{diff.days * 24 * 60 * 72:,}")
            self.card_zodiac.configure(text="Aquarius") # Placeholder
            self.card_stone.configure(text="Amethyst") # Placeholder
            self.card_flower.configure(text="Violet") # Placeholder

        except:
            messagebox.showerror("Error", "Check your inputs")

    def update_live_counter(self):
        if hasattr(self, 'birth_date'):
            now = datetime.now()
            diff = now - self.birth_date
            # Calculate precise age
            years = now.year - self.birth_date.year - ((now.month, now.day, now.hour, now.minute, now.second) < (self.birth_date.month, self.birth_date.day, self.birth_date.hour, self.birth_date.minute, self.birth_date.second))
            
            # Simple version for the live counter: Years, Months, Days, Secs
            self.live_age_lbl.configure(text=f"{years}Y {diff.days % 365}D {diff.seconds}S")
        
        self.after(1000, self.update_live_counter)

if __name__ == "__main__":
    app = SaasDashboardAgeApp()
    app.mainloop()
