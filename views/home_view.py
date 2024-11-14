import flet as ft
from components.navigation import create_nav_bar

def home_view(page, user_state, nav_state):
    return ft.View(
        "/",
        [
            ft.Row(
                [
                    create_nav_bar(nav_state, page),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Main page",
                                    size=32,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    f"Hello, {user_state.username}!",
                                    size=20,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        expand=True,
                        padding=50,
                    ), 
                ],
                expand=True,
            ),
        ],
    )