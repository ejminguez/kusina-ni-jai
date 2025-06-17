"""
Main game loop scene
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, GREEN, BLUE, LIGHT_GRAY,
    MAX_CONSECUTIVE_LOST_CUSTOMERS
)

class GameScene:
    def __init__(self, player, customer_system):
        self.player = player
        self.customer_system = customer_system
        self.text_renderer = TextRenderer()
        
        # UI elements
        self.cooking_button = Button(50, 600, 150, 50, "Cook", GREEN)
        self.upgrade_button = Button(220, 600, 150, 50, "Upgrades", BLUE)
        self.recipe_book_button = Button(390, 600, 150, 50, "Recipe Book")
        self.profile_button = Button(560, 600, 150, 50, "Profile")
        self.save_button = Button(730, 600, 150, 50, "Save Game")
        
        # Menu buttons
        self.menu_button = Button(SCREEN_WIDTH - 120, 20, 100, 30, "Menu")
        self.pause_button = Button(SCREEN_WIDTH - 230, 20, 100, 30, "Pause")
        
        # Game state
        self.message = ""
        self.message_timer = 0
        self.paused = False
        self.pause_menu_active = False
        
        # Pause menu buttons
        self.resume_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50, "Resume")
        self.pause_menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Main Menu")
        self.pause_exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50, "Exit Game")
        
    def handle_events(self, events):
        """Handle events for the game scene
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # If pause menu is active, only handle pause menu events
        if self.pause_menu_active:
            self.resume_button.is_hovered(mouse_pos)
            self.pause_menu_button.is_hovered(mouse_pos)
            self.pause_exit_button.is_hovered(mouse_pos)
            
            for event in events:
                if self.resume_button.is_clicked(mouse_pos, event):
                    self.pause_menu_active = False
                    self.paused = False
                    return None
                    
                if self.pause_menu_button.is_clicked(mouse_pos, event):
                    self.pause_menu_active = False
                    self.paused = False
                    return "menu"
                    
                if self.pause_exit_button.is_clicked(mouse_pos, event):
                    pygame.quit()
                    import sys
                    sys.exit()
                    
            return None
        
        # Regular game events
        self.cooking_button.is_hovered(mouse_pos)
        self.upgrade_button.is_hovered(mouse_pos)
        self.recipe_book_button.is_hovered(mouse_pos)
        self.profile_button.is_hovered(mouse_pos)
        self.save_button.is_hovered(mouse_pos)
        self.menu_button.is_hovered(mouse_pos)
        self.pause_button.is_hovered(mouse_pos)
        
        for event in events:
            if self.cooking_button.is_clicked(mouse_pos, event):
                return "cooking"
                
            if self.upgrade_button.is_clicked(mouse_pos, event):
                return "upgrade"
                
            if self.recipe_book_button.is_clicked(mouse_pos, event):
                return "recipe_book"
                
            if self.profile_button.is_clicked(mouse_pos, event):
                return "profile"
                
            if self.save_button.is_clicked(mouse_pos, event):
                self.player.save_player_data()
                self.show_message("Game saved!", 2.0)
                
            if self.menu_button.is_clicked(mouse_pos, event):
                return "menu"
                
            if self.pause_button.is_clicked(mouse_pos, event):
                self.paused = True
                self.pause_menu_active = True
                
        return None
        
    def update(self, dt):
        """Update the game scene
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            list: List of events that occurred during update
            str or None: Next scene if game over
        """
        # Don't update if paused
        if self.paused:
            return [], None
            
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
        
        # Update customers
        lost_customers = self.customer_system.update()
        
        # Handle lost customers
        events = []
        for customer in lost_customers:
            self.show_message(f"{customer.name} left without being served!", 3.0)
            events.append(("customer_left", customer))
            
            # Increment lost customer counter
            lost_count = self.player.add_lost_customer()
            
            # Check for game over
            if lost_count >= MAX_CONSECUTIVE_LOST_CUSTOMERS:
                return events, "game_over"
            
        # Check for completed orders
        completed_orders = self.customer_system.check_completed_orders()
        for order, reward in completed_orders:
            self.player.add_coins(reward)
            self.player.add_experience(reward // 2)
            self.show_message(f"Order completed! +{reward} coins", 3.0)
            events.append(("order_completed", order, reward))
            
            # Reset lost customer counter on successful order
            self.player.reset_lost_customers()
            
        return events, None
        
    def show_message(self, message, duration=2.0):
        """Show a temporary message
        
        Args:
            message: Message text
            duration: Duration in seconds
        """
        self.message = message
        self.message_timer = duration
        
    def render(self, screen):
        """Render the game scene
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(LIGHT_GRAY)
        
        # Render customers at the top
        self._render_customers(screen)
        
        # Render player info
        self._render_player_info(screen)
        
        # Render buttons
        self.cooking_button.draw(screen)
        self.upgrade_button.draw(screen)
        self.recipe_book_button.draw(screen)
        self.profile_button.draw(screen)
        self.save_button.draw(screen)
        self.menu_button.draw(screen)
        self.pause_button.draw(screen)
        
        # Render message if active
        if self.message:
            self.text_renderer.render_text(
                screen,
                self.message,
                "medium",
                BLACK,
                SCREEN_WIDTH // 2,
                500,
                "center"
            )
            
        # Render pause menu if active
        if self.pause_menu_active:
            self._render_pause_menu(screen)
            
    def _render_pause_menu(self, screen):
        """Render the pause menu overlay
        
        Args:
            screen: Pygame surface to render on
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Pause menu title
        self.text_renderer.render_text(
            screen,
            "PAUSED",
            "title",
            (255, 255, 255),
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 150,
            "center"
        )
        
        # Pause menu buttons
        self.resume_button.draw(screen)
        self.pause_menu_button.draw(screen)
        self.pause_exit_button.draw(screen)
            
    def _render_customers(self, screen):
        """Render the customer area
        
        Args:
            screen: Pygame surface to render on
        """
        # Customer area background
        customer_area_height = 150
        pygame.draw.rect(screen, (200, 220, 240), (0, 0, SCREEN_WIDTH, customer_area_height))
        
        # Draw customer slots
        slot_width = SCREEN_WIDTH // self.customer_system.customers.maxlen
        
        for i in range(self.customer_system.customers.maxlen):
            slot_rect = pygame.Rect(i * slot_width, 0, slot_width, customer_area_height)
            pygame.draw.rect(screen, (180, 200, 220), slot_rect, 2)
            
            if i < len(self.customer_system.customers):
                customer = list(self.customer_system.customers)[i]
                
                # Draw customer icon (placeholder circle)
                pygame.draw.circle(screen, (100, 100, 100), 
                                  (i * slot_width + slot_width // 2, 40), 
                                  20)
                
                # Draw customer name
                self.text_renderer.render_text(
                    screen,
                    customer.name,
                    "small",
                    BLACK,
                    i * slot_width + slot_width // 2,
                    70,
                    "center"
                )
                
                # Draw order
                self.text_renderer.render_text(
                    screen,
                    f"Order: {customer.order}",
                    "small",
                    BLACK,
                    i * slot_width + 10,
                    100,
                    "left"
                )
                
                # Draw patience bar
                patience_pct = customer.get_patience_percentage()
                bar_width = slot_width - 20
                bar_height = 10
                bar_x = i * slot_width + 10
                bar_y = 120
                
                self.text_renderer.render_patience_bar(
                    screen,
                    bar_x,
                    bar_y,
                    bar_width,
                    bar_height,
                    patience_pct
                )
                
    def _render_player_info(self, screen):
        """Render player information
        
        Args:
            screen: Pygame surface to render on
        """
        # Draw profile picture (placeholder)
        profile_rect = pygame.Rect(20, 170, 60, 60)
        pygame.draw.rect(screen, (200, 200, 200), profile_rect)
        pygame.draw.rect(screen, BLACK, profile_rect, 2)
        pygame.draw.circle(screen, (150, 150, 150), profile_rect.center, 25)
        
        # Draw username
        self.text_renderer.render_text(
            screen,
            self.player.username,
            "medium",
            BLACK,
            100,
            180,
            "left"
        )
        
        # Draw coins
        self.text_renderer.render_text(
            screen,
            f"Coins: {self.player.coins}",
            "medium",
            BLACK,
            100,
            210,
            "left"
        )
        
        # Draw level
        self.text_renderer.render_text(
            screen,
            f"Level: {self.player.level}",
            "medium",
            BLACK,
            20,
            250,
            "left"
        )
        
        # Draw experience bar
        self.text_renderer.render_text(
            screen,
            f"XP: {self.player.experience}/{self.player.experience_to_next_level}",
            "small",
            BLACK,
            20,
            280,
            "left"
        )
        
        # Draw XP bar
        xp_pct = self.player.experience / self.player.experience_to_next_level
        bar_width = 200
        bar_height = 10
        bar_x = 20
        bar_y = 300
        
        # Background bar
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))
        
        # XP level
        pygame.draw.rect(screen, (100, 200, 100), (bar_x, bar_y, int(bar_width * xp_pct), bar_height))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
