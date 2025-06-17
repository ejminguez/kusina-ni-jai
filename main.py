"""
Main entry point for Kusina ni Jai
"""
import pygame
import sys
import os
import json

# Make sure we can import from the project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, PASTEL_COLORS
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
from scenes.about_scene import AboutScene
from ui.sprite_manager import SpriteManager

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Get the user's screen resolution
        info = pygame.display.Info()
        self.user_screen_width = info.current_w
        self.user_screen_height = info.current_h
        
        # Set up the display
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        self._load_sprites()
        
        # Initialize game components
        self._initialize_game_components()
        
        # Game day system
        self.day = 1
        self.day_time = 8.0  # Start at 8:00 AM
        self.day_start = 8.0  # 8:00 AM
        self.day_end = 16.0   # 4:00 PM
        self.day_length = self.day_end - self.day_start  # 8 hours
        self.current_quote = self._get_daily_quote()
        
        # Start with the menu scene
        self.current_scene = "menu"
        
    def save_game_state(self):
        """Save the current game state"""
        try:
            # Save day and time information
            game_state = {
                "day": self.day,
                "day_time": self.day_time,
                "current_quote": self.current_quote
            }
            
            # Save to file
            with open("data/game_state.json", "w") as file:
                json.dump(game_state, file, indent=2)
                
            # Also save customer system state
            if hasattr(self, 'customer_system'):
                self.customer_system.day_count = self.day
                
        except Exception as e:
            print(f"Error saving game state: {e}")
            
    def load_game_state(self):
        """Load the game state if it exists"""
        try:
            if os.path.exists("data/game_state.json"):
                with open("data/game_state.json", "r") as file:
                    game_state = json.load(file)
                    self.day = game_state.get("day", 1)
                    self.day_time = game_state.get("day_time", 8.0)
                    self.current_quote = game_state.get("current_quote", self._get_daily_quote())
                    
                    # Update customer system
                    if hasattr(self, 'customer_system'):
                        self.customer_system.day_count = self.day
                        self.customer_system.difficulty_multiplier = 1.0 + (self.day - 1) * 0.1
        except Exception as e:
            print(f"Error loading game state: {e}")
            
    def _initialize_game_components(self):
        """Initialize or reinitialize game components"""
        self.player = Player()
        self.recipe_system = RecipeSystem()
        self.kitchen = Kitchen()
        self.customer_system = CustomerSystem(self.recipe_system)
        
        # Reset day system
        self.day = 1
        self.day_time = 8.0
        self.current_quote = self._get_daily_quote()
        
        # Initialize scenes
        self.scenes = {
            "menu": MainMenu(),
            "game": GameScene(self.player, self.customer_system, self.sprite_manager, self),
            "cooking": RecipeCreator(self.recipe_system, self.kitchen),
            "upgrade": UpgradeScene(self.player, self.kitchen),
            "recipe_book": RecipeBook(self.recipe_system),
            "profile": ProfileEditor(self.player, self.sprite_manager),
            "game_over": GameOver(self.player),
            "about": AboutScene()
        }
        
        # Load game state if not a new game
        self.load_game_state()
        
    def _load_sprites(self):
        """Load all game sprites"""
        # Load profile pictures
        self.sprite_manager.load_sprite("default_profile", "assets/sprites/default_profile.png")
        self.sprite_manager.load_sprite("chef1", "assets/sprites/chef1.png")
        self.sprite_manager.load_sprite("chef2", "assets/sprites/chef2.png")
        self.sprite_manager.load_sprite("chef3", "assets/sprites/chef3.png")
        
        # You can add more sprite loading here
        
    def _get_daily_quote(self):
        """Get a quote for the current day
        
        Returns:
            str: A motivational cooking quote
        """
        # Define quotes if they don't exist yet
        if not hasattr(self, 'day_quotes'):
            self.day_quotes = [
                "A recipe has no soul. You, as the cook, must bring soul to the recipe.",
                "Cooking is like love. It should be entered into with abandon or not at all.",
                "The only real stumbling block is fear of failure. In cooking you've got to have a what-the-hell attitude.",
                "Cooking is at once child's play and adult joy. And cooking done with care is an act of love.",
                "No one who cooks, cooks alone. Even at her most solitary, a cook in the kitchen is surrounded by generations of cooks past.",
                "Cooking is like painting or writing a song. Just as there are only so many notes or colors, there are only so many flavors - it's how you combine them that sets you apart.",
                "Cooking demands attention, patience, and above all, a respect for the gifts of the earth.",
                "The most indispensable ingredient of all good home cooking: love for those you are cooking for.",
                "Cooking is about passion, so it may look slightly temperamental in a way that it's too assertive to the naked eye.",
                "Cooking is like snow skiing: If you don't fall at least 10 times, then you're not skiing hard enough.",
                "Cooking requires confident guesswork and improvisation—experimentation and substitution, dealing with failure and uncertainty in a creative way.",
                "Cooking is like making love, you do it well, or you don't do it at all.",
                "Cooking is an observation-based process that you can't do if you're so completely focused on a recipe.",
                "Cooking is an art, but all art requires knowing something about the techniques and materials.",
                "Cooking is not difficult. Everyone has taste, even if they don't realize it. Even if you're not a great chef, there's nothing to stop you understanding the difference between what tastes good and what doesn't."
            ]
            
        # Use the day number to select a quote (cycling through the list)
        return self.day_quotes[(self.day - 1) % len(self.day_quotes)]
        
    def advance_time(self, hours):
        """Advance the game time
        
        Args:
            hours: Number of hours to advance
            
        Returns:
            bool: True if the day ended
        """
        self.day_time += hours
        
        # Check if day ended
        if self.day_time >= self.day_end:
            self.day += 1
            self.day_time = self.day_start
            self.current_quote = self._get_daily_quote()
            return True
            
        return False
        
    def get_day_progress(self):
        """Get the progress through the current day
        
        Returns:
            float: Progress from 0.0 to 1.0
        """
        return (self.day_time - self.day_start) / self.day_length
        
    def get_formatted_time(self):
        """Get the current time formatted as HH:MM
        
        Returns:
            str: Formatted time string
        """
        hours = int(self.day_time)
        minutes = int((self.day_time - hours) * 60)
        am_pm = "AM" if hours < 12 else "PM"
        
        # Convert to 12-hour format
        if hours > 12:
            hours -= 12
        elif hours == 0:
            hours = 12
            
        return f"{hours}:{minutes:02d} {am_pm}"
        
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
                    
                # Handle window resize
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.sprite_manager.update_screen_size(event.w, event.h)
                        
                # Handle fullscreen toggle
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            # Use the user's actual screen resolution
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            info = pygame.display.Info()
                            actual_width = info.current_w
                            actual_height = info.current_h
                            self.sprite_manager.update_screen_size(actual_width, actual_height)
                        else:
                            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                            self.sprite_manager.update_screen_size(SCREEN_WIDTH, SCREEN_HEIGHT)
                    
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
            # Check for new game request
            if scene_name == "game" and data and data.get("new_game", False):
                # Reset kitchen to default state
                if hasattr(self, 'kitchen'):
                    self.kitchen.reset()
                # Reset recipe system
                if hasattr(self, 'recipe_system'):
                    self.recipe_system.reset()
                # Reset customer system
                if hasattr(self, 'customer_system'):
                    self.customer_system.reset()
                # Reinitialize game components for a new game
                self._initialize_game_components()
            
            # Special handling for certain scenes
            if scene_name == "cooking":
                # Advance time when cooking (30 minutes)
                self.advance_time(0.5)
                # Refresh the cooking interface with the latest ingredients
                self.scenes["cooking"] = RecipeCreator(self.recipe_system, self.kitchen)
                
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
