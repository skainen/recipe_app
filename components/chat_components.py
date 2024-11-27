import flet as ft
from config.firebase_config import FirebaseConfig
from config.colors import AppColors
from config.google_search import GoogleImageSearch

def create_chat_components(page, chat_state, user_state, firebase, theme_state):
    colors = AppColors.get_colors(theme_state.is_dark)

    loading_dots = ft.Row(
        controls=[
            ft.Container(
                content=ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=colors.SECONDARY,
                ),
                margin=ft.margin.only(right=10),
            ),
            ft.Text("Generating recipe...", color=colors.TEXT_SECONDARY),
        ],
        visible=False,
    )
    
    chat_input = ft.TextField(
        label="What do you want to cook?",
        hint_text="Give name of a food or ingredients",
        border_radius=30,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        autofocus=True,
        bgcolor=colors.INPUT_BG,
        label_style=ft.TextStyle(color=colors.NAV_ICONS),
        border_color=colors.PRIMARY,
        focused_border_color=colors.SECONDARY,
        hint_style=ft.TextStyle(
            color=colors.NAV_ICONS,
        ),
        text_style=ft.TextStyle(
            color=colors.TEXT_PRIMARY,
        ),
        cursor_color=colors.TEXT_PRIMARY,
    )

        # Add recipe image container and search functionality
    recipe_image = ft.Container(
        content=ft.Text(
            "🖼️ Recipe Image",
            size=16,
            color=colors.TEXT_SECONDARY,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=colors.CARD_BG,
        border_radius=10,
        padding=10,
        alignment=ft.alignment.center,
        height=200,
        width=330,
    )

    async def update_recipe_image(recipe_title: str):
        try:
            # Load API keys from your config
            api_key = page.client_storage.get("google_api_key")
            search_engine_id = page.client_storage.get("google_search_engine_id")
            
            if api_key and search_engine_id:
                image_search = GoogleImageSearch(api_key, search_engine_id)
                image_url = image_search.search_image(f"{recipe_title} food recipe")
                
                if image_url:
                    recipe_image.content = ft.Image(
                        src=image_url,
                        fit=ft.ImageFit.COVER,
                        border_radius=10,
                        width=330,
                        height=200,
                    )
                    page.update()
        except Exception as e:
            print(f"Error updating recipe image: {e}")

    
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=colors.SECONDARY,
        tooltip="Send message",
    )

    recipe_display = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=5,
    )

    # Add loading indicator
    loading_indicator = ft.ProgressRing(visible=False)

    chat_input_container = ft.Container(
        content=ft.Row(
            controls=[chat_input, send_button, loading_indicator],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor=colors.PRIMARY,
        border_radius=30,
        animate=ft.animation.Animation(300, "easeOut"),
    )
    
    recipe_result_container = ft.Container(
        visible=False,
        content=recipe_display,
        expand=True,
        bgcolor=colors.PRIMARY,
        border_radius=30,
        animate=ft.animation.Animation(300, "easeOut"),
    )

    error_text = ft.Text(
        color=colors.ERROR,
        visible=False,
        size=14
    )

    async def send_message(e):
        if not user_state.is_logged_in or not hasattr(page, 'claude_api'):
            error_text.value = "Please login and set Claude API key in profile settings"
            error_text.visible = True
            page.update()
            return

        if not chat_input.value:
            return

        try:
            loading_dots.visible = True
            loading_indicator.visible = True
            chat_input.disabled = True
            send_button.disabled = True
            page.update()

            recipe_response = page.claude_api.generate_recipe(
                ingredients=chat_input.value,
                firebase=firebase,
                user_id=user_state.user_id
            )

            image_url = None
            api_key = await page.client_storage.get_async("google_api_key")
            search_engine_id = await page.client_storage.get_async("google_search_engine_id")
            
            if api_key and search_engine_id:
                try:
                    image_search = GoogleImageSearch(api_key, search_engine_id)
                    image_url = image_search.search_image(f"{recipe_response['title']} food recipe")
                except Exception as e:
                    print(f"Image search error: {e}")

            '''
            # Save recipe to Firebase (maybe unnecessary so commented out for now)
            # This updates it automatically when recipe is generated, we also have
            # a button for saving to Firebase so let's use that instead
            recipe_data = {
            "title": recipe_response["title"],
            "description": recipe_response["description"],
            "image_url": image_url,
            "ingredients": chat_input.value  # Save the original ingredients
            }
            '''

            # Store recipe in chat state only (don't save to Firebase yet)
            chat_state.current_recipe = {
                "title": recipe_response["title"],
                "description": recipe_response["description"],
                "image_url": image_url,
                "ingredients": chat_input.value
            }

            # Update UI and show recipe
            chat_state.showing_input = False
            chat_input.value = ""
            chat_input_container.visible = False
            recipe_result_container.visible = True
            
            recipe_display.controls.clear()
            recipe_display.controls.extend([
                ft.Container(
                    content=ft.Column([
                        # Title Section
                        ft.Container(
                            content=ft.Text(
                                chat_state.current_recipe["title"],
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=colors.TEXT_PRIMARY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            margin=ft.margin.only(bottom=20),
                            alignment=ft.alignment.center,
                        ),
                        
                        # Image Section
                        ft.Container(
                            content=ft.Image(
                                src=image_url,
                                fit=ft.ImageFit.COVER,
                                border_radius=15,
                            ) if image_url else ft.Container(
                                content=ft.Column([
                                    ft.Icon(
                                        ft.icons.RESTAURANT_MENU,
                                        size=40,
                                        color=colors.TEXT_SECONDARY,
                                    ),
                                    ft.Text(
                                        "Recipe Image",
                                        size=16,
                                        color=colors.TEXT_SECONDARY,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                #bgcolor=colors.PRIMARY,
                            ),
                            border_radius=15,
                            padding=10,
                            alignment=ft.alignment.center,
                            height=300,
                            width=330,
                        ),
                        
                        # Description Section
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Text(
                                        "Suggestion:",
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors.TEXT_PRIMARY,
                                    ),
                                    margin=ft.margin.only(bottom=10),
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        chat_state.current_recipe["description"],
                                        size=16,
                                        color=colors.WHITE,
                                        text_align=ft.TextAlign.JUSTIFY,
                                    ),
                                    padding=20,
                                    bgcolor=colors.PRIMARY,
                                    border_radius=10,
                                ),
                            ]),
                            margin=ft.margin.only(top=20, bottom=20),
                            width=330,
                        ),
                        
                        # Action Buttons
                        ft.Container(
                            content=ft.Row([
                                ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Text("Save Recipe", color=colors.WHITE),
                                    ], spacing=5),
                                    style=ft.ButtonStyle(
                                        bgcolor=colors.SECONDARY,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                    on_click=lambda _: save_recipe(),
                                ),
                                ft.OutlinedButton(
                                    content=ft.Row([
                                        ft.Text("New Recipe", color=colors.SECONDARY),
                                    ], spacing=5),
                                    style=ft.ButtonStyle(
                                        side=ft.BorderSide(2, colors.SECONDARY),
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                    on_click=lambda _: new_recipe_request(),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            spacing=10),
                            margin=ft.margin.only(top=10),
                            padding=ft.padding.symmetric(vertical=10),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    ),
                    padding=20,
                    bgcolor=colors.PRIMARY,
                    border_radius=20,
                    width=370,
                ),
            ])

        except Exception as e:
            error_text.value = f"Error: {str(e)}"
            error_text.visible = True
        
        finally:
            loading_indicator.visible = False
            chat_input.disabled = False
            send_button.disabled = False
            page.update()

    # Save recipe to Firebase
    def save_recipe():
        if not user_state.is_logged_in:
            error_text.value = "Please login to save recipes"
            error_text.visible = True
            page.update()
            return

        try:
            print("\n=== Starting save_recipe ===")
            print(f"Current recipe data: {chat_state.current_recipe}")
            print(f"User ID: {user_state.user_id}")

            # Ensure we have a recipe to save
            if not chat_state.current_recipe:
                error_text.value = "No recipe to save"
                error_text.visible = True
                page.update()
                return

            # Create properly structured recipe data
            recipe_description = chat_state.current_recipe.get('description', '')
            recipe_title = chat_state.current_recipe.get('title', '')

            print(f"Title: {recipe_title}")
            print(f"Description length: {len(recipe_description)}")

            # If we have a string instead of structured data, parse it
            if isinstance(recipe_description, str) and not recipe_title:
                print("Parsing string response...")
                # Try to extract title and description
                lines = recipe_description.split('\n')
                recipe_title = "Recipe"  # Default title
                if len(lines) > 0 and not lines[0].startswith('1.'):
                    recipe_title = lines[0].strip()
                    recipe_description = '\n'.join(lines[1:]).strip()

            response_data = {
                'title': recipe_title,
                'description': recipe_description,
                'image_url': chat_state.current_recipe.get('image_url', '')
            }
            print(f"Prepared response data: {response_data}")

            # Save to Firebase chat history
            result = firebase.save_chat_history(
                user_id=user_state.user_id,
                prompt=chat_state.current_recipe.get('ingredients', ''),
                response=response_data
            )

            print(f"Save result: {result}")

            if result["success"]:
                snack = ft.SnackBar(
                    content=ft.Text(
                        "Recipe saved successfully!",
                        color=colors.WHITE,
                    ),
                    bgcolor=colors.SECONDARY,
                )
                page.overlay.append(snack)
                snack.open = True
                page.update()
                
                # Clear current recipe to prevent double-save
                chat_state.current_recipe = None
                #page.go("/history")
            else:
                error_text.value = f"Failed to save recipe: {result.get('error', 'Unknown error')}"
                error_text.visible = True
                    
        except Exception as e:
            print(f"Error in save_recipe: {str(e)}")
            error_text.value = f"Error saving recipe: {str(e)}"
            error_text.visible = True
        
        page.update()
        

    def new_recipe_request():
        error_text.visible = False
        chat_state.current_recipe = None
        chat_state.showing_input = True
        recipe_result_container.visible = False
        chat_input_container.visible = True
        page.update()

    chat_input.on_submit = send_message
    send_button.on_click = send_message

    return ft.Column([
        error_text,
        chat_input_container,
        recipe_result_container
    ])