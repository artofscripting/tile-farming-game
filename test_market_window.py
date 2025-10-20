from market import Market
from market_window import MarketWindow

# Create market and window
market = Market()
window = MarketWindow(market)

# Check change labels
print('Change labels initialized:')
for crop_name, labels in list(window.labels.items())[:3]:
    change_text = labels['change'].text
    print(f'  {crop_name}: "{change_text}"')

window.close()

