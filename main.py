import flet as ft
from datetime import datetime, date

# --- Global Style Config ---
ACCENT = "#007AFF"
BG_WHITE = "#FFFFFF"
BG_PANEL = "#FBFBFC"
TEXT_MAIN = "#1D1D1F"
TEXT_SECONDARY = "#86868B"
BORDER_COLOR = "#F2F2F7"

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

class AnalyticsCard(ft.Container):
    def __init__(self, title, icon, value_text="--"):
        super().__init__()
        self.value_label = ft.Text(value_text, size=20, weight="bold", color=TEXT_MAIN)
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color=ACCENT, size=14), ft.Text(title, size=10, color=TEXT_SECONDARY, weight="w500")], spacing=6),
                self.value_label,
            ],
            spacing=2,
        )
        self.padding = 18
        self.border_radius = 12
        self.bgcolor = BG_WHITE
        self.border = ft.border.all(1, BORDER_COLOR)
        self.shadow = ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.01, ft.Colors.BLACK), offset=ft.Offset(0, 2))
        self.expand = True

def main(page: ft.Page):
    page.title = "AgePro Pro - Split Design"
    page.bgcolor = BG_WHITE
    page.padding = 0
    page.window_width = 1300
    page.window_height = 900
    page.fonts = {"Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"}
    page.theme = ft.Theme(font_family="Outfit")

    # --- Left Panel: Input Section ---
    
    input_style = {
        "border_radius": 8,
        "border_color": BORDER_COLOR,
        "focused_border_color": ACCENT,
        "bgcolor": BG_PANEL,
        "color": TEXT_MAIN,
        "label_style": ft.TextStyle(color=TEXT_SECONDARY, size=11),
        "height": 45,
        "content_padding": 12
    }

    name_input = ft.TextField(label="Full Name", **input_style)
    year_input = ft.TextField(label="Year", expand=True, **input_style)
    month_input = ft.TextField(label="Month", expand=True, **input_style)
    day_input = ft.TextField(label="Day", expand=True, **input_style)

    # --- Right Panel: Results Area ---
    
    res_age = ft.Text("0", size=150, weight="bold", color=ACCENT)
    res_name = ft.Text("Analytics Ready", size=26, weight="bold", color=TEXT_MAIN)
    life_bar = ft.ProgressBar(width=400, height=8, color=ACCENT, bgcolor=BORDER_COLOR, border_radius=4, value=0)
    life_text = ft.Text("Life Journey Progress: --%", size=12, color=TEXT_SECONDARY)

    cards = [
        AnalyticsCard("Zodiac Sign", ft.Icons.STARS),
        AnalyticsCard("Next Birthday", ft.Icons.CAKE),
        AnalyticsCard("Days Lived", ft.Icons.CALENDAR_MONTH),
        AnalyticsCard("Total Weeks", ft.Icons.CALENDAR_VIEW_WEEK),
        AnalyticsCard("Heartbeats", ft.Icons.FAVORITE),
        AnalyticsCard("Sleep & Dreams", ft.Icons.BEDTIME)
    ]

    grid = ft.ResponsiveRow([
        ft.Column([cards[0]], col={"sm": 6, "md": 4}),
        ft.Column([cards[1]], col={"sm": 6, "md": 4}),
        ft.Column([cards[2]], col={"sm": 6, "md": 4}),
        ft.Column([cards[3]], col={"sm": 6, "md": 4}),
        ft.Column([cards[4]], col={"sm": 6, "md": 4}),
        ft.Column([cards[5]], col={"sm": 6, "md": 4}),
    ], spacing=15, run_spacing=15)

    def calculate_click(e):
        try:
            name = name_input.value or "User"
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
            
            cards[0].value_label.value = get_zodiac(m, d)
            try:
                nb = date(today.year, m, d)
                if nb < today.date(): nb = date(today.year + 1, m, d)
            except: nb = date(today.year + 1, 3, 1)
            
            cards[1].value_label.value = f"{(nb - today.date()).days} Days"
            cards[2].value_label.value = f"{diff.days:,}"
            cards[3].value_label.value = f"{diff.days // 7:,}"
            cards[4].value_label.value = f"{diff.days * 24 * 60 * 72:,}"
            cards[5].value_label.value = f"{int(age * 0.33)} Yrs"

            results_container.opacity = 1
            results_container.visible = True
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Check your date format!"))
            page.snack_bar.open = True
            page.update()

    # --- UI Layout Assembly ---

    left_panel = ft.Container(
        content=ft.Column([
            ft.Row([ft.Image(src="Age.png", height=35), ft.Text("AgePro", size=22, weight="bold", color=TEXT_MAIN)], spacing=10),
            ft.Container(height=40),
            ft.Text("USER INFORMATION", size=10, weight="bold", color=TEXT_SECONDARY),
            name_input,
            ft.Container(height=15),
            ft.Text("DATE OF BIRTH", size=10, weight="bold", color=TEXT_SECONDARY),
            ft.Row([year_input, month_input, day_input], spacing=10),
            ft.Container(height=30),
            ft.ElevatedButton(
                text="ANALYZE NOW",
                on_click=calculate_click,
                height=50,
                width=float("inf"),
                style=ft.ButtonStyle(bgcolor=ACCENT, color="white", shape=ft.RoundedRectangleBorder(radius=8))
            ),
            ft.Container(expand=True),
            ft.Text("Developed by Tunix Elite", size=10, color=TEXT_SECONDARY)
        ], spacing=10),
        width=400,
        padding=50,
        bgcolor=BG_PANEL,
        border=ft.border.only(right=ft.BorderSide(1, BORDER_COLOR))
    )

    results_container = ft.Column([
        ft.Container(
            content=ft.Column([
                res_name,
                res_age,
                ft.Text("YEARS OLD", size=14, weight="bold", color=TEXT_SECONDARY, letter_spacing=2),
                ft.Container(height=20),
                life_text,
                life_bar
            ], horizontal_alignment="center", spacing=0),
            padding=40,
        ),
        ft.Container(padding=ft.padding.only(left=40, right=40), content=grid)
    ], expand=True, visible=False, animate_opacity=400)

    page.add(
        ft.Row([
            left_panel,
            ft.Container(
                content=results_container,
                expand=True,
                bgcolor=BG_WHITE,
                padding=40
            )
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.run(main)
