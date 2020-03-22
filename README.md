# GeneticUAVPlanning #
The use of Genetic Algorithms to solve the Travelling salesman in the conext of UAV Planning 

This set of Files simulates the planning of Unmanned Air Vehicles (UAVs) to inspect ships in a maritime tactical picture.  The UAV planning is to schedule an efficient route to inspect a number of ships in the maritime tactical picture. The maritime tactical picture is simulated in PyGame. 

![picture alt](https://github.com/JulesVerny/GeneticUAVPlanning/blob/master/Typical_Route.png "UAV Planning")

The UAV Planning is based upon a Travelling Salesman Problem (TSP) using Genetic Algorithms. This is through the use of mlrose package developed by Genevieve Hayes.

https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847

The mlrose package takes a set of coordinates and responds with an proposed sequence order. The mlrose package uses Genetic Algorithm, and so takes around 10 seconds to process through 200 iterations of populations.

### Core Principles ###
In this ship simulation, the ships are in constant motion, and so I call the UAV planning twice. The first call is based upon the the current ship positions. This returns an initial assumed sequence, and UAV travel speed, to make a first order prediction of the ships positions at the UAV arrival, based upon the original sequence.  These reviseed ship coordinates are used to call into the planning again.    

Because the planning takes a little while to execute, I have placed this in a Flask based web server, which is called from a seperate thread from the main simulation.   

### Simulation File ###
The simulation of ships is based upon a scenario file: SimpleScenario5.csv.   The csv file is based upon a sequence of events that Create, Update and Delete Ship Tracks. The UAV Always starts, and completes from the Track 00 (Portsmouth Harbour).  The simulaiton file also inlcudes Requested Times to Generate a Plan, and When to Start the UAV Simulation. The Scenario file is read into the simulation through pandas.  
![picture alt](https://github.com/JulesVerny/GeneticUAVPlanning/blob/master/ScenarioFileImage.PNG "Scenario File")

Note the Simulation has to Halt, waiting upon Planning Thread to complete the Plan generation response, before it can continue to perfom the UAV simulation.  
### Conclsions ###
Some ratehr mixed results. The planning does take rather a long time. The routes appear to require aroind 200 generations to come up with acceptbale results. See how adjusting the mlrose.TSP parameters within the MPWebServer (Line 62) alters the speed and performance of the propsod plans. 
I will probaly investigate the develoment of my own genetic algorithms to attmept to speed up the execution, and see if there are any differences in perfomances over the mlrose package. 
### Useage ###
The Mission Planning Web Server, which inlcudes the calls into mlrose,  is started using:
  python MPWebServer.py

The main UAV Simulation is then started using:
  python UAV_Scenario.py

The following files support the  UAV Simulation
* MPWebServer.py     : This is the Mission Planning Web Server. It accepts the JSON based coordinates, and makes calls into the core mlrose TSP algorithms. It is based upon Flask web server and Json processing
* UAV_Scenario.py  : This is the main simulaiton script.  It coordinates the main simulation by reading the csv based scenario filw and scheduling the simulation events. This scripot uses Threading to Seperate the Mission Planning Thread upon  a "PLAN" event, but then has to Join (or Wait) upon that Thread before it can process the "START UAV" event
* TacticalPicture.py   : This is a Tactical picture graphics, based upon pygame. It maintains a list of ship Tracks. 
* RoutePlanning.py  : This script processes Tactical Picture Ship Tracks and prepares the Json based coordinates payload and calls into the Mission Planning Web Server
* Track.py  : An Entity class to represent each ship Track

Press Escape in pygame window to halt the siumlation, at any time.

### Main Python Package Dependencies ###
mlrose, pygame, flask, numpy, pandas, matplotlib, requests

### Acknowledgments: ###
* Solving Travelling Salesperson Problems with Python  by Genevieve Hayes: 
https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847


