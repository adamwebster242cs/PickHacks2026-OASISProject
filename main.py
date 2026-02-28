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
    flow_rate = actual_tile_water_demand / 60
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
    colors = {'Reservoir 1': 'cyan', 'Reservoir 2': 'blue'}
    
    for name, pos in Reservoirs.items():
        # Get color from dict, default to 'white' if name is unexpected
        dot_color = colors.get(name, 'white') 
        plt.plot(pos[0], pos[1], marker='*', color=dot_color, markersize=15, label=name)
    
    plt.title("Legacy Infrastructure & Optimal Expansion")
    plt.legend(loc='upper right')
    plt.draw()
    plt.pause(0.1)


# =============================================================================
# FLASK API — added below your original code, nothing above this line changed.
# Run with:  python OASISv2.py
# Then open: http://localhost:5000
# =============================================================================

import json
import math
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)


@app.route("/")
def index():
    """Serve the frontend."""
    return send_from_directory(".", "oasis.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """
    Generate a new city grid using your existing functions.
    Expects JSON: { size, hotspots, decay, max_demand, pipe_diam, pipe_c, power_cost }
    Returns:      { grid, water_demand, centers, res1_pos, legacy_cost }
    """
    data       = request.get_json()
    size       = int(data.get("size", 50))
    hotspots   = int(data.get("hotspots", 6))
    decay      = float(data.get("decay", 0.5))
    max_demand = float(data.get("max_demand", 10))
    pipe_diam  = float(data.get("pipe_diam", 18))
    pipe_c     = float(data.get("pipe_c", 120))
    power_cost = float(data.get("power_cost", 0.12))

    # --- Use your exact functions ---
    grid = buildGrid(size, size)

    centers = [
        (random.randint(5, size - 5), random.randint(5, size - 5))
        for _ in range(hotspots)
    ]

    # populate_urban_bloom writes into the module-level Water_Demand dict and returns it
    local_water_demand_tuples = populate_urban_bloom(grid, centers, max_demand, decay)

    # Convert tuple keys → "x,y" string keys so JSON can serialize them
    water_demand_str = {f"{x},{y}": v for (x, y), v in local_water_demand_tuples.items()}

    # Place Reservoir 1 at a random legacy position
    r1x = random.randint(5, size - 5)
    r1y = random.randint(5, size - 5)
    res1_pos  = (r1x, r1y)
    Reservoirs_local = {"Reservoir 1": res1_pos}

    # Calculate legacy cost using your single_res_cost function
    # single_res_cost expects tuple keys, so pass local_water_demand_tuples
    legacy_cost = single_res_cost("Reservoir 1", local_water_demand_tuples, Reservoirs_local)

    return jsonify({
        "grid":         grid,
        "water_demand": water_demand_str,
        "centers":      [list(c) for c in centers],
        "res1_pos":     list(res1_pos),
        "legacy_cost":  round(legacy_cost, 4),
    })


@app.route("/api/optimize/stream", methods=["POST"])
def api_optimize_stream():
    """
    Run find_best_second_reservoir, streaming progress as Server-Sent Events.
    Expects JSON: { water_demand (str keys), res1_pos, size }
    Streams:      data: { x, y, cost, best_cost, best_pos, progress, evaluated, total, improved }
                  data: { done: true, best_pos, best_cost }
    """
    data         = request.get_json()
    water_demand_str = data["water_demand"]       # { "x,y": demand }
    r1x, r1y     = data["res1_pos"]
    size         = int(data.get("size", 50))

    # Convert string keys back to tuple keys for your functions
    water_demand_tuples = {
        (int(k.split(",")[0]), int(k.split(",")[1])): v
        for k, v in water_demand_str.items()
    }

    Reservoirs_local = {"Reservoir 1": (r1x, r1y)}

    # Build candidate list and shuffle (mirrors find_best_second_reservoir logic)
    candidates = [
        (x, y)
        for y in range(size)
        for x in range(size)
        if (x, y) not in Reservoirs_local.values()
    ]
    random.shuffle(candidates)
    total = len(candidates)

    def generate():
        best_coord = (0, 0)
        min_total_cost = float('inf')

        for i, (x, y) in enumerate(candidates):
            # Temporarily add the second reservoir — exactly like your function does
            Reservoirs_local["Reservoir 2"] = (x, y)

            # Use your next_res_cost function directly
            current_cost = next_res_cost(Reservoirs_local, water_demand_tuples)

            improved = False
            if current_cost < min_total_cost:
                min_total_cost = current_cost
                best_coord     = (x, y)
                improved       = True

            # Stream every 5th step and all improvements to keep updates smooth
            if improved or i % 5 == 0:
                payload = {
                    "x":         x,
                    "y":         y,
                    "cost":      round(current_cost, 4),
                    "best_cost": round(min_total_cost, 4),
                    "best_pos":  list(best_coord),
                    "progress":  round((i + 1) / total * 100, 1),
                    "evaluated": i + 1,
                    "total":     total,
                    "improved":  improved,
                }
                yield f"data: {json.dumps(payload)}\n\n"

        # Final event
        yield f"data: {json.dumps({'done': True, 'best_pos': list(best_coord), 'best_cost': round(min_total_cost, 4)})}\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


@app.route("/api/cost", methods=["POST"])
def api_cost():
    """
    Calculate system cost for a manually placed reservoir using your functions.
    Expects JSON: { water_demand (str keys), reservoirs: {"Reservoir 1": [x,y], ...} }
    Returns:      { cost }
    """
    data             = request.get_json()
    water_demand_str = data["water_demand"]
    raw_reservoirs   = data["reservoirs"]

    # Convert back to the formats your functions expect
    water_demand_tuples = {
        (int(k.split(",")[0]), int(k.split(",")[1])): v
        for k, v in water_demand_str.items()
    }
    Reservoirs_local = {k: tuple(v) for k, v in raw_reservoirs.items()}

    if len(Reservoirs_local) == 1:
        key  = list(Reservoirs_local.keys())[0]
        cost = single_res_cost(key, water_demand_tuples, Reservoirs_local)
    else:
        cost = next_res_cost(Reservoirs_local, water_demand_tuples)

    return jsonify({"cost": round(cost, 4)})


# =============================================================================
# ENTRY POINT
# Run as a Flask server:  python OASISv2.py
# Your original __main__ block is preserved below and will NOT run in this mode
# because Flask takes over __main__. To run the original matplotlib version,
# rename this file or comment out app.run().
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  OASIS SERVER — http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, threaded=True)
