"""
Text rendering utilities for the game
"""
import pygame
from config import BLACK, WHITE, RED, YELLOW, GREEN

class TextRenderer:
    def __init__(self):
        self.fonts = {
            'small': pygame.font.SysFont(None, 24),
            'medium': pygame.font.SysFont(None, 32),
            'large': pygame.font.SysFont(None, 48),
            'title': pygame.font.SysFont(None, 64)
        }
        
    def render_text(self, screen, text, size, color, x, y, align="left"):
        """Render text with specified parameters
        
        Args:
            screen: Pygame surface to render on
            text: Text string to render
            size: Font size ('small', 'medium', 'large', 'title')
            color: RGB color tuple
            x, y: Position coordinates
            align: Text alignment ('left', 'center', 'right')
        """
        font = self.fonts.get(size, self.fonts['medium'])
        text_surface = font.render(text, True, color)
        
        if align == "center":
            text_rect = text_surface.get_rect(center=(x, y))
        elif align == "right":
            text_rect = text_surface.get_rect(right=x, centery=y)
        else:  # left align
            text_rect = text_surface.get_rect(left=x, centery=y)
            
        screen.blit(text_surface, text_rect)
        return text_rect
        
    def render_multiline(self, screen, text_lines, size, color, x, y, line_spacing=5, align="left"):
        """Render multiple lines of text
        
        Args:
            screen: Pygame surface to render on
            text_lines: List of text strings
            size: Font size ('small', 'medium', 'large', 'title')
            color: RGB color tuple
            x, y: Position of first line
            line_spacing: Vertical space between lines
            align: Text alignment ('left', 'center', 'right')
        """
        font = self.fonts.get(size, self.fonts['medium'])
        height = font.get_height() + line_spacing
        
        for i, line in enumerate(text_lines):
            self.render_text(screen, line, size, color, x, y + i * height, align)
            
    def render_patience_bar(self, screen, x, y, width, height, patience_pct):
        """Render a patience bar with color based on percentage
        
        Args:
            screen: Pygame surface to render on
            x, y: Position of bar
            width, height: Dimensions of bar
            patience_pct: Percentage of patience remaining (0.0 to 1.0)
        """
        # Background bar
        pygame.draw.rect(screen, WHITE, (x, y, width, height))
        
        # Patience level
        if patience_pct > 0.6:
            color = GREEN  # Green
        elif patience_pct > 0.3:
            color = YELLOW  # Yellow
        else:
            color = RED  # Red
            
        pygame.draw.rect(screen, color, (x, y, int(width * patience_pct), height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 1)  # Border
