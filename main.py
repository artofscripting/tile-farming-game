import pyglet
from game_window import GameWindow
from splash_screen import SplashScreen


def main():
    print("🌾 Advanced Farming Game Controls:")
    print("💰 Economy & Inventory:")
    print("  - Start with $1000 and various seeds")
    print("  - Money and barn capacity shown in right panel")
    print("🌱 Seed Selection:")
    print("  - Seeds: Carrot, Tomato, Blueberry, etc.")
    print("🚜 Farming Operations:")
    print("  - BUY TILES: Purchase forest land ($50 each)")
    from constants import game_config
    barn_cost = game_config['barn_place_cost']
    seed_bin_cost = game_config['seed_bin_place_cost']
    print(f"  - BUILD: Place barns (${barn_cost}) and seed bins (${seed_bin_cost})")
    print("  - PLOW: Till owned land to prepare for planting") 
    print("  - PLANT SEEDS: Plant selected seeds on tilled soil")
    print("  - HARVEST: Collect mature crops for money")
    print("⌨️ Keyboard Controls:")
    print("  - P: Purchase new tractor (30+ prestige, progressive cost)")
    print("  - R: Reset farm")
    print("  - ESC: Exit current mode")
    print("📈 Market System:")
    print("  - Crop prices fluctuate every 30 seconds")
    print("  - Prices can trend up, down, or stay stable")
    print("  - Store crops in barns and sell when prices are high!")
    print("🎮 Click buttons to enter different modes, then click tiles to interact!")
    
    global game_window_instance
    def start_game():
        global game_window_instance
        game_window_instance = GameWindow()
    SplashScreen(next_callback=start_game)
    pyglet.app.run()


if __name__ == '__main__':
    main()

