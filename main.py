import flet as ft
from datetime import datetime, date

# --- Premium Color Palette ---
ACCENT = "#6366F1"  # Indigo
ACCENT_PINK = "#EC4899"
ACCENT_TEAL = "#14B8A6"
ACCENT_AMBER = "#F59E0B"
BG_PANEL = "#FBFBFC"
BG_WHITE = "#FFFFFF"
TEXT_MAIN = "#1E293B"
TEXT_SECONDARY = "#64748B"
BORDER_COLOR = "#F1F5F9"

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

class BentoCard(ft.Container):
    def __init__(self, title, value, icon, color, col_span={"sm": 6, "md": 4}):
        super().__init__()
        self.value_text = ft.Text(value, size=22, weight="bold", color=TEXT_MAIN)
        self.content = ft.Column([
            ft.Container(
                content=ft.Icon(icon, color=color, size=20),
                padding=10,
                bgcolor=ft.Colors.with_opacity(0.1, color),
                border_radius=12
            ),
            ft.Container(height=10),
            ft.Text(title, size=11, weight="bold", color=TEXT_SECONDARY),
            self.value_text,
        ], spacing=0)
        
        self.padding = 25
        self.border_radius = 30
        self.bgcolor = ft.Colors.with_opacity(0.7, BG_WHITE)
        self.blur = ft.Blur(15, 15)
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.5, BORDER_COLOR))
        self.shadow = ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.03, ft.Colors.BLACK), offset=ft.Offset(0, 10))
        self.animate_scale = ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK)
        self.on_hover = self.toggle_hover
        self.data = col_span

    def toggle_hover(self, e):
        self.scale = 1.03 if e.data == "true" else 1.0
        self.bgcolor = ft.Colors.with_opacity(0.9, BG_WHITE) if e.data == "true" else ft.Colors.with_opacity(0.7, BG_WHITE)
        self.update()

