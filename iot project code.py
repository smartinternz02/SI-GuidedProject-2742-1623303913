from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result
from cloudant.result import Result, ResultByKey

import datetime
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import cv2
import numpy as np
import sys
import ibmiotf.application
import ibmiotf.device
import random
import time

#Provide your IBM Watson Device Credentials
organization = "qkrfgv"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"



def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(cmd.data['command'])
       
        if(cmd.data['command']=="rotatetoys"):
                print("Rotate Toys")
                
        if(cmd.data['command']=="playmusic"):
                print("Play Music")
                

        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# IBM Cloudant Legacy authentication
client = Cloudant("apikey-v2-5jk8pfubd1yc1rgkyaol6aadz67jj9y6zwsvoaqoeuw", "533d636dbf1f1af287084765af2385ae",
                  url="https://apikey-v2-5jk8pfubd1yc1rgkyaol6aadz67jj9y6zwsvoaqoeuw:533d636dbf1f1af287084765af2385ae@18f2cb94-c45a-4276-b31d-702c0306bcb0-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()

database_name = "babycare"

my_database = client.create_database(database_name)

if my_database.exists():
    print(f"'{database_name}' successfully created.")
    json_document = {
                    "_id": "1001",
                    "name":"kavya"
                    }
    new_document = my_database.create_document(json_document)
    if new_document.exists():
        print("Document '{new_document}' successfully created.")

result_collection = Result(my_database.all_docs, include_docs=True)
# Get the result for matching a key
result = result_collection['1001']  #search by id, if id=1001   

print("---------------")
print("the data with id =1001 is")
print (result)
print("---------------")
# Iterate over the result collection
for result in result_collection:
    print(result)# it will print all the records

# First retrieve the document
for document in my_database:
    my_document = my_database['1001'] 

# Update the document content
# This can be done as you would any other dictionary
my_document['babyGood'] = 'Fine'
my_document['babyCry'] = 'RotateToys'
my_document['babycru'] = 'playMusic'

# You must save the document in order to update it on the database
my_document.save()

result_collection = Result(my_database.all_docs, include_docs=True)
# Get the result for matching a key
result = result_collection['1001']     
# Iterate over the result collection
print (result)


