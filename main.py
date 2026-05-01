import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from PIL import Image

# --- Theme Configuration ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class LandscapeDesktopAgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - Desktop Edition")
        self.geometry("1100x650") # Desktop Landscape Size
        self.resizable(False, False)
        self.configure(fg_color="#F2F2F7")

        self.setup_ui()

    def setup_ui(self):
        # Main Split Layout
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # --- LEFT PANEL (Inputs) ---
        self.left_panel = ctk.CTkFrame(self.main_container, fg_color="#FFFFFF", corner_radius=25, border_width=1, border_color="#E5E5EA")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Hero Image in Left Panel
        try:
            img = Image.open("Age.png")
            # Quality resizing for desktop
            w, h = img.size
            new_w = 400
            new_h = int(h * (new_w / w))
            self.icon_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            self.icon_label = ctk.CTkLabel(self.left_panel, image=self.icon_image, text="")
            self.icon_label.pack(pady=(40, 10))
        except: pass

        ctk.CTkLabel(self.left_panel, text="Age Calculator", 
                     font=ctk.CTkFont(family="SF Pro Display", size=32, weight="bold"),
                     text_color="#000000").pack()
        
        ctk.CTkLabel(self.left_panel, text="Enter your details to generate life insights", 
                     font=ctk.CTkFont(family="SF Pro Text", size=14),
                     text_color="#8E8E93").pack(pady=(0, 30))

        # Input Form
        self.form_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=40)

        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Full Name", 
                                       height=50, corner_radius=12, border_width=0,
                                       fg_color="#F2F2F7", text_color="#000000",
                                       font=ctk.CTkFont(size=15))
        self.name_entry.pack(fill="x", pady=(0, 15))

        # Date Inputs
        self.date_row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.date_row.pack(fill="x")
        
        entry_cfg = {"height": 50, "corner_radius": 12, "border_width": 0, "fg_color": "#F2F2F7", "text_color": "#000000", "font": ("SF Pro Text", 14)}
        
        self.year_e = ctk.CTkEntry(self.date_row, placeholder_text="Year", width=100, **entry_cfg)
        self.year_e.pack(side="left", expand=True, padx=(0, 5))
        
        self.month_e = ctk.CTkEntry(self.date_row, placeholder_text="Month", width=80, **entry_cfg)
        self.month_e.pack(side="left", expand=True, padx=5)
        
        self.day_e = ctk.CTkEntry(self.date_row, placeholder_text="Day", width=80, **entry_cfg)
        self.day_e.pack(side="left", expand=True, padx=(5, 0))

        self.calc_btn = ctk.CTkButton(self.left_panel, text="Calculate Analytics", 
                                      height=55, corner_radius=20, 
                                      fg_color="#007AFF", hover_color="#0056D2",
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      command=self.calculate)
        self.calc_btn.pack(pady=30, padx=40, fill="x")

        # --- RIGHT PANEL (Results) ---
        self.right_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Welcome Card (Empty state)
        self.empty_state = ctk.CTkLabel(self.right_panel, text="Results will appear here\nafter calculation.", 
                                       font=ctk.CTkFont(size=16), text_color="#8E8E93")
        self.empty_state.pack(expand=True)

        # Actual Results Container (Hidden initially)
        self.results_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        
        # Result Header
        self.res_card = ctk.CTkFrame(self.results_container, fg_color="#FFFFFF", corner_radius=25, border_width=1, border_color="#E5E5EA")
        self.res_card.pack(fill="x", pady=(0, 20))
        
        self.res_name = ctk.CTkLabel(self.res_card, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#000000")
        self.res_name.pack(pady=(30, 5))
        
        self.res_age = ctk.CTkLabel(self.res_card, text="", font=ctk.CTkFont(size=72, weight="bold"), text_color="#007AFF")
        self.res_age.pack(pady=(0, 30))

        # Stats Grid
        self.stats_grid = ctk.CTkFrame(self.results_container, fg_color="transparent")
        self.stats_grid.pack(fill="both", expand=True)
        self.stats_grid.columnconfigure((0, 1), weight=1)

        self.st_zodiac = self.create_stat_box(self.stats_grid, "ZODIAC SIGN", 0, 0)
        self.st_next = self.create_stat_box(self.stats_grid, "NEXT BIRTHDAY", 0, 1)
        self.st_days = self.create_stat_box(self.stats_grid, "TOTAL DAYS", 1, 0)
        self.st_hearts = self.create_stat_box(self.stats_grid, "HEARTBEATS (EST.)", 1, 1)

    def create_stat_box(self, parent, label, row, col):
        b = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#E5E5EA", height=120)
        b.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
        ctk.CTkLabel(b, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color="#8E8E93").pack(pady=(20, 0))
        v = ctk.CTkLabel(b, text="", font=ctk.CTkFont(size=20, weight="bold"), text_color="#000000")
        v.pack(pady=(0, 20))
        return v

    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            y, m, d = int(self.year_e.get()), int(self.month_e.get()), int(self.day_e.get())
            birth = date(y, m, d)
            today = date.today()

            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            total_days = (today - birth).days
            heartbeats = total_days * 24 * 60 * 72
            
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

            # Switch views
            self.empty_state.pack_forget()
            self.results_container.pack(fill="both", expand=True)

            # Update Labels
            self.res_name.configure(text=f"Welcome, {name}")
            self.res_age.configure(text=f"{age} Years")
            self.st_zodiac.configure(text=sign)
            self.st_next.configure(text=f"{days_to} Days Left")
            self.st_days.configure(text=f"{total_days:,}")
            self.st_hearts.configure(text=f"{heartbeats:,}")

        except:
            messagebox.showerror("Error", "Please check your birth date details.")

if __name__ == "__main__":
    app = LandscapeDesktopAgeApp()
    app.mainloop()
