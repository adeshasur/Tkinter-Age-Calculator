import flet as ft
from datetime import datetime, date

# --- Global Style Config ---
ACCENT = "#007AFF"
BG_WHITE = "#FFFFFF"
BG_SUBTLE = "#FBFBFC"
TEXT_MAIN = "#1D1D1F" # Apple Charcoal
TEXT_SECONDARY = "#86868B" # Apple Gray
BORDER_SOFT = "#F2F2F7"

# --- Logic ---

def get_zodiac(month, day):
    try:
        zodiac_signs = [(1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"), (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"), (12, 31, "Capricorn")]
        for m, d, sign in zodiac_signs:
            if month < m or (month == m and day <= d):
                return sign
    except: pass
    return "Unknown"

# --- Reusable Components ---

class DashboardTile(ft.Container):
    def __init__(self, title, icon, value_text="--"):
        super().__init__()
        self.value_label = ft.Text(value_text, size=22, weight="bold", color=TEXT_MAIN)
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color=ACCENT, size=14), ft.Text(title, size=11, color=TEXT_SECONDARY, weight="w500")], spacing=6),
                self.value_label,
            ],
            spacing=4,
        )
        self.padding = 20
        self.border_radius = 12
        self.bgcolor = BG_WHITE
        self.border = ft.border.all(1, BORDER_SOFT)
        self.shadow = ft.BoxShadow(spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.02, ft.Colors.BLACK), offset=ft.Offset(0, 4))
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        self.expand = True

def main(page: ft.Page):
    page.title = "AgePro Elite"
    page.bgcolor = BG_WHITE
    page.padding = 0
    page.window_width = 1200
    page.window_height = 900
    page.fonts = {"Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"}
    page.theme = ft.Theme(font_family="Outfit")

    # --- UI State Controllers ---
    
    name_input = ft.TextField(label="Full Name", border="underline", border_color=BORDER_SOFT, focused_border_color=ACCENT, text_size=14)
    year_input = ft.TextField(label="Year", width=80, border="underline", border_color=BORDER_SOFT, focused_border_color=ACCENT)
    month_input = ft.TextField(label="Month", width=70, border="underline", border_color=BORDER_SOFT, focused_border_color=ACCENT)
    day_input = ft.TextField(label="Day", width=60, border="underline", border_color=BORDER_SOFT, focused_border_color=ACCENT)

    res_age = ft.Text("0", size=140, weight="bold", color=ACCENT)
    res_name = ft.Text("Ready to Analyze", size=24, weight="w500", color=TEXT_MAIN)
    life_bar = ft.ProgressBar(width=400, height=8, color=ACCENT, bgcolor=BORDER_SOFT, border_radius=4)
    life_text = ft.Text("Journey Progress: --%", size=12, color=TEXT_SECONDARY)

    tiles = [
        DashboardTile("Zodiac Sign", ft.Icons.STARS),
        DashboardTile("Next Birthday", ft.Icons.CAKE),
        DashboardTile("Days Lived", ft.Icons.CALENDAR_TODAY),
        DashboardTile("Total Weeks", ft.Icons.CALENDAR_VIEW_WEEK),
        DashboardTile("Heartbeats", ft.Icons.FAVORITE),
        DashboardTile("Years of Sleep", ft.Icons.BEDTIME)
    ]

    # --- Action Logic ---
    
    def calculate_click(e):
        try:
            btn.content = ft.Text("ANALYZING...", weight="bold")
            page.update()

            name = name_input.value or "Explorer"
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            today = datetime.now()
            
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            perc = min(1.0, age / 80)
            
            res_name.value = f"Hi, {name}"
            res_age.value = str(age)
            life_bar.value = perc
            life_text.value = f"Life Journey Progress: {int(perc*100)}%"
            
            tiles[0].value_label.value = get_zodiac(m, d)
            try:
                nb = date(today.year, m, d)
                if nb < today.date(): nb = date(today.year + 1, m, d)
            except: nb = date(today.year + 1, 3, 1)
            
            tiles[1].value_label.value = f"{(nb - today.date()).days} Days"
            tiles[2].value_label.value = f"{diff.days:,}"
            tiles[3].value_label.value = f"{diff.days // 7:,}"
            tiles[4].value_label.value = f"{diff.days * 24 * 60 * 72:,}"
            tiles[5].value_label.value = f"{int(age * 0.33)} Yrs"

            results_area.visible = True
            btn.content = ft.Text("RUN ANALYSIS", weight="bold")
            page.update()
        except:
            btn.content = ft.Text("RUN ANALYSIS", weight="bold")
            page.snack_bar = ft.SnackBar(ft.Text("Invalid birth date!"))
            page.snack_bar.open = True
            page.update()

    btn = ft.ElevatedButton(
        content=ft.Text("RUN ANALYSIS", weight="bold"),
        on_click=calculate_click,
        height=50,
        width=250,
        style=ft.ButtonStyle(bgcolor=ACCENT, color="white", shape=ft.RoundedRectangleBorder(radius=10))
    )

    # --- Composition ---

    header = ft.Container(
        content=ft.Row([
            ft.Row([ft.Image(src="Age.png", height=30), ft.Text("AgePro", size=20, weight="bold", color=TEXT_MAIN)], spacing=10),
            ft.Text("v2.0 Elite Edition", size=10, color=TEXT_SECONDARY)
        ], alignment="spaceBetween"),
        padding=ft.padding.only(left=60, right=60, top=30, bottom=30),
        border=ft.border.only(bottom=ft.BorderSide(1, BORDER_SOFT))
    )

    input_card = ft.Container(
        content=ft.Column([
            ft.Text("Calculate your life metrics with precision.", size=14, color=TEXT_SECONDARY),
            ft.Container(height=10),
            name_input,
            ft.Row([year_input, month_input, day_input], spacing=20),
            ft.Container(height=20),
            btn
        ], horizontal_alignment="center", spacing=15),
        padding=40,
        bgcolor=BG_WHITE,
        border_radius=24,
        border=ft.border.all(1, BORDER_SOFT),
        shadow=ft.BoxShadow(blur_radius=40, color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK)),
        width=500
    )

    results_area = ft.Column([
        ft.Container(
            content=ft.Column([
                res_name,
                res_age,
                ft.Text("YEARS OLD", size=14, weight="bold", color=TEXT_SECONDARY),
                ft.Container(height=30),
                life_text,
                life_bar
            ], horizontal_alignment="center", spacing=0),
            padding=40,
            margin=ft.margin.only(top=40)
        ),
        ft.ResponsiveRow([
            ft.Column([tiles[0]], col={"sm": 6, "md": 4}),
            ft.Column([tiles[1]], col={"sm": 6, "md": 4}),
            ft.Column([tiles[2]], col={"sm": 6, "md": 4}),
            ft.Column([tiles[3]], col={"sm": 6, "md": 4}),
            ft.Column([tiles[4]], col={"sm": 6, "md": 4}),
            ft.Column([tiles[5]], col={"sm": 6, "md": 4}),
        ], spacing=20, run_spacing=20, width=900)
    ], visible=False, horizontal_alignment="center")

    page.add(
        ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    ft.Container(height=40),
                    input_card,
                    results_area,
                    ft.Container(height=100)
                ], horizontal_alignment="center", scroll="auto"),
                expand=True,
                bgcolor=BG_SUBTLE
            )
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.run(main)
