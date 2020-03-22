#
#  A Tactical Picture Processing  Class 
# ============================================================================================
import pygame 
import random 
import Track
import math
# ===========================================================================================================
#frame rate per second
FPS = 20	#  Experiment Performance Seems rather sensitive to Computer performance  

#size of our window
SCREENWIDTH = 1000
SCREENHEIGHT = 800

TRACK_WIDTH = 10
UAVWIDTH = 20

REF = 0
SHIP = 1
UAV = 2

#RGB colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

UAVSPEED = 4.0
UAVINSPECTTHRESHHOLD = 50.0
# ==========================================================================================
#initialize our screen using width and height vars
pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('UAV Planning Scenario')

TranspaprentSurface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
TranspaprentSurface.set_colorkey((0,0,0))
TranspaprentSurface.set_alpha(20)
# ===============================================================
def UAVSpeedToNextWaypoint(CurrentX, CurrentY, NextX,NextY):
	DeltaX = NextX-CurrentX
	DeltaY = NextY-CurrentY
	
	Magnitude = math.sqrt(DeltaX*DeltaX + DeltaY*DeltaY)
	VelX = UAVSPEED*DeltaX/Magnitude
	VelY = UAVSPEED*DeltaY/Magnitude
	return VelX, VelY

# Track Display
# =========================================================================
#game class
class LPDDisplay:
	def __init__(self):
	
		# Initialise pygame paramters				
		self.MainGameFont = pygame.font.SysFont("calibri",20)
	
		self.DisplayTracksList = []			
		self.GTimeDisplay = 0
		self.DisplayedRoute = []
		self.UAVPosX = 0.0
		self.UAVPosY = 0.0
		self.UAVRunning = False
		self.UAVXVel = 0.0
		self.UAVYVel = 0.0
		self.UAVPlannedRouteSequenceByTN = []
		self.UAVNextWayPointTNListId = 1
		self.ActualRouteSequence = []
		
	# =====================================================================================
	def CreateTrack(self,Time,NewTrack):
		self.DisplayTracksList.append(NewTrack)
		print(str(Time), ": ", NewTrack.TN, " Type: ", NewTrack.Type, " Created Event")	

	def UpdateTrackVelocity(self,Time,UpdatedTN,NewXVel,NewYVel):
		# Find the CorrespondingInstance
		for i in range (0,len(self.DisplayTracksList)):
			if(self.DisplayTracksList[i].TN == UpdatedTN):
				self.DisplayTracksList[i].ChangeVelocity(NewXVel,NewYVel)
				print(str(Time), ": ", UpdatedTN, " Velocity Updated Event")				
		
		
	def DeleteTrack(self,Time,DeletedTN):
		# Find the CorrespondingInstance
		ItemToDelete = -1
		for i in range (0,len(self.DisplayTracksList)):
			if(self.DisplayTracksList[i].TN == DeletedTN):
				ItemToDelete = i			
		
		if(ItemToDelete>-1):
			del self.DisplayTracksList[ItemToDelete] 
			print(str(Time), ": ", DeletedTN, " Deleted Event")	

	# ============================================================================
	def GetTrackInstanceByTN(self,TrackNumber):
		# Find the CorrespondingInstance
		FoundInstance = -1
		for i in range (0,len(self.DisplayTracksList)):
			if(self.DisplayTracksList[i].TN == TrackNumber):
				FoundInstance = i	
		return FoundInstance
	# ================================================================================
	def FindNextValidInstance(self, PlanSequence, TrackNumber, ExpectedLoc):
		# Attempt to Find By TN
		FoundInstance = self.GetTrackInstanceByTN(TrackNumber)
		NextLoc = ExpectedLoc
		while(FoundInstance<0):
			NextLoc = NextLoc +1
			if(NextLoc == len(PlanSequence)):
				NextLoc = 0
			NextTN = PlanSequence[NextLoc]
			FoundInstance = self.GetTrackInstanceByTN(NextTN)
			
		return FoundInstance
	# =====================================================================================
	def InitialiseUAV(self,Time,ProposedRouteSequenceByTN):
	
		# Perform  Copy, as suspect ProposedRouteSequenceByTN is manipulatd by Refrence in another Thread
		self.UAVPlannedRouteSequenceByTN.clear()
		for PlanItem in ProposedRouteSequenceByTN:
			self.UAVPlannedRouteSequenceByTN.append(PlanItem)
	
		for EachTrack in self.DisplayTracksList:
			EachTrack.SetNoneObserved()
	
		#InitialTrackReference = self.FindNextValidInstance(self.UAVPlannedRouteSequenceByTN,self.UAVPlannedRouteSequenceByTN[0],0)	# Shoudl be OK as Plan starts at Ship 0, never deleted, awlays exists

		self.UAVPosX = self.DisplayTracksList[0].Xpos  
		self.UAVPosY = self.DisplayTracksList[0].Ypos 
		self.UAVNextWayPointTNListId = 1
		self.UAVRunning = True
		
		NextWayPointTrackInstance = self.FindNextValidInstance(self.UAVPlannedRouteSequenceByTN,self.UAVPlannedRouteSequenceByTN[self.UAVNextWayPointTNListId],self.UAVNextWayPointTNListId)	# Shoudl be OK as Plan starts at Ship 0, never deleted, awlays exists

		self.UAVXVel, self.UAVYVel= UAVSpeedToNextWaypoint(self.UAVPosX,self.UAVPosY, self.DisplayTracksList[NextWayPointTrackInstance].Xpos,self.DisplayTracksList[NextWayPointTrackInstance].Ypos)		 		
		print(str(Time), ": UAV Started Plan at :[",  self.UAVPosX, " , ",self.UAVPosY, "]")	
		self.ActualRouteSequence.clear()
		self.ActualRouteSequence.append((self.UAVPosX,self.UAVPosY))

	# ===========================================================================================
	def UpdateAndCheckUAVVelocity(self,Time):
		# Check that the UAV within the Next Track [NextWaypiont]
		self.UAVPosX = self.UAVPosX + self.UAVXVel
		self.UAVPosY = self.UAVPosY + self.UAVYVel	
		
		NextWayPointTrackInstance = self.FindNextValidInstance(self.UAVPlannedRouteSequenceByTN,self.UAVPlannedRouteSequenceByTN[self.UAVNextWayPointTNListId],self.UAVNextWayPointTNListId)	# Tracking Towards next Waypoint Track instance
				
		DistanceToNextTrack = (self.UAVPosX-self.DisplayTracksList[NextWayPointTrackInstance].Xpos)*(self.UAVPosX-self.DisplayTracksList[NextWayPointTrackInstance].Xpos)+ (self.UAVPosY-self.DisplayTracksList[NextWayPointTrackInstance].Ypos)*(self.UAVPosY-self.DisplayTracksList[NextWayPointTrackInstance].Ypos)
		if(DistanceToNextTrack<UAVINSPECTTHRESHHOLD):
			#Reached the next Track so revise Waypoints and Vekocities
			print(str(Time), " UAV  at: [",self.UAVPosX," , ",self.UAVPosY,"] Has Reached TN:", self.DisplayTracksList[NextWayPointTrackInstance].TN)
			self.DisplayTracksList[NextWayPointTrackInstance].SetObserved()
			if(self.DisplayTracksList[NextWayPointTrackInstance].TN==0):		
				self.UAVRunning = False
			if(self.UAVNextWayPointTNListId == (len(self.UAVPlannedRouteSequenceByTN)-1)):
				self.UAVNextWayPointTNListId=0
			else:
				self.UAVNextWayPointTNListId = self.UAVNextWayPointTNListId+1
				
			self.ActualRouteSequence.append((self.UAVPosX,self.UAVPosY))					
			NextWayPointTrackInstance = self.FindNextValidInstance(self.UAVPlannedRouteSequenceByTN,self.UAVPlannedRouteSequenceByTN[self.UAVNextWayPointTNListId],self.UAVNextWayPointTNListId)	# Attempt To Find next WayPoint Track Instance
		
		# Continous Chase down Next Track - assuming that is currenlty being Tracked		
		self.UAVXVel, self.UAVYVel= UAVSpeedToNextWaypoint(self.UAVPosX,self.UAVPosY, self.DisplayTracksList[NextWayPointTrackInstance].Xpos,self.DisplayTracksList[NextWayPointTrackInstance].Ypos)		 		
		
	# ==================================================================================
	def DrawTrack(self, TheTrack):
		# Track Icon is simply a Red Rect
		DisplayTrackItem = pygame.Rect(TheTrack.Xpos-TRACK_WIDTH/2, TheTrack.Ypos-TRACK_WIDTH/2, TRACK_WIDTH, TRACK_WIDTH)
		
		if(TheTrack.Observed):
			pygame.draw.rect(SCREEN, GREEN, DisplayTrackItem)
		else:
			pygame.draw.rect(SCREEN, RED, DisplayTrackItem)
	
		# TN Label
		TNFont = pygame.font.SysFont("calibri",18)
		TNDisplay = TNFont.render(str('{}'.format(TheTrack.TN).zfill(2)), True,RED)
		SCREEN.blit(TNDisplay,(TheTrack.Xpos+8,TheTrack.Ypos-12))
		
		# Need to Draw a Velocity Leader
		if(TheTrack.Type==SHIP):
			VelExtnPoint = TheTrack.Xpos + TheTrack.Xvel*500.0, TheTrack.Ypos + TheTrack.Yvel*500.0 
			pygame.draw.line(SCREEN, RED, (TheTrack.Xpos,TheTrack.Ypos),VelExtnPoint)
	
		# ==================================================================================
	def DrawRouteSequence(self, VisitSequenceByTN):
		# Only Draw Route if at least Pair of Points
		self.DisplayedRoute.clear()
		if(len(VisitSequenceByTN)>1):
			for i in range (0,len(VisitSequenceByTN)):
				TrackInstance1 = self.GetTrackInstanceByTN(VisitSequenceByTN[i])
				if((i+1)<len(VisitSequenceByTN)):
					NextIndex = i+1
				else:
					NextIndex=0
				TrackInstance2 = self.GetTrackInstanceByTN(VisitSequenceByTN[NextIndex])
				
				if((TrackInstance1>-1) and (TrackInstance2>-1)):
					LegStartPoint = int(self.DisplayTracksList[TrackInstance1].Xpos),int(self.DisplayTracksList[TrackInstance1].Ypos)				
					LegEndPoint = int(self.DisplayTracksList[TrackInstance2].Xpos),int(self.DisplayTracksList[TrackInstance2].Ypos)
					#print("Leg : ", str(i), str(LegStartPoint), "  , " , str(LegEndPoint)," ]")
					self.DisplayedRoute.append((LegStartPoint,LegEndPoint))		
					
	# ============================================================================	
	def DrawUAV(self, ):
		# UAV Icon is a Blue Circle
		DisplayUAVItem = pygame.Rect(self.UAVPosX-UAVWIDTH/2, self.UAVPosY-UAVWIDTH/2, UAVWIDTH, UAVWIDTH)
		pygame.draw.ellipse(SCREEN, BLUE, DisplayUAVItem)
		
	# ============================================================================	
	def DrawActualUAVRoute(self,):
		# Only Draw Route if at least Pair of Points
		
		# Need to clear downs the TranspaprentSurface
		TranspaprentSurface.fill((0,0,0))
		
		if(len(self.ActualRouteSequence)>1):
			for Leg in range(0,len(self.ActualRouteSequence)-1):
				(LegX1,LegY1) = self.ActualRouteSequence[Leg]
				(LegX2,LegY2) = self.ActualRouteSequence[Leg+1]			
				RelAngle = math.atan2((LegY2-LegY1),(LegX2-LegX1))	
				F1X, F1Y = LegX1 + UAVWIDTH*math.sin(RelAngle)/2,  LegY1 - UAVWIDTH*math.cos(RelAngle)/2	
				F2X, F2Y = LegX2 + UAVWIDTH*math.sin(RelAngle)/2,  LegY2 - UAVWIDTH*math.cos(RelAngle)/2	
				F3X, F3Y = LegX2 - UAVWIDTH*math.sin(RelAngle)/2,  LegY2 + UAVWIDTH*math.cos(RelAngle)/2
				F4X, F4Y = LegX1 - UAVWIDTH*math.sin(RelAngle)/2,  LegY1 + UAVWIDTH*math.cos(RelAngle)/2
				pygame.draw.polygon(TranspaprentSurface,GREEN,((F1X, F1Y ),(F2X, F2Y ),(F3X, F3Y ),(F4X, F4Y )))
				#Draw the Circle around each Intercept
				IntCircle = pygame.Rect(LegX1-UAVWIDTH/2, LegY1-UAVWIDTH/2, UAVWIDTH, UAVWIDTH)
				pygame.draw.ellipse(TranspaprentSurface,GREEN, IntCircle)
				SCREEN.blit(TranspaprentSurface, (0,0))
				# Draw Circles at each point
		
	# =======================================================================
    #  Display UpdateInlcuding Display
	def UpdateDisplay(self,SimulationTime):
	
		Quit = False	
		# ====================================
		#  Process Keyboard Entry
		KeyPressed = pygame.key.get_pressed()
		if (KeyPressed[pygame.K_ESCAPE]):
			print("Esc pressed")
			Quit = True  			
		pygame.event.pump() # process event queue
		# ===================================
		
		self.GTimeDisplay = SimulationTime
	
		# Display Background map
		bg = pygame.image.load("Solent.png")
		SCREEN.blit(bg,(0,0))
		
		# Updte and Draw all the Tracks
		for TrackItem in self.DisplayTracksList:
			TrackItem.UpdatePosition()
			self.DrawTrack(TrackItem)
		
		if(self.UAVRunning == True):
			# Update and Draw the UAV
			self.UpdateAndCheckUAVVelocity(SimulationTime)
		self.DrawUAV()
				
		# Draw the Displayed Route if it exists
		for (StartPt,EndPoint) in self.DisplayedRoute:
			pygame.draw.line(SCREEN, YELLOW, StartPt,EndPoint)
		
		# Draw Actual Route
		self.DrawActualUAVRoute()
		
		#  Display Game Time
		GameTimeDisplay = self.MainGameFont.render("Sim Time: " + str(self.GTimeDisplay) , True,(255,255,255))
		SCREEN.blit(GameTimeDisplay,(50.,20.))
	
		#Update the PyGame Display
		pygame.display.update()
		FPSCLOCK.tick(FPS)

		return Quit
		# ==========================================================================================
	def Closedown(self):
		pygame.quit()
