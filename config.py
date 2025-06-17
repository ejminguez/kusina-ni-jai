"""
Configuration settings for Kusina ni Jai
"""

# Display settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Kusina ni Jai"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BEIGE = (245, 245, 220)
GREEN = (150, 200, 150)
BLUE = (150, 150, 200)
RED = (200, 150, 150)
YELLOW = (255, 255, 0)
DARK_RED = (180, 0, 0)

# Pastel Colors
PASTEL_COLORS = [
    (255, 209, 220),  # Pastel Pink
    (209, 231, 255),  # Pastel Blue
    (255, 223, 186),  # Pastel Orange
    (186, 255, 201),  # Pastel Green
    (255, 186, 255),  # Pastel Purple
    (255, 255, 186),  # Pastel Yellow
    (209, 255, 255),  # Pastel Cyan
    (235, 222, 240)   # Pastel Lavender
]

# Game settings
STARTING_COINS = 100
STARTING_LEVEL = 1
STARTING_XP = 0
XP_TO_LEVEL = 100
XP_LEVEL_MULTIPLIER = 1.5
DEFAULT_USERNAME = "Chef"
DEFAULT_PROFILE_PIC = "assets/sprites/default_profile.png"
MAX_CONSECUTIVE_LOST_CUSTOMERS = 5

# Customer settings
MAX_CUSTOMERS = 4
CUSTOMER_SPAWN_INTERVAL = 20000  # milliseconds
MIN_PATIENCE = 30  # seconds
MAX_PATIENCE = 60  # seconds
KNOWN_RECIPE_CHANCE = 0.7

# File paths
RECIPES_FILE = "data/recipes.json"
INGREDIENTS_FILE = "data/ingredients.json"
SAVE_FILE = "data/save.json"
PROFILE_FILE = "data/profile.json"

# Default game assets
DEFAULT_INGREDIENTS = ["rice", "egg", "tomato", "onion", "garlic"]
DEFAULT_TOOLS = ["pan", "pot"]

# Upgrade costs
INGREDIENT_COST = 50
TOOL_COST = 100

# Filipino names for customers
FILIPINO_NAMES = [
    "Juan", "Maria", "Pedro", "Rosa", "Jose", "Lourdes", "Miguel", "Luzviminda",
    "Antonio", "Josefina", "Eduardo", "Teresita", "Ricardo", "Gloria", "Manuel",
    "Corazon", "Francisco", "Imelda", "Andres", "Remedios", "Roberto", "Juana",
    "Danilo", "Natividad", "Mariano", "Rosario", "Ernesto", "Leticia", "Rodrigo",
    "Felicidad", "Alejandro", "Erlinda", "Jaime", "Carmela", "Renato", "Dolores",
    "Rodel", "Marilou", "Efren", "Maricel", "Dindo", "Lorna", "Arnel", "Divina"
]

# Filipino recipes
FILIPINO_RECIPES = [
    {
        "name": "Adobo",
        "ingredients": ["chicken", "garlic", "vinegar", "soy sauce"],
        "tools": ["pot"],
        "cooking_time": 60,
        "difficulty": 3
    },
    {
        "name": "Sinigang",
        "ingredients": ["pork", "tomato", "onion", "tamarind"],
        "tools": ["pot"],
        "cooking_time": 75,
        "difficulty": 3
    },
    {
        "name": "Pancit Canton",
        "ingredients": ["noodles", "chicken", "carrot", "cabbage"],
        "tools": ["pan"],
        "cooking_time": 45,
        "difficulty": 2
    },
    {
        "name": "Lumpia",
        "ingredients": ["ground pork", "carrot", "onion", "wrapper"],
        "tools": ["pan"],
        "cooking_time": 40,
        "difficulty": 3
    },
    {
        "name": "Lechon Kawali",
        "ingredients": ["pork belly", "salt", "oil"],
        "tools": ["pot", "pan"],
        "cooking_time": 90,
        "difficulty": 4
    },
    {
        "name": "Kare-Kare",
        "ingredients": ["oxtail", "peanut butter", "eggplant", "string beans"],
        "tools": ["pot"],
        "cooking_time": 120,
        "difficulty": 5
    },
    {
        "name": "Tinola",
        "ingredients": ["chicken", "ginger", "chili leaves", "green papaya"],
        "tools": ["pot"],
        "cooking_time": 60,
        "difficulty": 2
    },
    {
        "name": "Sisig",
        "ingredients": ["pork face", "onion", "chili", "calamansi"],
        "tools": ["pan"],
        "cooking_time": 50,
        "difficulty": 4
    },
    {
        "name": "Bicol Express",
        "ingredients": ["pork", "coconut milk", "chili", "shrimp paste"],
        "tools": ["pot"],
        "cooking_time": 55,
        "difficulty": 3
    },
    {
        "name": "Humba",
        "ingredients": ["pork belly", "soy sauce", "vinegar", "brown sugar"],
        "tools": ["pot"],
        "cooking_time": 80,
        "difficulty": 3
    }
]

# Additional Filipino ingredients
FILIPINO_INGREDIENTS = [
    "pork", "chicken", "vinegar", "soy sauce", "tamarind", "noodles", 
    "cabbage", "ground pork", "wrapper", "pork belly", "salt", "oil",
    "oxtail", "peanut butter", "eggplant", "string beans", "ginger",
    "chili leaves", "green papaya", "pork face", "chili", "calamansi",
    "coconut milk", "shrimp paste", "brown sugar"
]
