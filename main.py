import random
import matplotlib.pyplot as plt

#Lets make sure use a lot of comments on our code, so we can easily explain it if asked about it. We can also use these comments to help us remember what we were thinking when we wrote the code, and to help us debug it later on if we need to.

width = 10 #in kilometers
height = 10 #in kilometers
Reservoirs = {}
#res_x = random.randint(0, width)
#res_y = random.randint(0, height)
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
    Water_Demand = {}
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

def getReservoirDistance(location, reservoir): #will need to be changed to include actual values of reservoir
    #manhattan distance
    x1, y1 = location(x1, y1)
    x2, y2 = reservoir(x2, y2)
    return abs(x1[0] - x2[0]) + abs(y1[1] - y2[1])

def get_nearest_reservoir(location, Reservoirs):
    nearest_reservoir = 0

    distance = getReservoirDistance(location, Reservoirs[0])
    for reservoir in Reservoirs:
        distance_from_reservoir = getReservoirDistance(location, reservoir)
        if distance_from_reservoir < distance:
            nearest_reservoir = reservoir
            distance = distance_from_reservoir
        
    return nearest_reservoir

def get_pressure_loss(distance_from_reservoir, actual_tile_water_demand):
    pipe_length = distance_from_reservoir * 3280.84 #convert kilometers to feet, since the formula uses feet
    flow_rate = actual_tile_water_demand
    pipe_coefficient = 120 #assume Aluminum pipes with couplers, can be changed if needed
    pipe_inside_diameter = 1.5 #assume 1.5 inch diameter
    return (4.53 * pipe_length * ((flow_rate/pipe_coefficient) ** 1.852)/(pipe_inside_diameter ** 4.857))

def get_transport_power(pressure_loss, actual_tile_water_demand):
    return (pressure_loss * actual_tile_water_demand) / (3600000)

def get_transport_cost(transport_power, power_cost): #Cost = L * Q^2 => distance * demand^2 ; I'm assuming our flow rate is constant, and i added a weight on the demand
    return (transport_power * 24) * power_cost #Returns the daily cost of transporting water in dollars, from kilowatt hours

def single_res_cost(reservoir, Water_Demand):
    total = 0

    for location, demand in Water_Demand.items():
        distance = getReservoirDistance(location, reservoir)
        actual_demand = 2100 + (546*demand)
        pressure_loss = get_pressure_loss(distance, actual_demand)
        transport_power = get_transport_power(pressure_loss, actual_demand)
        transport_cost = get_transport_cost(transport_power, 0.12) #Assuming power cost of 12 cents per kWh
        total += transport_cost

    return total

def next_res_cost(Reservoirs, Water_Demand):
    total = 0

    for location, demand in Water_Demand.items():
        nearest_reservoir = get_nearest_reservoir(location, Reservoirs)
        distance = getReservoirDistance(location, nearest_reservoir)
        actual_demand = 2100 + (546*demand)
        pressure_loss = get_pressure_loss(distance, actual_demand)
        transport_power = get_transport_power(pressure_loss, actual_demand)
        transport_cost = get_transport_cost(transport_power, 0.12)
        total += transport_cost

    return total

def get_best_resevoir_location(city_map, Reservoirs, Water_Demand):
    best_location = (0, 0)
    
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

plt.ion()

visualize_city(city_map, random.randint(1, 49), random.randint(1, 49))

plt.show(block=True)