"""
Sprite manager for loading and handling game sprites
"""
import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.spritesheets = {}
        self.original_screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.current_screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.scale_factor_x = 1.0
        self.scale_factor_y = 1.0
        
    def load_sprite(self, name, path, scale=1.0):
        """Load a single sprite
        
        Args:
            name: Name to reference the sprite
            path: Path to the sprite image
            scale: Scale factor for the sprite
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            if os.path.exists(path):
                sprite = pygame.image.load(path).convert_alpha()
                
                # Scale the sprite
                width = int(sprite.get_width() * scale)
                height = int(sprite.get_height() * scale)
                sprite = pygame.transform.scale(sprite, (width, height))
                
                self.sprites[name] = sprite
                return True
            else:
                # Create a placeholder sprite
                self._create_placeholder(name, 64, 64)
                return False
        except pygame.error:
            # Create a placeholder sprite
            self._create_placeholder(name, 64, 64)
            return False
            
    def _create_placeholder(self, name, width, height):
        """Create a placeholder sprite
        
        Args:
            name: Name to reference the sprite
            width: Width of the placeholder
            height: Height of the placeholder
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw a simple placeholder (colored rectangle with text)
        pygame.draw.rect(surface, (200, 200, 200), (0, 0, width, height))
        pygame.draw.rect(surface, (100, 100, 100), (0, 0, width, height), 2)
        
        # Add text if the font module is initialized
        if pygame.font.get_init():
            font = pygame.font.SysFont(None, 14)
            text = font.render(name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            surface.blit(text, text_rect)
            
        self.sprites[name] = surface
        
    def load_spritesheet(self, name, path, sprite_width, sprite_height, rows, cols):
        """Load a spritesheet and split it into individual sprites
        
        Args:
            name: Base name for the sprites
            path: Path to the spritesheet image
            sprite_width: Width of each sprite in the sheet
            sprite_height: Height of each sprite in the sheet
            rows: Number of rows in the spritesheet
            cols: Number of columns in the spritesheet
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            if os.path.exists(path):
                sheet = pygame.image.load(path).convert_alpha()
                self.spritesheets[name] = sheet
                
                # Split the spritesheet into individual sprites
                for row in range(rows):
                    for col in range(cols):
                        x = col * sprite_width
                        y = row * sprite_height
                        sprite = sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                        sprite_name = f"{name}_{row}_{col}"
                        self.sprites[sprite_name] = sprite
                        
                return True
            else:
                # Create placeholder sprites
                for row in range(rows):
                    for col in range(cols):
                        sprite_name = f"{name}_{row}_{col}"
                        self._create_placeholder(sprite_name, sprite_width, sprite_height)
                return False
        except pygame.error:
            # Create placeholder sprites
            for row in range(rows):
                for col in range(cols):
                    sprite_name = f"{name}_{row}_{col}"
                    self._create_placeholder(sprite_name, sprite_width, sprite_height)
            return False
            
    def get_sprite(self, name):
        """Get a sprite by name
        
        Args:
            name: Name of the sprite
            
        Returns:
            Surface: The sprite surface or a placeholder if not found
        """
        if name in self.sprites:
            return self.sprites[name]
        else:
            # Create a placeholder if the sprite doesn't exist
            self._create_placeholder(name, 64, 64)
            return self.sprites[name]
            
    def update_screen_size(self, width, height):
        """Update the scale factors based on new screen size
        
        Args:
            width: New screen width
            height: New screen height
        """
        self.current_screen_size = (width, height)
        self.scale_factor_x = width / self.original_screen_size[0]
        self.scale_factor_y = height / self.original_screen_size[1]
        
    def get_scaled_rect(self, x, y, width, height):
        """Get a scaled rectangle based on the current scale factors
        
        Args:
            x, y: Position of the rectangle
            width, height: Dimensions of the rectangle
            
        Returns:
            Rect: Scaled rectangle
        """
        return pygame.Rect(
            int(x * self.scale_factor_x),
            int(y * self.scale_factor_y),
            int(width * self.scale_factor_x),
            int(height * self.scale_factor_y)
        )
        
    def scale_rect(self, rect):
        """Scale a rectangle based on the current scale factors
        
        Args:
            rect: Rectangle to scale
            
        Returns:
            Rect: Scaled rectangle
        """
        return pygame.Rect(
            int(rect.x * self.scale_factor_x),
            int(rect.y * self.scale_factor_y),
            int(rect.width * self.scale_factor_x),
            int(rect.height * self.scale_factor_y)
        )
        
    def scale_pos(self, pos):
        """Scale a position based on the current scale factors
        
        Args:
            pos: Position tuple (x, y)
            
        Returns:
            tuple: Scaled position
        """
        return (
            int(pos[0] * self.scale_factor_x),
            int(pos[1] * self.scale_factor_y)
        )
        
    def scale_sprite(self, sprite, width=None, height=None):
        """Scale a sprite to a specific size or by the global scale factors
        
        Args:
            sprite: Sprite surface to scale
            width: Target width (optional)
            height: Target height (optional)
            
        Returns:
            Surface: Scaled sprite
        """
        if width is None:
            width = int(sprite.get_width() * self.scale_factor_x)
        if height is None:
            height = int(sprite.get_height() * self.scale_factor_y)
            
        return pygame.transform.scale(sprite, (width, height))
        
    def get_scaled_font_size(self, size):
        """Get a scaled font size based on the current scale factors
        
        Args:
            size: Original font size
            
        Returns:
            int: Scaled font size
        """
        # Use the average of x and y scale factors for font scaling
        scale = (self.scale_factor_x + self.scale_factor_y) / 2
        return int(size * scale)
