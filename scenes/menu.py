"""
Main menu scene
"""
import pygame
import os
import json
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, GREEN, PASTEL_COLORS

class MainMenu:
    def __init__(self):
        self.text_renderer = TextRenderer()
        
        # Check if save file exists
        self.has_save = os.path.exists("data/save.json")
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        if self.has_save:
            # If save exists, show continue and new game options
            self.continue_button = Button(
                button_x,
                280,
                button_width,
                button_height,
                "Continue Game",
                PASTEL_COLORS[2]  # Pastel Orange
            )
            
            self.new_game_button = Button(
                button_x,
                350,
                button_width,
                button_height,
                "New Game",
                PASTEL_COLORS[3]  # Pastel Green
            )
            
            self.about_button = Button(
                button_x,
                420,
                button_width,
                button_height,
                "About",
                PASTEL_COLORS[1]  # Pastel Blue
            )
            
            self.exit_button = Button(
                button_x,
                490,
                button_width,
                button_height,
                "Exit Game",
                PASTEL_COLORS[0]  # Pastel Pink
            )
        else:
            # If no save, just show start game option
            self.start_button = Button(
                button_x,
                300,
                button_width,
                button_height,
                "Start Game",
                GREEN
            )
            
            self.about_button = Button(
                button_x,
                370,
                button_width,
                button_height,
                "About"
            )
            
            self.exit_button = Button(
                button_x,
                440,
                button_width,
                button_height,
                "Exit Game"
            )
            
        # Confirmation dialog for new game
        self.show_confirmation = False
        self.confirm_yes_button = Button(
            SCREEN_WIDTH // 2 - 120,
            SCREEN_HEIGHT // 2 + 20,
            100,
            40,
            "Yes",
            PASTEL_COLORS[3]  # Pastel Green
        )
        
        self.confirm_no_button = Button(
            SCREEN_WIDTH // 2 + 20,
            SCREEN_HEIGHT // 2 + 20,
            100,
            40,
            "No",
            PASTEL_COLORS[0]  # Pastel Pink
        )
        
    def handle_events(self, events):
        """Handle events for the main menu
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
            dict: Additional data to pass to the next scene
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        if self.has_save:
            self.continue_button.is_hovered(mouse_pos)
            self.new_game_button.is_hovered(mouse_pos)
        else:
            self.start_button.is_hovered(mouse_pos)
            
        self.about_button.is_hovered(mouse_pos)
        self.exit_button.is_hovered(mouse_pos)
        
        if self.show_confirmation:
            self.confirm_yes_button.is_hovered(mouse_pos)
            self.confirm_no_button.is_hovered(mouse_pos)
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.has_save:
                    return "game", {}
                else:
                    return "game", {"new_game": True}
                    
            if self.show_confirmation:
                # Handle confirmation dialog
                if self.confirm_yes_button.is_clicked(mouse_pos, event):
                    self._reset_game()
                    return "game", {"new_game": True}
                    
                if self.confirm_no_button.is_clicked(mouse_pos, event):
                    self.show_confirmation = False
                    
            else:
                # Handle main menu buttons
                if self.has_save:
                    if self.continue_button.is_clicked(mouse_pos, event):
                        return "game", {}
                        
                    if self.new_game_button.is_clicked(mouse_pos, event):
                        self.show_confirmation = True
                else:
                    if self.start_button.is_clicked(mouse_pos, event):
                        return "game", {"new_game": True}
                    
                if self.about_button.is_clicked(mouse_pos, event):
                    return "about", {}
                    
                if self.exit_button.is_clicked(mouse_pos, event):
                    pygame.quit()
                    import sys
                    sys.exit()
                
        return None, {}
        
    def _reset_game(self):
        """Reset the game by deleting save files"""
        save_files = ["data/save.json", "data/profile.json", "data/game_state.json"]
        for file in save_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
        
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
        # Clear screen with a pastel background
        screen.fill(PASTEL_COLORS[7])  # Pastel Lavender
        
        # Draw title
        self.text_renderer.render_text(
            screen, 
            "Kusina ni Jai", 
            "title", 
            BLACK, 
            SCREEN_WIDTH // 2, 
            150, 
            "center"
        )
        
        self.text_renderer.render_text(
            screen, 
            "A Cooking Simulation Game", 
            "medium", 
            BLACK, 
            SCREEN_WIDTH // 2, 
            220, 
            "center"
        )
        
        # Draw buttons
        if self.has_save:
            self.continue_button.draw(screen)
            self.new_game_button.draw(screen)
        else:
            self.start_button.draw(screen)
            
        self.about_button.draw(screen)
        self.exit_button.draw(screen)
        
        # Draw instructions
        self.text_renderer.render_text(
            screen, 
            "Press ENTER to start", 
            "medium", 
            BLACK, 
            SCREEN_WIDTH // 2, 
            560, 
            "center"
        )
        
        # Draw confirmation dialog if active
        if self.show_confirmation:
            self._render_confirmation_dialog(screen)
            
    def _render_confirmation_dialog(self, screen):
        """Render the confirmation dialog
        
        Args:
            screen: Pygame surface to render on
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Draw dialog box
        dialog_width = 400
        dialog_height = 200
        dialog_x = SCREEN_WIDTH // 2 - dialog_width // 2
        dialog_y = SCREEN_HEIGHT // 2 - dialog_height // 2
        
        pygame.draw.rect(screen, PASTEL_COLORS[6], (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Draw message
        self.text_renderer.render_text(
            screen,
            "Start a new game?",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 40,
            "center"
        )
        
        self.text_renderer.render_text(
            screen,
            "This will delete your current progress.",
            "medium",
            BLACK,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 10,
            "center"
        )
        
        # Draw buttons
        self.confirm_yes_button.draw(screen)
        self.confirm_no_button.draw(screen)
