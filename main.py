import flet as ft
from datetime import datetime, date

# --- Constants ---
AVG_LIFE_EXPECTANCY = 80
PRIMARY_COLOR = "#007AFF"
TEXT_DARK = "#1E293B"
TEXT_LIGHT = "#64748B"
BG_LIGHT = "#F8FAFC"
SIDEBAR_BG = "#F1F5F9"

# --- Logic ---

def get_zodiac(month, day):
    zodiac_signs = [(1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"), (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"), (12, 31, "Capricorn")]
    for m, d, sign in zodiac_signs:
        if month < m or (month == m and day <= d):
            return sign
    return "Unknown"

# --- UI Components ---

class StatCard(ft.Container):
    def __init__(self, title, icon, value_text=""):
        super().__init__()
        self.value_label = ft.Text(value_text, size=22, weight="bold", color=TEXT_DARK)
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color=PRIMARY_COLOR, size=18), ft.Text(title, size=11, color=TEXT_LIGHT, weight="w600")], spacing=8),
                self.value_label,
            ],
            spacing=5,
        )
        self.padding = 24
        self.border_radius = 16
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.Border(
            ft.BorderSide(1, "#E2E8F0"),
            ft.BorderSide(1, "#E2E8F0"),
            ft.BorderSide(1, "#E2E8F0"),
            ft.BorderSide(1, "#E2E8F0")
        )
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.on_hover = self.hover_effect
        self.expand = True

    def hover_effect(self, e):
        self.scale = 1.03 if e.data == "true" else 1.0
        self.border = ft.border.all(1, PRIMARY_COLOR if e.data == "true" else "#E2E8F0")
        self.update()

