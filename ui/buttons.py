"""
Button classes for UI elements
"""
import pygame
from config import BLACK, GRAY, GREEN, BLUE, RED

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, text_color=BLACK, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, font_size)
        self.hovered = False
        
    def draw(self, screen):
        # Draw button with slightly lighter color when hovered
        current_color = tuple(min(c + 20, 255) for c in self.color) if self.hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            return True
        return False


class ToggleButton(Button):
    def __init__(self, x, y, width, height, text, color=GRAY, selected_color=GREEN, text_color=BLACK, font_size=24):
        super().__init__(x, y, width, height, text, color, text_color, font_size)
        self.selected = False
        self.selected_color = selected_color
        
    def draw(self, screen):
        # Use selected color if selected
        current_color = self.selected_color if self.selected else self.color
        if self.hovered and not self.selected:
            current_color = tuple(min(c + 20, 255) for c in current_color)
            
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def toggle(self):
        self.selected = not self.selected
        return self.selected


class IngredientButton(ToggleButton):
    def __init__(self, x, y, width, height, ingredient_name, color=GRAY, selected_color=GREEN, text_color=BLACK, font_size=24):
        super().__init__(x, y, width, height, ingredient_name, color, selected_color, text_color, font_size)
        self.ingredient_name = ingredient_name


class ToolButton(ToggleButton):
    def __init__(self, x, y, width, height, tool_name, color=GRAY, selected_color=BLUE, text_color=BLACK, font_size=24):
        super().__init__(x, y, width, height, tool_name, color, selected_color, text_color, font_size)
        self.tool_name = tool_name


class CookButton(Button):
    def __init__(self, x, y, width, height, text="Cook!", color=RED, text_color=BLACK, font_size=32):
        super().__init__(x, y, width, height, text, color, text_color, font_size)
