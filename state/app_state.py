import flet as ft

class NavState:
    def __init__(self):
        self.visible = False
        self.container = ft.Container(
            visible=False,
            animate=ft.animation.Animation(300, "easeOut")
        )
        self.hamburger_icon = ft.IconButton(
            icon=ft.icons.MENU,
            icon_color=ft.colors.BLUE_400,
            icon_size=30,
        )

class UserState:
    def __init__(self):
        self.is_logged_in = False
        self.username = ""
        self.name = ""
        self.age = ""
        self.gender = ""
        self.allergies = ""

class ChatState:
    def __init__(self):
        self.showing_input = True
        self.current_recipe = None