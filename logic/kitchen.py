"""
Kitchen logic for managing ingredients, tools, and cooking
"""
import json
import os
from config import INGREDIENTS_FILE, DEFAULT_INGREDIENTS, DEFAULT_TOOLS

class Kitchen:
    def __init__(self):
        self.ingredients = {}
        self.tools = {}
        self.load_ingredients_and_tools()
        
    def load_ingredients_and_tools(self):
        """Load ingredients and tools from file"""
        try:
            if os.path.exists(INGREDIENTS_FILE):
                with open(INGREDIENTS_FILE, "r") as file:
                    data = json.load(file)
                    
                    # Load ingredients
                    for ingredient in data.get("ingredients", []):
                        self.ingredients[ingredient["name"]] = {
                            "cost": ingredient["cost"],
                            "unlocked": ingredient["unlocked"],
                            "category": ingredient["category"]
                        }
                        
                    # Load tools
                    for tool in data.get("tools", []):
                        self.tools[tool["name"]] = {
                            "cost": tool["cost"],
                            "unlocked": tool["unlocked"],
                            "category": tool["category"]
                        }
            else:
                # Create default ingredients and tools
                self._create_defaults()
        except Exception as e:
            print(f"Error loading ingredients and tools: {e}")
            self._create_defaults()
            
    def _create_defaults(self):
        """Create default ingredients and tools"""
        # Clear existing data
        self.ingredients = {}
        self.tools = {}
        
        # Default ingredients
        for ingredient in DEFAULT_INGREDIENTS:
            self.ingredients[ingredient] = {
                "cost": 0,
                "unlocked": True,
                "category": "basic"
            }
            
        # Additional locked ingredients
        additional_ingredients = ["chicken", "beef", "carrot", "bell pepper", "potato"]
        for ingredient in additional_ingredients:
            self.ingredients[ingredient] = {
                "cost": 50,
                "unlocked": False,
                "category": "advanced"
            }
            
        # Default tools
        for tool in DEFAULT_TOOLS:
            self.tools[tool] = {
                "cost": 0,
                "unlocked": True,
                "category": "basic"
            }
            
        # Additional locked tools
        additional_tools = ["oven", "grill", "blender"]
        for tool in additional_tools:
            self.tools[tool] = {
                "cost": 100,
                "unlocked": False,
                "category": "advanced"
            }
            
        self.save_ingredients_and_tools()
            
    def save_ingredients_and_tools(self):
        """Save ingredients and tools to file"""
        try:
            os.makedirs(os.path.dirname(INGREDIENTS_FILE), exist_ok=True)
            
            ingredients_list = []
            for name, data in self.ingredients.items():
                ingredients_list.append({
                    "name": name,
                    "cost": data["cost"],
                    "unlocked": data["unlocked"],
                    "category": data["category"]
                })
                
            tools_list = []
            for name, data in self.tools.items():
                tools_list.append({
                    "name": name,
                    "cost": data["cost"],
                    "unlocked": data["unlocked"],
                    "category": data["category"]
                })
                
            data = {
                "ingredients": ingredients_list,
                "tools": tools_list
            }
            
            with open(INGREDIENTS_FILE, "w") as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"Error saving ingredients and tools: {e}")
            
    def get_unlocked_ingredients(self):
        """Get list of unlocked ingredients"""
        return [name for name, data in self.ingredients.items() if data["unlocked"]]
        
    def get_unlocked_tools(self):
        """Get list of unlocked tools"""
        return [name for name, data in self.tools.items() if data["unlocked"]]
        
    def get_locked_ingredients(self):
        """Get list of locked ingredients with their costs"""
        return [(name, data["cost"]) for name, data in self.ingredients.items() if not data["unlocked"]]
        
    def get_locked_tools(self):
        """Get list of locked tools with their costs"""
        return [(name, data["cost"]) for name, data in self.tools.items() if not data["unlocked"]]
        
    def unlock_ingredient(self, ingredient_name):
        """Unlock an ingredient
        
        Args:
            ingredient_name: Name of ingredient to unlock
            
        Returns:
            tuple: (success, cost)
        """
        if ingredient_name in self.ingredients and not self.ingredients[ingredient_name]["unlocked"]:
            cost = self.ingredients[ingredient_name]["cost"]
            self.ingredients[ingredient_name]["unlocked"] = True
            self.save_ingredients_and_tools()
            return True, cost
        return False, 0
        
    def unlock_tool(self, tool_name):
        """Unlock a tool
        
        Args:
            tool_name: Name of tool to unlock
            
        Returns:
            tuple: (success, cost)
        """
        if tool_name in self.tools and not self.tools[tool_name]["unlocked"]:
            cost = self.tools[tool_name]["cost"]
            self.tools[tool_name]["unlocked"] = True
            self.save_ingredients_and_tools()
            return True, cost
        return False, 0
        
    def reset(self):
        """Reset kitchen to default state"""
        # Delete the ingredients file if it exists
        if os.path.exists(INGREDIENTS_FILE):
            try:
                os.remove(INGREDIENTS_FILE)
            except Exception as e:
                print(f"Error deleting ingredients file: {e}")
                
        # Recreate defaults
        self._create_defaults()
