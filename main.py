import random
import matplotlib.pyplot as plt

#Lets make sure use a lot of comments on our code, so we can easily explain it if asked about it. We can also use these comments to help us remember what we were thinking when we wrote the code, and to help us debug it later on if we need to.

Reservoirs = {}
Water_Demand = {}
#res_x = random.randint(0, width)
#res_y = random.randint(0, pyheight)
#Reservoirs[(res_x, res_y)] = 0

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

            #fill grid with random integers
            Water_Demand[(x, y)] = random.randint(1, 10) #I just used 10 as the highest demand - Jacob
            Water_Demand[(x, y)] = grid[y][x]
            #formula for conversion of water_demand to actual_water_demand = 2100+546(water_demand) 

    return Water_Demand #Returns the dictionary 

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

def getReservoirDistance(location, reservoir_key, Reservoirs):
    # 1. location is a tuple (x, y) from Water_Demand
    x1, y1 = location 
    
    # 2. reservoir_key is the string "Reservoir 1"
    # 3. Reservoirs[reservoir_key] gives us the tuple (rx, ry)
    x2, y2 = Reservoirs[reservoir_key]
    
    return abs(x1 - x2) + abs(y1 - y2)

def get_nearest_reservoir(location, Reservoirs):
    res_list = list(Reservoirs.keys())
    nearest_reservoir = res_list[0]
    
    # Initialize with the distance to the first reservoir
    min_dist = getReservoirDistance(location, nearest_reservoir, Reservoirs)
    
    for res_key in res_list:
        d = getReservoirDistance(location, res_key, Reservoirs)
        if d < min_dist:
            min_dist = d
            nearest_reservoir = res_key
            
    return nearest_reservoir

def get_pressure_loss(distance_from_reservoir, actual_tile_water_demand):
    pipe_length = distance_from_reservoir * 3280.84 #convert kilometers to feet, since the formula uses feet
    flow_rate = actual_tile_water_demand
    pipe_coefficient = 120 #assume Aluminum pipes with couplers, can be changed if needed
    pipe_inside_diameter = 18 #assume 1.5 inch diameter
    return (4.53 * pipe_length * ((flow_rate/pipe_coefficient) ** 1.852)/(pipe_inside_diameter ** 4.857))

def get_transport_power(pressure_loss, actual_tile_water_demand):
    return (pressure_loss * actual_tile_water_demand) / (3600000)

def get_transport_cost(transport_power, power_cost): #Cost = L * Q^2 => distance * demand^2 ; I'm assuming our flow rate is constant, and i added a weight on the demand
    return (transport_power * 24) * power_cost #Returns the daily cost of transporting water in dollars, from kilowatt hours

def single_res_cost(reservoir_name, Water_Demand, Reservoirs):
    total = 0
    # Use the name/key to look up the reservoir in the function below
    for location, demand in Water_Demand.items():
        # Pass the string name "Reservoir 1", not the coordinates
        distance = getReservoirDistance(location, reservoir_name, Reservoirs)
        
        # ... rest of your math ...
        actual_demand = 2100 + (546 * demand)
        pressure_loss = get_pressure_loss(distance, actual_demand)
        transport_power = get_transport_power(pressure_loss, actual_demand)
        transport_cost = get_transport_cost(transport_power, 0.12)
        total += transport_cost
    return total

def next_res_cost(Reservoirs, Water_Demand):
    total = 0

    # You MUST use 'location, demand' here to separate the key from the value
    for location, demand in Water_Demand.items():
        nearest_reservoir = get_nearest_reservoir(location, Reservoirs)
        distance = getReservoirDistance(location, nearest_reservoir, Reservoirs)
        
        # Now 'demand' is just a number, and this math will work:
        actual_demand = 2100 + (546 * demand)
        
        pressure_loss = get_pressure_loss(distance, actual_demand)
        transport_power = get_transport_power(pressure_loss, actual_demand)
        transport_cost = get_transport_cost(transport_power, 0.12)
        total += transport_cost

    return total

def get_best_resevoir_location(city_map, Reservoirs, Water_Demand):
    best_location = (0, 0)

