import flet as ft
from config.colors import AppColors
from config.fonts import AppFonts
from state.app_state import ThemeState
from config.firebase_config import FirebaseConfig

def register_view(page, user_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)
    firebase = FirebaseConfig()

    register_username = ft.TextField(
        label="Username",
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
    )
    
    register_password = ft.TextField(
        label="Password",
        password=True,
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
    )
    
    confirm_password = ft.TextField(
        label="Confirm Password",
        password=True,
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
    )
    
    register_error = ft.Text(
        "",
        color=colors.ERROR,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    def try_register(e):
        if register_password.value != confirm_password.value:
            register_error.value = "Passwords do not match"
            register_error.visible = True
            page.update()
            return

        if not register_username.value or not register_password.value:
            register_error.value = "Username and password required"
            register_error.visible = True
            page.update()
            return

        result = firebase.create_user(register_username.value, register_password.value)

        if result["success"]:
            user_state.is_logged_in = True
            user_state.username = register_username.value
            user_state.user_id = result.get("user_id")
            page.client_storage.set("user_id", result.get("user_id"))
            page.client_storage.set("username", register_username.value)
            page.go("/")
        else:
            register_error.value = f"Registration failed: {result['error']}"
            register_error.visible = True
        page.update()

    return ft.View(
        "/register",
        [
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=colors.PRIMARY,
                padding=50,
                content=ft.Column(
                    [
                        ft.Text(
                            "Create Account",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=colors.TEXT_PRIMARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Enter your details to register",
                            size=16,
                            color=colors.TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        register_username,
                        register_password,
                        confirm_password,
                        register_error,
                        ft.ElevatedButton(
                            "Register",
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
                            on_click=try_register,
                        ),
                        ft.TextButton(
                            "Already have an account? Login",
                            on_click=lambda _: page.go("/login"),
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: colors.TEXT_PRIMARY,
                                    ft.ControlState.HOVERED: colors.ACCENT,
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