def main(page: ft.Page):
    page.title = "AgePro Elite - Bento Edition"
    page.bgcolor = BG_WHITE
    page.padding = 0
    page.window_width = 1400
    page.window_height = 950
    page.fonts = {"Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"}
    page.theme = ft.Theme(font_family="Outfit")

    # --- Left Panel: Modern Input ---
    
    input_style = {
        "border_radius": 15,
        "border_color": BORDER_COLOR,
        "focused_border_color": ACCENT,
        "bgcolor": BG_PANEL,
        "color": TEXT_MAIN,
        "label_style": ft.TextStyle(color=TEXT_SECONDARY, size=12),
        "height": 55,
        "content_padding": 18
    }

    name_input = ft.TextField(label="Profile Name", **input_style)
    year_input = ft.TextField(label="Year", expand=True, **input_style)
    month_input = ft.TextField(label="Month", expand=True, **input_style)
    day_input = ft.TextField(label="Day", expand=True, **input_style)

    # --- Right Panel: Results Section ---
    
    res_age = ft.Text("0", size=100, weight="bold", color=TEXT_MAIN)
    res_name = ft.Text("Elite Analytics", size=28, weight="bold", color=TEXT_MAIN)
    
    progress_fill = ft.Container(
        width=0, height=20,
        gradient=ft.LinearGradient(colors=[ACCENT, ACCENT_PINK]),
        border_radius=10,
        animate=ft.Animation(1000, ft.AnimationCurve.EASE_OUT_QUART)
    )
    
    progress_track = ft.Container(
        content=ft.Stack([progress_fill]),
        width=500, height=20, bgcolor="#F1F5F9", border_radius=10
    )
    
    life_text = ft.Text("LIFE JOURNEY PROGRESS: --%", size=11, color=TEXT_SECONDARY, weight="bold")

    cards = [
        BentoCard("ZODIAC SIGN", "--", ft.Icons.STARS, ACCENT_AMBER, col_span={"sm": 12, "md": 4}),
        BentoCard("NEXT BIRTHDAY", "--", ft.Icons.CAKE, ACCENT_PINK),
        BentoCard("DAYS LIVED", "--", ft.Icons.AUTO_GRAPH, ACCENT_TEAL),
        BentoCard("TOTAL WEEKS", "--", ft.Icons.CALENDAR_VIEW_WEEK, ACCENT),
        BentoCard("HEARTBEATS", "--", ft.Icons.FAVORITE, ft.Colors.RED_400),
        BentoCard("SLEEP & DREAMS", "--", ft.Icons.NIGHTS_STAY, ft.Colors.INDIGO_400)
    ]

    grid = ft.ResponsiveRow([
        ft.Column([cards[0]], col=cards[0].data),
        ft.Column([cards[1]], col=cards[1].data),
        ft.Column([cards[2]], col=cards[2].data),
        ft.Column([cards[3]], col=cards[3].data),
        ft.Column([cards[4]], col=cards[4].data),
        ft.Column([cards[5]], col=cards[5].data),
    ], spacing=25, run_spacing=25)

    def calculate_click(e):
        try:
            name = name_input.value or "Member"
            y, m, d = int(year_input.value), int(month_input.value), int(day_input.value)
            birth = datetime(y, m, d)
            today = datetime.now()
            
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            diff = today - birth
            perc = min(1.0, age / 80)
            
            res_name.value = f"Welcome, {name}"
            res_age.value = str(age)
            progress_fill.width = 500 * perc
            life_text.value = f"LIFE JOURNEY PROGRESS: {int(perc*100)}%"
            
            cards[0].value_text.value = get_zodiac(m, d)
            try:
                nb = date(today.year, m, d)
                if nb < today.date(): nb = date(today.year + 1, m, d)
            except: nb = date(today.year + 1, 3, 1)
            
            cards[1].value_text.value = f"{(nb - today.date()).days} Days"
            cards[2].value_text.value = f"{diff.days:,}"
            cards[3].value_text.value = f"{diff.days // 7:,}"
            cards[4].value_text.value = f"{diff.days * 24 * 60 * 72:,}"
            cards[5].value_text.value = f"{int(age * 0.33)} Yrs"

            results_container.visible = True
            results_container.opacity = 1
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid birth registry!"))
            page.snack_bar.open = True
            page.update()

    # --- UI Layout Assembly ---

    left_panel = ft.Container(
        content=ft.Column([
            ft.Column([
                ft.Text("AgePro", size=36, weight="bold", color=TEXT_MAIN),
                ft.Image(src="Age.png", height=90, fit="contain"),
            ], horizontal_alignment="center", spacing=10),
            ft.Container(height=60),
            ft.Text("REGISTRATION", size=10, weight="bold", color=TEXT_SECONDARY),
            name_input,
            ft.Container(height=15),
            ft.Text("BIRTH DETAILS", size=10, weight="bold", color=TEXT_SECONDARY),
            ft.Row([year_input, month_input, day_input], spacing=12),
            ft.Container(height=40),
            ft.ElevatedButton(
                content=ft.Text("UNLOCK ANALYTICS", weight="bold"),
                on_click=calculate_click,
                height=65,
                width=float("inf"),
                style=ft.ButtonStyle(bgcolor=ACCENT, color="white", shape=ft.RoundedRectangleBorder(radius=20))
            ),
            ft.Container(expand=True),
            ft.Text("Designed by Adheesha Sooriyaarachchi", size=10, color=TEXT_SECONDARY, italic=True)
        ], spacing=10, horizontal_alignment="center"),
        width=450,
        padding=60,
        bgcolor=BG_PANEL,
        border=ft.border.only(right=ft.BorderSide(1, BORDER_COLOR))
    )

    # --- The Masterpiece Canvas ---
    
    hero_section = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("SECURE DATA FEED: ACTIVE", size=10, weight="bold", color=ACCENT_TEAL),
                padding=ft.padding.symmetric(8, 15),
                bgcolor=ft.Colors.with_opacity(0.05, ACCENT_TEAL),
                border_radius=20
            ),
            res_name,
            res_age,
            ft.Text("YEARS OLD", size=14, weight="bold", color=TEXT_SECONDARY),
            ft.Container(height=30),
            life_text,
            progress_track
        ], horizontal_alignment="center", spacing=5),
        padding=40,
        border_radius=40,
        bgcolor=ft.Colors.with_opacity(0.8, BG_WHITE),
        blur=ft.Blur(20, 20),
        border=ft.border.all(1, ft.Colors.with_opacity(0.5, BORDER_COLOR)),
        shadow=ft.BoxShadow(blur_radius=60, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK), offset=ft.Offset(0, 20)),
        margin=ft.margin.only(bottom=40)
    )

    results_container = ft.Column([
        hero_section,
        grid
    ], expand=True, visible=False, animate_opacity=800, scroll="auto")

    # Background Blobs for Glassmorphism
    bg_blobs = ft.Stack([
        ft.Container(width=400, height=400, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=200, left=100, top=100, blur=ft.Blur(100, 100)),
        ft.Container(width=300, height=300, bgcolor=ft.Colors.with_opacity(0.1, ACCENT_PINK), border_radius=150, right=50, bottom=100, blur=ft.Blur(80, 80)),
        ft.Container(width=200, height=200, bgcolor=ft.Colors.with_opacity(0.05, ACCENT_TEAL), border_radius=100, left=300, bottom=50, blur=ft.Blur(60, 60)),
    ])

    page.add(
        ft.Row([
            left_panel,
            ft.Container(
                content=ft.Stack([
                    bg_blobs,
                    ft.Container(content=results_container, padding=70)
                ]),
                expand=True,
                bgcolor=BG_WHITE,
            )
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.run(main)
