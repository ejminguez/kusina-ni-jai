"""
Recipe system for managing and validating recipes
"""
import json
import os
import random
from config import RECIPES_FILE

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
        self.load_recipes()
        
    def load_recipes(self):
        """Load recipes from the recipes.json file"""
        try:
            if os.path.exists(RECIPES_FILE):
                with open(RECIPES_FILE, "r") as file:
                    data = json.load(file)
                    for recipe_data in data.get("recipes", []):
                        recipe = Recipe.from_dict(recipe_data)
                        self.recipes[recipe.name] = recipe
            else:
                # Create default recipes if file doesn't exist
                self._create_default_recipes()
        except Exception as e:
            print(f"Error loading recipes: {e}")
            self._create_default_recipes()
                
    def _create_default_recipes(self):
        """Create default recipes if no file exists"""
        default_recipes = [
            Recipe("Fried Rice", ["rice", "egg", "garlic", "onion"], ["pan"], 60, 1),
            Recipe("Scrambled Eggs", ["egg"], ["pan"], 30, 1),
            Recipe("Tomato Omelette", ["egg", "tomato", "onion"], ["pan"], 45, 2),
            Recipe("Garlic Rice", ["rice", "garlic"], ["pot"], 40, 1)
        ]
        
        for recipe in default_recipes:
            recipe.discovered = True
            self.recipes[recipe.name] = recipe
            
        self.save_recipes()
            
    def save_recipes(self):
        """Save all recipes to the recipes.json file"""
        try:
            os.makedirs(os.path.dirname(RECIPES_FILE), exist_ok=True)
            
            recipes_data = {
                "recipes": [recipe.to_dict() for recipe in self.recipes.values()]
            }
            
            with open(RECIPES_FILE, "w") as file:
                json.dump(recipes_data, file, indent=2)
        except Exception as e:
            print(f"Error saving recipes: {e}")
            
    def get_recipe(self, name):
        """Get a recipe by name"""
        return self.recipes.get(name)
    
    def get_all_recipes(self):
        """Get all recipes"""
        return list(self.recipes.values())
    
    def get_discovered_recipes(self):
        """Get all discovered recipes"""
        return [recipe for recipe in self.recipes.values() if recipe.discovered]
    
    def add_recipe(self, recipe):
        """Add a new recipe"""
        self.recipes[recipe.name] = recipe
        self.save_recipes()
        
    def validate_recipe_creation(self, ingredients, tools):
        """Check if the combination of ingredients and tools can create a valid recipe
        
        Returns:
            tuple: (recipe_name, is_valid)
        """
        # First check if this matches an existing recipe
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
            
    def get_random_recipe(self, discovered_only=True):
        """Get a random recipe
        
        Args:
            discovered_only: If True, only return discovered recipes
            
        Returns:
            Recipe or None if no recipes available
        """
        if discovered_only:
            recipes = self.get_discovered_recipes()
        else:
            recipes = self.get_all_recipes()
            
        if recipes:
            return random.choice(recipes)
        return None
