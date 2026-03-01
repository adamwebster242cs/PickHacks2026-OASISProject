# PickHacks2026-OASISProject
36 Hour deadline group project with the goal of creating an optimization model that an determine optimal reservoir placement in a grid to minimize water transportation costs.

To run:
1. Clone repository / Download files
2. Download dependencies listed in requirements.txt via "pip install -r requirements.txt"
3. Run main.py
4. Click the ctrl + click the link provided by the terminal or open a new tab and go to http://localhost:5000/




Main Features:
- You can decide on Grid Size, Centers of Demand, Demand Decay Rate, and Peak Demand.
- For the animation feature, you can alter the speed at which the animation plays, and the measurement per tile, which changes the overall predicted outcome.

To use:

1. Select preferred City Grid Parameters.
2. Click Generate City Map to view a current city layout, with one reservoir placed and ready to go.
3. Click Run Optimization to see the animation and calculation play out.
4. View the Cost Analyis, Reservoir Locations, and Activity Logs on the right side.



Pressure Loss Formula used:
<img width="810" height="530" alt="image" src="https://github.com/user-attachments/assets/875ece1c-c49b-4f9d-9711-054133efa4f8" />

Hydraulic Pump Power Formula used:
<img width="767" height="777" alt="image" src="https://github.com/user-attachments/assets/88fd39af-ffa4-4cef-9d94-d98ed4341458" />
