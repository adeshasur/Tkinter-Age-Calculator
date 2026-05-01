import flet as ft
from datetime import datetime, date, timedelta
import math

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
        self.value_label = ft.Text(value_text, size=26, weight="bold", color=ft.Colors.WHITE)
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color=ft.Colors.CYAN_400, size=20), ft.Text(title, size=12, color=ft.Colors.BLUE_GREY_400, weight="w600", font_family="SF Pro Text")], spacing=10),
                self.value_label,
            ],
            spacing=5,
        )
        self.padding = 25
        self.border_radius = 24
        self.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
        self.border = ft.Border(
            ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE))
        )
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.on_hover = self.hover_effect
        self.expand = True

    def hover_effect(self, e):
        self.scale = 1.05 if e.data == "true" else 1.0
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE) if e.data == "true" else ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
        self.update()

def main(page: ft.Page):
    page.title = "Age Pro - Elite Analytics"
    page.window_width = 1200
    page.window_height = 900
    page.bgcolor = "#050810"
    page.padding = 0
    page.fonts = {
        "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Outfit")

    # --- UI Elements ---
    
    name_input = ft.TextField(label="Full Name", border_radius=15, border_color=ft.Colors.BLUE_GREY_800, focused_border_color=ft.Colors.CYAN_400, label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500))
    year_input = ft.TextField(label="Year", border_radius=15, width=110, border_color=ft.Colors.BLUE_GREY_800)
    month_input = ft.TextField(label="Month", border_radius=15, width=100, border_color=ft.Colors.BLUE_GREY_800)
    day_input = ft.TextField(label="Day", border_radius=15, width=90, border_color=ft.Colors.BLUE_GREY_800)

    res_age = ft.Text("0", size=120, weight="bold", color=ft.Colors.CYAN_400)
    res_name = ft.Text("", size=28, weight="bold", color=ft.Colors.WHITE)
    life_progress = ft.ProgressBar(width=400, color=ft.Colors.CYAN_400, bgcolor=ft.Colors.BLUE_GREY_900, height=8, border_radius=5)
    progress_text = ft.Text("Life Journey Progress: 0%", size=14, color=ft.Colors.BLUE_GREY_400)
    
    card_zodiac = StatCard("Zodiac Sign", ft.Icons.STARS)
    card_days = StatCard("Days Lived", ft.Icons.CALENDAR_MONTH)
    card_hearts = StatCard("Heartbeats", ft.Icons.FAVORITE)
    card_weeks = StatCard("Total Weeks", ft.Icons.CALENDAR_VIEW_WEEK)
    card_sleep = StatCard("Years Dreaming", ft.Icons.BEDTIME)
    card_next = StatCard("Next Birthday", ft.Icons.CAKE)

    dashboard = ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    res_name, 
                    res_age, 
                    ft.Text("YEARS OLD", size=16, weight="bold", color=ft.Colors.BLUE_GREY_500, letter_spacing=2),
                    ft.Divider(height=40, color="transparent"),
                    progress_text,
                    life_progress
                ], horizontal_alignment="center", spacing=0),
                padding=60,
                border_radius=40,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.with_opacity(0.1, ft.Colors.CYAN_700), ft.Colors.with_opacity(0.02, ft.Colors.BLACK)]
                ),
                border=ft.Border(
                    ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.CYAN_400)),
                    ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.CYAN_400)),
                    ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.CYAN_400)),
                    ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.CYAN_400))
                ),
                margin=ft.Margin(0, 0, 0, 30)
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
                spacing=25,
                run_spacing=25,
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
            progress_text.value = f"Life Journey Progress: {int(perc*100)}% (Based on 80yr avg)"
            
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
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid birth date. Please check!"))
            page.snack_bar.open = True
            page.update()

    # --- Layout Assembly ---
    
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="Age.png", height=100, fit="contain"),
                ft.Text("AGE PRO", size=28, weight="bold", color=ft.Colors.WHITE, letter_spacing=1),
                ft.Text("ELITE ANALYTICS ENGINE", size=10, color=ft.Colors.CYAN_400, weight="bold", letter_spacing=2),
                ft.Divider(height=60, color=ft.Colors.BLUE_GREY_900),
                name_input,
                ft.Row([year_input, month_input, day_input], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(padding=10), # Spacer
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.AUTO_GRAPH), ft.Text("RUN ANALYSIS", weight="bold")], alignment="center"),
                    bgcolor=ft.Colors.CYAN_700, 
                    color=ft.Colors.WHITE, 
                    height=60, 
                    on_click=calculate_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
                ft.Container(expand=True),
                ft.Text("F11 for Focus Mode", size=11, color=ft.Colors.BLUE_GREY_600),
            ],
            spacing=15,
            horizontal_alignment="center",
        ),
        width=400,
        padding=50,
        bgcolor="#0B1120",
        border_radius=0,
    )

    page.add(
        ft.Row(
            [
                sidebar,
                ft.Container(
                    content=ft.Column([dashboard], expand=True, scroll="auto", alignment="start"),
                    expand=True,
                    padding=60,
                    gradient=ft.RadialGradient(
                        center=ft.Alignment(0, -0.5),
                        radius=1.5,
                        colors=["#0D1525", "#050810"]
                    )
                )
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
