import flet as ft

class NavState:
    def __init__(self):
        self.visible = False
        self.container = ft.Container(
            visible=False,
            animate=ft.animation.Animation(300, "easeOut")
        )
        self.hamburger_icon = ft.IconButton(
            icon=ft.icons.MENU,
            icon_color=ft.colors.BLUE_400,
            icon_size=30,
        )

class UserState:
    def __init__(self):
        # Authentication states
        self.is_logged_in = False
        self.username = ""
        self.user_id = None  # Firebase UID
        
        # Profile information
        self.name = ""
        self.age = ""
        self.gender = ""
        self.allergies = ""
        
        # Session states
        self.last_login = None
        self.profile_loaded = False
        
    def reset(self):
        """Reset user state on logout"""
        self.is_logged_in = False
        self.username = ""
        self.user_id = None
        self.name = ""
        self.age = ""
        self.gender = ""
        self.allergies = ""
        self.profile_loaded = False
        
    def update_from_firebase(self, profile_data: dict):
        """Update user state from Firebase profile data"""
        self.name = profile_data.get('name', '')
        self.age = profile_data.get('age', '')
        self.gender = profile_data.get('gender', '')
        self.allergies = profile_data.get('allergies', '')
        self.last_login = profile_data.get('last_login')
        self.profile_loaded = True
        
    def to_dict(self) -> dict:
        """Convert user state to dictionary for Firebase storage"""
        return {
            'username': self.username,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'allergies': self.allergies,
            'last_login': self.last_login
        }

class ChatState:
    def __init__(self):
        self.showing_input = True
        self.current_recipe = None
        
        # New states for Firebase integration
        self.is_loading = False
        self.last_error = None
        self.saved_recipes = []
        self.current_recipe_id = None  # For updating existing recipes
        
    def reset(self):
        """Reset chat state"""
        self.showing_input = True
        self.current_recipe = None
        self.is_loading = False
        self.last_error = None
        self.current_recipe_id = None
        
    def set_recipe(self, recipe_data: dict):
        """Set current recipe from Firebase data"""
        self.current_recipe = {
            'id': recipe_data.get('id'),
            'title': recipe_data.get('title'),
            'description': recipe_data.get('description'),
            'ingredients': recipe_data.get('ingredients', []),
            'steps': recipe_data.get('steps', []),
            'created_at': recipe_data.get('created_at'),
            'updated_at': recipe_data.get('updated_at'),
            'is_favorite': recipe_data.get('is_favorite', False)
        }
        self.current_recipe_id = recipe_data.get('id')
        
    def to_dict(self) -> dict:
        """Convert current recipe to dictionary for Firebase storage"""
        if not self.current_recipe:
            return None
            
        return {
            'title': self.current_recipe.get('title'),
            'description': self.current_recipe.get('description'),
            'ingredients': self.current_recipe.get('ingredients', []),
            'steps': self.current_recipe.get('steps', []),
            'created_at': self.current_recipe.get('created_at'),
            'updated_at': self.current_recipe.get('updated_at'),
            'is_favorite': self.current_recipe.get('is_favorite', False)
        }

class AppState:
    def __init__(self):
        self.nav_state = NavState()
        self.user_state = UserState()
        self.chat_state = ChatState()
        
    def reset_all(self):
        """Reset all states on logout"""
        self.user_state.reset()
        self.chat_state.reset()

class ThemeState:
    def __init__(self):
        self.is_dark = True  # Default to dark theme