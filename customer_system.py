import pygame
import random
from collections import deque

class Customer:
    def __init__(self, name, patience, order, reward):
        self.name = name
        self.max_patience = patience
        self.patience = patience  # Patience in seconds
        self.order = order  # Name of the dish they want
        self.reward = reward  # Coins rewarded for completing the order
        self.served = False
        self.timer_start = pygame.time.get_ticks()
        
    def update(self):
        if not self.served:
            elapsed = (pygame.time.get_ticks() - self.timer_start) / 1000  # Convert to seconds
            self.patience = max(0, self.max_patience - elapsed)
            return self.patience <= 0  # Return True if customer ran out of patience
        return False
        
    def serve(self, dish_name):
        """Try to serve a dish to this customer"""
        if dish_name.lower() == self.order.lower():
            self.served = True
            return True
        return False

class CustomerSystem:
    def __init__(self, recipe_system):
        self.recipe_system = recipe_system
        self.customers = deque(maxlen=4)  # Queue of current customers
        self.max_customers = 4
        self.customer_spawn_timer = 0
        self.customer_spawn_interval = 20000  # 20 seconds between customers
        self.last_spawn_time = pygame.time.get_ticks()
        self.customer_names = ["Alex", "Jamie", "Casey", "Jordan", "Taylor", "Morgan", 
                              "Riley", "Quinn", "Avery", "Skyler"]
        
    def update(self):
        # Check if we should spawn a new customer
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.customer_spawn_interval and len(self.customers) < self.max_customers:
            self.spawn_customer()
            self.last_spawn_time = current_time
            
        # Update existing customers
        customers_to_remove = []
        for i, customer in enumerate(self.customers):
            if customer.update():  # Customer ran out of patience
                customers_to_remove.append(i)
                
        # Remove impatient customers (from back to front to avoid index issues)
        for i in sorted(customers_to_remove, reverse=True):
            self.customers.remove(self.customers[i])
            
    def spawn_customer(self):
        # Choose a random name
        name = random.choice(self.customer_names)
        
        # Set patience based on difficulty (30-60 seconds)
        patience = random.randint(30, 60)
        
        # Choose an order
        if random.random() < 0.7:  # 70% chance for known recipe
            discovered_recipes = self.recipe_system.get_discovered_recipes()
            if discovered_recipes:
                recipe = random.choice(discovered_recipes)
                order = recipe.name
            else:
                # Fallback to a basic recipe if none discovered yet
                all_recipes = self.recipe_system.get_all_recipes()
                recipe = random.choice(all_recipes)
                order = recipe.name
        else:
            # Generate a custom order that doesn't match any existing recipe
            order = self._generate_custom_order()
            
        # Set reward based on recipe difficulty or randomness for custom orders
        if order in self.recipe_system.recipes:
            recipe = self.recipe_system.get_recipe(order)
            reward = recipe.difficulty * 20 + random.randint(5, 15)
        else:
            # Custom orders pay more
            reward = random.randint(40, 80)
            
        # Create and add the customer
        customer = Customer(name, patience, order, reward)
        self.customers.append(customer)
        
    def _generate_custom_order(self):
        """Generate a custom order that doesn't match existing recipes"""
        adjectives = ["Spicy", "Sweet", "Tangy", "Creamy", "Savory", "Zesty", "Hearty"]
        foods = ["Stir Fry", "Noodles", "Curry", "Soup", "Stew", "Salad", "Special"]
        
        return f"{random.choice(adjectives)} {random.choice(foods)}"
        
    def try_serve_dish(self, dish_name):
        """Try to serve a dish to the first matching customer"""
        for customer in self.customers:
            if not customer.served and customer.serve(dish_name):
                return True
        return False
        
    def check_completed_orders(self):
        """Check for and remove served customers, returning their rewards"""
        completed = []
        customers_to_remove = []
        
        for customer in self.customers:
            if customer.served:
                completed.append((customer.order, customer.reward))
                customers_to_remove.append(customer)
                
        for customer in customers_to_remove:
            self.customers.remove(customer)
            
        return completed
        
    def render(self, screen):
        # Render customers and their orders
        customer_area_height = 150
        customer_area = pygame.Rect(0, 0, screen.get_width(), customer_area_height)
        pygame.draw.rect(screen, (200, 220, 240), customer_area)
        
        font = pygame.font.SysFont(None, 24)
        
        # Draw customer slots
        slot_width = screen.get_width() // self.max_customers
        
        for i in range(self.max_customers):
            slot_rect = pygame.Rect(i * slot_width, 0, slot_width, customer_area_height)
            pygame.draw.rect(screen, (180, 200, 220), slot_rect, 2)
            
            if i < len(self.customers):
                customer = self.customers[i]
                
                # Draw customer icon (placeholder circle)
                pygame.draw.circle(screen, (100, 100, 100), 
                                  (i * slot_width + slot_width // 2, 40), 
                                  20)
                
                # Draw customer name
                name_text = font.render(customer.name, True, (0, 0, 0))
                screen.blit(name_text, (i * slot_width + slot_width // 2 - name_text.get_width() // 2, 70))
                
                # Draw order
                order_text = font.render(f"Order: {customer.order}", True, (0, 0, 0))
                screen.blit(order_text, (i * slot_width + 10, 100))
                
                # Draw patience bar
                patience_pct = customer.patience / customer.max_patience
                bar_width = slot_width - 20
                bar_height = 10
                bar_x = i * slot_width + 10
                bar_y = 120
                
                # Background bar
                pygame.draw.rect(screen, (200, 200, 200), 
                                (bar_x, bar_y, bar_width, bar_height))
                
                # Patience level
                if patience_pct > 0.6:
                    color = (0, 255, 0)  # Green
                elif patience_pct > 0.3:
                    color = (255, 255, 0)  # Yellow
                else:
                    color = (255, 0, 0)  # Red
                    
                pygame.draw.rect(screen, color, 
                                (bar_x, bar_y, int(bar_width * patience_pct), bar_height))
