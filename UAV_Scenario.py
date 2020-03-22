#
#  Experimeting with UAV Surveaillance Routing
# 
#  requires pygame, numpy, matplotlib, 
# ==========================================================================================
import TacticalPicture # The LPD Dispays 
import Track
import numpy as np 
import random 
import pandas as pd
import RoutePlanning
import threading
# =======================================================================
# Track Types
REF = 0
SHIP = 1
UAV = 2

# Evenmt Types
CREATE = 1
UPDATE = 2
DELETE = 3

TOTAL_SIM_TIME = 2250
# =======================================================================

# Main Experiment Method 
def RunSimulation():
	GameTime = 0
    
	GameHistory = []
	
	# Open Up the Scanrio File and read into data famne
	print("========================================================")
	print("Scenario Details: ") 
	ScenarioDataFrame = pd.read_csv("SimpleScenario5.csv")
	#
	print(ScenarioDataFrame)
	NumberOfScenarioEvents = len(ScenarioDataFrame.index)
	print("Number of Scanrio Events: ", NumberOfScenarioEvents)
	NextScenarioEvent = 0
	TrackCreateCount = 0	
		
	#Create te Tactical Picture
	TPC = TacticalPicture.LPDDisplay()
		
	# Create a Route Planner
	TheRoutePlanner = RoutePlanning.RoutePlanner()
  	
	ScenarioQuit = False
	ScenarioTime = 0
    # =================================================================
	#Main Experiment Loop 
	while ((ScenarioTime< TOTAL_SIM_TIME) and (not ScenarioQuit)):    
			
		# Review Events from ScenarioDataFrame
		NextScenarioRow = ScenarioDataFrame.loc[NextScenarioEvent,:]
		if(ScenarioTime==NextScenarioRow['time']):
			# Process the Scenario Event
			# ========================================			
			if(NextScenarioRow["event"] == "CREATE"):
				if(NextScenarioRow["object"]=="SHIP"):
					NewTrack = Track.Track(int(NextScenarioRow["tn"]),NextScenarioRow["xpos"], NextScenarioRow["ypos"], NextScenarioRow["xvel"],NextScenarioRow["yvel"], SHIP)
					TPC.CreateTrack(ScenarioTime,NewTrack)
				if(NextScenarioRow["object"]=="REF"):
					NewTrack = Track.Track(int(NextScenarioRow["tn"]),NextScenarioRow["xpos"], NextScenarioRow["ypos"], NextScenarioRow["xvel"],NextScenarioRow["yvel"], REF)
					TPC.CreateTrack(ScenarioTime,NewTrack)
							
			if(NextScenarioRow["event"] == "UPDATE"):	
				UpdatedTN = int(NextScenarioRow["tn"])
				TPC.UpdateTrackVelocity(ScenarioTime,UpdatedTN,NextScenarioRow["xvel"],NextScenarioRow["yvel"])
			
			if(NextScenarioRow["event"] == "DELETE"):	
				DeletedTN = int(NextScenarioRow["tn"])
				TPC.DeleteTrack(ScenarioTime,DeletedTN)
			
			# ========================================
			if(NextScenarioRow["event"] == "PLAN"):
				print("====================================")
				print("Generating the Plan")
			
				# Generate the UAV Plan  in a Seperate Thread
				PlanningThread = threading.Thread(target = TheRoutePlanner.PlanRoute,args=(TPC.DisplayTracksList,))   # Need to Pass Parameters through an args list
				
				PlanningThread.start()
			# =========================================
			if(NextScenarioRow["event"] == "STARTUAV"):
						
				# Wait for the Planning Thread to Complete ? 
				PlanningThread.join()
				
				if(TheRoutePlanner.LatestPlan is not None):
					# Plot the Route Sequence
					TPC.DrawRouteSequence(TheRoutePlanner.PlanSequenceByTN)
			
					# Now Start UAV Against the Revised Sequence
					TPC.InitialiseUAV(ScenarioTime,TheRoutePlanner.PlanSequenceByTN)
					
			# ===========================================================
					
			if(NextScenarioEvent < NumberOfScenarioEvents-1):
				NextScenarioEvent = NextScenarioEvent+1

		# ================================================================
		#  TPC Update CDisplay ycle
		ScenarioQuit = TPC.UpdateDisplay(ScenarioTime)
		
		# ====================================================
		
		#if GameTime % 200 == 0:
		#	print("Game Time: ", GameTime,"  Game Score: ", "{0:.2f}".format(ReturnScore), )
		#	GameHistory.append((GameTime,ReturnScore))
		ScenarioTime = ScenarioTime+1

	# =============================================================
	# Wait and Cleanup
	print(" =====  End of Simulation :  press ENTER to Exit    =======")
	dog = input()
	TPC.Closedown()
	
	# =======================================================================
def main():
    #
	# Main Method Just Play our Experiment
	
	RunSimulation()
	print("========================================================")
	print()
	# =======================================================================
if __name__ == "__main__":
    main()
