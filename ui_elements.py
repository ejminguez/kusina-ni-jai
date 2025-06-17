import pygame

class UI:
    def __init__(self, player, customer_system):
        self.player = player
        self.customer_system = customer_system
        
        # UI elements for main game
        self.cooking_button_rect = pygame.Rect(50, 600, 150, 50)
        self.upgrade_button_rect = pygame.Rect(250, 600, 150, 50)
        
    def render_main_menu(self, screen):
        # Draw title
        font_large = pygame.font.SysFont(None, 64)
        font = pygame.font.SysFont(None, 32)
        
        title = font_large.render("Kusina ni Jai", True, (0, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 200))
        
        subtitle = font.render("A Cooking Simulation Game", True, (0, 0, 0))
        screen.blit(subtitle, (screen.get_width() // 2 - subtitle.get_width() // 2, 280))
        
        # Draw start button
        start_button = pygame.Rect(screen.get_width() // 2 - 100, 350, 200, 50)
        pygame.draw.rect(screen, (150, 200, 150), start_button)
        pygame.draw.rect(screen, (0, 0, 0), start_button, 2)
        
        start_text = font.render("Start Game", True, (0, 0, 0))
        screen.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2,
                                start_button.y + start_button.height // 2 - start_text.get_height() // 2))
        
        # Draw instructions
        instructions = font.render("Press ENTER to start", True, (0, 0, 0))
        screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, 450))
        
    def render_game(self, screen):
        # Draw player info
        font = pygame.font.SysFont(None, 24)
        
        # Draw coins
        coins_text = font.render(f"Coins: {self.player.coins}", True, (0, 0, 0))
        screen.blit(coins_text, (20, 170))
        
        # Draw level
        level_text = font.render(f"Level: {self.player.level}", True, (0, 0, 0))
        screen.blit(level_text, (20, 200))
        
        # Draw experience bar
        exp_text = font.render(f"XP: {self.player.experience}/{self.player.experience_to_next_level}", True, (0, 0, 0))
        screen.blit(exp_text, (20, 230))
        
        # Draw cooking button
        pygame.draw.rect(screen, (150, 200, 150), self.cooking_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.cooking_button_rect, 2)
        
        cooking_text = font.render("Cook", True, (0, 0, 0))
        screen.blit(cooking_text, (self.cooking_button_rect.x + self.cooking_button_rect.width // 2 - cooking_text.get_width() // 2,
                                  self.cooking_button_rect.y + self.cooking_button_rect.height // 2 - cooking_text.get_height() // 2))
        
        # Draw upgrade button
        pygame.draw.rect(screen, (150, 150, 200), self.upgrade_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.upgrade_button_rect, 2)
        
        upgrade_text = font.render("Upgrades", True, (0, 0, 0))
        screen.blit(upgrade_text, (self.upgrade_button_rect.x + self.upgrade_button_rect.width // 2 - upgrade_text.get_width() // 2,
                                  self.upgrade_button_rect.y + self.upgrade_button_rect.height // 2 - upgrade_text.get_height() // 2))
        
    def render_upgrade_menu(self, screen):
        # Clear screen
        screen.fill((240, 240, 240))
        
        # Draw title
        font_large = pygame.font.SysFont(None, 48)
        font = pygame.font.SysFont(None, 24)
        
        title = font_large.render("Upgrade Shop", True, (0, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))
        
        # Draw player coins
        coins_text = font.render(f"Coins: {self.player.coins}", True, (0, 0, 0))
        screen.blit(coins_text, (20, 120))
        
        # Draw available upgrades
        upgrades_title = font.render("Available Upgrades:", True, (0, 0, 0))
        screen.blit(upgrades_title, (50, 170))
        
        # Ingredient upgrades
        ingredients_to_unlock = ["chicken", "beef", "carrot", "bell pepper", "potato"]
        ingredients_y = 200
        
        for i, ingredient in enumerate(ingredients_to_unlock):
            if ingredient not in self.player.unlocked_ingredients:
                upgrade_rect = pygame.Rect(50, ingredients_y + i * 40, 200, 30)
                pygame.draw.rect(screen, (200, 200, 200), upgrade_rect)
                pygame.draw.rect(screen, (0, 0, 0), upgrade_rect, 1)
                
                ingredient_text = font.render(f"Unlock {ingredient} - 50 coins", True, (0, 0, 0))
                screen.blit(ingredient_text, (60, ingredients_y + i * 40 + 5))
        
        # Tool upgrades
        tools_to_unlock = ["oven", "grill", "blender"]
        tools_y = 200
        
        for i, tool in enumerate(tools_to_unlock):
            if tool not in self.player.unlocked_tools:
                upgrade_rect = pygame.Rect(350, tools_y + i * 40, 200, 30)
                pygame.draw.rect(screen, (200, 200, 200), upgrade_rect)
                pygame.draw.rect(screen, (0, 0, 0), upgrade_rect, 1)
                
                tool_text = font.render(f"Unlock {tool} - 100 coins", True, (0, 0, 0))
                screen.blit(tool_text, (360, tools_y + i * 40 + 5))
        
        # Back button
        back_button = pygame.Rect(50, 500, 100, 40)
        pygame.draw.rect(screen, (200, 200, 200), back_button)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 2)
        
        back_text = font.render("Back", True, (0, 0, 0))
        screen.blit(back_text, (back_button.x + back_button.width // 2 - back_text.get_width() // 2,
                               back_button.y + back_button.height // 2 - back_text.get_height() // 2))
