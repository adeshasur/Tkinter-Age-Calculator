import flet as ft
from datetime import datetime, date

# --- Design Language ---
ACCENT = "#007AFF"
SIDEBAR_BG = "#1A1C1E" # Deep Pro Charcoal
MAIN_BG = "#F5F7FA"
CARD_BG = "#FFFFFF"
TEXT_HEADING = "#111827"
TEXT_BODY = "#4B5563"
BORDER_COLOR = "#E5E7EB"

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
        self.value_label = ft.Text(value_text, size=24, weight="bold", color=TEXT_HEADING)
        self.content = ft.Column(
            [
                ft.Row([ft.Icon(icon, color=ACCENT, size=16), ft.Text(title, size=12, color=TEXT_BODY, weight="w500")], spacing=8),
                self.value_label,
            ],
            spacing=8,
        )
        self.padding = 24
        self.border_radius = 16
        self.bgcolor = CARD_BG
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        )
        self.border = ft.border.all(1, BORDER_COLOR)
        self.animate_scale = ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK)
        self.on_hover = self.hover_effect
        self.expand = True

    def hover_effect(self, e):
        self.scale = 1.04 if e.data == "true" else 1.0
        self.border = ft.border.all(1, ACCENT if e.data == "true" else BORDER_COLOR)
        self.shadow.blur_radius = 25 if e.data == "true" else 15
        self.update()

def main(page: ft.Page):
    page.title = "Age Pro - Elite Design"
    page.window_width = 1300
    page.window_height = 950
    page.bgcolor = MAIN_BG
    page.padding = 0
    page.fonts = {
        "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Outfit")

    # --- Sidebar Inputs ---
    
    input_style = {
        "border_radius": 10,
        "border_color": "#374151",
        "focused_border_color": ACCENT,
        "bgcolor": "#2D2F36",
        "color": ft.Colors.WHITE,
        "label_style": ft.TextStyle(color="#9CA3AF", size=12),
        "height": 48,
        "content_padding": 12,
        "cursor_color": ACCENT
    }

    name_input = ft.TextField(label="Full Name", **input_style)
    year_input = ft.TextField(label="Year", width=100, **input_style)
    month_input = ft.TextField(label="Month", width=80, **input_style)
    day_input = ft.TextField(label="Day", width=70, **input_style)

    # --- Dashboard Elements ---
    
    res_age = ft.Text("0", size=120, weight="bold", color=ACCENT)
    res_name = ft.Text("", size=28, weight="bold", color=TEXT_HEADING)
    life_progress = ft.ProgressBar(width=600, color=ACCENT, bgcolor="#E5E7EB", height=10, border_radius=5)
    progress_text = ft.Text("Journey Progress: 0%", size=14, color=TEXT_BODY, weight="w500")
    
    grid = ft.ResponsiveRow(
        [
            ft.Column([StatCard("Zodiac Sign", ft.Icons.STARS)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Next Birthday", ft.Icons.CAKE)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Total Days", ft.Icons.CALENDAR_MONTH)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Total Weeks", ft.Icons.CALENDAR_VIEW_WEEK)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Heartbeats", ft.Icons.FAVORITE)], col={"sm": 6, "md": 4}),
            ft.Column([StatCard("Sleep & Dreams", ft.Icons.BEDTIME)], col={"sm": 6, "md": 4}),
        ],
        spacing=24,
        run_spacing=24,
    )

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
        border_radius=32,
        bgcolor=CARD_BG,
        border=ft.border.all(1, BORDER_COLOR),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=30,
            color=ft.Colors.with_opacity(0.03, ft.Colors.BLACK),
            offset=ft.Offset(0, 10),
        ),
        margin=ft.margin.only(bottom=40),
    )

    dashboard = ft.Column(
        [hero_card, grid],
        visible=False,
        animate_opacity=600,
        scroll="auto",
        alignment=ft.MainAxisAlignment.START,
    )

    def calculate_click(e):
        try:
            name = name_input.value or "Explorer"
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            today = datetime.now()

            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            perc = min(1.0, age / AVG_LIFE_EXPECTANCY)
            
            res_name.value = f"Greetings, {name}"
            res_age.value = str(age)
            life_progress.value = perc
            progress_text.value = f"Life Journey Progress: {int(perc*100)}% (Based on 80yr avg)"
            
            # Update Grid
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
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid date!"))
            page.snack_bar.open = True
            page.update()

    # --- Dark Sidebar (Pro Aesthetic) ---
    
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Image(src="Age.png", height=70, fit="contain"),
                        ft.Text("AgePro", size=24, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("ELITE ANALYTICS ENGINE", size=9, color=ACCENT, weight="bold"),
                    ], horizontal_alignment="start", spacing=5),
                    margin=ft.margin.only(bottom=40)
                ),
                
                ft.Text("PROFILE SETTINGS", size=10, weight="bold", color="#6B7280"),
                name_input,
                ft.Container(height=10),
                ft.Text("BIRTH DATE", size=10, weight="bold", color="#6B7280"),
                ft.Row([year_input, month_input, day_input], spacing=8),
                
                ft.Container(height=40),
                ft.FilledButton(
                    content=ft.Row([ft.Icon(ft.Icons.AUTO_GRAPH, size=20), ft.Text("RUN ANALYSIS", weight="bold")], alignment="center"),
                    height=52,
                    on_click=calculate_click,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        color=ft.Colors.WHITE,
                        bgcolor=ACCENT
                    )
                ),
                
                ft.Container(expand=True),
                ft.Row([ft.Icon(ft.Icons.SECURITY, size=12, color="#4B5563"), ft.Text("Privacy Shield Active", size=10, color="#4B5563")], alignment="start"),
            ],
            spacing=12,
        ),
        width=300,
        padding=40,
        bgcolor=SIDEBAR_BG,
    )

    # --- Main Layout ---
    
    page.add(
        ft.Row(
            [
                sidebar,
                ft.Container(
                    content=ft.Column([dashboard], alignment=ft.MainAxisAlignment.START, horizontal_alignment="center"),
                    expand=True,
                    padding=ft.Padding(60, 40, 60, 60),
                    bgcolor=MAIN_BG
                )
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
