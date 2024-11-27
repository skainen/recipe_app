import flet as ft
from config.colors import AppColors
from config.fonts import AppFonts
from state.app_state import ThemeState

def login_view(page, user_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)
    
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.SECONDARY,
        focused_border_color=colors.ACCENT,
        color=colors.TEXT_PRIMARY,
        label_style=AppFonts.get_text_style(color=colors.TEXT_PRIMARY),
        text_style=AppFonts.get_text_style(color=colors.TEXT_PRIMARY),
        cursor_color=colors.SECONDARY,
        cursor_height=20,
        focused_bgcolor=colors.INPUT_BG,
        content_padding=ft.padding.all(10),
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.SECONDARY,
        focused_border_color=colors.ACCENT,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        cursor_color=colors.SECONDARY,
        cursor_height=20,
        focused_bgcolor=colors.INPUT_BG,
        content_padding=ft.padding.all(10),
    )

    def on_focus(e):
        print(f"TextField focused: {e.control.label}")
    
    def on_change(e):
        print(f"TextField changed: {e.control.label} = {e.control.value}")

    username_field.on_focus = on_focus
    username_field.on_change = on_change
    password_field.on_focus = on_focus
    password_field.on_change = on_change

    login_error = ft.Text(
        "",
        color=colors.ERROR,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    def try_login(e):
        print(f"[LOGIN] Attempting login for user: {username_field.value}")
        
        if not username_field.value or not password_field.value:
            login_error.value = "Username and password are required"
            login_error.visible = True
            page.update()
            return
            
        result = firebase.login_user(
            username=username_field.value,
            password=password_field.value
        )
        
        print(f"[LOGIN] Firebase login result: {result}")
        
        if result["success"]:
            user_state.is_logged_in = True
            user_state.username = username_field.value
            user_state.user_id = result["user_id"]
            page.client_storage.set("user_id", result["user_id"])
            page.client_storage.set("username", username_field.value)
            page.go("/")
        else:
            login_error.value = result.get("error", "Login failed")
            login_error.visible = True
            page.update()

    return ft.View(
        "/login",
        [
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=colors.PRIMARY,
                padding=50,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Anthropic Appetite",
                            text_align=ft.TextAlign.CENTER,
                            style=AppFonts.get_text_style(
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=colors.TEXT_PRIMARY,
                            )
                        ),
                        ft.Text(
                            "Please log in to continue",
                            size=16,
                            color=colors.TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        username_field,
                        password_field,
                        login_error,
                        ft.ElevatedButton(
                            "Login",
                            width=300,
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: colors.WHITE,
                                },
                                bgcolor={
                                    ft.ControlState.DEFAULT: colors.SECONDARY,
                                    ft.ControlState.HOVERED: colors.ACCENT,
                                }
                            ),
                            on_click=try_login,
                        ),
                        ft.TextButton(
                            "Don't have an account? Register",
                            on_click=lambda _: page.go("/register"),
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: colors.TEXT_PRIMARY,
                                    ft.ControlState.HOVERED: colors.SECONDARY,
                                }
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            )
        ],
        bgcolor=colors.BACKGROUND,
        padding=0,
    )