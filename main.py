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

def get_life_stage(age):
    if age < 3: return "INFANCY"
    if age < 12: return "CHILDHOOD"
    if age < 20: return "ADOLESCENCE"
    if age < 40: return "EARLY ADULTHOOD"
    if age < 65: return "MIDDLE ADULTHOOD"
    return "LATE ADULTHOOD"

# --- Reusable Components ---

class BentoCard(ft.Container):
    def __init__(self, title, value, icon, color, col_span={"sm": 6, "md": 4}):
        super().__init__()
        self.value_text = ft.Text(value, size=24, weight="bold", color=TEXT_MAIN)
        self.content = ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=18),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.08, color),
                    border_radius=12
                ),
                ft.Text(title, size=10, weight="bold", color=TEXT_SECONDARY),
            ], alignment="spaceBetween"),
            ft.Container(height=15),
            self.value_text,
        ], spacing=0)
        
        self.padding = 28
        self.border_radius = 28
        self.bgcolor = ft.Colors.with_opacity(0.75, BG_WHITE)
        self.blur = ft.Blur(15, 15)
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.4, BORDER_COLOR))
        self.shadow = ft.BoxShadow(blur_radius=40, color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK), offset=ft.Offset(0, 15))
        self.animate_scale = ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK)
        self.on_hover = self.toggle_hover
        self.data = col_span

    def toggle_hover(self, e):
        self.scale = 1.04 if e.data == "true" else 1.0
        self.bgcolor = ft.Colors.with_opacity(0.9, BG_WHITE) if e.data == "true" else ft.Colors.with_opacity(0.75, BG_WHITE)
        self.border = ft.border.all(1, ACCENT if e.data == "true" else ft.Colors.with_opacity(0.4, BORDER_COLOR))
        self.update()

