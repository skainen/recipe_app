import flet as ft

def register_view(page, user_state):
    register_username = ft.TextField(
        label="Username",
        width=300,
        border_radius=10,
    )
    
    register_password = ft.TextField(
        label="Password",
        password=True,
        width=300,
        border_radius=10,
    )
    
    confirm_password = ft.TextField(
        label="Confirm Password",
        password=True,
        width=300,
        border_radius=10,
    )
    
    register_error = ft.Text(
        "Passwords don't match or username is empty",
        color=ft.colors.RED_400,
        visible=False,
    )

    def try_register(e):
        if register_password.value == confirm_password.value and register_username.value:
            user_state.is_logged_in = True
            user_state.username = register_username.value
            page.go("/")
        else:
            register_error.visible = True
        page.update()

    return ft.View(
        "/register",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Create Account", size=32, weight=ft.FontWeight.BOLD),
                        register_username,
                        register_password,
                        confirm_password,
                        register_error,
                        ft.ElevatedButton(
                            "Register",
                            width=300,
                            on_click=try_register,
                        ),
                        ft.TextButton(
                            "Already have an account? Login",
                            on_click=lambda _: page.go("/login"),
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