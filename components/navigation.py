import flet as ft
from config.colors import AppColors

def create_nav_bar(nav_state, page, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)

    def toggle_nav(e):
        nav_state.visible = not nav_state.visible
        nav_state.container.visible = nav_state.visible
        nav_state.hamburger_icon.icon = ft.icons.CLOSE if nav_state.visible else ft.icons.MENU
        page.update()

    def navigate_to(route):
        def handle(e):
            page.go(route)
            if nav_state.visible:
                toggle_nav(None)
        return handle

    def create_nav_button(icon, label, on_click):
        button = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        icon,
                        color=colors.NAV_ICONS,
                        size=24,
                    ),
                    ft.Text(
                        label,
                        color=colors.TEXT_PRIMARY,
                        size=16,
                        weight="500",
                    ),
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=8,
            on_click=on_click,
        )

        def on_hover(e):
            if e.data == "true":
                button.bgcolor = ft.colors.with_opacity(0.1, colors.HOVER)
            else:
                button.bgcolor = None
            page.update()

        button.on_hover = on_hover
        return button

    def toggle_theme(e):
        # Toggle theme state
        theme_state.is_dark = not theme_state.is_dark
        new_colors = AppColors.get_colors(theme_state.is_dark)
        
        # Update page theme
        page.theme_mode = ft.ThemeMode.DARK if theme_state.is_dark else ft.ThemeMode.LIGHT
        page.bgcolor = new_colors.BACKGROUND
        page.window.bgcolor = new_colors.BACKGROUND
        
        # Save preference
        page.client_storage.set("theme_mode", "dark" if theme_state.is_dark else "light")
        
        # Trigger current route reload
        current_route = page.route
        page.views.clear()
        page.on_route_change(ft.RouteChangeEvent(route=current_route))
        
        # Close nav drawer
        if nav_state.visible:
            toggle_nav(None)

    nav_state.hamburger_icon = ft.IconButton(
        icon=ft.icons.MENU,
        icon_color=colors.BURGER,
        icon_size=30,
        on_click=toggle_nav,
        style=ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: colors.SECONDARY,
                ft.ControlState.HOVERED: colors.ACCENT,
            },
        ),
    )

    nav_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    "Menu",
                    size=20,
                    weight="bold",
                    color=colors.TEXT_PRIMARY,
                ),
                padding=ft.padding.only(left=12, top=8, bottom=16),
            ),
            create_nav_button(ft.icons.HOME_ROUNDED, "Home", navigate_to("/")),
            create_nav_button(ft.icons.CHAT_ROUNDED, "Recipe Chat", navigate_to("/chat")),
            create_nav_button(ft.icons.HISTORY_ROUNDED, "History", navigate_to("/history")),
            create_nav_button(ft.icons.PERSON_ROUNDED, "Profile", navigate_to("/profile")),
            ft.Container(
                content=ft.Divider(
                    color=colors.TEXT_SECONDARY,
                    thickness=0.5,
                ),
                margin=ft.margin.symmetric(vertical=16),
            ),
            create_nav_button(
                ft.icons.DARK_MODE_ROUNDED if theme_state.is_dark else ft.icons.LIGHT_MODE_ROUNDED,
                "Toggle theme",
                toggle_theme
            ),
            create_nav_button(ft.icons.LOGOUT_ROUNDED, "Logout", 
                lambda e: nav_state.on_logout()),
        ],
        spacing=2,
        scroll=ft.ScrollMode.AUTO,
    )

    nav_state.container = ft.Container(
        visible=False,
        content=ft.Container(
            content=nav_content,
            bgcolor=colors.NAV,
            border_radius=12,
            padding=ft.padding.only(top=8, bottom=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, colors.SECONDARY),
                offset=ft.Offset(0, 2),
            ),
            width=180,
        ),
        animate=ft.animation.Animation(300, "easeOut"),
    )

    # Use Stack for overlay effect
    return ft.Container(
        content=ft.Column(
            controls=[
                nav_state.hamburger_icon,
                nav_state.container
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.only(left=20, top=10),
        alignment=ft.alignment.top_left,
        expand=False,  # Don't expand the navigation container
        width=390,     # Set explicit width
    )