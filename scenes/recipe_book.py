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
        self.recipes_per_page = 4
        self.next_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 100, 40, "Next")
        self.prev_button = Button(SCREEN_WIDTH - 270, SCREEN_HEIGHT - 70, 100, 40, "Previous")
        
        # Selected recipe details
        self.selected_recipe = None
        
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
                
            # Check navigation buttons
            if self.next_button.is_clicked(mouse_pos, event):
                self._next_page()
                
            if self.prev_button.is_clicked(mouse_pos, event):
                self._prev_page()
                
            # Check recipe selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._check_recipe_selection(mouse_pos)
                
        return None
        
    def _next_page(self):
        """Go to next page of recipes"""
        discovered_recipes = self.recipe_system.get_discovered_recipes()
        max_pages = (len(discovered_recipes) - 1) // self.recipes_per_page + 1
        
        if self.current_page < max_pages - 1:
            self.current_page += 1
            self.selected_recipe = None
            
    def _prev_page(self):
        """Go to previous page of recipes"""
        if self.current_page > 0:
            self.current_page -= 1
            self.selected_recipe = None
            
    def _check_recipe_selection(self, mouse_pos):
        """Check if a recipe was clicked
        
        Args:
            mouse_pos: Mouse position tuple
        """
        discovered_recipes = self.recipe_system.get_discovered_recipes()
        start_idx = self.current_page * self.recipes_per_page
        end_idx = min(start_idx + self.recipes_per_page, len(discovered_recipes))
        
        for i in range(start_idx, end_idx):
            recipe_idx = i - start_idx
            recipe_rect = pygame.Rect(50, 150 + recipe_idx * 60, 300, 50)
            
            if recipe_rect.collidepoint(mouse_pos):
                self.selected_recipe = discovered_recipes[i]
                break
        
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
        
        # Draw recipe list
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
            # Calculate page info
            start_idx = self.current_page * self.recipes_per_page
            end_idx = min(start_idx + self.recipes_per_page, len(discovered_recipes))
            max_pages = (len(discovered_recipes) - 1) // self.recipes_per_page + 1
            
            # Draw page info
            self.text_renderer.render_text(
                screen,
                f"Page {self.current_page + 1} of {max_pages}",
                "small",
                BLACK,
                SCREEN_WIDTH // 2,
                100,
                "center"
            )
            
            # Draw recipe list
            for i in range(start_idx, end_idx):
                recipe_idx = i - start_idx
                recipe = discovered_recipes[i]
                
                # Draw recipe box
                recipe_rect = pygame.Rect(50, 150 + recipe_idx * 60, 300, 50)
                color = (220, 220, 180) if self.selected_recipe == recipe else (200, 200, 200)
                pygame.draw.rect(screen, color, recipe_rect)
                pygame.draw.rect(screen, BLACK, recipe_rect, 2)
                
                # Draw recipe name
                self.text_renderer.render_text(
                    screen,
                    recipe.name,
                    "medium",
                    BLACK,
                    recipe_rect.centerx,
                    recipe_rect.centery,
                    "center"
                )
            
            # Draw selected recipe details
            if self.selected_recipe:
                detail_rect = pygame.Rect(400, 150, SCREEN_WIDTH - 450, 300)
                pygame.draw.rect(screen, (220, 220, 220), detail_rect)
                pygame.draw.rect(screen, BLACK, detail_rect, 2)
                
                # Recipe name
                self.text_renderer.render_text(
                    screen,
                    self.selected_recipe.name,
                    "medium",
                    BLACK,
                    detail_rect.centerx,
                    170,
                    "center"
                )
                
                # Difficulty
                difficulty_stars = "★" * self.selected_recipe.difficulty
                self.text_renderer.render_text(
                    screen,
                    f"Difficulty: {difficulty_stars}",
                    "small",
                    BLACK,
                    detail_rect.centerx,
                    200,
                    "center"
                )
                
                # Cooking time
                self.text_renderer.render_text(
                    screen,
                    f"Cooking Time: {self.selected_recipe.cooking_time} seconds",
                    "small",
                    BLACK,
                    detail_rect.centerx,
                    230,
                    "center"
                )
                
                # Ingredients
                self.text_renderer.render_text(
                    screen,
                    "Ingredients:",
                    "small",
                    BLACK,
                    420,
                    260,
                    "left"
                )
                
                for i, ingredient in enumerate(self.selected_recipe.ingredients):
                    self.text_renderer.render_text(
                        screen,
                        f"- {ingredient}",
                        "small",
                        BLACK,
                        440,
                        290 + i * 25,
                        "left"
                    )
                    
                # Tools
                tools_y = 260 + len(self.selected_recipe.ingredients) * 25 + 20
                self.text_renderer.render_text(
                    screen,
                    "Tools:",
                    "small",
                    BLACK,
                    420,
                    tools_y,
                    "left"
                )
                
                for i, tool in enumerate(self.selected_recipe.tools):
                    self.text_renderer.render_text(
                        screen,
                        f"- {tool}",
                        "small",
                        BLACK,
                        440,
                        tools_y + 30 + i * 25,
                        "left"
                    )
        
        # Draw navigation buttons
        self.back_button.draw(screen)
        
        if discovered_recipes:
            max_pages = (len(discovered_recipes) - 1) // self.recipes_per_page + 1
            
            if self.current_page < max_pages - 1:
                self.next_button.draw(screen)
                
            if self.current_page > 0:
                self.prev_button.draw(screen)
