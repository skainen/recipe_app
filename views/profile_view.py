import flet as ft
from components.navigation import create_nav_bar

def profile_view(page, user_state, nav_state):
    profile_name = ft.TextField(
        label="Name",
        width=300,
        border_radius=10,
    )
    
    profile_age = ft.TextField(
        label="Age",
        width=300,
        border_radius=10,
    )
    
    profile_gender = ft.Dropdown(
        label="Gender",
        width=300,
        options=[
            ft.dropdown.Option("Male"),
            ft.dropdown.Option("Female"),
            ft.dropdown.Option("Other"),
        ],
    )
    
    profile_allergies = ft.TextField(
        label="Allergies",
        width=300,
        border_radius=10,
        multiline=True,
        min_lines=3,
        max_lines=5,
    )

    def update_profile(e):
        user_state.name = profile_name.value
        user_state.age = profile_age.value
        user_state.gender = profile_gender.value
        user_state.allergies = profile_allergies.value
        page.update()

    return ft.View(
        "/profile",
        [
            create_nav_bar(nav_state, page),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Profile Settings", size=32, weight=ft.FontWeight.BOLD),
                                profile_name,
                                profile_age,
                                profile_gender,
                                profile_allergies,
                                ft.ElevatedButton(
                                    "Save Changes",
                                    width=300,
                                    on_click=update_profile,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        padding=50,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        ],
    )