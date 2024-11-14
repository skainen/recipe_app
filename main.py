import flet as ft
from views.login_view import login_view
from views.register_view import register_view
from views.profile_view import profile_view
from views.chat_view import chat_view
from views.history_view import history_view
from views.home_view import home_view
from state.app_state import NavState, UserState, ChatState
from components.navigation import create_nav_bar

def main(page: ft.Page):
    page.title = "Recipe App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = ft.ScrollMode.ALWAYS

    # Initialize states
    nav_state = NavState()
    user_state = UserState()
    chat_state = ChatState()

    def route_change(route):
        page.views.clear()
        
        if not user_state.is_logged_in and route.route != "/register":
            page.views.append(login_view(page, user_state))
        else:
            if route.route == "/register":
                page.views.append(register_view(page, user_state))
            elif route.route == "/profile":
                page.views.append(profile_view(page, user_state, nav_state))
            elif route.route == "/chat":
                page.views.append(chat_view(page, chat_state, nav_state))
            elif route.route == "/history":
                page.views.append(history_view(page, nav_state))
            else:
                page.views.append(home_view(page, user_state, nav_state))
        page.update()

    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main)