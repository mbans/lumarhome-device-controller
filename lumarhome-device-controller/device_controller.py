import yeelight_controller
import switch_controller

#Provides functionality for:
#1. Retrieve status of switches
#2. Turn switches on/off


#All devices that have been 'discovered'
devices = {}

def discoverDevices():
    global devices
    lights=yeelight_controller.discover()
    
    deviceArray=[]
    for light in lights:
        devices[light['name']] =  light
        deviceArray.append(light)
        
    switches = switch_controller.getAllSwitchStatuses()

    for switch in switches:
        devices[switch['name']] = switch
        deviceArray.append(switch)

    return deviceArray

# Retrieve device with the given name
# Throws exception if no device is returned
def getDevice(deviceName):
    if deviceName not in devices.keys(): 
        raise Exception("No device '" + deviceName + "' present")
    return devices[deviceName]

# Set the state of the device either on/off
def power(deviceName, state):
    device = getDevice(deviceName)
    if device['type'] == "yeelight":
        return yeelight_controller.power(deviceName, state)
    elif device['type'] == "switch":
        return switch_controller.power(deviceName, state)
    else:
        raise Exception("unknown device type" + device['type'])
    
    
    
# Set brightness
def brightness(deviceName, brightness):
    device = getDevice(deviceName)
    if device['type'] == "yeelight":
        yeelight_controller.brightness(deviceName, brightness)
        return success()
    return noCapabilityResponse(deviceName, "brightness")

# Set hue
def hue(deviceName, hueLevel):
    device = getDevice(deviceName)
    if device['type'] == "yeelight":
        yeelight_controller.hue(deviceName, hueLevel)
        return success()
    return noCapabilityResponse(deviceName, "hue")

def setAttribute(device, attribute, value):  
    device[attribute] = value;

def success(): 
    return {"status_code" : 200}

def noCapabilityResponse(deviceName, capability):
        raise Exception("Device [" + deviceName + "] does not have " +capability+ " capabilities")
