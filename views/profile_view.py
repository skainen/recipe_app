import flet as ft
from state.app_state import ThemeState
from config.colors import AppColors
from config.fonts import AppFonts
from config.claude_api import ClaudeAPI

def profile_view(page, user_state, nav_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)

    # Error container for unauthorized access
    auth_error = ft.Container(
        visible=False,
        content=ft.Column([
            ft.Text(
                "Please log in to view your profile",
                size=16,
                color=colors.ERROR,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.ElevatedButton(
                "Go to Login",
                style=ft.ButtonStyle(
                    color={
                        ft.ControlState.DEFAULT: colors.TEXT_PRIMARY,
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
        spacing=10),
        padding=10,
        bgcolor=colors.PRIMARY,
    )

    # Load saved values
    saved_claude_key = page.client_storage.get("claude_api_key") or ""
    saved_google_key = page.client_storage.get("google_api_key") or ""
    saved_search_engine_id = page.client_storage.get("google_search_engine_id") or ""

    # Status message
    status_message = ft.Text(
        color=colors.SECONDARY,
        size=14,
        visible=False,
    )

    # Main profile container
    profile_name = ft.TextField(
        label="Name",
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
        cursor_color=colors.TEXT_PRIMARY,
    )
    
    profile_age = ft.TextField(
        label="Age",
        width=300,
        border_radius=10,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
        cursor_color=colors.TEXT_PRIMARY,
    )
    
    profile_allergies = ft.TextField(
        label="Allergies",
        width=300,
        border_radius=10,
        multiline=True,
        min_lines=3,
        max_lines=5,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
        cursor_color=colors.TEXT_PRIMARY,
    )

    google_api_key = ft.TextField(
        label="Google API Key",
        value=saved_google_key,
        width=300,
        border_radius=10,
        password=True,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
        cursor_color=colors.TEXT_PRIMARY,
    )

    google_search_engine_id = ft.TextField(
        label="Google Search Engine ID",
        value=saved_search_engine_id,
        width=300,
        border_radius=10,
        password=True,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
        cursor_color=colors.TEXT_PRIMARY,
    )

    claude_api_key = ft.TextField(
        label="Claude API Key",
        value=saved_claude_key,
        width=300,
        border_radius=10,
        password=True,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        color=colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        text_style=ft.TextStyle(color=colors.NAV_ICONS),
        cursor_color=colors.TEXT_PRIMARY,
    )

    def load_profile_data():
        """Load profile data from Firebase"""
        if not page.user_state.is_logged_in:
            return
            
        result = firebase.get_user_profile(page.user_state.user_id)
        if result["success"]:
            profile_data = result["profile"]
            profile_name.value = profile_data.get("name", "")
            profile_age.value = profile_data.get("age", "")
            profile_allergies.value = profile_data.get("allergies", "")
            page.update()

    def update_profile(e):
        if not page.user_state.is_logged_in:
            return
            
        # Save keys to client storage
        page.client_storage.set("google_api_key", google_api_key.value)
        page.client_storage.set("google_search_engine_id", google_search_engine_id.value)

        # Save profile data to Firebase
        profile_data = {
            "name": profile_name.value,
            "age": profile_age.value,
            "allergies": profile_allergies.value,
        }

        result = firebase.update_user_profile(page.user_state.user_id, profile_data)
        
        # Save API key and initialize Claude if provided
        if claude_api_key.value:
            page.client_storage.set("claude_api_key", claude_api_key.value)
            # Initialize Claude API
            claude_api = ClaudeAPI()
            if claude_api.initialize(claude_api_key.value):
                page.claude_api = claude_api
                status_message.value = "Profile saved successfully!"
            else:
                status_message.value = "Profile saved but API initialization failed."
        else:
            status_message.value = "Profile saved successfully!"
        
        # Update user state
        user_state.name = profile_name.value
        user_state.age = profile_age.value
        user_state.allergies = profile_allergies.value
        
        # Show success message
        status_message.visible = True
        page.update()

    profile_container = ft.Container(
        visible=True,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "Profile Settings",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=colors.TEXT_PRIMARY,
                            text_align=ft.TextAlign.CENTER,
                            style=AppFonts.get_text_style(
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=colors.TEXT_PRIMARY
                            )
                        ),
                        alignment=ft.alignment.center,
                        width=390,
                    ),
                    profile_name,
                    profile_age,
                    profile_allergies,
                    claude_api_key,
                    google_api_key,
                    google_search_engine_id,
                    status_message,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Save Changes",
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
                            on_click=update_profile,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Home Page",
                                    width=145,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.ControlState.DEFAULT: colors.WHITE,
                                        },
                                        bgcolor={
                                            ft.ControlState.DEFAULT: colors.SECONDARY,
                                            ft.ControlState.HOVERED: colors.ACCENT,
                                        }
                                    ),
                                    on_click=lambda _: page.go("/"),
                                ),
                                ft.ElevatedButton(
                                    "Go Chat",
                                    width=145,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.ControlState.DEFAULT: colors.WHITE,
                                        },
                                        bgcolor={
                                            ft.ControlState.DEFAULT: colors.SECONDARY,
                                            ft.ControlState.HOVERED: colors.ACCENT,
                                        }
                                    ),
                                    on_click=lambda _: page.go("/chat"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=10,
                        ),
                        width=300,
                        alignment=ft.alignment.center,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            width=390,
            alignment=ft.alignment.center,
        ),
        padding=20,
        expand=True,
        bgcolor=colors.PRIMARY,
    )

    return ft.View(
        "/profile",
        [
            ft.Container(
                content=ft.Column([
                    auth_error,
                    profile_container,
                ]),
                expand=True,
                bgcolor=colors.PRIMARY,
                alignment=ft.alignment.center,
            ),
        ],
        bgcolor=colors.BACKGROUND,
        padding=0,
    )