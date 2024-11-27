import flet as ft
from config.colors import AppColors
from config.fonts import AppFonts

def recipe_detail_view(page, user_state, nav_state, firebase, theme_state, recipe_id):
    colors = AppColors.get_colors(theme_state.is_dark)
    print(f"\n=== Recipe Detail View ===")
    print(f"Loading recipe ID: {recipe_id}")
    
    error_text = ft.Text(
        color=colors.ERROR,
        visible=False,
        size=14
    )

    recipe_display = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=5,
    )

    favorite_button = ft.IconButton(
        icon=ft.icons.FAVORITE_BORDER,
        icon_color=colors.TEXT_SECONDARY,
        tooltip="Add to favorites",
    )

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=colors.SECONDARY,
        on_click=lambda _: page.go("/history"),
        tooltip="Back to history",
    )

    loading_indicator = ft.ProgressRing(
        color=colors.SECONDARY,
        width=16,
        height=16,
        stroke_width=2,
    )

    def toggle_favorite():
        if not hasattr(toggle_favorite, 'recipe_data'):
            return
            
        try:
            is_favorite = not toggle_favorite.recipe_data.get('is_favorite', False)
            result = firebase.update_recipe_favorite(
                user_state.user_id,
                recipe_id,
                is_favorite
            )
            
            if result["success"]:
                toggle_favorite.recipe_data['is_favorite'] = is_favorite
                favorite_button.icon = ft.icons.FAVORITE if is_favorite else ft.icons.FAVORITE_BORDER
                favorite_button.icon_color = colors.SECONDARY if is_favorite else colors.TEXT_SECONDARY
                page.update()
        except Exception as e:
            print(f"Error toggling favorite: {e}")
            error_text.value = f"Error updating favorite status: {str(e)}"
            error_text.visible = True
            page.update()

    def load_recipe():
        print(f"\n=== Loading Recipe Data ===")
        print(f"User ID: {page.user_state.user_id}")
        print(f"Recipe ID: {recipe_id}")
        
        try:
            loading_indicator.visible = True
            page.update()
            
            result = firebase.get_recipe(page.user_state.user_id, recipe_id)
            print(f"Firebase result: {result}")
            
            if not result["success"]:
                error_text.value = "Failed to load recipe"
                error_text.visible = True
                loading_indicator.visible = False
                page.update()
                return

            recipe_data = result["recipe"]
            toggle_favorite.recipe_data = recipe_data  # Store recipe data for favorite toggle
            
            # Update favorite button state
            is_favorite = recipe_data.get('is_favorite', False)
            favorite_button.icon = ft.icons.FAVORITE if is_favorite else ft.icons.FAVORITE_BORDER
            favorite_button.icon_color = colors.SECONDARY if is_favorite else colors.TEXT_SECONDARY

            recipe_display.controls.clear()
            recipe_display.controls.extend([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            back_button,
                            ft.Text(
                                recipe_data.get("title", ""),
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=colors.TEXT_PRIMARY,
                                expand=True,
                                style=AppFonts.get_text_style(
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors.TEXT_PRIMARY
                                )
                            ),
                            favorite_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(
                            content=ft.Image(
                                src=recipe_data.get("image_url"),
                                fit=ft.ImageFit.COVER,
                                border_radius=10,
                            ) if recipe_data.get("image_url") else ft.Text(
                                "🖼️ Recipe Image",
                                size=16,
                                color=colors.TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            height=380,
                            width=440,
                            border_radius=10,
                            bgcolor=colors.PRIMARY,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Your input:",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=colors.TEXT_PRIMARY,
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                        ft.Container(
                            content=ft.Text(
                                recipe_data.get("ingredients", ""),
                                size=14,
                                color=colors.TEXT_SECONDARY,
                            ),
                            width=330,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Instructions:",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=colors.TEXT_PRIMARY,
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                        ft.Container(
                            content=ft.Text(
                                recipe_data.get("description", ""),
                                size=16,
                                color=colors.WHITE,
                            ),
                            width=330,
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"Created: {recipe_data.get('created_at', '').strftime('%Y-%m-%d %H:%M') if recipe_data.get('created_at') else 'Unknown'}",
                                size=12,
                                color=colors.TEXT_SECONDARY,
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    ),
                    padding=10,
                    bgcolor=colors.PRIMARY,
                    width=370,
                ),
            ])

        except Exception as e:
            print(f"Error loading recipe: {e}")
            error_text.value = f"Error loading recipe: {str(e)}"
            error_text.visible = True
        finally:
            loading_indicator.visible = False
            page.update()

    def check_auth():
        if not page.user_state.is_logged_in:
            page.go("/login")
            return
        load_recipe()

    def on_view_push(e):
        check_auth()
    
    page.on_view_push = on_view_push

    # Main content view
    view = ft.View(
        f"/recipe/{recipe_id}",
        [
            ft.Container(
                content=ft.Column([
                    loading_indicator,
                    error_text,
                    recipe_display,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=colors.BACKGROUND,
            ),
        ],
        bgcolor=colors.BACKGROUND,
        padding=0,
    )

    # Load recipe data immediately
    check_auth()

    return view