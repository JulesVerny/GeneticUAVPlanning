# UAV Planning using Genetic Algorithms and Simulated Annealing Methods#
## An Application of Travelling Salesman Problem ##
The use of two methods  to solve the Travelling salesman in the conext of UAV Planning 
* Genetic Algorithms  - mlrose package
* simulated annealing (ten Lines of Code !)

This set of Files simulates the planning of Unmanned Air Vehicles (UAVs) to inspect ships in a maritime tactical picture.  The UAV planning is to schedule an efficient route to inspect a number of ships in the maritime tactical picture. The maritime tactical picture is simulated in PyGame. 

![picture alt](https://github.com/JulesVerny/GeneticUAVPlanning/blob/master/Typical_Route.png "UAV Planning")


###TheGenetic Algorithm method:###
Solving the Travelling Salesman Problem (TSP) using Genetic Algorithms. This is through the use of the mlrose package developed by Genevieve Hayes.

https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847

The mlrose package takes a set of coordinates and responds with an proposed sequence order. The mlrose package uses Genetic Algorithm, and can take around 10 seconds to process through 200 iterations of populations.

###Simulated Annealing :###
The TSP can also be solved through a so called simulated annealing method. (And No I don't understand this method) The results seem pretty impressive for so little (involved code) Quick to execute and robust results so far.   Solving the Travelling Salesman Problem (TSP) through  simulated annealing (In ten Lines of Code !)

https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/

### Core Simulation Principles ###
In this ship simulation, the ships are in constant motion, and so I call the UAV planning twice. The first call is based upon the the current ship positions. This returns an initial assumed sequence. The problem is then predicted forward using UAV travel speed, to make a first order prediction of the ships positions at the UAV arrival, based upon the original sequence.  These revised ship coordinates are used to call into the planning again, to return a possible different order, as a rough order presumed sequence.      

Because the mlrose TSP takes a little while to execute, I have placed this into a Flask based web server, which is called from a separate thread from the main UAV simulation program.   

### Simulation File ###
The simulation of ships is based upon a scenario file: SimpleScenario5.csv.   The csv file is based upon a sequence of events that Create, Update and Delete Ship Tracks. The UAV Always starts, and completes from the Track 00 (Portsmouth Harbour).  The simulation file also includes the simulation times to Generate a Plan "PLAN", and When to Start the UAV Simulation "STARTUAV". The Scenario file is read into the simulation through pandas.  

![picture alt](https://github.com/JulesVerny/GeneticUAVPlanning/blob/master/ScenarioFileImage.PNG "Scenario File")

Note the Simulation has to Halt, waiting upon Planning Thread to complete the Plan generation response, before it can continue to perform the UAV simulation.  
The UAV Travels through the planned sequence, chasing the current ship positions. Each Ship is then marked Green, once it has been inspected.  Please note that some Ship Tracks are created, and some deleted post mission planning, and so some ships are left NOT inspected, and some previous waypoint inspectiosn are skipped, to the next current ship in sequence 
### Conclusions ###
Some rather mixed results with mlrose. The planning does take rather a long time. The routes appear to require around 200 generations to come up with acceptable results. Ypu can experimentby adjusting the mlrose.TSP parameters within the MPWebServer (Line 62) which will change the speed and performance of the proposed plans. 

I will probably investigate the development of my own genetic algorithms in an attempt to speed up the plan generation execution, and observe if there are any differences in performances over the mlrose package. 

However through googling TSP with Python I also discovered a Eric Phanson page on solving the TSP through Simulated annealing using ten lines of core pyhton code. Which is pretty imppressive.  I cannot really follow the code, but the code runs fast, and seems to generate delivers pretty robust results. 

![picture alt](https://github.com/JulesVerny/GeneticUAVPlanning/blob/master/TypicalRoute2.PNG "Plan with Anealing")

### Useage ###
Start the Mission Planning Web Server, which inlcudes the calls into mlrose,  is started using:
  * python MPWebServer.py     - This Web Server for the mlrose based Genetic Algorithm
  * python MPWebServer2.py    - This web server for the 'Ten Lines of Code' simulated annealing method

The main UAV Simulation is then started using:
  * python UAV_Scenario.py

The following files are required to run the UAV Simulation
* MPWebServer.py     : This is the Mission Planning Web Server using mlrose Genetic Algorithm methods. It accepts the JSON based coordinates, and makes calls into the core mlrose TSP algorithms. It is based upon Flask web server and Json processing
* MPWebServer2.py     : This is the Mission Planning Web Server using simulated annealing method. It accepts the same JSON based coordinates, and makes calls into the a simulated annealing method for solving TSP algorithms. 
* UAV_Scenario.py  : This is the main simulaiton script.  It coordinates the main simulation by reading the csv based scenario filw and scheduling the simulation events. This scripot uses Threading to Seperate the Mission Planning Thread upon  a "PLAN" event, but then has to Join (or Wait) upon that Thread before it can process the "START UAV" event
* TacticalPicture.py   : This is a Tactical picture graphics, based upon pygame. It maintains a list of ship Tracks. 
* RoutePlanning.py  : This script processes Tactical Picture Ship Tracks and prepares the Json based coordinates payload and calls into the Mission Planning Web Server
* Track.py  : An Entity class to represent each ship Track
* SimpleScenario5.csv  : This csv file sets up the simulation sequence. Track 00 needs to be creatd first, and all following simulation events in chronological simlaiton time order. Please note the speed of UAV to execute through the plan. This file is read by UAV_Scenario.py at line 36, if an alternative file is to be used 

Press Escape in pygame window to halt the siumlation, at any time.

### Main Python Package Dependencies ###
mlrose, pygame, flask, numpy, pandas,copy,  matplotlib, requests

### Acknowledgments: ###
Genevieve Hayes:  Solving Travelling Salesperson Problems with Python: 

https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847

Eric Phanson: Solving the TSP in Ten Lines of code:

https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/

