"""
Recipe creator scene for cooking dishes
"""
import pygame
from ui.buttons import Button, IngredientButton, ToolButton, CookButton
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, BEIGE

class RecipeCreator:
    def __init__(self, recipe_system, kitchen):
        self.recipe_system = recipe_system
        self.kitchen = kitchen
        self.text_renderer = TextRenderer()
        
        self.selected_ingredients = []
        self.selected_tools = []
        
        # UI elements
        self.ingredient_buttons = []
        self.tool_buttons = []
        self.cook_button = CookButton(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 150, 150, 50)
        self.back_button = Button(50, SCREEN_HEIGHT - 70, 100, 40, "Back")
        
        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 20
        self.scroll_area_height = SCREEN_HEIGHT - 300  # Area available for scrolling
        
        # Result message
        self.result_message = ""
        self.result_timer = 0
        
        # Create buttons for ingredients and tools
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up UI elements"""
        # Clear existing buttons
        self.ingredient_buttons = []
        self.tool_buttons = []
        self.scroll_offset = 0
        
        # Get unlocked ingredients and tools
        unlocked_ingredients = self.kitchen.get_unlocked_ingredients()
        unlocked_tools = self.kitchen.get_unlocked_tools()
        
        # Create ingredient buttons
        button_width = 100
        button_height = 40
        margin = 10
        
        # Ingredients area (left side)
        x_start = 50
        y_start = 150
        
        for i, ingredient in enumerate(unlocked_ingredients):
            row = i // 3
            col = i % 3
            x = x_start + col * (button_width + margin)
            y = y_start + row * (button_height + margin)
            
            self.ingredient_buttons.append(
                IngredientButton(x, y, button_width, button_height, ingredient)
            )
            
        # Tools area (right side)
        x_start = 450
        y_start = 150
        
        for i, tool in enumerate(unlocked_tools):
            row = i // 2
            col = i % 2
            x = x_start + col * (button_width + margin)
            y = y_start + row * (button_height + margin)
            
            self.tool_buttons.append(
                ToolButton(x, y, button_width, button_height, tool)
            )
            
        # Calculate max scroll based on content height
        if self.ingredient_buttons or self.tool_buttons:
            # Find the button with the lowest position
            all_buttons = self.ingredient_buttons + self.tool_buttons
            if all_buttons:
                last_button = max(all_buttons, key=lambda b: b.rect.bottom)
                content_height = last_button.rect.bottom - 150
                self.max_scroll = max(0, content_height - self.scroll_area_height)
            else:
                self.max_scroll = 0
        else:
            self.max_scroll = 0
        
    def handle_events(self, events):
        """Handle events for the recipe creator
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
            dict: Additional data to pass to the next scene
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states for fixed buttons
        self.cook_button.is_hovered(mouse_pos)
        self.back_button.is_hovered(mouse_pos)
        
        # Adjust mouse position for scrolling when checking ingredient/tool buttons
        scroll_adjusted_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
        
        # Update hover states for scrollable buttons
        for button in self.ingredient_buttons:
            # Only check buttons that are in the visible area
            button_rect = button.rect
            if 150 <= button_rect.y - self.scroll_offset <= SCREEN_HEIGHT - 200:
                button.is_hovered(scroll_adjusted_pos)
            
        for button in self.tool_buttons:
            # Only check buttons that are in the visible area
            button_rect = button.rect
            if 150 <= button_rect.y - self.scroll_offset <= SCREEN_HEIGHT - 200:
                button.is_hovered(scroll_adjusted_pos)
        
        for event in events:
            # Handle scrolling
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * self.scroll_speed
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check ingredient buttons
                for button in self.ingredient_buttons:
                    # Only check buttons that are in the visible area
                    button_rect = button.rect
                    if 150 <= button_rect.y - self.scroll_offset <= SCREEN_HEIGHT - 200:
                        if button_rect.collidepoint(scroll_adjusted_pos):
                            if button.toggle():
                                if button.ingredient_name not in self.selected_ingredients:
                                    self.selected_ingredients.append(button.ingredient_name)
                            else:
                                if button.ingredient_name in self.selected_ingredients:
                                    self.selected_ingredients.remove(button.ingredient_name)
                
                # Check tool buttons
                for button in self.tool_buttons:
                    # Only check buttons that are in the visible area
                    button_rect = button.rect
                    if 150 <= button_rect.y - self.scroll_offset <= SCREEN_HEIGHT - 200:
                        if button_rect.collidepoint(scroll_adjusted_pos):
                            if button.toggle():
                                if button.tool_name not in self.selected_tools:
                                    self.selected_tools.append(button.tool_name)
                            else:
                                if button.tool_name in self.selected_tools:
                                    self.selected_tools.remove(button.tool_name)
                
                # Check cook button
                if self.cook_button.is_clicked(mouse_pos, event):
                    result = self.cook()
                    if result[0]:  # If cooking was successful
                        return "game", {"cooked_dish": result[1]}
                    
                # Check back button
                if self.back_button.is_clicked(mouse_pos, event):
                    self.reset()
                    return "game", {}
                    
        return None, {}
        
    def update(self, dt):
        """Update the recipe creator
        
        Args:
            dt: Time delta in seconds
        """
        # Update result message timer
        if self.result_timer > 0:
            self.result_timer -= dt
            if self.result_timer <= 0:
                self.result_message = ""
        
    def cook(self):
        """Attempt to cook with the selected ingredients and tools
        
        Returns:
            tuple: (success, dish_name)
        """
        if not self.selected_ingredients or not self.selected_tools:
            self.show_result("Please select at least one ingredient and one tool", 2.0)
            return False, None
            
        # Validate the recipe
        recipe_name, is_valid = self.recipe_system.validate_recipe_creation(
            self.selected_ingredients, self.selected_tools)
            
        if is_valid:
            # Reset selections after successful cooking
            self.reset()
            self.show_result(f"Successfully cooked {recipe_name}!", 2.0)
            return True, recipe_name
        else:
            self.show_result("That combination doesn't make a valid dish", 2.0)
            return False, None
            
    def reset(self):
        """Reset all selections"""
        self.selected_ingredients = []
        self.selected_tools = []
        
        for button in self.ingredient_buttons:
            button.selected = False
            
        for button in self.tool_buttons:
            button.selected = False
            
    def show_result(self, message, duration=2.0):
        """Show a result message
        
        Args:
            message: Message text
            duration: Duration in seconds
        """
        self.result_message = message
        self.result_timer = duration
        
    def render(self, screen):
        """Render the recipe creator
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen with a light color
        screen.fill(BEIGE)
        
        # Draw title
        self.text_renderer.render_text(
            screen,
            "Cooking Station",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            50,
            "center"
        )
        
        # Draw sections
        self.text_renderer.render_text(
            screen,
            "Ingredients",
            "medium",
            BLACK,
            50,
            120,
            "left"
        )
        
        self.text_renderer.render_text(
            screen,
            "Tools",
            "medium",
            BLACK,
            450,
            120,
            "left"
        )
        
        # Create a clipping rect for the scrollable area
        scroll_area = pygame.Rect(0, 150, SCREEN_WIDTH, self.scroll_area_height)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            scrollbar_height = self.scroll_area_height * (self.scroll_area_height / (self.scroll_area_height + self.max_scroll))
            scrollbar_pos = 150 + (self.scroll_offset / self.max_scroll) * (self.scroll_area_height - scrollbar_height)
            pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH - 20, scrollbar_pos, 10, scrollbar_height))
            pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 20, scrollbar_pos, 10, scrollbar_height), 1)
        
        # Draw ingredient buttons (with scrolling)
        for button in self.ingredient_buttons:
            # Adjust button position for scrolling
            button_rect = button.rect.copy()
            button_rect.y -= self.scroll_offset
            
            # Only draw buttons that are in the visible area
            if scroll_area.colliderect(button_rect):
                # Store original rect
                original_rect = button.rect
                
                # Temporarily set the rect to the scrolled position
                button.rect = button_rect
                button.draw(screen)
                
                # Restore original rect
                button.rect = original_rect
        
        # Draw tool buttons (with scrolling)
        for button in self.tool_buttons:
            # Adjust button position for scrolling
            button_rect = button.rect.copy()
            button_rect.y -= self.scroll_offset
            
            # Only draw buttons that are in the visible area
            if scroll_area.colliderect(button_rect):
                # Store original rect
                original_rect = button.rect
                
                # Temporarily set the rect to the scrolled position
                button.rect = button_rect
                button.draw(screen)
                
                # Restore original rect
                button.rect = original_rect
        
        # Draw cook button (fixed position)
        self.cook_button.draw(screen)
        
        # Draw back button (fixed position)
        self.back_button.draw(screen)
        
        # Draw selected ingredients and tools
        selected_text = f"Selected: {', '.join(self.selected_ingredients)} | Tools: {', '.join(self.selected_tools)}"
        self.text_renderer.render_text(
            screen,
            selected_text,
            "small",
            BLACK,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 200,
            "center"
        )
        
        # Draw result message if active
        if self.result_message:
            self.text_renderer.render_text(
                screen,
                self.result_message,
                "medium",
                BLACK,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 100,
                "center"
            )
