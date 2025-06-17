# Kusina ni Jai

A 2D cooking simulation game built with Python and PyGame where you play as a chef serving customers with both known and custom recipes.

## Game Overview

In "Kusina ni Jai" (Jai's Kitchen), you are a chef who must prepare dishes for customers. Some customers will order dishes from your recipe book, while others will request custom dishes that you'll need to create by combining ingredients logically.

### Key Features

- **Recipe System**: Prepare dishes from known recipes or create new ones by combining ingredients
- **Customer System**: Serve customers before they run out of patience
- **Cooking Interface**: Select ingredients and tools to prepare dishes
- **Upgrade System**: Earn coins to unlock new ingredients and cooking tools

## Installation

1. Make sure you have Python 3.6+ installed
2. Install PyGame:
   ```
   pip install pygame
   ```
3. Clone this repository:
   ```
   git clone https://github.com/yourusername/kusina-ni-jai.git
   cd kusina-ni-jai
   ```
4. Run the game:
   ```
   python main.py
   ```

## How to Play

1. **Main Menu**: Press ENTER to start the game
2. **Serving Customers**: Watch the top of the screen for customer orders and their patience timers
3. **Cooking**:
   - Click the "Cook" button to enter the cooking interface
   - Select ingredients and tools by clicking on them
   - Click "Cook!" to prepare the dish
   - If your combination matches a recipe or makes logical sense, the dish will be created
4. **Upgrades**:
   - Click the "Upgrades" button to access the upgrade shop
   - Spend coins to unlock new ingredients and tools

## Game Mechanics

### Recipes
- **Known Recipes**: These are pre-defined combinations that always work
- **Custom Recipes**: When a customer orders something not in your recipe book, you'll need to create a logical combination
- **Recipe Discovery**: Successfully creating a new dish adds it to your recipe book

### Customers
- Each customer has a patience timer
- Serve them before the timer runs out to earn coins
- Different dishes have different rewards based on complexity

### Progression
- Earn coins by successfully serving customers
- Use coins to unlock new ingredients and tools
- Higher level ingredients and tools allow for more complex recipes

## Development

The game is structured into several key components:

- `main.py`: Main game loop and state management
- `game_states.py`: Enum for different game states
- `player.py`: Player data and progression
- `recipe_system.py`: Recipe management and validation
- `customer_system.py`: Customer generation and management
- `cooking_interface.py`: UI for selecting ingredients and tools
- `ui_elements.py`: General UI rendering

## Future Enhancements

- Add sound effects and background music
- Implement daily challenges and special orders
- Add more ingredients, tools, and recipes
- Create a story mode with character progression
- Add difficulty levels and time management challenges
