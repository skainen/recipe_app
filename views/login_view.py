import flet as ft

def login_view(page, user_state):
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_radius=10,
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        width=300,
        border_radius=10,
    )

    def try_login(e):
        username = username_field.value
        password = password_field.value
        if username and password:
            user_state.is_logged_in = True
            user_state.username = username
            page.go("/")
        page.update()

    return ft.View(
        "/login",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Recipe generator", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Please log in to continue", size=16, color=ft.colors.GREY_700),
                        username_field,
                        password_field,
                        ft.ElevatedButton(
                            "Login",
                            width=300,
                            on_click=try_login,
                        ),
                        ft.TextButton(
                            "Don't have an account? Register",
                            on_click=lambda _: page.go("/register"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=50,
                alignment=ft.alignment.center,
            )
        ],
    )