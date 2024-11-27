import flet as ft
from config.colors import AppColors
from config.fonts import AppFonts
from state.app_state import ThemeState
from components.navigation import create_nav_bar

def home_view(page, user_state, nav_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)
    
    # Error container for unauthorized access
    auth_error = ft.Container(
        visible=False,
        content=ft.Column([
            ft.Text(
                "Please log in to view the home page",
                size=16,
                color=colors.ERROR,
                text_align=ft.TextAlign.CENTER,
                style=AppFonts.get_text_style(size=16, color=colors.ERROR)
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

    # Main home container
    home_container = ft.Container(
        visible=True,
        content=ft.Column(
            [
                # Welcome texts
                ft.Container(
                    content=ft.Text(
                        "Anthropic Appetite",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=colors.TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                        style=AppFonts.get_text_style(
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=colors.TEXT_PRIMARY
                        )
                    ),
                    alignment=ft.alignment.center,
                    width=390,
                ),
                ft.Container(
                    content=ft.Text(
                        f"Cooking Recipe Generator",
                        size=16,
                        color=colors.ACCENT,
                        text_align=ft.TextAlign.CENTER,
                        style=AppFonts.get_text_style(
                            size=16,
                            color=colors.ACCENT
                        )
                    ),
                    alignment=ft.alignment.center,
                    width=390,
                ),
                
                # Divider
                ft.Container(
                    content=ft.Divider(
                        color=colors.SECONDARY,
                        height=2,
                    ),
                    width=300,
                    margin=ft.margin.only(top=20, bottom=20),
                ),
                
                # Instructions
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "How to use:",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=colors.ACCENT,
                            text_align=ft.TextAlign.CENTER,
                            style=AppFonts.get_text_style(
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=colors.ACCENT
                            )
                        ),
                        
                        # Step 1
                        ft.Container(
                            content=ft.Row([
                                ft.Text(
                                    "1.",
                                    size=16,
                                    color=colors.ACCENT,
                                    weight=ft.FontWeight.BOLD,
                                    style=AppFonts.get_text_style(
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors.ACCENT
                                    )
                                ),
                                ft.Text(
                                    "Submit API keys in Profile Settings",
                                    size=16,
                                    color=colors.ACCENT,
                                    style=AppFonts.get_text_style(
                                        size=16,
                                        color=colors.ACCENT
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                        
                        ft.ElevatedButton(
                            "Profile Settings",
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: colors.WHITE,
                                },
                                bgcolor={
                                    ft.ControlState.DEFAULT: colors.SECONDARY,
                                    ft.ControlState.HOVERED: colors.ACCENT,
                                }
                            ),
                            on_click=lambda _: page.go("/profile"),
                        ),
                        
                        # Step 2
                        ft.Container(
                            content=ft.Row([
                                ft.Text(
                                    "2.",
                                    size=16,
                                    color=colors.ACCENT,
                                    weight=ft.FontWeight.BOLD,
                                    style=AppFonts.get_text_style(
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors.ACCENT
                                    )
                                ),
                                ft.Text(
                                    "Start generating recipes in Chat",
                                    size=16,
                                    color=colors.ACCENT,
                                    style=AppFonts.get_text_style(
                                        size=16,
                                        color=colors.ACCENT
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            ),
                            margin=ft.margin.only(top=20),
                        ),
                        
                        ft.ElevatedButton(
                            "Generate Recipe",
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

                        # Step 3
                        ft.Container(
                            content=ft.Row([
                                ft.Text(
                                    "3.",
                                    size=16,
                                    color=colors.ACCENT,
                                    weight=ft.FontWeight.BOLD,
                                    style=AppFonts.get_text_style(
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors.ACCENT
                                    )
                                ),
                                ft.Text(
                                    "Cook & enjoy!",
                                    size=16,
                                    color=colors.ACCENT,
                                    style=AppFonts.get_text_style(
                                        size=16,
                                        color=colors.ACCENT
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            ),
                            margin=ft.margin.only(top=20),
                        ),
                        ft.ElevatedButton(
                            "Recipe History",
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: colors.WHITE,
                                },
                                bgcolor={
                                    ft.ControlState.DEFAULT: colors.SECONDARY,
                                    ft.ControlState.HOVERED: colors.ACCENT,
                                }
                            ),
                            on_click=lambda _: page.go("/history"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    ),
                    width=390,
                    padding=20,
                    bgcolor=colors.PRIMARY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=15,
        bgcolor=colors.PRIMARY,
    )

    def check_auth():
        is_authenticated = page.user_state.is_logged_in
        auth_error.visible = not is_authenticated
        home_container.visible = is_authenticated
        page.update()

    def on_view_push(e):
        check_auth()
    
    page.on_view_push = on_view_push

    return ft.View(
        "/",
        [
            ft.Stack([
                ft.Container(
                    content=ft.Column([
                        auth_error,
                        home_container,
                    ]),
                    width=390,
                    bgcolor=colors.PRIMARY,
                    padding=ft.padding.only(top=60),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ]),
        ],
        bgcolor=colors.BACKGROUND,
        padding=0,
        spacing=0,
    )