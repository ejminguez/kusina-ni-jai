"""
Customer system for managing customer orders and patience
"""
import pygame
import random
from collections import deque
import json
import os
from config import (
    MAX_CUSTOMERS, CUSTOMER_SPAWN_INTERVAL, 
    MIN_PATIENCE, MAX_PATIENCE, KNOWN_RECIPE_CHANCE,
    FILIPINO_NAMES
)

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
        """Update customer patience
        
        Returns:
            bool: True if customer ran out of patience
        """
        if not self.served:
            elapsed = (pygame.time.get_ticks() - self.timer_start) / 1000  # Convert to seconds
            self.patience = max(0, self.max_patience - elapsed)
            return self.patience <= 0  # Return True if customer ran out of patience
        return False
        
    def serve(self, dish_name):
        """Try to serve a dish to this customer
        
        Args:
            dish_name: Name of the dish being served
            
        Returns:
            bool: True if the dish matches the order
        """
        # Case-insensitive comparison
        if dish_name.lower() == self.order.lower():
            self.served = True
            return True
        return False
        
    def get_patience_percentage(self):
        """Get the percentage of patience remaining
        
        Returns:
            float: Patience percentage (0.0 to 1.0)
        """
        return self.patience / self.max_patience


class CustomerSystem:
    def __init__(self, recipe_system):
        self.recipe_system = recipe_system
        self.customers = deque(maxlen=MAX_CUSTOMERS)  # Queue of current customers
        self.customer_spawn_timer = 0
        self.customer_spawn_interval = CUSTOMER_SPAWN_INTERVAL  # milliseconds between customers
        self.last_spawn_time = pygame.time.get_ticks()
        self.customer_names = FILIPINO_NAMES if FILIPINO_NAMES else ["Alex", "Jamie", "Casey", "Jordan", "Taylor"]
        
    def update(self):
        """Update all customers and spawn new ones if needed
        
        Returns:
            list: List of customers who ran out of patience
        """
        # Check if we should spawn a new customer
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.customer_spawn_interval and len(self.customers) < MAX_CUSTOMERS:
            self.spawn_customer()
            self.last_spawn_time = current_time
            
        # Update existing customers
        customers_to_remove = []
        for i, customer in enumerate(self.customers):
            if customer.update():  # Customer ran out of patience
                customers_to_remove.append(i)
                
        # Remove impatient customers (from back to front to avoid index issues)
        removed_customers = []
        for i in sorted(customers_to_remove, reverse=True):
            removed_customers.append(self.customers[i])
            self.customers.remove(self.customers[i])
            
        return removed_customers
            
    def spawn_customer(self):
        """Spawn a new customer with a random order"""
        # Choose a random name
        name = random.choice(self.customer_names)
        
        # Set patience based on difficulty
        patience = random.randint(MIN_PATIENCE, MAX_PATIENCE)
        
        # Choose an order
        if random.random() < KNOWN_RECIPE_CHANCE:  # Chance for known recipe
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
        recipe_found = False
        for recipe in self.recipe_system.recipes.values():
            if recipe.name.lower() == order.lower():
                reward = recipe.difficulty * 20 + random.randint(5, 15)
                recipe_found = True
                break
                
        if not recipe_found:
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
        """Try to serve a dish to the first matching customer
        
        Args:
            dish_name: Name of the dish to serve
            
        Returns:
            tuple: (success, customer, reward) or (False, None, 0) if no match
        """
        for customer in self.customers:
            if not customer.served and customer.serve(dish_name):
                return True, customer, customer.reward
        return False, None, 0
        
    def check_completed_orders(self):
        """Check for and remove served customers, returning their rewards
        
        Returns:
            list: List of tuples (order, reward) for completed orders
        """
        completed = []
        customers_to_remove = []
        
        for customer in self.customers:
            if customer.served:
                completed.append((customer.order, customer.reward))
                customers_to_remove.append(customer)
                
        for customer in customers_to_remove:
            self.customers.remove(customer)
            
        return completed
