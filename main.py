import flet as ft
from datetime import datetime, date

# --- Constants ---
AVG_LIFE_EXPECTANCY = 80

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
        self.value_label = ft.Text(value_text, size=24, weight="bold", color="#1E293B")
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color="#007AFF", size=18), ft.Text(title, size=11, color="#64748B", weight="w600")], spacing=8),
                self.value_label,
            ],
            spacing=5,
        )
        self.padding = 20
        self.border_radius = 20
        self.bgcolor = ft.Colors.WHITE
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        )
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.on_hover = self.hover_effect
        self.expand = True

    def hover_effect(self, e):
        self.scale = 1.05 if e.data == "true" else 1.0
        self.shadow.blur_radius = 20 if e.data == "true" else 10
        self.update()

def main(page: ft.Page):
    page.title = "Age Pro - Elite Design"
    page.window_width = 1200
    page.window_height = 900
    page.bgcolor = "#F8FAFC"
    page.padding = 0
    page.fonts = {
        "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Outfit")

    # --- UI Elements ---
    
    input_style = {
        "border_radius": 15,
        "border_color": "#E2E8F0",
        "focused_border_color": "#007AFF",
        "bgcolor": "#FFFFFF",
        "color": "#1E293B",
        "label_style": ft.TextStyle(color="#64748B")
    }

    name_input = ft.TextField(label="Full Name", **input_style)
    year_input = ft.TextField(label="Year", width=110, **input_style)
    month_input = ft.TextField(label="Month", width=100, **input_style)
    day_input = ft.TextField(label="Day", width=90, **input_style)

    res_age = ft.Text("0", size=100, weight="bold", color="#007AFF")
    res_name = ft.Text("", size=24, weight="bold", color="#1E293B")
    life_progress = ft.ProgressBar(width=350, color="#007AFF", bgcolor="#E2E8F0", height=6, border_radius=5)
    progress_text = ft.Text("Journey Progress: 0%", size=12, color="#64748B")
    
    card_zodiac = StatCard("Zodiac", ft.Icons.STARS)
    card_days = StatCard("Days", ft.Icons.CALENDAR_MONTH)
    card_hearts = StatCard("Heartbeats", ft.Icons.FAVORITE)
    card_weeks = StatCard("Weeks", ft.Icons.CALENDAR_VIEW_WEEK)
    card_sleep = StatCard("Dreaming", ft.Icons.BEDTIME)
    card_next = StatCard("Next Birthday", ft.Icons.CAKE)

    # Dashboard Container
    dashboard = ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    res_name, 
                    res_age, 
                    ft.Text("YEARS OLD", size=14, weight="bold", color="#94A3B8"),
                    ft.Divider(height=20, color="transparent"),
                    progress_text,
                    life_progress
                ], horizontal_alignment="center", spacing=0),
                padding=35,
                border_radius=30,
                bgcolor="#FFFFFF",
                gradient=ft.RadialGradient(
                    center=ft.Alignment(0, 0),
                    radius=2,
                    colors=[ft.Colors.with_opacity(0.05, "#007AFF"), ft.Colors.WHITE]
                ),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                    offset=ft.Offset(0, 8),
                ),
                margin=ft.Margin(0, 0, 0, 20),
                animate_scale=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT)
            ),
            ft.ResponsiveRow(
                [
                    ft.Column([card_zodiac], col={"sm": 6, "md": 4}),
                    ft.Column([card_next], col={"sm": 6, "md": 4}),
                    ft.Column([card_days], col={"sm": 6, "md": 4}),
                    ft.Column([card_weeks], col={"sm": 6, "md": 4}),
                    ft.Column([card_hearts], col={"sm": 6, "md": 4}),
                    ft.Column([card_sleep], col={"sm": 6, "md": 4}),
                ],
                spacing=20,
                run_spacing=20,
            )
        ],
        visible=False,
        animate_opacity=600,
        expand=True
    )

    def calculate_click(e):
        try:
            name = name_input.value
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            today = datetime.now()

            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            
            # Calculations
            perc = min(1.0, age / AVG_LIFE_EXPECTANCY)
            
            res_name.value = f"Greetings, {name}"
            res_age.value = str(age)
            life_progress.value = perc
            progress_text.value = f"Journey Progress: {int(perc*100)}% (Based on 80yr avg)"
            
            card_zodiac.value_label.value = get_zodiac(m, d)
            card_days.value_label.value = f"{diff.days:,}"
            card_hearts.value_label.value = f"{diff.days * 24 * 60 * 72:,}"
            card_weeks.value_label.value = f"{diff.days // 7:,}"
            card_sleep.value_label.value = f"{int(age * 0.33)} Yrs"
            
            next_b = date(today.year, m, d)
            if next_b < today.date(): next_b = date(today.year + 1, m, d)
            card_next.value_label.value = f"{(next_b - today.date()).days} Days"

            dashboard.visible = True
            dashboard.opacity = 1
            dashboard.controls[0].scale = 1.02
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid date!"))
            page.snack_bar.open = True
            page.update()

    # --- Sidebar Assembly ---
    
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="Age.png", height=100, fit="contain"),
                ft.Text("AGE PRO", size=26, weight="bold", color="#1E293B"),
                ft.Text("ELITE ANALYTICS ENGINE", size=10, color="#007AFF", weight="bold"),
                ft.Divider(height=40, color="#F1F5F9"),
                name_input,
                ft.Row([year_input, month_input, day_input], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(padding=10),
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.AUTO_GRAPH), ft.Text("RUN ANALYSIS", weight="bold")], alignment="center"),
                    bgcolor="#007AFF", 
                    color=ft.Colors.WHITE, 
                    height=60, 
                    on_click=calculate_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
                ft.Container(expand=True),
                ft.Text("F11 for Focus Mode", size=11, color="#94A3B8"),
            ],
            spacing=15,
            horizontal_alignment="center",
        ),
        width=400,
        padding=40,
        bgcolor="#F1F5F9",
    )

    page.add(
        ft.Row(
            [
                sidebar,
                ft.Container(
                    content=ft.Column([dashboard], expand=True, scroll="auto", alignment="start"),
                    expand=True,
                    # REDUCED TOP PADDING TO MOVE IT UP
                    padding=ft.padding.only(left=40, top=10, right=40, bottom=40),
                    bgcolor="#F8FAFC"
                )
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
