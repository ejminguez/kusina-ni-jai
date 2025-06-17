"""
Upgrade shop scene
"""
import pygame
from ui.buttons import Button
from ui.text import TextRenderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, LIGHT_GRAY

class UpgradeScene:
    def __init__(self, player, kitchen):
        self.player = player
        self.kitchen = kitchen
        self.text_renderer = TextRenderer()
        
        # UI elements
        self.back_button = Button(50, SCREEN_HEIGHT - 70, 100, 40, "Back")
        self.upgrade_buttons = []
        
        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 20
        self.scroll_area_height = SCREEN_HEIGHT - 250  # Area available for scrolling
        
        # Result message
        self.result_message = ""
        self.result_timer = 0
        
        # Create upgrade buttons
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up UI elements"""
        self.upgrade_buttons = []
        self.scroll_offset = 0
        
        # Get locked ingredients and tools
        locked_ingredients = self.kitchen.get_locked_ingredients()
        locked_tools = self.kitchen.get_locked_tools()
        
        # Create ingredient upgrade buttons
        y_pos = 200
        for i, (ingredient, cost) in enumerate(locked_ingredients):
            button = Button(
                50,
                y_pos + i * 40,
                200,
                30,
                f"Unlock {ingredient} - {cost} coins"
            )
            self.upgrade_buttons.append({
                "button": button,
                "type": "ingredient",
                "name": ingredient,
                "cost": cost
            })
            
        # Create tool upgrade buttons
        y_pos = 200
        for i, (tool, cost) in enumerate(locked_tools):
            button = Button(
                350,
                y_pos + i * 40,
                200,
                30,
                f"Unlock {tool} - {cost} coins"
            )
            self.upgrade_buttons.append({
                "button": button,
                "type": "tool",
                "name": tool,
                "cost": cost
            })
            
        # Calculate max scroll based on content height
        if self.upgrade_buttons:
            last_button = max(self.upgrade_buttons, key=lambda b: b["button"].rect.bottom)
            content_height = last_button["button"].rect.bottom - 200
            self.max_scroll = max(0, content_height - self.scroll_area_height)
        else:
            self.max_scroll = 0
        
    def handle_events(self, events):
        """Handle events for the upgrade scene
        
        Args:
            events: List of pygame events
            
        Returns:
            str or None: Next scene name if transitioning, None otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        self.back_button.is_hovered(mouse_pos)
        
        # Adjust mouse position for scrolling when checking upgrade buttons
        scroll_adjusted_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
        
        for upgrade in self.upgrade_buttons:
            # Only check buttons that are in the visible area
            button_rect = upgrade["button"].rect
            if 200 <= button_rect.y - self.scroll_offset <= SCREEN_HEIGHT - 100:
                upgrade["button"].is_hovered(scroll_adjusted_pos)
        
        for event in events:
            # Check back button
            if self.back_button.is_clicked(mouse_pos, event):
                return "game"
                
            # Handle scrolling
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * self.scroll_speed
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                
            # Check upgrade buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                for upgrade in self.upgrade_buttons:
                    button_rect = upgrade["button"].rect
                    # Only check buttons that are in the visible area
                    if 200 <= button_rect.y - self.scroll_offset <= SCREEN_HEIGHT - 100:
                        # Adjust mouse position for scrolling
                        if button_rect.collidepoint(scroll_adjusted_pos):
                            self._purchase_upgrade(upgrade)
                            return None  # Stay in the same scene
                
        return None
        
    def _purchase_upgrade(self, upgrade):
        """Attempt to purchase an upgrade
        
        Args:
            upgrade: Upgrade data dictionary
        """
        if self.player.coins < upgrade["cost"]:
            self.show_result(f"Not enough coins! Need {upgrade['cost']} coins.", 2.0)
            return
            
        success = False
        if upgrade["type"] == "ingredient":
            success, cost = self.kitchen.unlock_ingredient(upgrade["name"])
        elif upgrade["type"] == "tool":
            success, cost = self.kitchen.unlock_tool(upgrade["name"])
            
        if success:
            self.player.spend_coins(cost)
            self.show_result(f"Unlocked {upgrade['name']}!", 2.0)
            # Refresh UI to remove purchased upgrade
            self._setup_ui()
        
    def update(self, dt):
        """Update the upgrade scene
        
        Args:
            dt: Time delta in seconds
        """
        # Update result message timer
        if self.result_timer > 0:
            self.result_timer -= dt
            if self.result_timer <= 0:
                self.result_message = ""
                
    def show_result(self, message, duration=2.0):
        """Show a result message
        
        Args:
            message: Message text
            duration: Duration in seconds
        """
        self.result_message = message
        self.result_timer = duration
        
    def render(self, screen):
        """Render the upgrade scene
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(LIGHT_GRAY)
        
        # Draw title
        self.text_renderer.render_text(
            screen,
            "Upgrade Shop",
            "large",
            BLACK,
            SCREEN_WIDTH // 2,
            50,
            "center"
        )
        
        # Draw player coins
        self.text_renderer.render_text(
            screen,
            f"Coins: {self.player.coins}",
            "medium",
            BLACK,
            20,
            120,
            "left"
        )
        
        # Draw available upgrades header
        self.text_renderer.render_text(
            screen,
            "Available Upgrades:",
            "medium",
            BLACK,
            50,
            170,
            "left"
        )
        
        # Create a clipping rect for the scrollable area
        scroll_area = pygame.Rect(0, 200, SCREEN_WIDTH, self.scroll_area_height)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            scrollbar_height = self.scroll_area_height * (self.scroll_area_height / (self.scroll_area_height + self.max_scroll))
            scrollbar_pos = 200 + (self.scroll_offset / self.max_scroll) * (self.scroll_area_height - scrollbar_height)
            pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH - 20, scrollbar_pos, 10, scrollbar_height))
            pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 20, scrollbar_pos, 10, scrollbar_height), 1)
        
        # Draw upgrade buttons (with scrolling)
        for upgrade in self.upgrade_buttons:
            button = upgrade["button"]
            # Adjust button position for scrolling
            button_rect = button.rect.copy()
            button_rect.y -= self.scroll_offset
            
            # Only draw buttons that are in the visible area
            if scroll_area.colliderect(button_rect):
                # Store original rect
                original_rect = button.rect
                
                # Temporarily set the rect to the scrolled position
                button.rect = button_rect
                button.draw(screen)
                
                # Restore original rect
                button.rect = original_rect
            
        # Draw back button (always at the bottom, outside scroll area)
        self.back_button.draw(screen)
        
        # Draw result message if active
        if self.result_message:
            self.text_renderer.render_text(
                screen,
                self.result_message,
                "medium",
                BLACK,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 120,
                "center"
            )
