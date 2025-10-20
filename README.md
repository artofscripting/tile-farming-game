# Tile Farming Game

An economic farming simulation game built with Python and Pyglet. Manage your farm with tractors, crops, buildings, and a dynamic market system featuring multiple selling mechanisms and a prestige progression system.

## 🎮 Game Overview

**Tile Farming** is an economic farming simulation where you start with a small plot of land and build a farming empire. The game features:

- **Dynamic Market System** with fluctuating crop prices
- **Multiple Selling Mechanisms** (Field, Barn, Orders)
- **Tractor Automation** with job queuing
- **Building Management** (Barns, Seed Bins)
- **Nutrient-Based Crop Growth**
- **Order Fulfillment System** for premium pricing
- **Prestige Progression** for advanced unlocks

## 🚀 Getting Started

### First Steps
- Start with $1,000 and basic seed types
- Buy land tiles ($50 each) to expand your farm
- Build barns ($200) and seed bins ($100) for storage
- Plant crops and harvest with tractors

## 🎯 Core Mechanics

### Land Management
- **Starting Area**: 3x3 grid (expandable to 50x25)
- **Tile States**: Unowned → Owned → Tilled → Planted → Growing → Ready Harvest
- **Buildings**: Barns for crop storage, Seed Bins for seed storage

### Crop System
- **Growth Cycle**: Plant → Grow (visual scaling) → Harvest Ready
- **Nutrient Requirements**: 7 nutrients (N, P, K, Ca, Mg, S, Water)
- **Harvest Bonuses**: Double yield with optimal nutrients
- **Available Crops**: Carrots, Tomatoes, Blueberries, Corn, etc.

### Tractor Operations
- **Multiple Tractors**: Purchase additional tractors (progressive cost)
- **Job Types**: Tilling, Planting, Fertilizing, Harvesting
- **Row Modes**: 1-row or 3-row operations
- **Job Queuing**: Queue multiple operations for automation

## 💰 Selling Mechanisms

The game features three distinct selling systems, each with different mechanics and strategic implications:

### 1. Field Harvesting (Immediate Sale)
**How it works:**
- Tractors harvest crops directly from the field
- If no barn storage is available, crops are sold immediately at current market price
- Harvested crops are accumulated during tractor jobs and sold in bulk when the job completes

**Strategic Considerations:**
- ✅ **Immediate cash flow** - Get money right away
- ❌ **Price risk** - Stuck with current market price
- ❌ **No storage control** - Can't wait for better prices
- 💡 **Best for**: Quick cash needs, low-value crops, emergency funds

### 2. Barn Storage & Manual Selling
**How it works:**
- Crops harvested by tractors are automatically stored in the nearest barn
- Players manually sell barn contents by **Shift + Right-clicking** on barn tiles
- All stored crops of one type are sold at once at current market price

**Strategic Considerations:**
- ✅ **Price timing control** - Wait for optimal market conditions
- ✅ **Bulk selling** - Sell large quantities when prices peak
- ✅ **Storage capacity** - Build multiple barns for more storage
- ❌ **Manual intervention required** - Not automated
- 💡 **Best for**: Market timing, large-scale operations, profit maximization

### 3. Order Fulfillment System (Premium Pricing)
**How it works:**
- Outside buyers post orders with specific crop requirements
- Orders offer **premium prices** (100%-500% above market value)
- Players accept orders and fulfill them by delivering crops from barn storage
- Orders have **time limits** and **quantity requirements**

**Order Types:**
- **Crop Type**: Specific crop required (e.g., "500 Tomatoes")
- **Quantity**: Amount needed (scales with game progress)
- **Premium Price**: 1.0x to 5.0x market price
- **Duration**: 3-7 days to complete
- **Status**: Incoming → Accepted → Fulfilled/Expired

**Strategic Considerations:**
- ✅ **Highest profit potential** - Premium pricing (up to 5x market value)
- ✅ **Guaranteed buyers** - No market fluctuation risk
- ❌ **Time pressure** - Must complete within deadline
- ❌ **Storage requirements** - Need barn capacity for order crops
- ❌ **Planning required** - Must grow specific crops in advance
- 💡 **Best for**: High-profit farming, strategic planning, risk-averse players

## 📊 Market System

### Dynamic Pricing
- **Update Frequency**: Every 30 seconds
- **Price Trends**: Up (↑), Stable (→), Down (↓)
- **Historical Data**: 180 days of price history available
- **Price Range**: Varies by crop type and market conditions

### Market Windows
- **Live Market (L key)**: Current prices and trends
- **Market History (H key)**: Price charts and analysis
- **Fertilizer Info (F key)**: Fertilizer costs and effects

## 🏗️ Building System

