import json
import os

class Recipe:
    def __init__(self, name, ingredients, tools, cooking_time, difficulty):
        self.name = name
        self.ingredients = ingredients  # List of ingredients
        self.tools = tools  # List of tools needed
        self.cooking_time = cooking_time  # Time in seconds
        self.difficulty = difficulty  # 1-5 scale
        self.discovered = False
        
    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "tools": self.tools,
            "cooking_time": self.cooking_time,
            "difficulty": self.difficulty,
            "discovered": self.discovered
        }
        
    @classmethod
    def from_dict(cls, data):
        recipe = cls(
            data["name"],
            data["ingredients"],
            data["tools"],
            data["cooking_time"],
            data["difficulty"]
        )
        recipe.discovered = data.get("discovered", False)
        return recipe

class RecipeSystem:
    def __init__(self):
        self.recipes = {}
        self.load_default_recipes()
        self.load_saved_recipes()
        
    def load_default_recipes(self):
        # Default recipes that are always available
        default_recipes = [
            Recipe("Fried Rice", ["rice", "egg", "garlic", "onion"], ["pan"], 60, 1),
            Recipe("Scrambled Eggs", ["egg"], ["pan"], 30, 1),
            Recipe("Tomato Omelette", ["egg", "tomato", "onion"], ["pan"], 45, 2),
            Recipe("Garlic Rice", ["rice", "garlic"], ["pot"], 40, 1)
        ]
        
        for recipe in default_recipes:
            self.recipes[recipe.name] = recipe
            
    def load_saved_recipes(self):
        # Load custom recipes from save file if it exists
        if os.path.exists("saved_recipes.json"):
            try:
                with open("saved_recipes.json", "r") as file:
                    saved_data = json.load(file)
                    for recipe_data in saved_data:
                        recipe = Recipe.from_dict(recipe_data)
                        self.recipes[recipe.name] = recipe
            except Exception as e:
                print(f"Error loading saved recipes: {e}")
                
    def save_recipes(self):
        # Save all recipes to file
        recipes_to_save = [recipe.to_dict() for recipe in self.recipes.values()]
        try:
            with open("saved_recipes.json", "w") as file:
                json.dump(recipes_to_save, file, indent=2)
        except Exception as e:
            print(f"Error saving recipes: {e}")
            
    def get_recipe(self, name):
        return self.recipes.get(name)
    
    def get_all_recipes(self):
        return list(self.recipes.values())
    
    def get_discovered_recipes(self):
        return [recipe for recipe in self.recipes.values() if recipe.discovered]
    
    def add_recipe(self, recipe):
        self.recipes[recipe.name] = recipe
        self.save_recipes()
        
    def validate_recipe_creation(self, ingredients, tools):
        """Check if the combination of ingredients and tools can create a valid recipe"""
        # This is where you'd implement your recipe validation logic
        # For now, we'll use a simple matching system
        
        for recipe_name, recipe in self.recipes.items():
            # Check if all required ingredients are used
            if all(ing in ingredients for ing in recipe.ingredients):
                # Check if all required tools are used
                if all(tool in tools for tool in recipe.tools):
                    # Mark as discovered if it wasn't before
                    if not recipe.discovered:
                        recipe.discovered = True
                        self.save_recipes()
                    return recipe_name, True
        
        # If no existing recipe matches, check if this could be a valid new recipe
        # This is where you'd implement custom recipe creation logic
        if len(ingredients) >= 2 and len(tools) >= 1:
            # Generate a new recipe name based on main ingredients
            new_name = self._generate_recipe_name(ingredients)
            
            # Create and save the new recipe
            new_recipe = Recipe(
                new_name,
                ingredients,
                tools,
                60,  # Default cooking time
                2    # Default difficulty
            )
            new_recipe.discovered = True
            self.add_recipe(new_recipe)
            
            return new_name, True
            
        return None, False
    
    def _generate_recipe_name(self, ingredients):
        """Generate a recipe name based on ingredients"""
        if len(ingredients) <= 2:
            return " and ".join(ingredients).title()
        else:
            main_ingredients = ingredients[:2]
            return f"{' and '.join(main_ingredients).title()} Mix"
