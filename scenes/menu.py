"""
Main menu scene
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, GREEN

class MainMenu:
    def __init__(self):
        self.text_renderer = TextRenderer()
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 100,
            350,
            200,
            50,
            "Start Game",
            GREEN
        )
        
    def handle_events(self, events):
        """Handle events for the main menu
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.is_hovered(mouse_pos)
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "game"
                
            if self.start_button.is_clicked(mouse_pos, event):
                return "game"
                
        return None
        
    def update(self, dt):
        """Update the main menu
        
        Args:
            dt: Time delta in seconds
        """
        pass
        
    def render(self, screen):
        """Render the main menu
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill((240, 240, 240))
        
        # Draw title
        self.text_renderer.render_text(
            screen, 
            "Kusina ni Jai", 
            "title", 
            BLACK, 
            SCREEN_WIDTH // 2, 
            200, 
            "center"
        )
        
        self.text_renderer.render_text(
            screen, 
            "A Cooking Simulation Game", 
            "medium", 
            BLACK, 
            SCREEN_WIDTH // 2, 
            280, 
            "center"
        )
        
        # Draw start button
        self.start_button.draw(screen)
        
        # Draw instructions
        self.text_renderer.render_text(
            screen, 
            "Press ENTER to start", 
            "medium", 
            BLACK, 
            SCREEN_WIDTH // 2, 
            450, 
            "center"
        )
