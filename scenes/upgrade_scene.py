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
        self.back_button = Button(50, 500, 100, 40, "Back")
        self.upgrade_buttons = []
        
        # Create upgrade buttons
        self._setup_ui()
        
        # Result message
        self.result_message = ""
        self.result_timer = 0
        
    def _setup_ui(self):
        """Set up UI elements"""
        self.upgrade_buttons = []
        
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
        
        for upgrade in self.upgrade_buttons:
            upgrade["button"].is_hovered(mouse_pos)
        
        for event in events:
            # Check back button
            if self.back_button.is_clicked(mouse_pos, event):
                return "game"
                
            # Check upgrade buttons
            for upgrade in self.upgrade_buttons:
                if upgrade["button"].is_clicked(mouse_pos, event):
                    self._purchase_upgrade(upgrade)
                    
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
        
        # Draw upgrade buttons
        for upgrade in self.upgrade_buttons:
            upgrade["button"].draw(screen)
            
        # Draw back button
        self.back_button.draw(screen)
        
        # Draw result message if active
        if self.result_message:
            self.text_renderer.render_text(
                screen,
                self.result_message,
                "medium",
                BLACK,
                SCREEN_WIDTH // 2,
                400,
                "center"
            )
