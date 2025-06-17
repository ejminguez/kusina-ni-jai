"""
About scene
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, BEIGE

class AboutScene:
    def __init__(self):
        self.text_renderer = TextRenderer()
        self.back_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 70, 100, 40, "Back")
        
    def handle_events(self, events):
        """Handle events for the about scene
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.is_hovered(mouse_pos)
        
        for event in events:
            if self.back_button.is_clicked(mouse_pos, event):
                return "menu"
                
        return None
        
    def update(self, dt):
        """Update the about scene
        
        Args:
            dt: Time delta in seconds
        """
        pass
        
    def render(self, screen):
        """Render the about scene
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BEIGE)
        
        # Draw title
        self.text_renderer.render_text(
            screen,
            "About Kusina ni Jai",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            50,
            "center"
        )
        
        # Draw developer info
        self.text_renderer.render_text(
            screen,
            "Developed by: Jai Minguez",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            120,
            "center"
        )
        
        # Draw game description
        about_text = [
            "Kusina ni Jai is a cooking simulation game where you play as a chef",
            "serving customers with both known and custom Filipino recipes.",
            "",
            "This game was created as a project to showcase Filipino cuisine",
            "and provide a fun, educational experience about cooking.",
            "",
            "The game features traditional Filipino dishes like Adobo, Sinigang,",
            "Lumpia, and many more, along with their key ingredients.",
            "",
            "I hope you enjoy playing this game as much as I enjoyed creating it!"
        ]
        
        y_pos = 180
        for line in about_text:
            self.text_renderer.render_text(
                screen,
                line,
                "small",
                BLACK,
                SCREEN_WIDTH // 2,
                y_pos,
                "center"
            )
            y_pos += 30
            
        # Draw inspiration section
        self.text_renderer.render_text(
            screen,
            "Inspiration",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            y_pos + 20,
            "center"
        )
        
        inspiration_text = [
            "This game was inspired by my love for Filipino food and cooking games.",
            "I wanted to create something that celebrates our culinary heritage",
            "while also being fun and engaging for players of all backgrounds.",
            "",
            "Special thanks to my family for their support and recipe suggestions!"
        ]
        
        y_pos += 60
        for line in inspiration_text:
            self.text_renderer.render_text(
                screen,
                line,
                "small",
                BLACK,
                SCREEN_WIDTH // 2,
                y_pos,
                "center"
            )
            y_pos += 30
        
        # Draw back button
        self.back_button.draw(screen)
