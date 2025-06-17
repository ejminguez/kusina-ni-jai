"""
Recipe book scene for viewing discovered recipes
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, LIGHT_GRAY, BEIGE

class RecipeBook:
    def __init__(self, recipe_system):
        self.recipe_system = recipe_system
        self.text_renderer = TextRenderer()
        
        # UI elements
        self.back_button = Button(50, SCREEN_HEIGHT - 70, 100, 40, "Back")
        
        # Recipe navigation
        self.current_page = 0
        self.recipes_per_page = 1  # Show one recipe per page for book-like appearance
        self.next_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2, 100, 40, "Next")
        self.prev_button = Button(50, SCREEN_HEIGHT // 2, 100, 40, "Previous")
        
        # Selected recipe details
        self.selected_recipe = None
        
        # Table of contents mode
        self.show_table_of_contents = True
        self.toc_buttons = []
        self.update_toc_buttons()
        
    def update_toc_buttons(self):
        """Update table of contents buttons"""
        self.toc_buttons = []
        discovered_recipes = self.recipe_system.get_discovered_recipes()
        
        button_height = 40
        button_width = 300
        button_margin = 10
        start_y = 150
        
        for i, recipe in enumerate(discovered_recipes):
            y = start_y + i * (button_height + button_margin)
            self.toc_buttons.append({
                "rect": pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, y, button_width, button_height),
                "recipe": recipe,
                "index": i
            })
        
    def handle_events(self, events):
        """Handle events for the recipe book
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        self.back_button.is_hovered(mouse_pos)
        self.next_button.is_hovered(mouse_pos)
        self.prev_button.is_hovered(mouse_pos)
        
        for event in events:
            # Check back button
            if self.back_button.is_clicked(mouse_pos, event):
                return "game"
                
            if self.show_table_of_contents:
                # Check table of contents buttons
                for button in self.toc_buttons:
                    if button["rect"].collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                        self.current_page = button["index"]
                        self.selected_recipe = button["recipe"]
                        self.show_table_of_contents = False
                        return None
            else:
                # Check navigation buttons
                if self.next_button.is_clicked(mouse_pos, event):
                    self._next_page()
                    
                if self.prev_button.is_clicked(mouse_pos, event):
                    self._prev_page()
                    
                # Check for table of contents button
                toc_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 40)
                if toc_button_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.show_table_of_contents = True
                    self.update_toc_buttons()
                    return None
                    
        return None
            
    def _next_page(self):
        """Go to next page of recipes"""
        discovered_recipes = self.recipe_system.get_discovered_recipes()
        max_pages = len(discovered_recipes)
        
        if self.current_page < max_pages - 1:
            self.current_page += 1
            self.selected_recipe = discovered_recipes[self.current_page]
            
    def _prev_page(self):
        """Go to previous page of recipes"""
        discovered_recipes = self.recipe_system.get_discovered_recipes()
        
        if self.current_page > 0:
            self.current_page -= 1
            self.selected_recipe = discovered_recipes[self.current_page]
        
    def update(self, dt):
        """Update the recipe book
        
        Args:
            dt: Time delta in seconds
        """
        pass
        
    def render(self, screen):
        """Render the recipe book
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BEIGE)
        
        # Draw title
        self.text_renderer.render_text(
            screen,
            "Recipe Book",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            50,
            "center"
        )
        
        # Draw recipe book
        discovered_recipes = self.recipe_system.get_discovered_recipes()
        
        if not discovered_recipes:
            self.text_renderer.render_text(
                screen,
                "No recipes discovered yet!",
                "medium",
                BLACK,
                SCREEN_WIDTH // 2,
                250,
                "center"
            )
        else:
            if self.show_table_of_contents:
                self._render_table_of_contents(screen, discovered_recipes)
            else:
                self._render_recipe_page(screen, discovered_recipes)
        
        # Draw back button
        self.back_button.draw(screen)
                
    def _render_table_of_contents(self, screen, recipes):
        """Render the table of contents
        
        Args:
            screen: Pygame surface to render on
            recipes: List of recipes to display
        """
        # Draw table of contents title
        self.text_renderer.render_text(
            screen,
            "Table of Contents",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            100,
            "center"
        )
        
        # Draw recipe buttons
        for button in self.toc_buttons:
            # Draw button background
            pygame.draw.rect(screen, (220, 220, 220), button["rect"])
            pygame.draw.rect(screen, BLACK, button["rect"], 2)
            
            # Draw recipe name
            self.text_renderer.render_text(
                screen,
                button["recipe"].name,
                "medium",
                BLACK,
                button["rect"].centerx,
                button["rect"].centery,
                "center"
            )
            
            # Draw difficulty stars
            difficulty_stars = "★" * button["recipe"].difficulty
            self.text_renderer.render_text(
                screen,
                f"Difficulty: {difficulty_stars}",
                "small",
                BLACK,
                button["rect"].right - 10,
                button["rect"].centery,
                "right"
            )
            
    def _render_recipe_page(self, screen, recipes):
        """Render a recipe page
        
        Args:
            screen: Pygame surface to render on
            recipes: List of recipes
        """
        # Calculate page info
        max_pages = len(recipes)
        
        if self.current_page >= len(recipes):
            self.current_page = 0
            
        recipe = recipes[self.current_page]
        self.selected_recipe = recipe
        
        # Draw page info
        self.text_renderer.render_text(
            screen,
            f"Page {self.current_page + 1} of {max_pages}",
            "small",
            BLACK,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 30,
            "center"
        )
        
        # Draw book background
        book_width = 600
        book_height = SCREEN_HEIGHT - 200
        book_x = SCREEN_WIDTH // 2 - book_width // 2
        book_y = 100
        
        # Draw book border
        pygame.draw.rect(screen, (220, 220, 220), (book_x, book_y, book_width, book_height))
        pygame.draw.rect(screen, BLACK, (book_x, book_y, book_width, book_height), 2)
        
        # Draw recipe name
        self.text_renderer.render_text(
            screen,
            recipe.name,
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            book_y + 40,
            "center"
        )
        
        # Draw decorative line
        line_y = book_y + 70
        pygame.draw.line(screen, BLACK, (book_x + 50, line_y), (book_x + book_width - 50, line_y), 2)
        
        # Difficulty
        difficulty_stars = "★" * recipe.difficulty
        self.text_renderer.render_text(
            screen,
            f"Difficulty: {difficulty_stars}",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            book_y + 100,
            "center"
        )
        
        # Cooking time
        self.text_renderer.render_text(
            screen,
            f"Cooking Time: {recipe.cooking_time} seconds",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            book_y + 130,
            "center"
        )
        
        # Ingredients
        self.text_renderer.render_text(
            screen,
            "Ingredients:",
            "medium",
            BLACK,
            book_x + 50,
            book_y + 180,
            "left"
        )
        
        for i, ingredient in enumerate(recipe.ingredients):
            self.text_renderer.render_text(
                screen,
                f"- {ingredient}",
                "small",
                BLACK,
                book_x + 70,
                book_y + 210 + i * 25,
                "left"
            )
            
        # Tools
        tools_y = book_y + 210 + len(recipe.ingredients) * 25 + 20
        self.text_renderer.render_text(
            screen,
            "Tools:",
            "medium",
            BLACK,
            book_x + 50,
            tools_y,
            "left"
        )
        
        for i, tool in enumerate(recipe.tools):
            self.text_renderer.render_text(
                screen,
                f"- {tool}",
                "small",
                BLACK,
                book_x + 70,
                tools_y + 30 + i * 25,
                "left"
            )
            
        # Draw navigation buttons
        if self.current_page < max_pages - 1:
            self.next_button.draw(screen)
            
        if self.current_page > 0:
            self.prev_button.draw(screen)
            
        # Draw table of contents button
        toc_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 40)
        pygame.draw.rect(screen, (220, 220, 220), toc_button_rect)
        pygame.draw.rect(screen, BLACK, toc_button_rect, 2)
        
        self.text_renderer.render_text(
            screen,
            "Table of Contents",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 50,
            "center"
        )
