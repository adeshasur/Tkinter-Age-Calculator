import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime, timedelta
from PIL import Image

# --- Theme Configuration ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Data
MONTH_DATA = {
    1: {"stone": "Garnet", "flower": "Carnation"},
    2: {"stone": "Amethyst", "flower": "Violet"},
    3: {"stone": "Aquamarine", "flower": "Daffodil"},
    4: {"stone": "Diamond", "flower": "Daisy"},
    5: {"stone": "Emerald", "flower": "Lily of the Valley"},
    6: {"stone": "Pearl", "flower": "Rose"},
    7: {"stone": "Ruby", "flower": "Larkspur"},
    8: {"stone": "Peridot", "flower": "Gladiolus"},
    9: {"stone": "Sapphire", "flower": "Aster"},
    10: {"stone": "Opal", "flower": "Marigold"},
    11: {"stone": "Topaz", "flower": "Chrysanthemum"},
    12: {"stone": "Turquoise", "flower": "Narcissus"}
}

class AdvancedAnalyticsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Age Pro - Advanced Analytics Edition")
        self.after(0, lambda: self.state('zoomed'))
        self.bind("<F11>", lambda e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))

        self.configure(fg_color="#F2F2F7")
        self.setup_ui()

    def get_zodiac(self, month, day):
        zodiac = [(1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"), (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"), (12, 31, "Capricorn")]
        for m, d, s in zodiac:
            if month < m or (month == m and day <= d): return s
        return "Unknown"

    def setup_ui(self):
        # Main split container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        # --- LEFT: INPUTS ---
        self.left = ctk.CTkFrame(self.container, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#E5E5EA")
        self.left.pack(side="left", fill="both", expand=True, padx=(0, 20))

        try:
            img = Image.open("Age.png")
            self.hero = ctk.CTkImage(light_image=img, dark_image=img, size=(450, 120))
            ctk.CTkLabel(self.left, image=self.hero, text="").pack(pady=(50, 10))
        except: pass

        ctk.CTkLabel(self.left, text="Age Pro", font=("SF Pro Display", 42, "bold")).pack()
        ctk.CTkLabel(self.left, text="Advanced Personal Insights", font=("SF Pro Text", 16), text_color="#8E8E93").pack(pady=(0, 40))

        # Form
        f = ctk.CTkFrame(self.left, fg_color="transparent")
        f.pack(fill="x", padx=60)

        self.name_e = ctk.CTkEntry(f, placeholder_text="Full Name", height=60, corner_radius=15, border_width=0, fg_color="#F2F2F7", font=("SF Pro Text", 16))
        self.name_e.pack(fill="x", pady=(0, 20))

        df = ctk.CTkFrame(f, fg_color="transparent")
        df.pack(fill="x")
        ec = {"height": 60, "corner_radius": 15, "border_width": 0, "fg_color": "#F2F2F7", "font": ("SF Pro Text", 16)}
        self.y_e = ctk.CTkEntry(df, placeholder_text="Year", width=120, **ec)
        self.y_e.pack(side="left", expand=True, padx=(0, 10))
        self.m_e = ctk.CTkEntry(df, placeholder_text="Month", width=100, **ec)
        self.m_e.pack(side="left", expand=True, padx=10)
        self.d_e = ctk.CTkEntry(df, placeholder_text="Day", width=100, **ec)
        self.d_e.pack(side="left", expand=True, padx=(10, 0))

        ctk.CTkButton(self.left, text="RUN ADVANCED ANALYTICS", height=65, corner_radius=20, fg_color="#007AFF", hover_color="#0056D2", font=("SF Pro Display", 18, "bold"), command=self.calculate).pack(pady=40, padx=60, fill="x")

        # --- RIGHT: DASHBOARD ---
        self.right = ctk.CTkFrame(self.container, fg_color="transparent")
        self.right.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # Initial Empty State
        self.empty = ctk.CTkLabel(self.right, text="Results Dashboard\nClick Generate to begin.", font=("SF Pro Text", 20), text_color="#8E8E93")
        self.empty.pack(expand=True)

        # Tabview (Visible after calculation)
        self.tabs = ctk.CTkTabview(self.right, corner_radius=30, fg_color="#FFFFFF", border_width=1, border_color="#E5E5EA", segmented_button_fg_color="#F2F2F7", segmented_button_selected_color="#007AFF")
        
        self.summary_tab = self.tabs.add("Summary")
        self.stats_tab = self.tabs.add("Life Stats")
        self.milestones_tab = self.tabs.add("Milestones")
        self.insights_tab = self.tabs.add("Personal Insights")

    def create_stat_card(self, parent, label, val_var, row, col):
        b = ctk.CTkFrame(parent, fg_color="#F2F2F7", corner_radius=20)
        b.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(b, text=label, font=("SF Pro Text", 12, "bold"), text_color="#8E8E93").pack(pady=(15, 0))
        ctk.CTkLabel(b, textvariable=val_var, font=("SF Pro Display", 22, "bold")).pack(pady=(0, 15))

    def calculate(self):
        try:
            name = self.name_e.get().strip()
            y, m, d = int(self.y_e.get()), int(self.m_e.get()), int(self.d_e.get())
            birth = date(y, m, d)
            today = date.today()

            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            delta = today - birth
            days = delta.days
            
            # Switch view
            self.empty.pack_forget()
            self.tabs.pack(fill="both", expand=True)

            # --- TAB: SUMMARY ---
            for w in self.summary_tab.winfo_children(): w.destroy()
            ctk.CTkLabel(self.summary_tab, text=f"Welcome, {name}", font=("SF Pro Display", 32, "bold"), text_color="#000000").pack(pady=(40, 5))
            ctk.CTkLabel(self.summary_tab, text=f"{age} Years Old", font=("SF Pro Display", 86, "bold"), text_color="#007AFF").pack()
            
            # Next Birthday Countdown
            next_b = date(today.year, m, d)
            if next_b < today: next_b = date(today.year + 1, m, d)
            days_to = (next_b - today).days
            ctk.CTkLabel(self.summary_tab, text=f"Your next birthday is in {days_to} days!", font=("SF Pro Text", 18), text_color="#8E8E93").pack(pady=20)

            # --- TAB: LIFE STATS ---
            for w in self.stats_tab.winfo_children(): w.destroy()
            sg = ctk.CTkFrame(self.stats_tab, fg_color="transparent")
            sg.pack(fill="both", expand=True, padx=40, pady=40)
            
            def add_s(l, v, r, c):
                f = ctk.CTkFrame(sg, fg_color="#F2F2F7", corner_radius=15, height=120)
                f.grid(row=r, column=c, padx=10, pady=10, sticky="ew")
                sg.grid_columnconfigure(c, weight=1)
                ctk.CTkLabel(f, text=l, font=("SF Pro Text", 11, "bold"), text_color="#8E8E93").pack(pady=(20,0))
                ctk.CTkLabel(f, text=v, font=("SF Pro Display", 20, "bold")).pack(pady=(0,20))

            add_s("TOTAL DAYS", f"{days:,}", 0, 0)
            add_s("EST. HEARTBEATS", f"{days * 24 * 60 * 72:,}", 0, 1)
            add_s("TOTAL WEEKS", f"{days // 7:,}", 1, 0)
            add_s("TOTAL HOURS", f"{days * 24:,}", 1, 1)
            add_s("EST. SLEEP (YRS)", f"{age // 3}", 2, 0)
            add_s("EST. MEALS", f"{days * 3:,}", 2, 1)

            # --- TAB: MILESTONES ---
            for w in self.milestones_tab.winfo_children(): w.destroy()
            ctk.CTkLabel(self.milestones_tab, text="Your Upcoming Milestones", font=("SF Pro Display", 24, "bold")).pack(pady=20)
            
            def add_m(l, d):
                f = ctk.CTkFrame(self.milestones_tab, fg_color="#F2F2F7", corner_radius=10)
                f.pack(fill="x", padx=40, pady=5)
                ctk.CTkLabel(f, text=l, font=("SF Pro Text", 14, "bold")).pack(side="left", padx=20, pady=15)
                ctk.CTkLabel(f, text=d, font=("SF Pro Display", 14), text_color="#007AFF").pack(side="right", padx=20)

            # Calculate milestone dates
            m_10k = (birth + timedelta(days=10000)).strftime("%Y-%m-%d")
            m_20k = (birth + timedelta(days=20000)).strftime("%Y-%m-%d")
            m_30k = (birth + timedelta(days=30000)).strftime("%Y-%m-%d")
            
            add_m("10,000 Days Old", m_10k)
            add_m("20,000 Days Old", m_20k)
            add_m("30,000 Days Old", m_30k)
            add_m("1 Billion Seconds", (birth + timedelta(seconds=1000000000)).strftime("%Y-%m-%d"))

            # --- TAB: INSIGHTS ---
            for w in self.insights_tab.winfo_children(): w.destroy()
            ig = ctk.CTkFrame(self.insights_tab, fg_color="transparent")
            ig.pack(pady=40)
            
            zod = self.get_zodiac(m, d)
            dt = MONTH_DATA.get(m, {"stone": "Unknown", "flower": "Unknown"})
            
            def add_i(l, v):
                f = ctk.CTkFrame(ig, fg_color="#F2F2F7", corner_radius=20, width=400)
                f.pack(pady=10, fill="x")
                ctk.CTkLabel(f, text=l, font=("SF Pro Text", 12, "bold"), text_color="#8E8E93").pack(pady=(15,0))
                ctk.CTkLabel(f, text=v, font=("SF Pro Display", 24, "bold"), text_color="#007AFF").pack(pady=(0,15))

            add_i("YOUR ZODIAC", zod)
            add_i("BIRTH STONE", dt["stone"])
            add_i("BIRTH FLOWER", dt["flower"])

        except:
            messagebox.showerror("Error", "Invalid Date Data")

if __name__ == "__main__":
    app = AdvancedAnalyticsApp()
    app.mainloop()
