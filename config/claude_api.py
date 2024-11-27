import anthropic
from typing import Optional
import json

class ClaudeAPI:
    def __init__(self):
        self.client: Optional[anthropic.Anthropic] = None
        
    def initialize(self, api_key: str) -> bool:
        try:
            if not api_key.startswith('sk-'):
                raise Exception("Invalid API key format")
                
            self.client = anthropic.Anthropic(
                api_key=api_key
            )
            return True
        except Exception as e:
            print(f"Failed to initialize Claude API: {e}")
            return False
    
    def generate_recipe(self, ingredients: str, firebase, user_id: str) -> dict:
        if not self.client:
            raise Exception("Claude API not initialized. Please set your API key in profile settings.")

        # Get user's allergies from Firebase
        profile_result = firebase.get_user_profile(user_id)
        user_allergies = ""
        if profile_result["success"]:
            user_allergies = profile_result["profile"].get("allergies", "")
            print(f"Retrieved user allergies: {user_allergies}")
        else:
            print("Failed to retrieve user allergies")
            
        prompt = """Given these ingredients: {ingredients}
        Create a recipe using these ingredients.
        User is allergic to these: {allergies}, DO NOT use these ingredients.
        Respond with ONLY a JSON object in this exact format, with no additional text:
        {{
            "title": "Recipe Name Here",
            "description": "Complete recipe here including ingredients list and instructions"
        }}"""
        
        try:
            # Create message
            message = self.client.messages.create(
                #model="claude-3-opus-20240229", # Better, costs more
                model="claude-3-haiku-20240307", # Cheaper, use for testing
                max_tokens=1000,
                messages=[{
                    "role": "user", 
                    "content": prompt.format(
                        ingredients=ingredients,
                        allergies=user_allergies if user_allergies else "none"
                        )
                }]
            )
            
            # Extract the content and parse JSON
            try:
                content = message.content[0].text
                recipe_data = json.loads(content)
            except (json.JSONDecodeError, AttributeError, IndexError) as e:
                print(f"Error parsing JSON: {e}")
                print(f"Raw content: {message.content}")
                raise Exception("Failed to parse recipe data")
            
            # Validate recipe data format
            if not isinstance(recipe_data, dict):
                raise Exception("Invalid recipe data format")
                
            if "title" not in recipe_data or "description" not in recipe_data:
                raise Exception("Missing required recipe fields")
            
            # Save to Firebase
            result = firebase.save_chat_history(
                user_id=user_id,
                prompt=ingredients,
                response=recipe_data["description"]
            )
            
            if not result["success"]:
                raise Exception("Failed to save recipe to history")
                
            return recipe_data
            
        except Exception as e:
            raise Exception(f"Error generating recipe: {str(e)}")

    def _format_recipe_data(self, content: str) -> dict:
        """Helper method to ensure proper recipe data format"""
        try:
            # Clean up the content if needed
            content = content.strip()
            if not content.startswith('{'):
                # Extract JSON if it's wrapped in other text
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    content = content[start:end]
                    
            recipe_data = json.loads(content)
            
            # Ensure required fields
            if not isinstance(recipe_data, dict):
                raise ValueError("Recipe data must be a dictionary")
                
            if "title" not in recipe_data or "description" not in recipe_data:
                raise ValueError("Missing required recipe fields")
                
            return recipe_data
        except Exception as e:
            print(f"Error formatting recipe data: {e}")
            print(f"Raw content: {content}")
            raise