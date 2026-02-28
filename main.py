import random
import matplotlib.pyplot as plt

def buildGrid(width, height):
    """Creates a 2D array of zeros representing the city plots."""
    grid = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        grid.append(row)
    return grid
    
def getDistance(xA, yA, xB, yB):
    return abs(xA - xB) + abs(yA - yB)

def populate_urban_bloom(grid, centers, max_demand, decay_rate):
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            for cx, cy in centers:
                distance = getDistance(x, y, cx, cy)
                
                # Calculate how much demand reaches this specific block
                bloom_val = max_demand - (distance * decay_rate)
                bloom_val = max(0, bloom_val) # No negative demand
                
                # If this center's bloom is stronger than a previous one, use it
                if bloom_val > grid[y][x]:
                    grid[y][x] = bloom_val
            
            # Add minor noise to make the city look less like a perfect circle
            if grid[y][x] > 0:
                scaled_noise = (int(decay_rate * 0.1))
                grid[y][x] += random.randint(0, 1)

            if grid[y][x] == 0:
                Possible_Demand = {
                    "No Demand": 7.5,
                    "Low Demand": 40,
                    "Medium Demand": 15,
                    "High Demand": 1.25
                }

                demand_type = random.choices(list(Possible_Demand.keys()), weights=Possible_Demand.values(), k=1)[0]
                if demand_type == "Low Demand":
                    grid[y][x] = random.randint(1, 3)
                elif demand_type == "Medium Demand":
                    grid[y][x] = random.randint(4, 7)
                elif demand_type == "High Demand":
                    grid[y][x] = random.randint(8, 10)
                

def calculateTotalSystemCost(grid, resX, resY):
    """Sums up the 'Price' of sending water to every building from (resX, resY)."""
    total_cost = 0
    height = len(grid)
    width = len(grid[0])
    
    for y in range(height):
        for x in range(width):
            demand = grid[y][x]
            if demand > 0:
                dist = getDistance(x, y, resX, resY)
                # Cost = Distance * Volume (Demand)
                total_cost += (dist * demand)
    
    return total_cost
    
    
def visualize_city(grid, resX, resY):
    plt.clf() # Clear the previous frame
    
    # Display the demand density
    plt.imshow(grid, cmap='magma', origin='upper')
    plt.colorbar(label='Water Demand')
    
    # Plot the reservoir as a bright blue star
    plt.plot(resX, resY, 'c*', markersize=15, label='Reservoir')
    
    plt.title(f"Reservoir Optimization - Current Pos: ({resX}, {resY})")
    plt.legend()
    plt.draw()
    plt.pause(0.05) # Brief pause to create animation effect




# 1. Setup the city
city_map = buildGrid(50, 50)
city_centers = {
    "HotspotA": (1,1),
    "HotspotB": (1,1),
    "HotspotC": (1,1),
    "HotspotD": (1,1),
    "HotspotE": (1,1),
    "HotspotF": (1,1)
}

for hotspot in city_centers:
    city_centers[hotspot] = (random.randint(5, 45), random.randint(5, 45))
downtowns = [(random.randint(1, 50), random.randint(1, 50)), (random.randint(1, 50), random.randint(1, 50)), (random.randint(1, 50), random.randint(1, 50))]

# 2. Paint the demand
populate_urban_bloom(city_map, downtowns, 10, 0.5)

# 3. Test a potential reservoir location
test_cost = calculateTotalSystemCost(city_map, 25, 25)
print(f"Total transportation cost for reservoir at (25,25): {test_cost}")

plt.ion() 

# Call your function with a starting position
visualize_city(city_map, 25, 25)

    return total
