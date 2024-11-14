import flet as ft
from components.navigation import create_nav_bar
from components.chat_components import create_chat_components

def chat_view(page, chat_state, nav_state):
    chat_input_container, recipe_result_container = create_chat_components(page, chat_state)
    
    return ft.View(
        "/chat",
        [
            create_nav_bar(nav_state, page),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column([
                            recipe_result_container,
                            chat_input_container,
                        ]),
                        expand=True,
                        bgcolor=ft.colors.WHITE,
                    ),
                ],
                expand=True,
            ),
        ],
    )