from mrjob.job import MRJob
import pandas as pd 
from math import sin, cos, sqrt, atan2, radians
import sys
from sklearn.cluster import KMeans
import numpy as np
import csv


class MRcount(MRJob):

	def mapper_init(self):

		self.sample = pd.read_csv('sample_trip.csv')
		self.coordinates = self.sample[["pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude"]]
		self.coordinates1 = self.coordinates[["pickup_longitude","pickup_latitude"]]
		self.coordinates2 = self.coordinates[["dropoff_longitude","dropoff_latitude"]]
		self.coordinate_array1 = np.array(self.coordinates1)
		self.coordinate_array2 = np.array(self.coordinates2)
		self.kmeans1 = KMeans(n_clusters= 100, random_state=0).fit(self.coordinate_array1)
		# self.kmeans2 = KMeans(n_clusters= 50, random_state=0).fit(self.coordinate_array2)


	def mapper(self, _, line):

		row = next(csv.reader([line]))
		if (len(row) > 0) and (row[1] != 'VendorID'):
			try:
				pick_lon = float(row[6])
				pick_lat = float(row[7])
				drop_lon = float(row[10])
				drop_lat = float(row[11])

				pick_clus = self.kmeans1.predict(np.array([pick_lon, pick_lat]).reshape(1,-1))[0]
				drop_clus = self.kmeans1.predict(np.array([drop_lon, drop_lat]).reshape(1,-1))[0] 

				key = (int(pick_clus), int(drop_clus))
				yield key, 1
			except:
				key = None

		

	def combiner(self, key, vals):
		
		value = sum(vals)
		yield key, value

	def reducer(self, key, vals):

		value = sum(vals)
		if value >= 5:
			yield key, value

if __name__ == '__main__':
	MRcount.run()




