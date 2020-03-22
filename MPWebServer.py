# Python Web Servcie using Flask  - handling Query Request and Posts
# https://www.youtube.com/watch?v=hAEJajltHxc
#
#  To Prcess a Coordinate List  into a Schedule order
#  Input
#  {
#	    "coordinates" : [
#			   {
#              "xcoord": "xvalue",
#			   "ycoord": "yvalue"
#			    },
#			   {
#              "xcoord": "xvalue",
#			   "ycoord": "yvalue"
#			    },
#			   {
#              "xcoord": "xvalue",
#			   "ycoord": "yvalue"
#			    },
#			   {
#              "xcoord": "xvalue",
#			   "ycoord": "yvalue"
#			    }
#			]
#	}
#
# ========================================================================
# JSOn processing - Need to use Postman App to send Json and review 
#  See https://www.youtube.com/watch?v=kvux1SiRIJQ
# ============================================================================== 
from flask import Flask, render_template, request,jsonify,json
import mlrose 
import numpy as np 
# ==================================================================
app = Flask(__name__)
# ========================================================================
# JSOn processing - Need to use Postman App to send Json and review 
@app.route("/process",methods=['POST'])
def process_coordinate_list():
	ReqCoordinateList = None
	CoordinatesList = []
	BestSequence = []
	
	req_data = request.get_json()		# Note the req data (json list) is ALREADY in python dictionary format

	print()
	#print(" Processing  JSON CoorinstaesList: ", type(req_data)) 
	#print(req_data)
	#print()
	if('coordinates' in req_data):						# To protect against Empty arguments
		ReqCoordinateList = req_data['coordinates']		# Coordinate list is enlcosed by the 'coordinates' element
  
		print("Processing the following Mission Planning Coordinate List Request:")
		for Accord in ReqCoordinateList:
			print("[ ", Accord["xcoord"], " , " , Accord["ycoord"], " ]") 
			CoordinatesList.append((Accord["xcoord"], Accord["ycoord"]))

		# =================== 
		# The core main mlrose based processing code
		Fitness_Coordinates = mlrose.TravellingSales(coords = CoordinatesList)
		ProblemFit = mlrose.TSPOpt(length = len(CoordinatesList),fitness_fn = Fitness_Coordinates,maximize = False)		
		BestSequence,BestFitness = mlrose.genetic_alg(ProblemFit, mutation_prob=0.33, max_attempts=175,random_state =4)   #  Was Mux prob 0.33, Max Attempts 125
		# ======================
		# Now Rotate the numpy BestSequence order to start at First Coordinate	
		ZeroIndex =   np.where(BestSequence==0)[0]			# Find the Index of Item= 0, only need the fisrt element
		OptimisedSequence = np.roll(BestSequence,-ZeroIndex) # Rotate the numpy array unsing the numpy roll method
		
		# Now Convert the Opimisised Sequence to a List to allow Jsonfiy to serialise the return 
		RtnSequence = OptimisedSequence.tolist()
		print("Completed Processing Optimal Route: ", OptimisedSequence)
		
	print()
	return jsonify({'result':'Success!','routeorder':RtnSequence,'bestfit':BestFitness})
# ========================================================================
# Main method to Start the Web Server - avoids setting up Environment variables
if __name__ == "__main__":
	app.run(debug=True,port = 7070)			# Note set to Debug to avoid having to restart the python Web App Server upon changs