def main(page: ft.Page):
    page.title = "AgePro Pro - Liquid Glass Edition"
    page.bgcolor = BG_WHITE
    page.padding = 0
    page.window_width = 1450
    page.window_height = 950
    page.fonts = {"Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"}
    page.theme = ft.Theme(font_family="Outfit")

    # --- Sidebar Styling ---
    
    input_style = {
        "border_radius": 14,
        "border_color": BORDER_COLOR,
        "focused_border_color": ACCENT,
        "bgcolor": BG_PANEL,
        "color": TEXT_MAIN,
        "label_style": ft.TextStyle(color=TEXT_SECONDARY, size=12),
        "height": 55,
        "content_padding": 18
    }

    name_input = ft.TextField(label="Full Name", **input_style)
    year_input = ft.TextField(label="Year", expand=True, **input_style)
    month_input = ft.TextField(label="Month", expand=True, **input_style)
    day_input = ft.TextField(label="Day", expand=True, **input_style)

    # --- Dashboard Elements ---
    
    res_age = ft.Text("0", size=120, weight="bold", color=TEXT_MAIN)
    res_name = ft.Text("Elite Performance", size=32, weight="bold", color=TEXT_MAIN)
    res_stage = ft.Text("SYSTEM IDLE", size=11, weight="bold", color=ACCENT)
    
    progress_fill = ft.Container(
        width=0, height=22,
        gradient=ft.LinearGradient(colors=[ACCENT, ACCENT_PINK]),
        border_radius=11,
        animate=ft.Animation(1200, ft.AnimationCurve.EASE_OUT_EXPO)
    )
    
    progress_track = ft.Container(
        content=ft.Stack([progress_fill]),
        width=550, height=22, bgcolor="#F1F5F9", border_radius=11,
        border=ft.border.all(1, BORDER_COLOR)
    )
    
    life_text = ft.Text("BIOLOGICAL JOURNEY: --%", size=11, color=TEXT_SECONDARY, weight="bold")

    cards = [
        BentoCard("ASTRONOMICAL SIGN", "--", ft.Icons.AUTO_AWESOME, ACCENT_AMBER, col_span={"sm": 12, "md": 4}),
        BentoCard("MILESTONE COUNTDOWN", "--", ft.Icons.TIMER, ACCENT_PINK),
        BentoCard("TOTAL EARTH DAYS", "--", ft.Icons.PUBLIC, ACCENT_TEAL),
        BentoCard("CHRONOLOGICAL WEEKS", "--", ft.Icons.NUMBERS, ACCENT),
        BentoCard("ESTIMATED BEATS", "--", ft.Icons.WAVES, ft.Colors.RED_400),
        BentoCard("NEUROLOGICAL REST", "--", ft.Icons.SELF_IMPROVEMENT, ft.Colors.INDIGO_400)
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
            
            res_name.value = f"Greetings, {name}"
            res_age.value = str(age)
            res_stage.value = get_life_stage(age)
            progress_fill.width = 550 * perc
            life_text.value = f"BIOLOGICAL JOURNEY: {int(perc*100)}%"
            
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
            page.snack_bar = ft.SnackBar(ft.Text("Invalid birth data detected!"))
            page.snack_bar.open = True
            page.update()

    # --- UI Layout Assembly ---

    left_panel = ft.Container(
        content=ft.Column([
            ft.Column([
                ft.Text("AgePro", size=38, weight="bold", color=TEXT_MAIN),
                ft.Image(src="Age.png", height=100, fit="contain"),
            ], horizontal_alignment="center", spacing=10),
            ft.Container(height=60),
            ft.Text("IDENTITY", size=10, weight="bold", color=TEXT_SECONDARY),
            name_input,
            ft.Container(height=15),
            ft.Text("GENETICS DATA", size=10, weight="bold", color=TEXT_SECONDARY),
            ft.Row([year_input, month_input, day_input], spacing=12),
            ft.Container(height=40),
            ft.ElevatedButton(
                content=ft.Text("INITIALIZE ANALYSIS", weight="bold"),
                on_click=calculate_click,
                height=65,
                width=float("inf"),
                style=ft.ButtonStyle(bgcolor=ACCENT, color="white", shape=ft.RoundedRectangleBorder(radius=18))
            ),
            ft.Container(expand=True),
            ft.Row([
                ft.Icon(ft.Icons.VERIFIED_USER, color=ACCENT_TEAL, size=14),
                ft.Text("Adheesha Sooriyaarachchi Certified", size=10, color=TEXT_SECONDARY)
            ], alignment="center")
        ], spacing=10, horizontal_alignment="center"),
        width=460,
        padding=60,
        bgcolor=BG_PANEL,
        border=ft.border.only(right=ft.BorderSide(1, BORDER_COLOR))
    )

    hero_section = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text("STABLE CONNECTION", size=10, weight="bold", color=ACCENT_TEAL),
                    padding=ft.padding.symmetric(8, 15),
                    bgcolor=ft.Colors.with_opacity(0.08, ACCENT_TEAL),
                    border_radius=20
                ),
                ft.Container(
                    content=res_stage,
                    padding=ft.padding.symmetric(8, 15),
                    bgcolor=ft.Colors.with_opacity(0.08, ACCENT),
                    border_radius=20
                ),
            ], alignment="center", spacing=15),
            ft.Container(height=10),
            res_name,
            res_age,
            ft.Text("YEARS OF AGE", size=14, weight="bold", color=TEXT_SECONDARY),
            ft.Container(height=35),
            life_text,
            progress_track
        ], horizontal_alignment="center", spacing=5),
        padding=ft.padding.symmetric(45, 60),
        border_radius=40,
        bgcolor=ft.Colors.with_opacity(0.85, BG_WHITE),
        blur=ft.Blur(25, 25),
        border=ft.border.all(1, ft.Colors.with_opacity(0.5, BORDER_COLOR)),
        shadow=ft.BoxShadow(blur_radius=60, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK), offset=ft.Offset(0, 25)),
        margin=ft.margin.only(bottom=40)
    )

    results_container = ft.Column([
        hero_section,
        grid
    ], expand=True, visible=False, animate_opacity=1000, scroll="auto")

    # Liquid Glass Background Blobs
    bg_blobs = ft.Stack([
        ft.Container(width=500, height=500, bgcolor=ft.Colors.with_opacity(0.12, ACCENT), border_radius=250, left=-100, top=-100, blur=ft.Blur(120, 120)),
        ft.Container(width=400, height=400, bgcolor=ft.Colors.with_opacity(0.1, ACCENT_PINK), border_radius=200, right=-50, bottom=-50, blur=ft.Blur(100, 100)),
        ft.Container(width=300, height=300, bgcolor=ft.Colors.with_opacity(0.08, ACCENT_TEAL), border_radius=150, left=300, bottom=100, blur=ft.Blur(80, 80)),
        ft.Container(width=250, height=250, bgcolor=ft.Colors.with_opacity(0.05, ACCENT_AMBER), border_radius=125, right=400, top=100, blur=ft.Blur(70, 70)),
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
