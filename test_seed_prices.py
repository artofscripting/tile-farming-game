#!/usr/bin/env python3
from constants import seeds_config

print("Seed prices from config:")
for seed in seeds_config[:5]:
    print(f"  {seed['name']}: ${seed['cost']}")

# Test the price lookup function
def get_seed_price(seed_name):
    for seed in seeds_config:
        if seed['name'] == seed_name:
            return seed['cost']
    return 10  # Default price if seed not found

print("\nTesting price lookup:")
test_seeds = ['Carrot', 'Tomato', 'Blueberry', 'Corn', 'Wheat']
for seed in test_seeds:
    price = get_seed_price(seed)
    print(f"  {seed}: ${price}")

