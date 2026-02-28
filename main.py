import random
import matplotlib.pyplot as plt

#Lets make sure use a lot of comments on our code, so we can easily explain it if asked about it. We can also use these comments to help us remember what we were thinking when we wrote the code, and to help us debug it later on if we need to.

def buildGrid(width, height):
    Water_Demand = {} #Create a dictionary to stroe value

    for x in range(width):
        for y in range(height):

            #fill grid with random integers
            Water_Demand[(x, y)] = random.randint(1, 10) #I just used 10 as the highest demand - Jacob

    return Water_Demand #Returns the dictionary 

def getDistance(x1, y1, x2, y2):
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

def transport_cost(distance, demand): #Cost = L * Q^2 => distance * demand^2 ; I'm assuming our flow rate is constant, and i added a weight on the demand
    return distance * (demand ** 2)

def single_res_cost(reservoir, Water_Demand): #Takes in reservoir location and water demands dictionary to comput cost of original reservoir
    total = 0

    for location, demand in Water_Demand.items():
        distance = getDistance(location, reservoir)
        total += transport_cost(distance, demand)

    return total
