import flet as ft

def create_nav_bar(nav_state, page):
    def toggle_nav(e):
        nav_state.visible = not nav_state.visible
        nav_state.container.visible = nav_state.visible
        nav_state.hamburger_icon.icon = ft.icons.CLOSE if nav_state.visible else ft.icons.MENU
        page.update()

    def go_to_home(e):
        page.go("/")
        toggle_nav(e)

    def go_to_chat(e):
        page.go("/chat")
        toggle_nav(e)

    def go_to_history(e):
        page.go("/history")
        toggle_nav(e)

    def go_to_profile(e):
        page.go("/profile")
        toggle_nav(e)

    nav_state.hamburger_icon.on_click = toggle_nav

    nav_content = ft.Column(
        controls=[
            ft.IconButton(
                icon=ft.icons.HOME,
                icon_color=ft.colors.BLUE_400,
                tooltip="Home",
                on_click=go_to_home,
            ),
            ft.IconButton(
                icon=ft.icons.CHAT,
                icon_color=ft.colors.BLUE_400,
                tooltip="Recipe Chat",
                on_click=go_to_chat,
            ),
            ft.IconButton(
                icon=ft.icons.HISTORY,
                icon_color=ft.colors.BLUE_400,
                tooltip="History",
                on_click=go_to_history,
            ),
            ft.IconButton(
                icon=ft.icons.PERSON,
                icon_color=ft.colors.BLUE_400,
                tooltip="Profile",
                on_click=go_to_profile,
            ),
        ],
        spacing=5,
    )

    nav_state.container.content = nav_content

    return ft.Container(
        content=ft.Column(
            controls=[nav_state.hamburger_icon, nav_state.container],
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.only(left=20, top=10),
        alignment=ft.alignment.top_left,
    )