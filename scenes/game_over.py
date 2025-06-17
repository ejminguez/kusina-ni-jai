"""
Game over scene
"""
import pygame
import random
import math
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, DARK_RED, GREEN

class GameOver:
    def __init__(self, player):
        self.player = player
        self.text_renderer = TextRenderer()
        
        # UI elements
        self.restart_button = Button(SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Try Again", GREEN)
        self.menu_button = Button(SCREEN_WIDTH // 2 - 100, 470, 200, 50, "Main Menu")
        self.quit_button = Button(SCREEN_WIDTH // 2 - 100, 540, 200, 50, "Quit Game")
        
        # Screen shake effect
        self.shake_duration = 2.0  # seconds
        self.shake_intensity = 10  # pixels
        self.shake_timer = self.shake_duration
        self.shake_offset = (0, 0)
        
    def handle_events(self, events):
        """Handle events for the game over scene
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Adjust mouse position for screen shake
        adjusted_pos = (mouse_pos[0] - self.shake_offset[0], mouse_pos[1] - self.shake_offset[1])
        
        # Update button hover states
        self.restart_button.is_hovered(adjusted_pos)
        self.menu_button.is_hovered(adjusted_pos)
        self.quit_button.is_hovered(adjusted_pos)
        
        for event in events:
            # Check restart button
            if self.restart_button.is_clicked(adjusted_pos, event):
                # Reset player state for a new game
                self.player.coins = 100
                self.player.consecutive_lost_customers = 0
                self.player.save_player_data()
                return "game"
                
            # Check menu button
            if self.menu_button.is_clicked(adjusted_pos, event):
                return "menu"
                
            # Check quit button
            if self.quit_button.is_clicked(adjusted_pos, event):
                pygame.quit()
                import sys
                sys.exit()
                
        return None
        
    def update(self, dt):
        """Update the game over scene
        
        Args:
            dt: Time delta in seconds
        """
        # Update screen shake
        if self.shake_timer > 0:
            self.shake_timer -= dt
            
            # Calculate shake intensity based on remaining time
            intensity = self.shake_intensity * (self.shake_timer / self.shake_duration)
            
            # Generate random offset
            if intensity > 0.5:  # Only shake if intensity is significant
                self.shake_offset = (
                    random.uniform(-intensity, intensity),
                    random.uniform(-intensity, intensity)
                )
            else:
                self.shake_offset = (0, 0)
        else:
            self.shake_offset = (0, 0)
        
    def render(self, screen):
        """Render the game over scene
        
        Args:
            screen: Pygame surface to render on
        """
        # Create a surface for the content (to apply shake)
        content_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Clear screen with dark color
        content_surface.fill((50, 0, 0))
        
        # Draw title
        self.text_renderer.render_text(
            content_surface,
            "GAME OVER",
            "title",
            DARK_RED,
            SCREEN_WIDTH // 2,
            150,
            "center"
        )
        
        # Draw reason
        self.text_renderer.render_text(
            content_surface,
            "Too many unsatisfied customers!",
            "large",
            (255, 100, 100),
            SCREEN_WIDTH // 2,
            220,
            "center"
        )
        
        # Draw stats
        self.text_renderer.render_text(
            content_surface,
            f"Final Level: {self.player.level}",
            "medium",
            (200, 200, 200),
            SCREEN_WIDTH // 2,
            280,
            "center"
        )
        
        self.text_renderer.render_text(
            content_surface,
            f"Coins Earned: {self.player.coins}",
            "medium",
            (200, 200, 200),
            SCREEN_WIDTH // 2,
            320,
            "center"
        )
        
        # Draw buttons
        self.restart_button.draw(content_surface)
        self.menu_button.draw(content_surface)
        self.quit_button.draw(content_surface)
        
        # Apply screen shake by blitting the content surface with an offset
        screen.blit(content_surface, self.shake_offset)
