import flet as ft
import traceback
from views.login_view import login_view
from views.register_view import register_view
from views.profile_view import profile_view
from views.chat_view import chat_view
from views.history_view import history_view
from views.home_view import home_view
from views.recipe_detail_view import recipe_detail_view
from state.app_state import NavState, UserState, ChatState, ThemeState
from components.navigation import create_nav_bar
from config.firebase_config import FirebaseConfig
from config.colors import AppColors
from config.fonts import AppFonts

def main(page: ft.Page):
    # Initialize states
    nav_state = NavState()
    user_state = UserState()
    chat_state = ChatState()
    theme_state = ThemeState()
    page.user_state = user_state
    
    page.fonts = {
        "Rockwell": "/assets/fonts/Rockwell-Bold.ttf",
        "Inter": "/assets/fonts/InterVariable.ttf",
    }

    # Add debug logging
    print(f"Available fonts: {page.fonts}")
    print(f"Font family being used: {AppFonts.get_font_family()}")

    # Initialize Firebase first
    try:
        firebase = FirebaseConfig()
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        return

    def handle_logout():
        print("[LOGOUT] Handling logout")
        user_state.reset()
        chat_state.reset()
        page.client_storage.clear()
        page.go("/login")
        page.update()

    def load_stored_session():
        try:
            print("\n[SESSION] Attempting to load stored session")
            stored_user_id = page.client_storage.get("user_id")
            stored_username = page.client_storage.get("username")
            stored_api_key = page.client_storage.get("claude_api_key")

            if stored_api_key:
                claude_api = ClaudeAPI()
                if claude_api.initialize(stored_api_key):
                    page.claude_api = claude_api
            
            if stored_user_id and stored_username:
                result = firebase.verify_session(stored_user_id)
                if result["success"]:
                    user_state.is_logged_in = True
                    user_state.user_id = stored_user_id
                    user_state.username = stored_username
                    return True
            return False
        except Exception as e:
            print(f"[SESSION] Error loading session: {str(e)}")
            return False

    def route_change(route):
        print(f"\n[ROUTE] Route change to: {route.route}")
        
        # Get current theme colors
        colors = AppColors.get_colors(theme_state.is_dark)

        try:
            # Skip authentication check for login and register routes
            if route.route not in ["/login", "/register"]:
                if not user_state.is_logged_in:
                    if not load_stored_session():
                        print("[ROUTE] No valid session, redirecting to login")
                        page.go("/login")
                        return
            
            # Clear existing views before creating new ones
            page.views.clear()
            
            # Create the appropriate view
            if route.route == "/register":
                view = register_view(page, user_state, firebase, theme_state)
                controls = view.controls
            elif route.route == "/login":
                view = login_view(page, user_state, firebase, theme_state)
                controls = view.controls
            else:
                # Only add navigation bar for authenticated routes
                nav_bar = create_nav_bar(nav_state, page, theme_state)
                
                if route.route == "/profile":
                    view = profile_view(page, user_state, nav_state, firebase, theme_state)
                elif route.route == "/chat":
                    view = chat_view(page, chat_state, nav_state, firebase, theme_state)
                elif route.route == "/history":
                    view = history_view(page, nav_state, firebase, theme_state)
                elif route.route.startswith("/recipe"):
                    recipe_id = route.route.split("/")[-1]
                    view = recipe_detail_view(page, user_state, nav_state, firebase, theme_state, recipe_id)
                else:  # Default route "/"
                    view = home_view(page, user_state, nav_state, firebase, theme_state)
                
                controls = [nav_bar] + view.controls if nav_bar else view.controls

            # Create new view with proper structure
            page.views.append(
                ft.View(
                    route=view.route,
                    controls=[
                        ft.Stack([
                            # Main content
                            ft.Container(
                                content=ft.Column(
                                    controls=controls[1:] if len(controls) > 1 else controls,
                                    expand=True,
                                    scroll=ft.ScrollMode.AUTO
                                ),
                                width=390,
                                height=700,
                                padding=ft.padding.only(top=50),
                                alignment=ft.alignment.top_center,
                                bgcolor=colors.BACKGROUND,
                            ),
                            # Navigation overlay
                            controls[0] if len(controls) > 0 and route.route not in ["/login", "/register"] else ft.Container(),
                        ]),
                    ],
                    padding=0,
                    spacing=0,
                    bgcolor=colors.BACKGROUND,
                )
            )
            
        except Exception as e:
            print(f"[ROUTE] Error in route_change: {str(e)}")
            print(f"[ROUTE] Stack trace: {traceback.format_exc()}")
            if "W500" not in str(e):  # Only handle non-W500 errors
                handle_logout()
            return
        finally:
            page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Event handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    nav_state.on_logout = handle_logout

    # App configuration
    page.title = "Recipe App"
    page.theme_mode = ft.ThemeMode.DARK if theme_state.is_dark else ft.ThemeMode.LIGHT
    page.bgcolor = AppColors.get_colors(theme_state.is_dark).BACKGROUND
    page.padding = 0
    page.spacing = 0
    page.scroll = None
    
    # Configure window
    page.window.bgcolor = AppColors.get_colors(theme_state.is_dark).BACKGROUND
    page.window.width = 390
    page.window.height = 700
    page.window.resizable = True
    page.window.maximizable = True
    page.window.title_bar_hidden = False
    page.window.title_bar_buttons_hidden = False
    page.window.center()

    # Initial route
    if load_stored_session():
        page.go("/")
    else:
        page.go("/login")

ft.app(target=main, assets_dir="assets")