def find_best_second_reservoir(Water_Demand, current_reservoirs):
    best_coord = (0, 0)
    min_total_cost = float('inf')
    
    # Iterate through every tile in the 50x50 grid
    for y in range(50):
        for x in range(50):
            # Skip if there is already a reservoir at this exact spot
            if (x, y) in current_reservoirs.values():
                continue
            
            # 1. Temporarily add the second reservoir
            current_reservoirs["Reservoir 2"] = (x, y)
            
            # 2. Calculate the system cost with TWO reservoirs
            # Buildings automatically use the nearest one in this function
            current_cost = next_res_cost(current_reservoirs, Water_Demand)
            
            # 3. If this is the cheapest we've seen, save it
            if current_cost < min_total_cost:
                min_total_cost = current_cost
                best_coord = (x, y)
    
    return best_coord, min_total_cost
    
def visualize_city(grid, Reservoirs):
    plt.clf() 
    
    # 1. Draw the demand heatmap
    plt.imshow(grid, cmap='magma', origin='upper')
    plt.colorbar(label='Water Demand')
    
    # 2. DRAW THE BOUNDARY BLOCK
    # This checks every tile to see if its neighbor belongs to a different reservoir
    for y in range(50):
        for x in range(50):
            nearest = get_nearest_reservoir((x, y), Reservoirs)
            # Check right neighbor
            if x < 49:
                if get_nearest_reservoir((x+1, y), Reservoirs) != nearest:
                    plt.plot([x + 0.5, x + 0.5], [y - 0.5, y + 0.5], color='white', lw=1, alpha=0.6)
            # Check bottom neighbor
            if y < 49:
                if get_nearest_reservoir((x, y+1), Reservoirs) != nearest:
                    plt.plot([x - 0.5, x + 0.5], [y + 0.5, y + 0.5], color='white', lw=1, alpha=0.6)
    
    # 3. Plot the reservoirs
    colors = ['cyan', 'blue', 'lime'] # Different colors for different reservoirs
    for i, (name, pos) in enumerate(Reservoirs.items()):
        plt.plot(pos[0], pos[1], marker='*', color=colors[i % 3], markersize=15, label=name)
    
    plt.title("City Water Demand & Reservoir Service Zones")
    plt.legend()
    plt.draw()
    plt.pause(0.1)

# Call your function with a starting position
#visualize_city(city_map, 25, 25)

    #return total

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

if __name__ == "__main__":
    # 1. Place the first reservoir randomly
    res1_x, res1_y = random.randint(1, 49), random.randint(1, 49)
    Reservoirs["Reservoir 1"] = (res1_x, res1_y)
    
    # 2. Find the best spot for the second reservoir
    print("Finding the most efficient spot for Reservoir 2... (This may take a moment)")
    best_pos, best_cost = find_best_second_reservoir(Water_Demand, Reservoirs)
    
    # 3. Finalize Reservoir 2 position
    Reservoirs["Reservoir 2"] = best_pos
    
    print(f"Optimal Location for Reservoir 2: {best_pos}")
    print(f"New Minimum System Cost: ${best_cost:,.2f}")

    # 4. Visualization
    plt.ion()
    visualize_city(city_map, Reservoirs) # Show city and both reservoirs
    plt.plot(best_pos[0], best_pos[1], 'b*', markersize=15, label='Optimal Reservoir 2')
    plt.legend()
    # ONLY run this after you are 100% sure Reservoirs["Reservoir 1"] is set
if "Reservoir 1" in Reservoirs:
    # 1. Get the baseline (Legacy)
    # We temporarily hide Reservoir 2 to see what the cost WAS
    res2_temp = Reservoirs.pop("Reservoir 2", None) 
    initial_cost = single_res_cost("Reservoir 1", Water_Demand, Reservoirs)
    
    # 2. Put Reservoir 2 back to see what the cost IS NOW
    if res2_temp:
        Reservoirs["Reservoir 2"] = res2_temp
    
    optimized_cost = next_res_cost(Reservoirs, Water_Demand)
    
    # 3. Final display logic
    savings = initial_cost - optimized_cost
    if initial_cost > 0:
        percent_improvement = (savings / initial_cost) * 100
        print(f"Success! Savings: {percent_improvement:.1f}%")
        plt.show(block=True)
