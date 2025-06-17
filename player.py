"""
Player class for managing player state and progression
"""
import json
import os
from config import (
    STARTING_COINS, STARTING_LEVEL, STARTING_XP, XP_TO_LEVEL, 
    XP_LEVEL_MULTIPLIER, DEFAULT_USERNAME, DEFAULT_PROFILE_PIC,
    PROFILE_FILE
)

class Player:
    def __init__(self):
        self.coins = STARTING_COINS
        self.level = STARTING_LEVEL
        self.experience = STARTING_XP
        self.experience_to_next_level = XP_TO_LEVEL
        self.username = DEFAULT_USERNAME
        self.profile_pic = DEFAULT_PROFILE_PIC
        self.color = (0, 255, 0)  # Default color (green)
        self.consecutive_lost_customers = 0
        self.load_player_data()
        
    def load_player_data(self):
        """Load player data from save file if it exists"""
        save_path = "data/save.json"
        if os.path.exists(save_path):
            try:
                with open(save_path, "r") as file:
                    data = json.load(file)
                    self.coins = data.get("coins", STARTING_COINS)
                    self.level = data.get("level", STARTING_LEVEL)
                    self.experience = data.get("experience", STARTING_XP)
                    self.experience_to_next_level = data.get("experience_to_next_level", XP_TO_LEVEL)
                    self.consecutive_lost_customers = data.get("consecutive_lost_customers", 0)
            except Exception as e:
                print(f"Error loading player data: {e}")
                
        # Load profile data
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as file:
                    data = json.load(file)
                    self.username = data.get("username", DEFAULT_USERNAME)
                    self.profile_pic = data.get("profile_pic", DEFAULT_PROFILE_PIC)
                    
                    # Load color as a list and convert to tuple
                    color_list = data.get("color", [0, 255, 0])
                    self.color = tuple(color_list)
            except Exception as e:
                print(f"Error loading profile data: {e}")
                
    def save_player_data(self):
        """Save player data to file"""
        save_path = "data/save.json"
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            data = {
                "coins": self.coins,
                "level": self.level,
                "experience": self.experience,
                "experience_to_next_level": self.experience_to_next_level,
                "consecutive_lost_customers": self.consecutive_lost_customers
            }
            
            with open(save_path, "w") as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"Error saving player data: {e}")
            
    def save_profile_data(self):
        """Save profile data to file"""
        try:
            os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
            
            data = {
                "username": self.username,
                "profile_pic": self.profile_pic,
                "color": list(self.color)  # Convert tuple to list for JSON serialization
            }
            
            with open(PROFILE_FILE, "w") as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"Error saving profile data: {e}")
        
    def add_coins(self, amount):
        """Add coins to player
        
        Args:
            amount: Amount of coins to add
        """
        self.coins += amount
        self.save_player_data()
        
    def spend_coins(self, amount):
        """Spend coins if player has enough
        
        Args:
            amount: Amount of coins to spend
            
        Returns:
            bool: True if successful, False if not enough coins
        """
        if self.coins >= amount:
            self.coins -= amount
            self.save_player_data()
            return True
        return False
        
    def add_experience(self, amount):
        """Add experience and level up if needed
        
        Args:
            amount: Amount of experience to add
            
        Returns:
            bool: True if player leveled up
        """
        self.experience += amount
        
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            self.save_player_data()
            return True
            
        self.save_player_data()
        return False
        
    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * XP_LEVEL_MULTIPLIER)
        
    def update_username(self, username):
        """Update player username
        
        Args:
            username: New username
        """
        self.username = username
        self.save_profile_data()
        
    def update_profile_pic(self, profile_pic):
        """Update player profile picture
        
        Args:
            profile_pic: Path to new profile picture
        """
        self.profile_pic = profile_pic
        self.save_profile_data()
        
    def update_color(self, color):
        """Update player color theme
        
        Args:
            color: RGB color tuple
        """
        self.color = color
        self.save_profile_data()
        
    def add_lost_customer(self):
        """Add a lost customer to the counter
        
        Returns:
            bool: True if player has lost too many customers
        """
        self.consecutive_lost_customers += 1
        self.save_player_data()
        return self.consecutive_lost_customers
        
    def reset_lost_customers(self):
        """Reset the lost customer counter"""
        self.consecutive_lost_customers = 0
        self.save_player_data()
