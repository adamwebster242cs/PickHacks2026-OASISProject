import random
import matplotlib.pyplot as plt

#Lets make sure use a lot of comments on our code, so we can easily explain it if asked about it. We can also use these comments to help us remember what we were thinking when we wrote the code, and to help us debug it later on if we need to.

def buildGrid(width, height):
    Water_Demand = {} #Create a dictionary to stroe value

    for x in range(width):
        for y in range(height):

            #fill grid with random integers
            Water_Demand[(x, y)] = random.randint(1, 10) #I just used 10 as the highest demand - Jacob
            #formula for conversion of water_demand to actual_water_demand = 2100+546(water_demand) 

    return Water_Demand #Returns the dictionary 

def getDistance(x1, y1, x2, y2): #will need to be changed to include actual values of reservoir
    #manhattan distance
    return abs(x1[0] - x2[0]) + abs(y1[1] - y2[1])

# If we use a function like this, we can cause whats called Urban Bloom, where we mark high cost areas initially, and the areas around it gradually decrease in cost. Causing an effect like a real cities' demand for something like this.
def urbanBloom():
    return

def calculateTotalSystemCost():
    return

# I think we should use matplotlib to visualize our final "perfect" reservoir spot on a map using a heat map to show the demand across the city. We can use a color gradient to indicate areas of high demand (red) to low demand (blue), with the reservoir location marked clearly.  - Jacob Agrees
def visualizeCity():
    return

def get_pressure_loss(distance_from_reservoir, actual_tile_water_demand):
    pipe_length = distance_from_reservoir
    flow_rate = actual_tile_water_demand
    pipe_coefficient = 120 #assume Aluminum pipes with couplers, can be changed if needed
    pipe_inside_diameter = 1.5 #assume 1.5 inch diameter
    return (4.53 * pipe_length * ((flow_rate/pipe_coefficient) ** 1.852)/(pipe_inside_diameter ** 4.857))

def get_transport_power(pressure_loss, actual_tile_water_demand):
    return (pressure_loss * actual_tile_water_demand) / (3600000)

def get_transport_cost(transport_power, power_cost): #Cost = L * Q^2 => distance * demand^2 ; I'm assuming our flow rate is constant, and i added a weight on the demand
    return (transport_power * 24) * power_cost #Returns the daily cost of transporting water in dollars, from kilowatt hours

def single_res_cost(reservoir, Water_Demand): #Takes in reservoir location and water demands dictionary to comput cost of original reservoir
    total = 0

    for location, demand in Water_Demand.items():
        distance = getDistance(location, reservoir)
        actual_demand = 2100 + (546*demand)
        pressure_loss = get_pressure_loss(distance, actual_demand)
        transport_power = get_transport_power(pressure_loss, actual_demand)
        transport_cost = get_transport_cost(transport_power, 0.12) #Assuming power cost of 12 cents per kWh
        total += transport_cost

    return total
