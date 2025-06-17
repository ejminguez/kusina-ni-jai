"""
Game over scene
"""
import pygame
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
        
    def handle_events(self, events):
        """Handle events for the game over scene
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        self.restart_button.is_hovered(mouse_pos)
        self.menu_button.is_hovered(mouse_pos)
        self.quit_button.is_hovered(mouse_pos)
        
        for event in events:
            # Check restart button
            if self.restart_button.is_clicked(mouse_pos, event):
                # Reset player state for a new game
                self.player.coins = 100
                self.player.consecutive_lost_customers = 0
                self.player.save_player_data()
                return "game"
                
            # Check menu button
            if self.menu_button.is_clicked(mouse_pos, event):
                return "menu"
                
            # Check quit button
            if self.quit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                import sys
                sys.exit()
                
        return None
        
    def update(self, dt):
        """Update the game over scene
        
        Args:
            dt: Time delta in seconds
        """
        pass
        
    def render(self, screen):
        """Render the game over scene
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen with dark color
        screen.fill((50, 0, 0))
        
        # Draw title
        self.text_renderer.render_text(
            screen,
            "GAME OVER",
            "title",
            DARK_RED,
            SCREEN_WIDTH // 2,
            150,
            "center"
        )
        
        # Draw reason
        self.text_renderer.render_text(
            screen,
            "Too many unsatisfied customers!",
            "large",
            (255, 100, 100),
            SCREEN_WIDTH // 2,
            220,
            "center"
        )
        
        # Draw stats
        self.text_renderer.render_text(
            screen,
            f"Final Level: {self.player.level}",
            "medium",
            (200, 200, 200),
            SCREEN_WIDTH // 2,
            280,
            "center"
        )
        
        self.text_renderer.render_text(
            screen,
            f"Coins Earned: {self.player.coins}",
            "medium",
            (200, 200, 200),
            SCREEN_WIDTH // 2,
            320,
            "center"
        )
        
        # Draw buttons
        self.restart_button.draw(screen)
        self.menu_button.draw(screen)
        self.quit_button.draw(screen)
