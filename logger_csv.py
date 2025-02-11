import csv
from datetime import datetime
from time import sleep
import os.path
import boto3

class Logger:
	# constructor
	def __init__(self):
		self.headerList=[]
		self.rowList=[]
		self.file_name = "/home/leaf/strawberry-plant-lysimeter-capstone/sensor_data.csv"
		self.bucket_name = "strawberry-lysimeter-data"
	
	# collect the data into the dictionary
	def collect_data(self, name, variable):
		''' collect data and assign to class variable '''
		self.headerList.append(name)
		self.rowList.append(variable)
        
	def log_data_csv(self):
		''' log the data into csv files '''		
		if os.path.isfile(self.file_name):
			with open(self.file_name, 'a+', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(self.rowList)
		else:
			with open(self.file_name, mode='w', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(self.headerList)
				writer.writerow(self.rowList)
				
		self.headerList=[]
		self.rowList=[]
	
	# add the csv file into the aws server
	def add_server(self):
		s3 = boto3.client('s3')
		s3.upload_file(self.file_name, self.bucket_name, "sensor_data.csv")
		print(f"Uploaded {self.file_name} to {self.bucket_name}")
		
	'''
	# the file names are named per day
	def get_file_name(self):
		file_name = self.file_name.split('.')
		file_name = file_name[0] + "{:%B_%d_%Y}".format(datetime.now()) "." + file_name[1]
		
		return file_name
	'''
	
