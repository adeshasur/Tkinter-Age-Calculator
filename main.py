import flet as ft
from datetime import datetime, date, timedelta

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
        self.value_label = ft.Text(value_text, size=24, weight="bold", color=ft.Colors.WHITE)
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color=ft.Colors.BLUE_400, size=20), ft.Text(title, size=12, color=ft.Colors.BLUE_GREY_200, weight="w500")], spacing=10),
                self.value_label,
            ],
            spacing=5,
        )
        self.padding = 20
        self.border_radius = 20
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY_900)
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE))
        self.expand = True

def main(page: ft.Page):
    page.title = "Age Pro - Ultimate UX"
    page.window_width = 1100
    page.window_height = 800
    page.bgcolor = "#0B1120"
    page.padding = 40
    page.fonts = {
        "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Outfit")

    # App State
    birth_date_ref = {"val": None}

    # --- UI Elements ---
    
    # Left Column: Input Card
    name_input = ft.TextField(label="Full Name", border_radius=15, border_color=ft.Colors.BLUE_GREY_700, focused_border_color=ft.Colors.BLUE_400, label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_400))
    year_input = ft.TextField(label="Year", border_radius=15, width=100, border_color=ft.Colors.BLUE_GREY_700)
    month_input = ft.TextField(label="Month", border_radius=15, width=80, border_color=ft.Colors.BLUE_GREY_700)
    day_input = ft.TextField(label="Day", border_radius=15, width=80, border_color=ft.Colors.BLUE_GREY_700)

    # Result Labels
    res_age = ft.Text("0", size=100, weight="bold", color=ft.Colors.BLUE_400)
    res_name = ft.Text("", size=24, weight="w500", color=ft.Colors.WHITE)
    
    # Stats Grid
    card_zodiac = StatCard("Zodiac Sign", ft.Icons.STARS)
    card_days = StatCard("Days Lived", ft.Icons.CALENDAR_MONTH)
    card_hearts = StatCard("Est. Heartbeats", ft.Icons.FAVORITE)
    card_weeks = StatCard("Weeks Lived", ft.Icons.CALENDAR_VIEW_WEEK)
    card_sleep = StatCard("Years Asleep", ft.Icons.BEDTIME)
    card_next = StatCard("Next Birthday", ft.Icons.CAKE)

    # Dashboard Container
    dashboard = ft.Column(
        [
            ft.Container(
                content=ft.Column([res_name, res_age, ft.Text("Years of wisdom and growth.", color=ft.Colors.BLUE_GREY_400)], horizontal_alignment="center", spacing=0),
                padding=40,
                border_radius=30,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_400),
                border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.BLUE_400)),
                margin=ft.margin.only(bottom=20)
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
        animate_opacity=300
    )

    def calculate_click(e):
        try:
            name = name_input.value
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            birth_date_ref["val"] = birth
            today = datetime.now()

            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            
            # Update Dashboard
            res_name.value = f"Welcome, {name}"
            res_age.value = str(age)
            
            card_zodiac.value_label.value = get_zodiac(m, d)
            card_days.value_label.value = f"{diff.days:,}"
            card_hearts.value_label.value = f"{diff.days * 24 * 60 * 72:,}"
            card_weeks.value_label.value = f"{diff.days // 7:,}"
            card_sleep.value_label.value = f"{age // 3} Yrs"
            
            next_b = date(today.year, m, d)
            if next_b < today.date(): next_b = date(today.year + 1, m, d)
            card_next.value_label.value = f"{(next_b - today.date()).days} Days"

            dashboard.visible = True
            dashboard.opacity = 1
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid birth date!"))
            page.snack_bar.open = True
            page.update()

    # --- Layout Assembly ---
    
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="Age.png", height=80, fit="contain"),
                ft.Text("AGE PRO", size=24, weight="bold", color=ft.Colors.WHITE),
                ft.Divider(height=40, color=ft.Colors.BLUE_GREY_800),
                name_input,
                ft.Row([year_input, month_input, day_input], spacing=10),
                ft.ElevatedButton("Run Analysis", icon=ft.Icons.AUTO_GRAPH, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, height=55, on_click=calculate_click),
                ft.Text("Press F11 for Full Screen", size=10, color=ft.Colors.BLUE_GREY_600),
            ],
            spacing=20,
            horizontal_alignment="center",
        ),
        width=350,
        padding=40,
        bgcolor="#111827",
        border_radius=30,
    )

    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=20, color="transparent"),
                ft.Column([dashboard], expand=True, scroll="auto")
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
