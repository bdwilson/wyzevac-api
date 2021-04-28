# 4/2021 - https://github.com/bdwilson/wyzevac-api
#
# sudo apt-get install python3 python3-pip 
# sudo pip3 install flask wyze_sdk
#
# Note: wyze-sdk requires Python 3.9, thus docker is the preferred
# way to run this. 
#
# Set your email, password and port to run this service on.
#
# If you have more than one device on your account, you'll need to 
# determine which device you want to control by using /api/list
#
# Usage: /api/[deviceid]/[clean|charge|pause|rooms|suction]
#
# - /api/list will list you devices on your account.
#
# - /api/JA_RO2_XXXXXXXXX/rooms lists rooms with ID numbers
#
# - "clean" takes optional additional arguments of room #'s comma separated
#   /api/JA_RO2_XXXXXXXXX/clean/12,13,14
# 
# - "suction" takes optional arguments quiet, standard, strong
#   /api/JA_RO2_XXXXXXXXX/suction/quiet 
# 
# - "battery" returns a string representing percentage battery 
#   remaining
# 
# - "mode" returns 1 if sweeping, 0 if charging, 5 if returning to charge, 4 іf
# stuck and needs help
#
# There is little error checking and no security here.
# 
from flask import Flask, render_template, flash, request
import os
import unittest
import logging
#import smartbridge
#from smartbridge.factory import ProviderFactory, ProviderList
import uuid
from http.client import HTTPConnection
#from smartbridge.interfaces.devices import VacuumSuction
from wyze_sdk import Client
from wyze_sdk.models.devices import DeviceModels, Vacuum, VacuumSuctionLevel
from wyze_sdk.errors import WyzeApiError

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '32624076087108375603827608277'

valid_commands = ["clean", "charge", "room", "pause", "list", "rooms", "suction", "battery", "mode"]

config = {
    "port": "WYZEVAC_PORT", # port for your service to run on
	"user": "WYZEVAC_USER",
	"pass": "WYZEVAC_PASS"
}

def sendCommand(device,command,command2):
	#if (valid_commands[command]):
	if command in str(valid_commands):
		client = Client(config['user'],config['pass'])
		if (command == "list"):
			print(client.vacuums.list())
			for vacuum in client.vacuums.list():
                                ret = ""
                                ret = "Name: " + vacuum.nickname+ " (Device ID: " + vacuum.mac + ")"
                                return(ret)
		vacuum = client.vacuums.info(device_mac=device)
		if (command == "rooms"):
			rooms = vacuum.rooms
			ret = ""
			for x in range(len(rooms)):
				ret = ret + "Room: " + rooms[x].name +  " (ID: "  + rooms[x].id +  ") Clean State: " + rooms[x].clean_state + " Room Clean: " + rooms[x].room_clean + "<br>"
			return(ret)
		if (command == "clean" and command2 != 0):
			my_rooms=[]
			my_rooms = command2.split(",")
			client.vacuums.sweep_rooms(device_mac=device,room_ids=my_rooms)
		elif (command == "clean"):
			client.vacuums.clean(device_mac=device)
		if (command == "charge"):
			client.vacuums.dock(device_mac=device,device_model=vacuum.product.model)	
		if (command == "mode"):
                        return(str(vacuum.mode))
		if (command == "battery"):
			return(str(vacuum.voltage))
		if (command == "pause"):
			vacuum.pause()	
		if (command == "suction"):
			if (command2 == "quiet"):
			        client.vacuums.set_suction_level(device_mac=device,suction_level=VacuumSuctionLevel.QUIET,device_model=vacuum.product.model)	
			elif (command2 == "standard"):
			        client.vacuums.set_suction_level(device_mac=device,suction_level=VacuumSuctionLevel.STANDARD,device_model=vacuum.product.model)	
			elif (command2 == "strong"):
			        client.vacuums.set_suction_level(device_mac=device,suction_level=VacuumSuctionLevel.STRONG,device_model=vacuum.product.model)	
		return(command, " executed")
		#return(command)

@app.route("/", methods=['GET'])
def info():
	return("/api/[device]/[clean|charge|edge|spot|stop|playsound]")

@app.route("/api/<string:device>/<string:command>", methods=['GET'])
def api(command,device,rooms=0):
	val = sendCommand(device,command,rooms)
	if val:
		return(val)

@app.route("/api/<string:device>/<string:command>/<string:rooms>", methods=['GET'])
def api2(command,device=0,rooms=0):
	val = sendCommand(device,command,rooms)
	if val:
		return(val)
 
@app.route("/api/list", methods=['GET'])
def api3():
	val = sendCommand("1","list",0)
	if val:
		return(val)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config['port'], debug=False)


