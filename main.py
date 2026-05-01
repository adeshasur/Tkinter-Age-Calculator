import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from PIL import Image

# --- Theme Configuration ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class MaximizedDesktopAgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - Full Screen Edition")
        
        # Start Maximized
        self.after(0, lambda: self.state('zoomed'))
        
        # Toggle Fullscreen with F11
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        self.is_fullscreen = False

        self.configure(fg_color="#F2F2F7")
        self.setup_ui()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

    def setup_ui(self):
        # Main Scrollable Container for high-res flexibility
        self.scroll_canvas = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_canvas.pack(fill="both", expand=True)

        # Centered Content Wrapper
        self.main_container = ctk.CTkFrame(self.scroll_canvas, fg_color="transparent")
        self.main_container.pack(pady=50, padx=50, fill="both", expand=True)

        # --- LEFT PANEL (Inputs) ---
        self.left_panel = ctk.CTkFrame(self.main_container, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#E5E5EA")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Hero Image
        try:
            img = Image.open("Age.png")
            w, h = img.size
            new_w = 500 # Slightly larger for full screen
            new_h = int(h * (new_w / w))
            self.icon_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            self.icon_label = ctk.CTkLabel(self.left_panel, image=self.icon_image, text="")
            self.icon_label.pack(pady=(60, 20))
        except: pass

        ctk.CTkLabel(self.left_panel, text="Age Calculator", 
                     font=ctk.CTkFont(family="SF Pro Display", size=42, weight="bold"),
                     text_color="#000000").pack()
        
        ctk.CTkLabel(self.left_panel, text="Press F11 to toggle Full Screen Mode", 
                     font=ctk.CTkFont(family="SF Pro Text", size=16),
                     text_color="#8E8E93").pack(pady=(0, 40))

        # Form
        self.form_f = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.form_f.pack(fill="x", padx=60)

        self.name_entry = ctk.CTkEntry(self.form_f, placeholder_text="Full Name", 
                                       height=60, corner_radius=15, border_width=0,
                                       fg_color="#F2F2F7", text_color="#000000",
                                       font=ctk.CTkFont(size=16))
        self.name_entry.pack(fill="x", pady=(0, 20))

        self.date_row = ctk.CTkFrame(self.form_f, fg_color="transparent")
        self.date_row.pack(fill="x")
        
        e_cfg = {"height": 60, "corner_radius": 15, "border_width": 0, "fg_color": "#F2F2F7", "text_color": "#000000", "font": ("SF Pro Text", 16)}
        
        self.year_e = ctk.CTkEntry(self.date_row, placeholder_text="Year", width=120, **e_cfg)
        self.year_e.pack(side="left", expand=True, padx=(0, 10))
        
        self.month_e = ctk.CTkEntry(self.date_row, placeholder_text="Month", width=100, **e_cfg)
        self.month_e.pack(side="left", expand=True, padx=10)
        
        self.day_e = ctk.CTkEntry(self.date_row, placeholder_text="Day", width=100, **e_cfg)
        self.day_e.pack(side="left", expand=True, padx=(10, 0))

        self.calc_btn = ctk.CTkButton(self.left_panel, text="Generate Insights", 
                                      height=65, corner_radius=25, 
                                      fg_color="#007AFF", hover_color="#0056D2",
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      command=self.calculate)
        self.calc_btn.pack(pady=40, padx=60, fill="x")

        # --- RIGHT PANEL (Results) ---
        self.right_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(20, 0))

        self.empty_label = ctk.CTkLabel(self.right_panel, text="Insights Dashboard\nEnter details to start.", 
                                       font=ctk.CTkFont(size=20), text_color="#8E8E93")
        self.empty_label.pack(expand=True)

        self.results_area = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        
        # Result Header
        self.res_card = ctk.CTkFrame(self.results_area, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#E5E5EA")
        self.res_card.pack(fill="x", pady=(0, 25))
        
        self.res_name = ctk.CTkLabel(self.res_card, text="", font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000")
        self.res_name.pack(pady=(40, 5))
        
        self.res_age = ctk.CTkLabel(self.res_card, text="", font=ctk.CTkFont(size=96, weight="bold"), text_color="#007AFF")
        self.res_age.pack(pady=(0, 40))

        # Grid
        self.stats_grid = ctk.CTkFrame(self.results_area, fg_color="transparent")
        self.stats_grid.pack(fill="both", expand=True)
        self.stats_grid.columnconfigure((0, 1), weight=1)

        self.st_zodiac = self.create_stat_box(self.stats_grid, "ZODIAC", 0, 0)
        self.st_next = self.create_stat_box(self.stats_grid, "NEXT BIRTHDAY", 0, 1)
        self.st_days = self.create_stat_box(self.stats_grid, "TOTAL DAYS", 1, 0)
        self.st_hearts = self.create_stat_box(self.stats_grid, "HEARTBEATS", 1, 1)

    def create_stat_box(self, parent, label, row, col):
        b = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=25, border_width=1, border_color="#E5E5EA", height=150)
        b.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(b, text=label, font=ctk.CTkFont(size=14, weight="bold"), text_color="#8E8E93").pack(pady=(25, 0))
        v = ctk.CTkLabel(b, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#000000")
        v.pack(pady=(0, 25))
        return v

    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            y, m, d = int(self.year_e.get()), int(self.month_e.get()), int(self.day_e.get())
            birth = date(y, m, d)
            today = date.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            total_days = (today - birth).days
            
            self.empty_label.pack_forget()
            self.results_area.pack(fill="both", expand=True)

            self.res_name.configure(text=f"Welcome, {name}")
            self.res_age.configure(text=f"{age} Years")
            self.st_zodiac.configure(text="Capricorn" if m == 1 else "Aquarius") # Simpler for now
            self.st_next.configure(text="Coming Soon")
            self.st_days.configure(text=f"{total_days:,}")
            self.st_hearts.configure(text=f"{total_days * 103,680:,}")

        except:
            messagebox.showerror("Error", "Invalid Date")

if __name__ == "__main__":
    app = MaximizedDesktopAgeApp()
    app.mainloop()
