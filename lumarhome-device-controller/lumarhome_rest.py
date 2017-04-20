import device_controller
import traceback
from flask import Flask, jsonify

app = Flask(__name__)

discoveredDevices=False
username="lumarhome"

# Discovers and returns all devices for the given user, the devices are then 'cached' for future use
@app.route("/ping", methods=['GET'])
def ping():
    return success({"msg":"pong"})

# Discovers and returns all devices for the given user, the devices are then 'cached' for future use
@app.route("/devices", methods=['GET'])
def discoverDevices():
    try:
        global discoveredDevices
        devices=device_controller.discoverDevices()
        discoveredDevices=True
        return success(devices)
    except Exception as error:
        print(traceback.format_exc())
        return fail(error)

# Retrieves device by name
@app.route("/devices/<string:deviceName>", methods=['GET']) 
def getDevice(deviceName):
    try:
        if not discoveredDevices: 
            discoverDevices()

        device = device_controller.getDevice(deviceName)
        return success(device)
    except Exception as error:
        return fail(error)
    
# Power the device on or off
@app.route("/devices/<string:deviceName>/state/<string:state>", methods=['GET']) 
def power(deviceName, state):
        discoverIfRequired()
        return success(device_controller.power(deviceName, state))        

@app.route("/devices/<string:deviceName>/brightness/<int:brightnessLevel>", methods=['GET']) 
def brightness(deviceName, brightnessLevel):
    try:
        discoverIfRequired()
        device_controller.brightness(deviceName, brightnessLevel)        
        return getDevice(deviceName)
    except Exception as error:
        return fail(error)

@app.route("/devices/<string:deviceName>/hue/<int:hueLevel>", methods=['GET']) 
def hue(deviceName, hueLevel):
    try:
        discoverIfRequired()
        device_controller.hue(deviceName, hueLevel)        
        getDevice(deviceName)
    except Exception as error:
        return fail(error)

    
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def discoverIfRequired():
    if not discoveredDevices:
        discoverDevices()

def fail(message):
    resp = jsonify({"message" : str(message)})
    resp.status_code=400
    return resp

def success(data):
    resp = jsonify(data=data)
    resp.status_code=200
    return resp
    
def successStr(message):
    resp = jsonify({"message" : message})
    resp.status_code=200
    return resp

#Threaaded = True as issue with returning HTTP GET to Angular (found in StackOVerflow)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, threaded=True)