import flet as ft

def create_chat_components(page, chat_state):
    chat_input = ft.TextField(
        hint_text="Input ingredients here",
        border_radius=30,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        autofocus=True,
    )
    
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.BLUE_400,
        tooltip="Send message",
    )

    recipe_display = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10,
    )

    chat_input_container = ft.Container(
        content=ft.Row(
            controls=[chat_input, send_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor=ft.colors.SURFACE_VARIANT,
        animate=ft.animation.Animation(300, "easeOut"),
    )

    recipe_result_container = ft.Container(
        visible=False,
        content=recipe_display,
        expand=True,
        animate=ft.animation.Animation(300, "easeOut"),
    )

    def send_message(e):
        user_message = chat_input.value
        if user_message:
            chat_state.showing_input = False
            chat_input.value = ""
            chat_input_container.visible = False
            recipe_result_container.visible = True
            chat_state.current_recipe = {
                "title": "Cook this!",
                "description": "*AI generated recipe here*",
                "image_placeholder": "Image of the recipe here"
            }
            update_recipe_display()
            page.update()

    def update_recipe_display():
        recipe_display.controls.clear()
        if chat_state.current_recipe: # This is a comment!
            recipe_display.controls.extend([
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            chat_state.current_recipe["title"],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "🖼️ Recipe Image",
                                size=16,
                                color=ft.colors.GREY_700,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            bgcolor=ft.colors.GREY_200,
                            border_radius=10,
                            padding=20,
                            alignment=ft.alignment.center,
                            height=200,
                            width=300,
                        ),
                        ft.Container(
                            content=ft.Text(
                                chat_state.current_recipe["description"],
                                size=16,
                            ),
                            padding=ft.padding.only(top=20),
                        ),
                    ]),
                    padding=20,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Ask for another recipe",
                        on_click=lambda _: new_recipe_request(),
                    ),
                    padding=ft.padding.only(left=20),
                ),
            ])

    def new_recipe_request():
        chat_state.current_recipe = None
        chat_state.showing_input = True
        recipe_result_container.visible = False
        chat_input_container.visible = True
        page.update()

    chat_input.on_submit = send_message
    send_button.on_click = send_message

    return chat_input_container, recipe_result_container