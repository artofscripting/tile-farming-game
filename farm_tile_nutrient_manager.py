import random
from constants import game_config


class FarmTileNutrientManager:
    """Manages soil nutrients for a farm tile"""

    def __init__(self, tile):
        self.tile = tile
        self.nutrients = self._initialize_nutrients()

    def _initialize_nutrients(self):
        """Initialize nutrients with random variation"""
        default_nutrients = game_config.get('default_tile_nutrients', {
            'nitrogen': 10, 'phosphorus': 8, 'potassium': 12,
            'calcium': 5, 'magnesium': 3, 'sulfur': 2, 'water': 15
        })

        # Apply ±5% random variation to each nutrient
        nutrients = {}
        for nutrient, base_value in default_nutrients.items():
            # Calculate 5% variation range
            variation = base_value * 0.05
            # Generate random value within ±5% of base value
            random_value = base_value + random.uniform(-variation, variation)
            # Round to 1 decimal place and ensure non-negative
            nutrients[nutrient] = max(0.1, round(random_value, 1))

        return nutrients

    def check_nutrient_doubling_bonus(self, seed_data):
        """Check if soil nutrients meet the doubling thresholds for this crop"""
        nutrient_keys = ['nitrogen', 'phosphorus', 'potassium', 'calcium', 'magnesium', 'sulfur', 'water']

        for nutrient in nutrient_keys:
            double_key = f"{nutrient}_double"
            if double_key in seed_data:
                required_amount = seed_data[double_key]
                current_amount = self.nutrients.get(nutrient, 0)

                if current_amount < required_amount:
                    return False  # One nutrient is insufficient

        return True  # All nutrients meet the doubling threshold

    def consume_nutrients_for_harvest(self, seed_data):
        """Consume nutrients from soil during harvest based on crop requirements"""
        nutrient_keys = ['nitrogen', 'phosphorus', 'potassium', 'calcium', 'magnesium', 'sulfur', 'water']
        nutrients_consumed = []

        for nutrient in nutrient_keys:
            use_key = f"{nutrient}_use"
            if use_key in seed_data:
                consumption = seed_data[use_key]
                if consumption > 0:
                    # Consume nutrients, but don't go below 0
                    old_amount = self.nutrients.get(nutrient, 0)
                    self.nutrients[nutrient] = max(0, old_amount - consumption)
                    actual_consumed = old_amount - self.nutrients[nutrient]
                    if actual_consumed > 0:
                        nutrients_consumed.append(f"{nutrient}-{actual_consumed}")

        if nutrients_consumed:
            nutrients_summary = ", ".join(nutrients_consumed)
            print(f"  Nutrients consumed by {seed_data['name']}: {nutrients_summary}")

        # Update visual appearance after nutrient consumption
        self.tile.visual_manager.update_visual_appearance()

    def get_nutrient_level(self, nutrient):
        """Get the current level of a specific nutrient"""
        return self.nutrients.get(nutrient, 0)

    def get_all_nutrients(self):
        """Get all nutrient levels"""
        return self.nutrients.copy()

    def set_nutrient_level(self, nutrient, amount):
        """Set the level of a specific nutrient"""
        self.nutrients[nutrient] = max(0, amount)

