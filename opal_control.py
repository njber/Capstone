# By Nick Berriman
# Opal Network Control System
# This file is designed to work with the Opal Simulators
# This example is a load node. it is provided with a voltage and then
# sends back a current draw to the main system
# Requirements
# dependencies
from signal import signal, SIGINT
import subprocess
import RtlabApi
import time
import sys
from pprint import pprint
import json
from time import sleep
import asyncio
import websockets
import pathlib
import csv

#################################################################################
#### Global Variables

#Remote Server
uri = "ws://server.alastairbate.me:8080" #<"ws://server.alastairbate.me:8080"

#Insert the location of the project's llp file here. E.g.
C:/Users/Opal/Project/Prokect.llp #<
projectName = "C:/Users/Alastair/UTS/Grid Simulator Capstone 2020 - Documents/Final Products/Bus2.1-2018B/Capstone-Final-VoltageBus2.llp" #<INSERT PROJECT INFO

# Allocate this simulation node a number between 0 and 3 as worked out mutally with
other nodes
BusNumber = 2
# The following come from the file system config folder in workspace/models/ (((themodel we are working on ))) / Opcommon
# rtdemo1.param

# Before filling in the following variables you need to have Built, loaded and preferably test executed the model using Rtlab
# You need to provide this program with the signals you want to share with other nodes, and the

#In this example the current meansurement is the signal that will be provided backto the server 

SignalToSend = 'basic_example1/sm_computation/Bus2Voltage/do not delete this gain/port1' #read i.e. local value to sendo
CurrentSignalToSend = 'basic_example1/sm_computation/SharedCurrent/do not delete this gain/port1'

#in this example the voltage is what is needed to do the calculations and is provided into the system with this param
ParameterToControl1 = 'basic_example1/sm_computation/Bus1injectVoltage/Gain'
#control i.e. remote value
# ParameterToControl2 = 'acquisition1/sc_user_interface/port1' #control i.e. remotevalue
# ParameterToControl3 = 'acquisition1/sc_user_interface/port1' #control i.e. remotevalue

# To use more than one external input, also uncomment the code in the asyncio loop
#################################################################################
# Do not change anything below this line except when adding extra inputs
lastSendTime = time.time()
Data = []

def handler(signal_received, frame):
 RtlabApi.CloseProject()
 with open('data.csv',mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(["bus1SharedCurrent","bus1Voltage","bus2SharedCurrent","bus2Voltage","current Time","bus1Time","bus2Time","Full Update Time"])
    for line in Data:
        print(line)
    for line in Data:
        csv_writer.writerow(line)
    sys.exit(0)

signal(SIGINT,handler)
RtlabApi.OpenProject(projectName)

realTimeMode = RtlabApi.SOFT_SIM_MODE
RtlabApi.Load(realTimeMode,1)
print("The Model is Loaded")

RtlabApi.Execute(1)
print("The model is running")

# Get control
print('get control')
RtlabApi.GetSystemControl(1)
RtlabApi.GetAcquisitionControl(1)
RtlabApi.GetParameterControl(1)
RtlabApi.GetSignalControl(1)
print('got control')
print('running')

#-----------------------------------------
# Loop to send data to Server
#-----------------------------------------
while True:
    async def updateValues():
        async with websockets.connect(uri) as websocket:
            busData = {"instr":"Opal", "BusNumber": BusNumber, "BusValue":
RtlabApi.GetSignalsByName(SignalToSend),
"currentValue":RtlabApi.GetSignalsByName(CurrentSignalToSend),
"time":str(time.time())}
    await websocket.send(json.dumps(busData))
    Update = json.loads(await websocket.recv())
    RtlabApi.SetParametersByName(ParameterToControl1, float(Update["bus1"])) #update bus 0
    # RtlabApi.SetParameterByName(ParameterToControl2, float(Update["bus3"])) #update bus 0 # Uncomment to use
    # RtlabApi.SetParameterByName(ParameterToControl3, float(Update["bus4"])) #update bus 0 # Uncomment to use

Data.append([Update["bus1SharedCurrent"],Update["bus1"],Update["bus2SharedCurrent"],Update["bus2"],time.time(),Update["bus1UpdateTime"],Update["bus2UpdateTime"],(time.time()-float(Update["bus2UpdateTime"]))])
    asyncio.get_event_loop().run_until_complete(updateValues())