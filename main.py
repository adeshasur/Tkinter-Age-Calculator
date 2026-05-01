import flet as ft
from datetime import datetime, date

# --- Global Style Config ---
ACCENT = "#007AFF"
ACCENT_LIGHT = "#5AC8FA"
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
    def __init__(self, title, icon, color, value_text="--"):
        super().__init__()
        self.value_label = ft.Text(value_text, size=24, weight="bold", color=TEXT_MAIN)
        self.content = ft.Column(
            [
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=16),
                        padding=8,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                        border_radius=10
                    ),
                    ft.Text(title, size=10, color=TEXT_SECONDARY, weight="w700")
                ], spacing=10),
                ft.Container(height=5),
                self.value_label,
            ],
            spacing=0,
        )
        self.padding = 24
        self.border_radius = 24
        self.bgcolor = BG_WHITE
        self.border = ft.border.all(1, BORDER_COLOR)
        self.shadow = ft.BoxShadow(spread_radius=0, blur_radius=25, color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK), offset=ft.Offset(0, 8))
        self.animate_scale = ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK)
        self.on_hover = self.toggle_hover
        self.expand = True

    def toggle_hover(self, e):
        self.scale = 1.05 if e.data == "true" else 1.0
        self.border = ft.border.all(1, ACCENT if e.data == "true" else BORDER_COLOR)
        self.update()

