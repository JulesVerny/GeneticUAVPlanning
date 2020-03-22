#
#  Route Planning
# Now Makes a Web Service call to MPWebServer (Which implements the mlrose based Mission Planning 
# pip install mlrose
# https://towardsdatascience.com/solving-travelling-salesperson-problems-with-python-5de7e883d847
#
# ============================================================================================
import mlrose 
import numpy as np 
import Track
#from collections import deque
import math
import matplotlib.pyplot as plt 
import requests
import json
# ===========================================================================================================
#  Some Constants
UAVSPEED = 4.0     # NOTE Actual Simulaiton inTactical Pictrue so ensure SAME

# ==================================================================================
# Sanity Check	Plotter
def PlotSequence(CoordinateList,OptimisedSequence):
	XPoints = []
	YPoints = []
	for EachItem in OptimisedSequence:
		xpt,ypt = CoordinateList[EachItem]
		XPoints.append(xpt)
		YPoints.append(ypt)

	plt.scatter(XPoints,YPoints)
	plt.plot(XPoints,YPoints)
	plt.show()
			
# =========================================================================
def CreateCoordinatesDict(CoordList):
	CoordDictList = []					# Retrun is a List of dict ('xcoord': xvalue, 'ycoord':yvalue) items 
	for (xpt,ypt) in CoordList:
		CoordDictItem = {}
		CoordDictItem['xcoord'] = xpt
		CoordDictItem['ycoord'] = ypt
		CoordDictList.append(CoordDictItem)
	return CoordDictList
# ====================================================================
# Route Planner Tasks
class RoutePlanner:
	def __init__(self):
	
		# Initialise Planer 				
		self.LatestPlan = None  # The Best Plan 
		self.PlanSequenceByTN = []		# Plan Sequcne By TNs	
	# ==================================================================================
	def OptimiseRoute(self, CoordinateList):
	
		# Create the JSON Coordinats list
		JSONDict = CreateCoordinatesDict(CoordinateList)
		
		#print("The JSON Request Dict: ", type(JSONDict)) 
		#print(JSONDict)
	
		# Now Set up a Web Call to the MP Web Server
		url = 'http://localhost:7070/process'
		Response = requests.post(url, json={'coordinates':JSONDict})			# Feed json web request with top level JSON element : 'coordinates' 
			
		OptimisedSequence = []
		BestFitness = -1.0
		if Response.status_code != 200:
			print("Web ERROR : " + str(Response.status_code))
		else:
			JsonResponse = Response.json()
			#print(JsonResponse['result'])
			#print(JsonResponse['routeorder'])
			#print(JsonResponse['bestfit'])	
			OptimisedSequence = JsonResponse['routeorder']
			BestFitness = JsonResponse['bestfit']
				
		return OptimisedSequence,BestFitness	
	# ==================================================================================
	def CalculateInitialBestRoute(self, TrackPositionsList):
		# Calculate the Route Sequence  from TrackPositionsList
		CoordinatesList = []
		
		for EachTrack in  TrackPositionsList:
			CoordinatesList.append((EachTrack.Xpos, EachTrack.Ypos))
		
		BestSequence,BestFitness = self.OptimiseRoute(CoordinatesList)
	
		# Sanity Check	Plot
		#PlotSequence(CoordinatesList,BestSequence)
	
		return BestSequence,BestFitness	
	# ============================================================================
    #  Revised Route Calculation  based upon Projected Track Positions 
	def RevisedRouteReview(self,InitialSequence,CurrentTrackPositionsList):
		AccumulatedTime = 0	
		NewCoordinateList = []
		
		# Add the First WayPoint Postion as Not disputed
		ZeroTrack = CurrentTrackPositionsList[InitialSequence[0]]
		NewCoordinateList.append((ZeroTrack.Xpos, ZeroTrack.Ypos))
	
		for NextLeg in range(1,len(InitialSequence)):
			CurrentTrack = CurrentTrackPositionsList[InitialSequence[NextLeg-1]]
			NextTrack = CurrentTrackPositionsList[InitialSequence[NextLeg]]
			# Project Forward the Track Positions accordmg to the running Accumulated Time
			ProjectedCurrentTrackXPos, ProjectedCurrentTrackYPos =  CurrentTrack.Xpos + float(AccumulatedTime)*(CurrentTrack.Xvel), CurrentTrack.Ypos + float(AccumulatedTime)*(CurrentTrack.Yvel)
			ProjectedNextTrackXPos, ProjectedNextTrackYPos =  NextTrack.Xpos + float(AccumulatedTime)*(NextTrack.Xvel), NextTrack.Ypos + float(AccumulatedTime)*(NextTrack.Yvel)
					
			DeltaX,DeltaY = ProjectedNextTrackXPos -ProjectedCurrentTrackXPos, ProjectedNextTrackYPos -ProjectedCurrentTrackYPos
			DeltaDistance =  math.sqrt(DeltaX*DeltaX + DeltaY*DeltaY)
			DeltaTime = DeltaDistance/UAVSPEED
			AccumulatedTime = AccumulatedTime + int(DeltaTime)

			# Re project the Next Track Position with Revised Accumulatd Time
			ProjectedNextTrackXPos, ProjectedNextTrackYPos =  NextTrack.Xpos + float(AccumulatedTime)*(NextTrack.Xvel), NextTrack.Ypos + float(AccumulatedTime)*(NextTrack.Yvel)

			# Now Add into the Revised Coordnates Collection
			NewCoordinateList.append((ProjectedNextTrackXPos, ProjectedNextTrackYPos))
						
		# Now Rerun the Basic TSP Optimisaiton against the Revised List
		RevisedSequence,BestFitness = self.OptimiseRoute(NewCoordinateList)
		
		# Sanity Check	Plot
		#PlotSequence(NewCoordinateList,RevisedSequence)
		
		# NOTE that the Revised Sequecne IS ORDERED by Initial Sequence list ORDER NOT same as TPC Track 
		TListOrder = []
		for EachRevSeqItem in RevisedSequence:
			TListOrder.append(InitialSequence[EachRevSeqItem])
		
		return TListOrder,BestFitness
		
	# ==========================================================================================
	#  General Plan - and RePlan
	def PlanRoute(self, TrackList):
		self.PlanSequenceByTN.clear()
		# Initial Calculations
		BestSequence,BestFitness = self.CalculateInitialBestRoute(TrackList)
		# Recalculated
		RevisedSequence,BestFitness= self.RevisedRouteReview(BestSequence,TrackList)
		for RouteItem in RevisedSequence:
			#print(TrackList[RouteItem].TN)
			self.PlanSequenceByTN.append(TrackList[RouteItem].TN)

		print()
		print(" Planned Route Sequence: ",  self.PlanSequenceByTN)
		print()		
		self.LatestPlan = RevisedSequence

	# ==========================================================================================