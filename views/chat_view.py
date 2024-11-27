import flet as ft
from components.navigation import create_nav_bar
from components.chat_components import create_chat_components
from state.app_state import ThemeState
from config.colors import AppColors
from config.fonts import AppFonts

def chat_view(page, chat_state, nav_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)

    # Error container for unauthorized access
    auth_error = ft.Container(
        visible=False,
        content=ft.Column([
            ft.Text(
                "Please log in to use the recipe generator",
                size=16,
                color=colors.ERROR,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.ElevatedButton(
                "Go to Login",
                style=ft.ButtonStyle(
                    color={
                        ft.ControlState.DEFAULT: colors.PRIMARY,
                    },
                    bgcolor={
                        ft.ControlState.DEFAULT: colors.SECONDARY,
                        ft.ControlState.HOVERED: colors.ACCENT,
                    }
                ),
                on_click=lambda _: page.go("/login")
            )
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20),
        padding=20,
        bgcolor=colors.PRIMARY,
    )

    # Main chat container
    chat_container = ft.Container(
        visible=True,
        content=create_chat_components(page, chat_state, page.user_state, firebase, theme_state),  # Pass theme_state
        expand=True,
        bgcolor=colors.PRIMARY,
        border=ft.border.all(color=colors.PRIMARY, width=2),
        border_radius=10,
    )

    def check_auth():
        is_authenticated = page.user_state.is_logged_in  # Use actual user state
        auth_error.visible = not is_authenticated
        chat_container.visible = is_authenticated
        page.update()

    def on_view_push(e):
        check_auth()
    
    page.on_view_push = on_view_push

    def handle_session_expired():
        snack = ft.SnackBar(
            content=ft.Text(
                "Session expired. Please login again.",
                color=colors.WHITE
            ),
            bgcolor=colors.SECONDARY,
        )
        page.overlay.append(snack)
        snack.open = True
        page.go("/login")
        page.update()

    return ft.View(
        "/chat",
        [
            ft.ResponsiveRow(
                [
                    ft.Container(
                        content=ft.Column([
                            auth_error,
                            chat_container,
                        ]),
                        expand=True,
                        bgcolor=colors.PRIMARY,
                        padding=20,
                        border_radius=10,
                    ),
                ],
                expand=True,
            ),
        ],
        bgcolor=colors.BACKGROUND,  # Changed to BACKGROUND to match the overall theme
    )