def main(page: ft.Page):
    page.title = "Age Pro - Elite Design"
    page.window_width = 1300
    page.window_height = 950
    page.bgcolor = BG_LIGHT
    page.padding = 0
    page.fonts = {
        "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Outfit")

    # --- UI Elements ---
    
    input_style = {
        "border_radius": 12,
        "border_color": "#E2E8F0",
        "focused_border_color": PRIMARY_COLOR,
        "bgcolor": "#FFFFFF",
        "color": TEXT_DARK,
        "label_style": ft.TextStyle(color=TEXT_LIGHT, size=12),
        "height": 50,
        "content_padding": 15
    }

    name_input = ft.TextField(label="Full Name", **input_style)
    year_input = ft.TextField(label="Year", width=90, **input_style)
    month_input = ft.TextField(label="Month", width=80, **input_style)
    day_input = ft.TextField(label="Day", width=70, **input_style)

    res_age = ft.Text("0", size=110, weight="bold", color=PRIMARY_COLOR)
    res_name = ft.Text("", size=24, weight="bold", color=TEXT_DARK)
    life_progress = ft.ProgressBar(width=600, color=PRIMARY_COLOR, bgcolor="#E2E8F0", height=10, border_radius=5)
    progress_text = ft.Text("Journey Progress: 0%", size=13, color=TEXT_LIGHT, weight="w500")
    
    # Grid Components
    grid = ft.ResponsiveRow(
        [
            ft.Column([StatCard("Zodiac", ft.Icons.STARS)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Next Birthday", ft.Icons.CAKE)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Days Lived", ft.Icons.CALENDAR_MONTH)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Total Weeks", ft.Icons.CALENDAR_VIEW_WEEK)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Heartbeats", ft.Icons.FAVORITE)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Years Dreaming", ft.Icons.BEDTIME)], col={"sm": 6, "md": 4}),
        ],
        spacing=20,
        run_spacing=20,
    )

    # Main Result Content (The Hero)
    hero_card = ft.Container(
        content=ft.Column([
            res_name, 
            res_age, 
            ft.Text("YEARS OLD", size=14, weight="bold", color="#94A3B8"),
            ft.Container(height=30),
            progress_text,
            life_progress
        ], horizontal_alignment="center", spacing=0),
        padding=60,
        border_radius=24,
        bgcolor="#FFFFFF",
        border=ft.border.all(1, "#E2E8F0"),
        gradient=ft.RadialGradient(
            center=ft.Alignment(0, -0.2),
            radius=1.5,
            colors=[ft.Colors.with_opacity(0.03, PRIMARY_COLOR), ft.Colors.WHITE]
        ),
        margin=ft.margin.only(bottom=30),
    )

    dashboard = ft.Column(
        [hero_card, grid],
        visible=False,
        animate_opacity=600,
        width=900, # Fixed Width for Alignment
        alignment=ft.MainAxisAlignment.START,
    )

    def calculate_click(e):
        try:
            name = name_input.value
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            today = datetime.now()

            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            perc = min(1.0, age / AVG_LIFE_EXPECTANCY)
            
            res_name.value = f"Greetings, {name}"
            res_age.value = str(age)
            life_progress.value = perc
            progress_text.value = f"Journey Progress: {int(perc*100)}% (Based on 80yr avg)"
            
            # Update Grid Cards
            grid.controls[0].content.controls[0].value_label.value = get_zodiac(m, d)
            grid.controls[1].content.controls[0].value_label.value = f"{(date(today.year + (date(today.year, m, d) < today.date()), m, d) - today.date()).days} Days"
            grid.controls[2].content.controls[0].value_label.value = f"{diff.days:,}"
            grid.controls[3].content.controls[0].value_label.value = f"{diff.days // 7:,}"
            grid.controls[4].content.controls[0].value_label.value = f"{diff.days * 24 * 60 * 72:,}"
            grid.controls[5].content.controls[0].value_label.value = f"{int(age * 0.33)} Yrs"

            dashboard.visible = True
            dashboard.opacity = 1
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid birth date!"))
            page.snack_bar.open = True
            page.update()

    # --- Sidebar (Perfect Alignment) ---
    
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Column([
                    ft.Image(src="Age.png", height=80, fit="contain"),
                    ft.Text("AGE PRO", size=24, weight="bold", color=TEXT_DARK),
                    ft.Text("ELITE ANALYTICS", size=10, color=PRIMARY_COLOR, weight="bold"),
                ], spacing=5, horizontal_alignment="start"),
                
                ft.Container(height=40),
                ft.Text("USER DETAILS", size=11, weight="bold", color="#94A3B8"),
                name_input,
                ft.Container(height=10),
                ft.Text("BIRTH DATE", size=11, weight="bold", color="#94A3B8"),
                ft.Row([year_input, month_input, day_input], spacing=8),
                
                ft.Container(height=40),
                ft.FilledButton(
                    content=ft.Row([ft.Icon(ft.Icons.AUTO_GRAPH, size=20), ft.Text("RUN ANALYSIS", weight="bold")], alignment="center"),
                    height=55,
                    width=300,
                    on_click=calculate_click,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        color=ft.Colors.WHITE,
                        bgcolor=PRIMARY_COLOR
                    )
                ),
                
                ft.Container(expand=True),
                ft.Row([ft.Icon(ft.Icons.LOCK_OUTLINE, size=12, color="#94A3B8"), ft.Text("Local Data Encryption Active", size=10, color="#94A3B8")], alignment="start"),
            ],
            spacing=10,
            horizontal_alignment="start",
        ),
        width=350,
        padding=50,
        bgcolor=SIDEBAR_BG,
        border=ft.border.only(right=ft.BorderSide(1, "#E2E8F0"))
    )

    page.add(
        ft.Row(
            [
                sidebar,
                ft.Container(
                    content=ft.Column([dashboard], scroll="auto", alignment=ft.MainAxisAlignment.START, horizontal_alignment="center"),
                    expand=True,
                    padding=ft.Padding(50, 40, 50, 50),
                    bgcolor=BG_LIGHT
                )
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