def main(page: ft.Page):
    page.title = "AgePro Pro - Elite Dashboard"
    page.bgcolor = BG_WHITE
    page.padding = 0
    page.window_width = 1350
    page.window_height = 950
    page.fonts = {"Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"}
    page.theme = ft.Theme(font_family="Outfit")

    # --- Left Panel: Input Section ---
    
    input_style = {
        "border_radius": 12,
        "border_color": BORDER_COLOR,
        "focused_border_color": ACCENT,
        "bgcolor": BG_PANEL,
        "color": TEXT_MAIN,
        "label_style": ft.TextStyle(color=TEXT_SECONDARY, size=12),
        "height": 52,
        "content_padding": 15
    }

    name_input = ft.TextField(label="Full Name", **input_style)
    year_input = ft.TextField(label="Year", expand=True, **input_style)
    month_input = ft.TextField(label="Month", expand=True, **input_style)
    day_input = ft.TextField(label="Day", expand=True, **input_style)

    # --- Right Panel: Analytics Dashboard ---
    
    res_age = ft.Text("0", size=150, weight="bold", color=TEXT_MAIN)
    res_name = ft.Text("Ready to Analyze", size=32, weight="bold", color=TEXT_MAIN)
    
    progress_fill = ft.Container(
        width=0, height=24,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0), colors=[ACCENT, ACCENT_LIGHT]),
        border_radius=12,
        animate=ft.Animation(1000, ft.AnimationCurve.EASE_OUT_QUART)
    )
    
    progress_track = ft.Container(
        content=ft.Stack([progress_fill]),
        width=550, height=24, bgcolor="#F2F2F7", border_radius=12,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 5))
    )
    
    life_text = ft.Text("LIFE JOURNEY PROGRESS: --%", size=11, color=TEXT_SECONDARY, weight="bold")

    cards = [
        AnalyticsCard("ZODIAC SIGN", ft.Icons.STARS, "#F59E0B"),
        AnalyticsCard("NEXT BIRTHDAY", ft.Icons.CAKE, "#EC4899"),
        AnalyticsCard("DAYS LIVED", ft.Icons.CALENDAR_MONTH, "#3B82F6"),
        AnalyticsCard("TOTAL WEEKS", ft.Icons.CALENDAR_VIEW_WEEK, "#8B5CF6"),
        AnalyticsCard("HEARTBEATS", ft.Icons.FAVORITE, "#EF4444"),
        AnalyticsCard("SLEEP & DREAMS", ft.Icons.BEDTIME, "#10B981")
    ]

    grid = ft.ResponsiveRow([
        ft.Column([cards[0]], col={"sm": 6, "md": 4}),
        ft.Column([cards[1]], col={"sm": 6, "md": 4}),
        ft.Column([cards[2]], col={"sm": 6, "md": 4}),
        ft.Column([cards[3]], col={"sm": 6, "md": 4}),
        ft.Column([cards[4]], col={"sm": 6, "md": 4}),
        ft.Column([cards[5]], col={"sm": 6, "md": 4}),
    ], spacing=25, run_spacing=25)

    def calculate_click(e):
        try:
            name = name_input.value or "Explorer"
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            today = datetime.now()
            
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            perc = min(1.0, age / 80)
            
            res_name.value = f"Hi, {name}"
            res_age.value = str(age)
            progress_fill.width = 550 * perc
            life_text.value = f"LIFE JOURNEY PROGRESS: {int(perc*100)}%"
            
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

            results_container.visible = True
            results_container.opacity = 1
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid birth date!"))
            page.snack_bar.open = True
            page.update()

    # --- UI Layout Assembly ---

    left_panel = ft.Container(
        content=ft.Column([
            ft.Column([
                ft.Text("AgePro", size=34, weight="bold", color=TEXT_MAIN),
                ft.Image(src="Age.png", height=85, fit="contain"),
            ], horizontal_alignment="center", spacing=10),
            ft.Container(height=50),
            ft.Text("MEMBER PROFILE", size=10, weight="bold", color=TEXT_SECONDARY),
            name_input,
            ft.Container(height=15),
            ft.Text("BIRTH REGISTRY", size=10, weight="bold", color=TEXT_SECONDARY),
            ft.Row([year_input, month_input, day_input], spacing=10),
            ft.Container(height=40),
            ft.ElevatedButton(
                content=ft.Text("GENERATE INSIGHTS", weight="bold"),
                on_click=calculate_click,
                height=60,
                width=float("inf"),
                style=ft.ButtonStyle(bgcolor=ACCENT, color="white", shape=ft.RoundedRectangleBorder(radius=15))
            ),
            ft.Container(expand=True),
            ft.Row([ft.Text("Crafted by Adheesha Sooriyaarachchi", size=10, color=TEXT_SECONDARY, italic=True)], alignment="center")
        ], spacing=10, horizontal_alignment="center"),
        width=440,
        padding=60,
        bgcolor=BG_PANEL,
        border=ft.border.only(right=ft.BorderSide(1, BORDER_COLOR))
    )

    hero_section = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.AUTO_GRAPH, color=ACCENT, size=16), ft.Text("LIVE ANALYTICS ENGINE", size=11, color=ACCENT, weight="bold")], alignment="center"),
                bgcolor=ft.Colors.with_opacity(0.05, ACCENT),
                padding=ft.padding.symmetric(12, 20),
                border_radius=30,
            ),
            ft.Container(height=10),
            res_name,
            res_age,
            ft.Text("YEARS OLD", size=14, weight="bold", color=TEXT_SECONDARY),
            ft.Container(height=40),
            life_text,
            progress_track
        ], horizontal_alignment="center", spacing=0),
        padding=60,
        border_radius=40,
        bgcolor="#FFFFFF",
        border=ft.border.all(1, BORDER_COLOR),
        shadow=ft.BoxShadow(blur_radius=60, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 20)),
        margin=ft.margin.only(bottom=50)
    )

    results_container = ft.Column([
        hero_section,
        ft.Container(padding=ft.padding.only(left=10, right=10), content=grid)
    ], expand=True, visible=False, animate_opacity=800, scroll="auto")

    page.add(
        ft.Row([
            left_panel,
            ft.Container(
                content=results_container,
                expand=True,
                bgcolor=BG_WHITE,
                padding=70,
                gradient=ft.LinearGradient(begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1), colors=[BG_WHITE, BG_PANEL])
            )
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.run(main)
