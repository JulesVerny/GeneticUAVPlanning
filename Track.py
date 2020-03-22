#  A Simple Track Type class
import numpy as np 
# =========================================================================
# Track Types
REF = 0
SHIP = 1
UAV = 2

class Track:
	def __init__(self,NewTN, InitialXpos, InitialYpos, InitialXVel,InitialYVel,TrackType):
		self.TN = NewTN
		self.Xpos = InitialXpos
		self.Ypos = InitialYpos
		self.Xvel = InitialXVel
		self.Yvel = InitialYVel		
		self.Type = TrackType
		self.Observed = False
		
    #  Revise Track Velocity
	def ChangeVelocity(self, NewXVel,NewYVel):
		self.Xvel = NewXVel
		self.Yvel = NewYVel	

	#  Update Track Position
	def UpdatePosition(self,):
		self.Xpos = self.Xpos + self.Xvel
		self.Ypos = self.Ypos + self.Yvel	
	
	def SetObserved(self,):
		self.Observed = True
	
	def SetNoneObserved(self,):
		self.Observed = False