import ibmiotf.application
import ibmiotf.device
import random
import json
import time
import sys
#Provide your IBM Watson Device Credentials
organization = "emnnr1"
deviceType = "ESP32"
deviceId = "12345"
authMethod = "token"
authToken = "12345678"


# Initialize the device client.
T=0
H=0

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='playmusic':
                print("PLAY MUSIC IS RECEIVED")
               
               
        elif cmd.data['command']=='rotatetoys':
                print("ROTATE TOYS IS RECEIVED")

       
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
 deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
 deviceCli = ibmiotf.device.Client(deviceOptions)
#..............................................

except Exception as e:
 print("Caught exception connecting device: %s" % str(e))
 sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        temp=random.randint(0,100)
        babyGood = 'Fine'
        babycry = 'baby is crying do something'
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'Temperature':temp, 'BabyGood' : babyGood,  'Babycry' : babycry }}
        #print (data)
        def myOnPublishCallback():
            print (data)

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
       
        deviceCli.commandCallback = myCommandCallback
        time.sleep(5)

# Disconnect the device and application from the cloud
deviceCli.disconnect()
