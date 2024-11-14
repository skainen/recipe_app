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
                                ft.Text(
                                    f"History of tomatoes in Europe:",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Brought from the Americas by Spanish explorers in the 16th century, tomatoes were first "
                                    "viewed with suspicion in Europe due to their resemblance to nightshade plants. By the 18th "
                                    "century, however, tomatoes had become a beloved ingredient, especially in Italy, where they "
                                    "featured prominently in pasta sauces and other dishes. Today, tomatoes are a global culinary staple.",
                                    size=16,
                                ),
                                ft.Text(
                                    f"History of strawberries:",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Strawberries have been enjoyed since ancient Roman times, valued not only for their flavor but "
                                    "also for their medicinal properties. The wild strawberry was widely cultivated in Europe by the "
                                    "17th century, and the modern garden strawberry (a hybrid from North America and Chile) became popular "
                                    "in the 18th century. Today, strawberries are enjoyed worldwide in desserts, salads, and fresh from the vine.",
                                    size=16,
                                ),
                                ft.Text(
                                    f"Explore the 10 Best Recipes with Fish and Milk:",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.TextButton(
                                    "Click here to view recipes",
                                    on_click=lambda e: page.launch_url("https://example.com/10-best-recipes-with-fish-and-milk")
                                )
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