### Barns
- **Cost**: $200 (base) + upgrades
- **Capacity**: 100 units per barn (upgradeable)
- **Functions**: Crop storage, manual selling, order fulfillment
- **Upgrades**: Increase capacity, reduce costs

### Seed Bins
- **Cost**: $100
- **Capacity**: 50 seed units per bin
- **Functions**: Seed storage, planting efficiency
- **Benefits**: Faster planting, seed organization

## 🚜 Tractor Management

### Tractor Types
- **Base Tractor**: Free, basic operations
- **Additional Tractors**: Purchased with prestige points

### Prestige System
**What is Prestige?**
- Prestige is a special currency earned through successful farming operations
- Start with 1 prestige
- Earned by fulfilling premium orders

**How to Earn Prestige:**
- **Order Revenue**: Gain 1 prestige for every $750 earned from order fulfillment (cumulative across all orders)
- Example: $1,500 total order earnings = 2 prestige points

**How to Use Prestige:**
- **Purchase Additional Tractors**: 
  - Second tractor: 50 prestige  
  - Third tractor: 70 prestige
  - Each additional tractor costs 20 more prestige than the previous
- **Strategic Investment**: Prestige enables farm expansion and automation

**Prestige Strategy:**
- Focus on high-value orders to earn prestige faster
- Use prestige to unlock tractor automation for larger-scale farming
- Balance between immediate profits and long-term farm expansion

### Operation Modes
- **Single Row**: Process one row at a time
- **Triple Row**: Process three rows simultaneously (advanced tractors)
- **Job Queuing**: Queue multiple operations for automation

## 🎮 Controls

### Basic Controls
- **B**: Select barn (build mode)
- **S**: Select seed bin (build mode)
- **M**: Market prices
- **L**: Live market window
- **H**: Market history
- **F**: Fertilizer info

### Tractor Controls
- **TAB**: Switch between tractors
- **P**: Purchase new tractor (uses prestige points)
- **SPACEBAR**: Auto-till all rows
- **T**: Manual till current row

### Advanced Controls
- **Shift + Right-click (Barn)**: Sell all stored crops
- **Shift + Left-click (Barn)**: Upgrade barn
- **ESC**: Exit current mode
- **R**: Reset farm

## 💡 Strategy Guide

### Early Game (Days 1-10)
1. **Expand Land**: Buy 10-15 tiles for basic farm
2. **Build Infrastructure**: 1-2 barns, 1 seed bin
3. **Focus on Basics**: Grow high-value crops like tomatoes
4. **Market Timing**: Sell immediately for quick cash

### Mid Game (Days 10-50)
1. **Scale Operations**: Multiple tractors, large farm area
2. **Storage Strategy**: Build several barns for market timing
3. **Order System**: Start accepting premium orders to earn prestige
4. **Prestige Investment**: Use earned prestige to purchase additional tractors
5. **Market Analysis**: Use history window for price predictions

### Late Game (Days 50+)
1. **Order Specialization**: Focus on high-demand crops
2. **Bulk Operations**: Maximize tractor efficiency
3. **Profit Optimization**: Combine all three selling methods
4. **Empire Building**: Largest possible farm with full automation

### Profit Maximization Tips
- **Barn Selling**: Store crops during price dips, sell during peaks
- **Order Fulfillment**: Accept orders for crops you can grow reliably (earns prestige)
- **Field Harvesting**: Use for overflow when barns are full
- **Market Monitoring**: Check prices every 30 seconds
- **Prestige Investment**: Use prestige to unlock tractor automation
- **Bulk Discounts**: Larger orders often have better premiums

## 🏆 Game Features

- **Save/Load System**: Persistent game state
- **Debug Mode**: Start with $100,000 for testing
- **Visual Feedback**: Crop growth animations, tractor movements
- **Economic Simulation**: Realistic market fluctuations
- **Progressive Difficulty**: Scaling order requirements
- **Multiple UI Windows**: Market data, order management, financial tracking

## 🔧 Technical Details

- **Engine**: Python + Pyglet
- **Resolution**: 1013x768 (fixed)
- **Tile System**: 32x32 pixel grid
- **Configuration**: JSON-based game data
- **Performance**: Optimized batch rendering

## 📝 Development Notes

The game features a modular architecture with specialized managers:
- `FarmManager`: Land and tile management
- `TractorManager`: Automated farming operations
- `Market`: Dynamic pricing system
- `OrderSystem`: Premium order management
- `Finance`: Transaction tracking

Built with extensibility in mind - new crops, buildings, and mechanics can be added through configuration files.

---

**Enjoy building your farming empire in Tile Farming! 🌾🚜**</content>
<parameter name="filePath">c:\Users\ArtOf\PycharmProjects\pythonProject\README.md