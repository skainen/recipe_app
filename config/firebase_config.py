import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

class FirebaseConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
            
            try:
                # Get the current directory (where this file is)
                current_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Config file should be in the same directory
                config_path = os.path.join(current_dir, 'recipe-app-b03c1.json')
                
                if not os.path.exists(config_path):
                    raise FileNotFoundError(
                        f"Firebase config file not found. Please place .json file in the config folder"
                    )
                
                # Initialize Firebase
                cred = credentials.Certificate(config_path)
                firebase_admin.initialize_app(cred)
                cls._instance.db = firestore.client()
                print("Firebase initialized successfully")
            except Exception as e:
                print(f"Firebase initialization error: {str(e)}")
                raise
                
        return cls._instance

    def create_user(self, username: str, password: str) -> dict:
        try:
            # Create auth user
            user = auth.create_user(
                email=f"{username}@recipe-app.com",
                password=password
            )
            
            # Create user profile
            self.db.collection('users').document(user.uid).set({
                'username': username,
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_login': firestore.SERVER_TIMESTAMP
            })
            
            return {
                "success": True,
                "user_id": user.uid,
                "username": username
            }
        except auth.EmailAlreadyExistsError:
            return {
                "success": False,
                "error": "Username already exists"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_user_profile(self, user_id: str, profile_data: dict) -> dict:
        """
        Update user profile data in Firestore
        
        Parameters:
        user_id (str): Firebase user ID
        profile_data (dict): Dictionary containing profile data
        
        Returns:
        dict: Success status and error message if any
        """
        try:
            # Update profile document
            self.db.collection('users').document(user_id).set({
                'name': profile_data.get('name', ''),
                'age': profile_data.get('age', ''),
                'allergies': profile_data.get('allergies', ''),
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)  # merge=True to preserve existing fields
            
            return {
                "success": True
            }
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_user_profile(self, user_id: str) -> dict:
        """
        Retrieve user profile data from Firestore
        
        Parameters:
        user_id (str): Firebase user ID
        
        Returns:
        dict: Profile data or error message
        """
        try:
            # Get profile document
            doc = self.db.collection('users').document(user_id).get()
            
            if doc.exists:
                profile_data = doc.to_dict()
                return {
                    "success": True,
                    "profile": profile_data
                }
            else:
                return {
                    "success": False,
                    "error": "Profile not found"
                }
        except Exception as e:
            print(f"Error getting profile: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def login_user(self, username: str, password: str) -> dict:
        try:
            # Import the Auth module for sign-in
            from firebase_admin import auth
            
            # Get user by email first to check existence
            email = f"{username}@recipe-app.com"
            try:
                user = auth.get_user_by_email(email)
                
                # Update last login
                self.db.collection('users').document(user.uid).update({
                    'last_login': firestore.SERVER_TIMESTAMP
                })
                
                return {
                    "success": True,
                    "user_id": user.uid,
                    "username": username
                }
            except auth.UserNotFoundError:
                return {
                    "success": False,
                    "error": "User not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def verify_session(self, user_id: str) -> dict:
        try:
            # Verify user exists
            user = auth.get_user(user_id)
            return {
                "success": True,
                "user": user
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    def save_chat_history(self, user_id: str, prompt: str, response: dict) -> dict:
        """
        Save chat history with recipe information
        """
        try:
            print(f"Saving chat history for user {user_id}")
            print(f"Response data: {response}")
            
            # Ensure we have a dictionary for response
            if isinstance(response, str):
                response = {
                    'title': 'Recipe',
                    'description': response,
                    'image_url': ''
                }
            
            # Create a new chat history document
            chat_ref = self.db.collection('users').document(user_id)\
                        .collection('chat_history').document()
            
            doc_data = {
                'prompt': prompt,
                'response': response,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'is_favorite': False
            }
            print(f"Saving document: {doc_data}")
            
            chat_ref.set(doc_data)
            
            return {
                "success": True,
                "chat_id": chat_ref.id
            }
        except Exception as e:
            print(f"Error saving chat history: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {
                "success": False,
                "error": str(e)
            }

    def save_favorite_recipe(self, user_id: str, recipe: dict) -> dict:
        try:
            # Create a new favorite recipe document
            recipe_ref = self.db.collection('users').document(user_id)\
                            .collection('favorite_recipes').document()
            
            recipe_data = {
                'title': recipe.get('title', ''),
                'description': recipe.get('description', ''),
                'timestamp': firestore.SERVER_TIMESTAMP,
            }
            
            recipe_ref.set(recipe_data)
            
            return {
                "success": True,
                "recipe_id": recipe_ref.id
            }
        except Exception as e:
            print(f"Error saving favorite recipe: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_user_recipes(self, user_id: str, limit: int = 50) -> dict:
        """Get all recipes for a user from chat history"""
        try:
            print(f"\n=== Getting User Recipes ===")
            print(f"User ID: {user_id}")
            
            chat_ref = self.db.collection('users').document(user_id)\
                        .collection('chat_history')
            
            print("Getting recipes from chat_history...")
            recipes = chat_ref.order_by('timestamp', direction=firestore.Query.DESCENDING)\
                        .limit(limit)\
                        .stream()
            
            recipe_list = []
            for idx, recipe in enumerate(recipes):
                try:
                    chat_data = recipe.to_dict()
                    print(f"\nProcessing recipe {idx + 1}:")
                    print(f"Raw chat data: {chat_data}")
                    
                    response = chat_data.get('response', {})
                    print(f"Response data: {response}")
                    
                    if isinstance(response, str):
                        print("Got string response, parsing...")
                        lines = response.split('\n')
                        title = "Recipe"
                        if len(lines) > 0 and not lines[0].startswith('1.'):
                            title = lines[0].strip()
                            description = '\n'.join(lines[1:]).strip()
                        else:
                            description = response
                        image_url = ''
                    else:
                        print("Got structured response...")
                        title = response.get('title', 'Recipe')
                        description = response.get('description', '')
                        image_url = response.get('image_url', '')
                    
                    recipe_data = {
                        'id': recipe.id,
                        'title': title,
                        'description': description,
                        'image_url': image_url,
                        'ingredients': chat_data.get('prompt', ''),
                        'created_at': chat_data.get('timestamp'),
                        'is_favorite': chat_data.get('is_favorite', False)
                    }
                    print(f"Processed recipe data: {recipe_data}")
                    recipe_list.append(recipe_data)
                    
                except Exception as e:
                    print(f"Error processing recipe {recipe.id}: {e}")
                    continue
            
            print(f"\nTotal recipes found: {len(recipe_list)}")
            return {
                "success": True,
                "recipes": recipe_list
            }
        except Exception as e:
            print(f"Error getting recipes: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def get_chat_history(self, user_id: str) -> dict:
        try:
            # Get all chat history documents for the user
            chats = self.db.collection('users').document(user_id)\
                         .collection('chat_history')\
                         .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                         .limit(50)\
                         .stream()
            
            chat_list = []
            for chat in chats:
                chat_data = chat.to_dict()
                chat_data['id'] = chat.id
                chat_list.append(chat_data)
            
            return {
                "success": True,
                "chats": chat_list
            }
        except Exception as e:
            print(f"Error getting chat history: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    # For recipes_view
    def get_recipe(self, user_id: str, recipe_id: str) -> dict:
        """
        Get a specific recipe by ID from chat_history
        """
        try:
            print(f"Getting recipe {recipe_id} for user {user_id}")
            doc = self.db.collection('users').document(user_id)\
                        .collection('chat_history').document(recipe_id).get()
                        
            if doc.exists:
                chat_data = doc.to_dict()
                response = chat_data.get('response', {})
                
                # Handle both string and dict responses
                if isinstance(response, str):
                    lines = response.split('\n')
                    title = "Recipe"
                    if len(lines) > 0 and not lines[0].startswith('1.'):
                        title = lines[0].strip()
                        description = '\n'.join(lines[1:]).strip()
                    else:
                        description = response
                    image_url = ''
                else:
                    title = response.get('title', 'Recipe')
                    description = response.get('description', '')
                    image_url = response.get('image_url', '')
                
                recipe_data = {
                    'id': doc.id,
                    'title': title,
                    'description': description,
                    'image_url': image_url,
                    'ingredients': chat_data.get('prompt', ''),
                    'created_at': chat_data.get('timestamp'),
                    'is_favorite': chat_data.get('is_favorite', False)
                }
                
                return {
                    "success": True,
                    "recipe": recipe_data
                }
            else:
                return {
                    "success": False,
                    "error": "Recipe not found"
                }
        except Exception as e:
            print(f"Error getting recipe: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_favorite_recipes(self, user_id: str) -> dict:
        try:
            # Get all favorite recipe documents for the user
            recipes = self.db.collection('users').document(user_id)\
                           .collection('favorite_recipes')\
                           .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                           .stream()
            
            recipe_list = []
            for recipe in recipes:
                recipe_data = recipe.to_dict()
                recipe_data['id'] = recipe.id
                recipe_list.append(recipe_data)
            
            return {
                "success": True,
                "recipes": recipe_list
            }
        except Exception as e:
            print(f"Error getting favorite recipes: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def update_recipe_favorite(self, user_id: str, recipe_id: str, is_favorite: bool) -> dict:
        """
        Update the favorite status of a recipe
        """
        try:
            self.db.collection('users').document(user_id)\
                .collection('chat_history').document(recipe_id)\
                .update({
                    'is_favorite': is_favorite,
                    'updated_at': firestore.SERVER_TIMESTAMP
                })
            
            return {
                "success": True
            }
        except Exception as e:
            print(f"Error updating recipe favorite status: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }