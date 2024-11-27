import flet as ft
from config.colors import AppColors
from config.fonts import AppFonts
from state.app_state import ThemeState

def history_view(page, nav_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)
    print("\n=== History View ===")
    print(f"User logged in: {page.user_state.is_logged_in}")
    print(f"User ID: {page.user_state.user_id}")

    # Error container for unauthorized access
    auth_error = ft.Container(
        visible=False,
        content=ft.Column([
            ft.Text(
                "Please log in to view your recipe history",
                size=16,
                color=colors.ERROR,
                text_align=ft.TextAlign.CENTER,
                style=AppFonts.get_text_style(size=16, color=colors.ERROR),
            ),
            ft.ElevatedButton(
                "Go to Login",
                style=ft.ButtonStyle(
                    color={
                        ft.ControlState.DEFAULT: colors.TEXT_PRIMARY,
                    },
                    bgcolor={
                        ft.ControlState.DEFAULT: colors.SECONDARY,
                        ft.ControlState.HOVERED: colors.ACCENT,
                    }
                ),
                on_click=lambda _: page.go("/login")
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20),
        padding=20,
        bgcolor=colors.PRIMARY,
    )

    search_input = ft.TextField(
        hint_text="Search recipes by title...",
        border_radius=30,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        hint_style=ft.TextStyle(color=colors.TEXT_SECONDARY),
        text_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        cursor_color=colors.TEXT_PRIMARY,
        width=330,
        prefix_icon=ft.icons.SEARCH,
    )

    recipe_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10,
    )

    all_recipes = []  # Store all recipes for filtering


    def create_recipe_card(recipe):
        try:
            card = ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(
                        ft.icons.RESTAURANT_MENU,
                        color=colors.SECONDARY,
                        size=20,
                    ),
                    title=ft.TextButton(
                        text=recipe.get("title", "Untitled Recipe"),
                        style=ft.ButtonStyle(
                            color=colors.TEXT_PRIMARY,
                            bgcolor=ft.colors.TRANSPARENT,
                        ),
                        on_click=lambda _: page.go(f"/recipe/{recipe['id']}"),
                    ),
                    trailing=ft.Icon(
                        ft.icons.RESTAURANT_MENU,
                        color=colors.SECONDARY,
                        size=20,
                    ),
                ),
                margin=ft.margin.only(bottom=5),
                bgcolor=colors.PRIMARY,
                border_radius=10,
                ink=True,
                animate=ft.animation.Animation(300, "easeOut"),
            )

            return card

        except Exception as e:
            print(f"Error creating recipe card: {e}")
            return None

    search_input = ft.TextField(
        hint_text="Search recipes by title...",
        border_radius=30,
        bgcolor=colors.INPUT_BG,
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        hint_style=ft.TextStyle(color=colors.TEXT_SECONDARY),
        text_style=ft.TextStyle(color=colors.TEXT_PRIMARY),
        cursor_color=colors.TEXT_PRIMARY,
        width=330,
        prefix_icon=ft.icons.SEARCH,
    )

    def filter_recipes(e):
        search_term = search_input.value.lower()
        recipe_list.controls.clear()
        
        filtered_recipes = all_recipes
        if search_term:
            filtered_recipes = [r for r in all_recipes if search_term in r.get("title", "").lower()]
        
        if not filtered_recipes:
            recipe_list.controls.append(
                ft.Text(
                    "No recipes found",
                    color=colors.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                    style=AppFonts.get_text_style(size=16, color=colors.ERROR)
                )
            )
        else:
            for recipe in filtered_recipes:
                card = create_recipe_card(recipe)
                if card:
                    recipe_list.controls.append(card)
        
        page.update()

    def load_recipes():
        print("\n=== Loading Recipes ===")
        
        if not page.user_state.is_logged_in:
            print("User not logged in, skipping load")
            return
            
        print(f"Loading recipes for user: {page.user_state.user_id}")
        result = firebase.get_user_recipes(page.user_state.user_id)
        print(f"Firebase result: {result}")
        
        if result["success"]:
            recipes = result["recipes"]
            print(f"Found {len(recipes)} recipes")
            recipe_list.controls.clear()
            
            nonlocal all_recipes
            all_recipes = recipes
            
            if not recipes:
                print("No recipes found")
                recipe_list.controls.append(
                    ft.Text(
                        "No recipes yet. Try generating some!",
                        color=colors.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    )
                )
            else:
                print("Creating recipe cards...")
                for recipe in recipes:
                    print(f"Creating card for recipe: {recipe.get('title', 'No title')}")
                    card = create_recipe_card(recipe)
                    if card:
                        recipe_list.controls.append(card)
            
            print("Updating page...")
            page.update()
        else:
            print(f"Error loading recipes: {result.get('error')}")

    # Main history container
    history_container = ft.Container(
        visible=True,
        content=ft.Column([
            ft.Text(
                "Recipe History",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=colors.TEXT_PRIMARY,
                style=AppFonts.get_text_style(size=16, color=colors.ERROR)
            ),
            search_input,
            ft.Divider(color=colors.SECONDARY, height=2),
            recipe_list,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20),
        padding=20,
        expand=True,
        bgcolor=colors.PRIMARY,
    )

    # Bind search input to filter function
    search_input.on_change = filter_recipes

    def check_auth():
        print("\n=== Checking Auth ===")
        is_authenticated = page.user_state.is_logged_in
        print(f"Is authenticated: {is_authenticated}")
        
        auth_error.visible = not is_authenticated
        history_container.visible = is_authenticated
        
        if is_authenticated:
            print("User authenticated, loading recipes...")
            load_recipes()
        else:
            print("User not authenticated, showing error")
            
        page.update()

    def on_view_push(e):
        print("\n=== View Push Event ===")
        check_auth()

    page.on_view_push = on_view_push

    # Create the view first
    view = ft.View(
        "/history",
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column([
                            auth_error,
                            history_container,
                        ]),
                        expand=True,
                        bgcolor=colors.PRIMARY,
                        padding=20,
                        border_radius=10,
                    ),
                ],
                expand=True,
            ),
        ],
        bgcolor=colors.BACKGROUND,
        padding=20,
    )

    # Then check auth after everything is defined
    check_auth()

    return view

