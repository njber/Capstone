#!/usr/bin/env python
# websockets server for Opal
import asyncio
import websockets
import json
import subprocess
from time import sleep
import time
# voltage, time, current
CurrentBusValues = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
async def update(websocket, path):
    update = json.loads(await websocket.recv())
    # print(update)
    if update['instr'] == "request_data":
        updateValue = [CurrentBusValues[0][0], CurrentBusValues[1][0],
        CurrentBusValues[2][0],CurrentBusValues[3][0],CurrentBusValues[0][2],
        CurrentBusValues[1][2],CurrentBusValues[2][2],CurrentBusValueBusValues[3][0]]
        await websocket.send(json.dumps(updateValue))
        print(CurrentBusValues)
    else:
        CurrentBusValues[update["BusNumber"]-1][0] = update["BusValue"]
        CurrentBusValues[update["BusNumber"]-1][1] = update["time"]
        CurrentBusValues[update["BusNumber"]-1][2] = update["currentValue"]
        await websocket.send(json.dumps({"bus1": CurrentBusValues[0][0],
        "bus1UpdateTime":CurrentBusValues[0][1],
        "bus1SharedCurrent":CurrentBusValues[0][2], "bus2": CurrentBusValues[1][0],
        "bus2UpdateTime":CurrentBusValues[1][1],
        "bus2SharedCurrent":CurrentBusValues[0][2]}))
        print(CurrentBusValues)
start_server = websockets.serve(update, "0.0.0.0", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
