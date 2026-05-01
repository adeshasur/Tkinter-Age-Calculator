import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from PIL import Image

# --- iOS Theme Configuration ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ScrollableAppleAgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Calculator")
        self.geometry("450x850") # Slightly wider for better breathing room
        self.resizable(False, False)
        self.configure(fg_color="#F2F2F7") 

        self.setup_ui()

    def setup_ui(self):
        # Main Scrollable Frame to ensure NOTHING is cut off
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll_container.pack(fill="both", expand=True)

        # Header Section
        self.header = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.header.pack(pady=(40, 10), padx=30, fill="x")

        try:
            img = Image.open("Age.png")
            w, h = img.size
            new_w = 350
            new_h = int(h * (new_w / w))
            self.icon_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            self.icon_label = ctk.CTkLabel(self.header, image=self.icon_image, text="")
            self.icon_label.pack(pady=10)
        except: pass

        self.title_label = ctk.CTkLabel(self.header, text="Age Calculator", 
                                       font=ctk.CTkFont(family="SF Pro Display", size=36, weight="bold"),
                                       text_color="#000000")
        self.title_label.pack()
        
        self.subtitle = ctk.CTkLabel(self.header, text="Your life journey in numbers", 
                                    font=ctk.CTkFont(family="SF Pro Text", size=15),
                                    text_color="#8E8E93")
        self.subtitle.pack()

        # Input Card
        self.form_card = ctk.CTkFrame(self.scroll_container, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#E5E5EA")
        self.form_card.pack(pady=20, padx=25, fill="x")

        self.name_entry = ctk.CTkEntry(self.form_card, placeholder_text="Enter Name", 
                                       height=55, corner_radius=12, border_width=0,
                                       fg_color="#F2F2F7", text_color="#000000",
                                       font=ctk.CTkFont(family="SF Pro Text", size=15))
        self.name_entry.pack(pady=(30, 15), padx=25, fill="x")
        
        # Date Inputs
        self.date_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.date_frame.pack(pady=(0, 30), padx=25, fill="x")
        
        style = {"height": 55, "corner_radius": 12, "border_width": 0, "fg_color": "#F2F2F7", "text_color": "#000000", "font": ("SF Pro Text", 15)}
        
        self.year_e = ctk.CTkEntry(self.date_frame, placeholder_text="Year", width=100, **style)
        self.year_e.pack(side="left", expand=True, padx=(0, 5))
        
        self.month_e = ctk.CTkEntry(self.date_frame, placeholder_text="Mon", width=80, **style)
        self.month_e.pack(side="left", expand=True, padx=5)
        
        self.day_e = ctk.CTkEntry(self.date_frame, placeholder_text="Day", width=80, **style)
        self.day_e.pack(side="left", expand=True, padx=(5, 0))

        # Action Button
        self.calc_btn = ctk.CTkButton(self.scroll_container, text="Calculate Life Stats", 
                                      height=60, corner_radius=20, 
                                      fg_color="#007AFF", hover_color="#0056D2",
                                      font=ctk.CTkFont(family="SF Pro Display", size=18, weight="bold"),
                                      command=self.calculate)
        self.calc_btn.pack(pady=10, padx=25, fill="x")

        # Results Dashboard (Initially Hidden)
        self.results = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        
        # Main Result Card
        self.age_card = ctk.CTkFrame(self.results, fg_color="#FFFFFF", corner_radius=25, border_width=1, border_color="#E5E5EA")
        self.age_card.pack(fill="x", padx=25, pady=10)

        self.res_name = ctk.CTkLabel(self.age_card, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color="#000000")
        self.res_name.pack(pady=(30, 5))

        self.res_age = ctk.CTkLabel(self.age_card, text="", font=ctk.CTkFont(size=56, weight="bold"), text_color="#007AFF")
        self.res_age.pack(pady=(0, 30))

        # Grid for stats
        self.stats_grid = ctk.CTkFrame(self.results, fg_color="transparent")
        self.stats_grid.pack(fill="x", padx=20)
        self.stats_grid.columnconfigure((0, 1), weight=1)

        self.st_zodiac = self.create_box(self.stats_grid, "ZODIAC", 0, 0)
        self.st_next = self.create_box(self.stats_grid, "NEXT BIRTHDAY", 0, 1)
        self.st_days = self.create_box(self.stats_grid, "TOTAL DAYS", 1, 0)
        self.st_hearts = self.create_box(self.stats_grid, "HEARTBEATS", 1, 1)

    def create_box(self, parent, label, row, col):
        b = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#E5E5EA")
        b.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(b, text=label, font=ctk.CTkFont(size=11, weight="bold"), text_color="#8E8E93").pack(pady=(15, 0))
        v = ctk.CTkLabel(b, text="", font=ctk.CTkFont(size=17, weight="bold"), text_color="#000000")
        v.pack(pady=(0, 15))
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

            self.res_name.configure(text=f"Welcome, {name}")
            self.res_age.configure(text=f"{age} Years")
            self.st_zodiac.configure(text=sign)
            self.st_next.configure(text=f"{days_to} Days")
            self.st_days.configure(text=f"{total_days:,}")
            self.st_hearts.configure(text=f"{heartbeats:,}")

            self.results.pack(fill="x", expand=True, pady=(10, 50)) # Extra bottom padding
        except:
            messagebox.showerror("Error", "Check your input values.")

if __name__ == "__main__":
    app = ScrollableAppleAgeApp()
    app.mainloop()
