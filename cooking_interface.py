import pygame

class CookingInterface:
    def __init__(self, recipe_system):
        self.recipe_system = recipe_system
        self.selected_ingredients = []
        self.selected_tools = []
        self.available_ingredients = ["rice", "egg", "tomato", "onion", "garlic", "potato", "chicken", "beef", "carrot", "bell pepper"]
        self.available_tools = ["pan", "pot", "oven", "grill", "blender"]
        
        # UI elements
        self.ingredient_buttons = []
        self.tool_buttons = []
        self.cooking_button = None
        self.back_button = None
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Create ingredient buttons
        button_width = 100
        button_height = 40
        margin = 10
        
        # Ingredients area (left side)
        x_start = 50
        y_start = 150
        
        for i, ingredient in enumerate(self.available_ingredients):
            row = i // 3
            col = i % 3
            x = x_start + col * (button_width + margin)
            y = y_start + row * (button_height + margin)
            
            self.ingredient_buttons.append({
                "rect": pygame.Rect(x, y, button_width, button_height),
                "name": ingredient,
                "selected": False
            })
            
        # Tools area (right side)
        x_start = 450
        y_start = 150
        
        for i, tool in enumerate(self.available_tools):
            row = i // 2
            col = i % 2
            x = x_start + col * (button_width + margin)
            y = y_start + row * (button_height + margin)
            
            self.tool_buttons.append({
                "rect": pygame.Rect(x, y, button_width, button_height),
                "name": tool,
                "selected": False
            })
            
        # Cook button
        self.cooking_button = pygame.Rect(350, 400, 150, 50)
        
        # Back button
        self.back_button = pygame.Rect(50, 500, 100, 40)
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check ingredient buttons
            for button in self.ingredient_buttons:
                if button["rect"].collidepoint(event.pos):
                    button["selected"] = not button["selected"]
                    if button["selected"]:
                        if button["name"] not in self.selected_ingredients:
                            self.selected_ingredients.append(button["name"])
                    else:
                        if button["name"] in self.selected_ingredients:
                            self.selected_ingredients.remove(button["name"])
            
            # Check tool buttons
            for button in self.tool_buttons:
                if button["rect"].collidepoint(event.pos):
                    button["selected"] = not button["selected"]
                    if button["selected"]:
                        if button["name"] not in self.selected_tools:
                            self.selected_tools.append(button["name"])
                    else:
                        if button["name"] in self.selected_tools:
                            self.selected_tools.remove(button["name"])
            
            # Check cook button
            if self.cooking_button.collidepoint(event.pos):
                return self.cook()
                
            # Check back button
            if self.back_button.collidepoint(event.pos):
                self.reset()
                return None, False
                
        return None
        
    def update(self):
        # This method would handle any ongoing cooking animations or processes
        # For now, it just returns the result of the last action
        return None
        
    def cook(self):
        """Attempt to cook with the selected ingredients and tools"""
        if not self.selected_ingredients or not self.selected_tools:
            return None, False
            
        # Validate the recipe
        recipe_name, is_valid = self.recipe_system.validate_recipe_creation(
            self.selected_ingredients, self.selected_tools)
            
        if is_valid:
            # Reset selections after successful cooking
            self.reset()
            return recipe_name, True
        else:
            return None, False
            
    def reset(self):
        """Reset all selections"""
        self.selected_ingredients = []
        self.selected_tools = []
        
        for button in self.ingredient_buttons:
            button["selected"] = False
            
        for button in self.tool_buttons:
            button["selected"] = False
        
    def render(self, screen):
        # Clear screen with a light color
        screen.fill((245, 245, 220))  # Beige background for cooking area
        
        # Draw title
        font_large = pygame.font.SysFont(None, 48)
        font = pygame.font.SysFont(None, 24)
        
        title = font_large.render("Cooking Station", True, (0, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))
        
        # Draw sections
        ingredients_title = font.render("Ingredients", True, (0, 0, 0))
        screen.blit(ingredients_title, (50, 120))
        
        tools_title = font.render("Tools", True, (0, 0, 0))
        screen.blit(tools_title, (450, 120))
        
        # Draw ingredient buttons
        for button in self.ingredient_buttons:
            color = (150, 200, 150) if button["selected"] else (200, 200, 200)
            pygame.draw.rect(screen, color, button["rect"])
            pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2)
            
            text = font.render(button["name"], True, (0, 0, 0))
            screen.blit(text, (button["rect"].x + button["rect"].width // 2 - text.get_width() // 2,
                              button["rect"].y + button["rect"].height // 2 - text.get_height() // 2))
        
        # Draw tool buttons
        for button in self.tool_buttons:
            color = (150, 150, 200) if button["selected"] else (200, 200, 200)
            pygame.draw.rect(screen, color, button["rect"])
            pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2)
            
            text = font.render(button["name"], True, (0, 0, 0))
            screen.blit(text, (button["rect"].x + button["rect"].width // 2 - text.get_width() // 2,
                              button["rect"].y + button["rect"].height // 2 - text.get_height() // 2))
        
        # Draw cook button
        pygame.draw.rect(screen, (200, 150, 150), self.cooking_button)
        pygame.draw.rect(screen, (0, 0, 0), self.cooking_button, 2)
        
        cook_text = font.render("Cook!", True, (0, 0, 0))
        screen.blit(cook_text, (self.cooking_button.x + self.cooking_button.width // 2 - cook_text.get_width() // 2,
                               self.cooking_button.y + self.cooking_button.height // 2 - cook_text.get_height() // 2))
        
        # Draw back button
        pygame.draw.rect(screen, (200, 200, 200), self.back_button)
        pygame.draw.rect(screen, (0, 0, 0), self.back_button, 2)
        
        back_text = font.render("Back", True, (0, 0, 0))
        screen.blit(back_text, (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                               self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))
        
        # Draw selected ingredients and tools
        selected_text = font.render(f"Selected: {', '.join(self.selected_ingredients)} | Tools: {', '.join(self.selected_tools)}", 
                                   True, (0, 0, 0))
        screen.blit(selected_text, (50, 350))
