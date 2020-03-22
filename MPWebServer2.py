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
# Note this variant uses an alternative TSP solver - using simulated annealing  
#  https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
#  Solves the Travelling Salesman Problem (TSP) through  simulated annealing (In ten Lines of Code !)
# ========================================================================
from flask import Flask, render_template, request,jsonify,json
import random, math, copy
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
	
	if('coordinates' in req_data):						# To protect against Empty arguments
		ReqCoordinateList = req_data['coordinates']		# Coordinate list is enlcosed by the 'coordinates' element
  
		print("Processing the following Mission Planning Coordinate List Request:")
		for Accord in ReqCoordinateList:
			print("[ ", Accord["xcoord"], " , " , Accord["ycoord"], " ]") 
			CoordinatesList.append([Accord["xcoord"], Accord["ycoord"]])    # Note arrange as [List of [x,y]] instead of tuples
		# =================== 	
		cities = CoordinatesList
		NumberOfCities = len(cities)
		# ==================================		
		# Main TSP Anenealing Method in tens Lines of Code
		# And I really do not pretend to undestand this code
		# See https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/  for an attempted explanation !
		tour = random.sample(range(NumberOfCities),NumberOfCities);
		for temperature in np.logspace(0,5,num=100000)[::-1]:
			[i,j] = sorted(random.sample(range(NumberOfCities),2))
			newTour =  tour[:i] + tour[j:j+1] +  tour[i+1:j] + tour[i:i+1] + tour[j+1:]
			if math.exp( ( sum([ math.sqrt(sum([(cities[tour[(k+1) % NumberOfCities]][d] - cities[tour[k % NumberOfCities]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]]) - sum([math.sqrt(sum([(cities[newTour[(k+1) % NumberOfCities]][d] - cities[newTour[k % NumberOfCities]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])) / temperature) > random.random():
				tour = copy.copy(newTour)

		BestSequence = [tour[i % NumberOfCities] for i in range(NumberOfCities+1)]
		BestSequenceNP = np.array(BestSequence[:-1])
		print("Best Sequence: ", BestSequenceNP)
		# ======================
		# Now Rotate the numpy BestSequence order to start at First Coordinate	
		ZeroIndex =   np.where(BestSequenceNP==0)[0]			# Find the Index of Item= 0, only need the fisrt element
		OptimisedSequence = np.roll(BestSequenceNP,-ZeroIndex) # Rotate the numpy array unsing the numpy roll method
		
		# Now Convert the Opimisised Sequence to a List to allow Jsonfiy to serialise the return 
		RtnSequence = OptimisedSequence.tolist()
		print("Completed Processing Optimal Route: ", OptimisedSequence)
		BestFitness = 0.0
	print()
	return jsonify({'result':'Success!','routeorder':RtnSequence,'bestfit':BestFitness})
# ========================================================================
# Main method to Start the Web Server - avoids setting up Environment variables
if __name__ == "__main__":
	app.run(debug=True,port = 7070)			# Note set to Debug to avoid having to restart the python Web App Server upon changs