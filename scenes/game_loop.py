"""
Main game loop scene
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from ui.animation_manager import AnimationManager, EasingAnimation
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, GREEN, BLUE, LIGHT_GRAY,
    MAX_CONSECUTIVE_LOST_CUSTOMERS, PASTEL_COLORS
)

class GameScene:
    def __init__(self, player, customer_system, sprite_manager=None, game_instance=None):
        self.player = player
        self.customer_system = customer_system
        self.sprite_manager = sprite_manager
        self.game_instance = game_instance  # Reference to the main game for day/time
        self.text_renderer = TextRenderer()
        
        # Animation manager
        self.animation_manager = AnimationManager()
        self._setup_animations()
        
        # UI elements - moved to bottom of screen
        button_y = SCREEN_HEIGHT - 70
        self.cooking_button = Button(50, button_y, 150, 50, "Cook", GREEN)
        self.upgrade_button = Button(220, button_y, 150, 50, "Upgrades", BLUE)
        self.recipe_book_button = Button(390, button_y, 150, 50, "Recipe Book")
        self.profile_button = Button(560, button_y, 150, 50, "Profile")
        self.save_button = Button(730, button_y, 150, 50, "Save Game")
        
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
        
        # Customer animations
        self.customer_animations = {}
        
        # Show quote animation
        self.show_quote = True
        self.quote_timer = 5.0  # Show quote for 5 seconds
        
    def _setup_animations(self):
        """Set up animations"""
        # Button hover animations
        self.animation_manager.create_easing_animation(
            "button_hover", 
            0.3, 
            EasingAnimation.EASING_EASE_OUT, 
            False
        )
        
        # Message fade animation
        self.animation_manager.create_easing_animation(
            "message_fade", 
            0.5, 
            EasingAnimation.EASING_EASE_IN_OUT, 
            False
        )
        
        # Pause menu animation
        self.animation_manager.create_easing_animation(
            "pause_menu", 
            0.3, 
            EasingAnimation.EASING_EASE_OUT, 
            False
        )
        
        # Quote animation
        self.animation_manager.create_easing_animation(
            "quote_fade", 
            1.0, 
            EasingAnimation.EASING_EASE_IN_OUT, 
            True  # Make it loop for continuous fading
        )
        
    def handle_events(self, events):
        """Handle events for the game scene
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        # Skip event handling during quote display
        if self.show_quote:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.show_quote = False
                    self.quote_timer = 0
            return None
            
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
                # Save game state
                if self.game_instance:
                    self.game_instance.save_game_state()
                self.show_message("Game saved!", 2.0)
                
            if self.menu_button.is_clicked(mouse_pos, event):
                return "menu"
                
            if self.pause_button.is_clicked(mouse_pos, event):
                self.paused = True
                self.pause_menu_active = True
                # Reset and start pause menu animation
                pause_anim = self.animation_manager.get_animation("pause_menu")
                if pause_anim:
                    pause_anim.reset()
                
        return None
        
    def update(self, dt):
        """Update the game scene
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            list: List of events that occurred during update
            str or None: Next scene if game over
        """
        # Update animations
        self.animation_manager.update(dt)
        
        # Update quote timer
        if self.show_quote:
            self.quote_timer -= dt
            if self.quote_timer <= 0:
                self.show_quote = False
            return [], None
        
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
            
            # Advance time when serving a customer (15 minutes)
            if self.game_instance:
                day_ended = self.game_instance.advance_time(0.25)
                if day_ended:
                    self.show_quote = True
                    self.quote_timer = 5.0
            
        return events, None
        
    def show_message(self, message, duration=2.0):
        """Show a temporary message
        
        Args:
            message: Message text
            duration: Duration in seconds
        """
        self.message = message
        self.message_timer = duration
        
        # Reset and start message fade animation
        message_anim = self.animation_manager.get_animation("message_fade")
        if message_anim:
            message_anim.reset()
        
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
        
        # Render day and time info
        if self.game_instance:
            self._render_day_time(screen)
        
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
            # Get message fade animation progress
            message_anim = self.animation_manager.get_animation("message_fade")
            opacity = 1.0
            if message_anim:
                # Fade in for the first half of the message duration
                if self.message_timer > 0:
                    time_ratio = min(1.0, (2.0 - self.message_timer) / 2.0)
                    opacity = message_anim.get_progress() if time_ratio < 0.5 else 1.0
                else:
                    opacity = 0.0
            
            # Apply opacity to text color
            text_color = (0, 0, 0, int(255 * opacity))
            
            self.text_renderer.render_text(
                screen,
                self.message,
                "medium",
                text_color,
                SCREEN_WIDTH // 2,
                500,
                "center"
            )
            
        # Render pause menu if active
        if self.pause_menu_active:
            self._render_pause_menu(screen)
            
        # Render daily quote if active
        if self.show_quote and self.game_instance and hasattr(self.game_instance, 'current_quote'):
            self._render_daily_quote(screen)
            
    def _render_day_time(self, screen):
        """Render the day and time information
        
        Args:
            screen: Pygame surface to render on
        """
        # Draw day number
        self.text_renderer.render_text(
            screen,
            f"Day {self.game_instance.day}",
            "medium",
            BLACK,
            SCREEN_WIDTH - 150,
            70,
            "center"
        )
        
        # Draw current time
        self.text_renderer.render_text(
            screen,
            self.game_instance.get_formatted_time(),
            "medium",
            BLACK,
            SCREEN_WIDTH - 150,
            100,
            "center"
        )
        
        # Draw time progress bar
        progress = self.game_instance.get_day_progress()
        bar_width = 200
        bar_height = 10
        bar_x = SCREEN_WIDTH - 250
        bar_y = 130
        
        # Background bar
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress bar
        pygame.draw.rect(screen, PASTEL_COLORS[2], (bar_x, bar_y, int(bar_width * progress), bar_height))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Draw start and end times
        self.text_renderer.render_text(
            screen,
            "8:00 AM",
            "small",
            BLACK,
            bar_x,
            bar_y + 20,
            "left"
        )
        
        self.text_renderer.render_text(
            screen,
            "4:00 PM",
            "small",
            BLACK,
            bar_x + bar_width,
            bar_y + 20,
            "right"
        )
            
    def _render_daily_quote(self, screen):
        """Render the daily quote overlay
        
        Args:
            screen: Pygame surface to render on
        """
        # Safety check
        if not self.game_instance or not hasattr(self.game_instance, 'current_quote'):
            return
            
        # Get quote animation progress
        quote_anim = self.animation_manager.get_animation("quote_fade")
        progress = quote_anim.get_progress() if quote_anim else 1.0
        
        # Calculate opacity based on time remaining
        fade_time = 1.0  # Fade in/out time in seconds
        if self.quote_timer < fade_time:
            opacity = self.quote_timer / fade_time
        elif self.quote_timer > 4.0:  # 5.0 - fade_time
            opacity = (5.0 - self.quote_timer) / fade_time
        else:
            opacity = 1.0
            
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(180 * opacity)))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Draw day number
        self.text_renderer.render_text(
            screen,
            f"Day {self.game_instance.day}",
            "large",
            (255, 255, 255, int(255 * opacity)),
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            "center"
        )
        
        # Draw quote
        quote = self.game_instance.current_quote
        
        # Split quote into multiple lines if needed
        words = quote.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 50:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
                
        if current_line:
            lines.append(current_line)
            
        # Draw each line
        for i, line in enumerate(lines):
            self.text_renderer.render_text(
                screen,
                line,
                "medium",
                (255, 255, 255, int(255 * opacity)),
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 30 + i * 30,
                "center"
            )
            
        # Draw tap to continue message
        self.text_renderer.render_text(
            screen,
            "Tap to continue",
            "small",
            (255, 255, 255, int(255 * opacity)),
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            "center"
        )
            
    def _render_pause_menu(self, screen):
        """Render the pause menu overlay
        
        Args:
            screen: Pygame surface to render on
        """
        # Get pause menu animation progress
        pause_anim = self.animation_manager.get_animation("pause_menu")
        progress = pause_anim.get_progress() if pause_anim else 1.0
        
        # Semi-transparent overlay with animation
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(180 * progress)))  # Black with animated alpha
        screen.blit(overlay, (0, 0))
        
        # Pause menu title with scale animation
        scale = 0.5 + 0.5 * progress  # Scale from 0.5 to 1.0
        title_font = pygame.font.SysFont(None, int(64 * scale))
        title_text = title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)
        
        # Pause menu buttons with fade-in
        if progress > 0.5:  # Only show buttons after overlay is mostly visible
            button_alpha = min(255, int(255 * (progress - 0.5) * 2))
            
            # Store original colors
            resume_color = self.resume_button.color
            menu_color = self.pause_menu_button.color
            exit_color = self.pause_exit_button.color
            
            # Apply alpha to button colors
            self.resume_button.color = self._apply_alpha_to_color(resume_color, button_alpha)
            self.pause_menu_button.color = self._apply_alpha_to_color(menu_color, button_alpha)
            self.pause_exit_button.color = self._apply_alpha_to_color(exit_color, button_alpha)
            
            # Draw buttons
            self.resume_button.draw(screen)
            self.pause_menu_button.draw(screen)
            self.pause_exit_button.draw(screen)
            
            # Restore original colors
            self.resume_button.color = resume_color
            self.pause_menu_button.color = menu_color
            self.pause_exit_button.color = exit_color
            
    def _apply_alpha_to_color(self, color, alpha):
        """Apply alpha to a color
        
        Args:
            color: RGB color tuple
            alpha: Alpha value (0-255)
            
        Returns:
            tuple: RGBA color tuple
        """
        return (color[0], color[1], color[2], alpha)
            
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
                
                # Create animation for this customer if it doesn't exist
                customer_id = id(customer)
                if customer_id not in self.customer_animations:
                    self.animation_manager.create_easing_animation(
                        f"customer_{customer_id}",
                        0.5,
                        EasingAnimation.EASING_BOUNCE,
                        False
                    )
                    self.customer_animations[customer_id] = True
                
                # Get animation progress
                anim = self.animation_manager.get_animation(f"customer_{customer_id}")
                progress = anim.get_progress() if anim else 1.0
                
                # Draw customer icon with animation
                icon_size = 20 + int(10 * progress)  # Size grows from 20 to 30
                pygame.draw.circle(
                    screen, 
                    (100, 100, 100), 
                    (i * slot_width + slot_width // 2, 40), 
                    icon_size
                )
                
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
        # Draw profile picture
        profile_rect = pygame.Rect(20, 170, 60, 60)
        
        # Draw profile background with player's color
        player_color = self.player.color if hasattr(self.player, "color") else (0, 255, 0)
        pygame.draw.rect(screen, player_color, (profile_rect.x - 3, profile_rect.y - 3, profile_rect.width + 6, profile_rect.height + 6))
        
        # Draw profile picture
        if self.sprite_manager:
            # Extract sprite name from path
            sprite_name = self.player.profile_pic.split("/")[-1].split(".")[0]
            sprite = self.sprite_manager.get_sprite(sprite_name)
            # Scale sprite to fit the profile rect
            sprite = pygame.transform.scale(sprite, (profile_rect.width, profile_rect.height))
            screen.blit(sprite, profile_rect)
        else:
            # Draw placeholder if sprite manager is not available
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
        
        # XP level with player's color
        pygame.draw.rect(screen, player_color, (bar_x, bar_y, int(bar_width * xp_pct), bar_height))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
