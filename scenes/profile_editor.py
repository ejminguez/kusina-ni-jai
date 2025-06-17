"""
Profile editor scene for customizing player profile
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, LIGHT_GRAY, BEIGE, GREEN

class ProfileEditor:
    def __init__(self, player):
        self.player = player
        self.text_renderer = TextRenderer()
        
        # UI elements
        self.back_button = Button(50, SCREEN_HEIGHT - 70, 100, 40, "Back")
        self.save_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 70, 100, 40, "Save", GREEN)
        
        # Username input
        self.username = self.player.username
        self.username_active = False
        self.username_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 40)
        
        # Profile picture selection
        self.profile_pics = [
            "assets/sprites/default_profile.png",
            "assets/sprites/chef1.png",
            "assets/sprites/chef2.png",
            "assets/sprites/chef3.png"
        ]
        self.selected_pic = self.player.profile_pic
        self.pic_buttons = []
        
        # Create profile pic buttons
        for i, pic in enumerate(self.profile_pics):
            x = SCREEN_WIDTH // 2 - 150 + (i % 2) * 160
            y = 300 + (i // 2) * 160
            self.pic_buttons.append({
                "rect": pygame.Rect(x, y, 150, 150),
                "pic": pic
            })
            
    def handle_events(self, events):
        """Handle events for the profile editor
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        self.back_button.is_hovered(mouse_pos)
        self.save_button.is_hovered(mouse_pos)
        
        for event in events:
            # Check back button
            if self.back_button.is_clicked(mouse_pos, event):
                return "game"
                
            # Check save button
            if self.save_button.is_clicked(mouse_pos, event):
                self._save_profile()
                return "game"
                
            # Check username input
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if username field was clicked
                if self.username_rect.collidepoint(event.pos):
                    self.username_active = True
                else:
                    self.username_active = False
                    
                # Check if a profile pic was clicked
                for pic_button in self.pic_buttons:
                    if pic_button["rect"].collidepoint(event.pos):
                        self.selected_pic = pic_button["pic"]
                        
            # Handle text input for username
            if event.type == pygame.KEYDOWN and self.username_active:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_RETURN:
                    self.username_active = False
                else:
                    # Limit username length
                    if len(self.username) < 20:
                        self.username += event.unicode
                
        return None
        
    def _save_profile(self):
        """Save profile changes"""
        self.player.update_username(self.username)
        self.player.update_profile_pic(self.selected_pic)
        
    def update(self, dt):
        """Update the profile editor
        
        Args:
            dt: Time delta in seconds
        """
        pass
        
    def render(self, screen):
        """Render the profile editor
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BEIGE)
        
        # Draw title
        self.text_renderer.render_text(
            screen,
            "Edit Profile",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            50,
            "center"
        )
        
        # Draw username label
        self.text_renderer.render_text(
            screen,
            "Username:",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            170,
            "center"
        )
        
        # Draw username input box
        color = (180, 180, 220) if self.username_active else (200, 200, 200)
        pygame.draw.rect(screen, color, self.username_rect)
        pygame.draw.rect(screen, BLACK, self.username_rect, 2)
        
        # Draw username text
        self.text_renderer.render_text(
            screen,
            self.username,
            "medium",
            BLACK,
            self.username_rect.x + 10,
            self.username_rect.centery,
            "left"
        )
        
        # Draw profile picture label
        self.text_renderer.render_text(
            screen,
            "Select Profile Picture:",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            270,
            "center"
        )
        
        # Draw profile picture options
        for pic_button in self.pic_buttons:
            # Draw selection highlight
            if pic_button["pic"] == self.selected_pic:
                highlight_rect = pygame.Rect(
                    pic_button["rect"].x - 5,
                    pic_button["rect"].y - 5,
                    pic_button["rect"].width + 10,
                    pic_button["rect"].height + 10
                )
                pygame.draw.rect(screen, (100, 200, 100), highlight_rect)
            
            # Draw picture box
            pygame.draw.rect(screen, (200, 200, 200), pic_button["rect"])
            pygame.draw.rect(screen, BLACK, pic_button["rect"], 2)
            
            # Draw placeholder for profile picture
            # In a real implementation, you would load and draw the actual image here
            pygame.draw.circle(
                screen,
                (150, 150, 150),
                pic_button["rect"].center,
                50
            )
            
            # Draw picture name
            pic_name = pic_button["pic"].split("/")[-1].split(".")[0]
            self.text_renderer.render_text(
                screen,
                pic_name,
                "small",
                BLACK,
                pic_button["rect"].centerx,
                pic_button["rect"].bottom + 20,
                "center"
            )
        
        # Draw buttons
        self.back_button.draw(screen)
        self.save_button.draw(screen)
