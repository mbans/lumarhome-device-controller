import switch_controller
import yeelight_controller
import device_controller
from flask import Flask, jsonify

app = Flask(__name__)

discoveredDevices=False

username="lumarhome"
#
# Discovers and returns all devices for the given user, the devices are then 'cached' for future use
#
@app.route("/devices", methods=['GET'])
def discoverDevices():
    try:
        global discoveredDevices
        devices=device_controller.discoverDevices(username)
        discoveredDevices=True
        return response(jsonify(status=200, data=devices),200)
    except Exception as error:
        print error
        return response(jsonify({"error" : str("Error discovering devices " + str(error))}),400) 



#
# Retrieves device by name
#
@app.route("/devices/<string:deviceName>", methods=['GET']) 
def getDevice(deviceName):
    try:
        if not discoveredDevices: 
            discoverDevices()
            
        device = device_controller.getDevice(deviceName, username)

        return response(jsonify(status=200, data=device),200) 
    except Exception as error:
        print error
        return response(jsonify({"error" : str("Error getting device " + deviceName + ", error="+str(error))}),400)



# Power the device on or off
# TODO: Move this to the DeviceController
@app.route("/devices/<string:deviceName>/state/<string:state>", methods=['GET']) 
def power(deviceName, state):
    #try: 
        username = "lumarhome"
        if not discoveredDevices:
            discoverDevices()
                
        device = device_controller.getDevice(deviceName, username)
        deviceName = device['name']
        deviceType = device['type']
        
        print 'Retrieved device '  + deviceName + " with type " + deviceType
                
        if deviceType == "yeelight":
            yeelight_controller.power(deviceName, state)
        elif deviceType == "switch":
            switch_controller.setSwitchStatus(deviceName, state, username)
        else:
            raise Exception("unknown device type")
        
        return response(jsonify(status=200),200) 
    #except Exception as error:
    #    print error
    #    return response(jsonify({"error" : str("Error getting device " + deviceName + ", error="+str(error))}),400)

#
# 
#
#@app.route("/bulbs", methods=['GET'])
#def discover():
#    try:
#        discoverBulbs=yeelight_controller.discover()
#        return response(jsonify(status=200, data=discoverBulbs),200)
#   except Exception as error:
#       return response(str("Error discovering bulbs " + str(error)),400) 

@app.route('/switches', methods=['GET'])
def switches(): 
    try:
        statuses = switch_controller.getAllSwitchStatuses(username)
        for status in statuses:
            status['on'] = '/switches/' + status['id'] + '/' + 'state' + '/on'
            status['off'] = '/switches/' + status['id'] + '/' + 'state' + '/off'
        
        return response(jsonify(status=200, data=statuses),200) 
    except Exception as error:
        return jsonify(status = 400, operation='switches', value=str(error)) 


@app.route('/switches/<string:switchId>/state/<string:state>', methods=['GET'])
def setState(switchId, state): 
    #try:
        switchResponse = switch_controller.setState(switchId, state)
        return response(jsonify(status=200, data=switchResponse),200) 
        # except Exception as error:
        #
        #return jsonify(status = 400, operation='switching ' + switchId + " " + state, value=str(error)) 

            
@app.route('/bulbs/status', methods = ['GET'])
def getStatuses():
    statuses=yeelight_controller.getStatuses()
    return response(jsonify(status=200, data = statuses),200)

@app.route('/bulbs/<string:bulbName>/power/<string:power>', methods = ['GET'])
def power2(bulbName, power):
    try:
        yeelight_controller.power(bulbName, power)
        return jsonify(status = 200, bulb=bulbName, operation='power', value=power) 
    except Exception as error:
        return jsonify(status = 400, bulb=bulbName, operation='power', value=str(error)) 

        
@app.route('/bulbs/<string:bulbName>/brightness/<string:brightness>', methods = ['GET'])
def brightness(bulbName, brightness):
    try: 
        yeelight_controller.brightness(bulbName, brightness)
        return jsonify(status = 200, bulb=bulbName, operation='brightness', value=brightness) 
    except Exception as error:
        return jsonify(status = 400, bulb=bulbName, operation='brightness', value='Error setting brightness ' + str(error)) 

@app.route('/bulbs/<string:bulbName>/hue/<string:hue>', methods = ['GET'])
def hue(bulbName, hue):
    try: 
        yeelight_controller.hue(bulbName, hue)
        return response(jsonify(status = 200, bulb=bulbName, operation='hue', value=hue),200)
    except Exception as error:
        return response(jsonify(status = 400, bulb=bulbName, operation='hue', value=str(error)),400)

#@app.route('/bulbs/<string:bulbName>/power/', methods = ['POST'])
#def state(bulbName):
#    yeelight_controller.power(bulbName, power)
##    power=request.form['power']
#   return response(jsonify(success = 200), 200)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def success(bulbName, operation, value):
    resp = jsonify(status=200, bulb=bulbName,operation=operation,value=value) 
    resp.status_code = 200
    return resp

def failure(bulbName, operation, value):
    resp = jsonify(status=400, bulb=bulbName,operation=operation,value=value) 
    resp.status_code = 400
    return resp

def response(resp, statusCode):
    resp.status_code = statusCode
    return resp

#Threaaded = True as issue with returning HTTP GET to Angular (found in StackOVerflow)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, threaded=True)