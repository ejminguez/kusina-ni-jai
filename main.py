"""
Main entry point for Kusina ni Jai
"""
import pygame
import sys
import os

# Make sure we can import from the project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from player import Player
from logic.recipe_logic import RecipeSystem
from logic.customer import CustomerSystem
from logic.kitchen import Kitchen
from scenes.menu import MainMenu
from scenes.game_loop import GameScene
from scenes.recipe_creator import RecipeCreator
from scenes.upgrade_scene import UpgradeScene
from scenes.recipe_book import RecipeBook
from scenes.profile_editor import ProfileEditor
from scenes.game_over import GameOver

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components
        self.player = Player()
        self.recipe_system = RecipeSystem()
        self.kitchen = Kitchen()
        self.customer_system = CustomerSystem(self.recipe_system)
        
        # Initialize scenes
        self.scenes = {
            "menu": MainMenu(),
            "game": GameScene(self.player, self.customer_system),
            "cooking": RecipeCreator(self.recipe_system, self.kitchen),
            "upgrade": UpgradeScene(self.player, self.kitchen),
            "recipe_book": RecipeBook(self.recipe_system),
            "profile": ProfileEditor(self.player),
            "game_over": GameOver(self.player)
        }
        
        # Start with the menu scene
        self.current_scene = "menu"
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # Handle scene-specific events
            next_scene, data = self._handle_scene_events(events)
            if next_scene:
                self._change_scene(next_scene, data)
                
            # Update current scene
            result = self._update_scene(dt)
            if result:
                next_scene = result
                if next_scene:
                    self._change_scene(next_scene, {})
            
            # Render current scene
            self._render_scene()
            
            # Update display
            pygame.display.flip()
            
        # Clean up
        pygame.quit()
        sys.exit()
        
    def _handle_scene_events(self, events):
        """Handle events for the current scene
        
        Returns:
            tuple: (next_scene, data) or (None, {}) if no scene change
        """
        scene = self.scenes[self.current_scene]
        
        if hasattr(scene, "handle_events"):
            result = scene.handle_events(events)
            
            # Check if the scene wants to change
            if isinstance(result, tuple) and len(result) == 2:
                next_scene, data = result
                if next_scene:
                    return next_scene, data
            elif result:
                return result, {}
                
        return None, {}
        
    def _update_scene(self, dt):
        """Update the current scene
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            str or None: Next scene if scene wants to change
        """
        scene = self.scenes[self.current_scene]
        
        if hasattr(scene, "update"):
            result = scene.update(dt)
            
            # Special handling for game scene
            if self.current_scene == "game" and isinstance(result, tuple) and len(result) == 2:
                events, next_scene = result
                return next_scene
            
        return None
            
    def _render_scene(self):
        """Render the current scene"""
        scene = self.scenes[self.current_scene]
        
        if hasattr(scene, "render"):
            scene.render(self.screen)
            
    def _change_scene(self, scene_name, data=None):
        """Change to a different scene
        
        Args:
            scene_name: Name of the scene to change to
            data: Optional data to pass to the scene
        """
        if scene_name in self.scenes:
            self.current_scene = scene_name
            
            # Handle special scene transitions
            if scene_name == "game" and data and "cooked_dish" in data:
                # If returning from cooking with a dish
                dish_name = data["cooked_dish"]
                success, customer, reward = self.customer_system.try_serve_dish(dish_name)
                
                if success:
                    self.player.add_coins(reward)
                    self.player.add_experience(reward // 2)
                    self.scenes["game"].show_message(f"Served {dish_name}! +{reward} coins", 3.0)
                    # Reset lost customer counter on successful order
                    self.player.reset_lost_customers()
                    
        else:
            print(f"Scene '{scene_name}' does not exist")

if __name__ == "__main__":
    game = Game()
    game.run()
