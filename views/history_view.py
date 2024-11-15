import flet as ft
from components.navigation import create_nav_bar

def history_view(page, nav_state):
    return ft.View(
        "/history",
        [
            create_nav_bar(nav_state, page),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column([
                            ft.Text("History", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                            ft.Text("Your recent recipes will appear here"),
                        ]),
                        padding=40,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        ],
    )