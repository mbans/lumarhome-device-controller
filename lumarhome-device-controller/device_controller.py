import yeelight_controller
import switch_controller
 

#Provides functionality for:
#1. Retrieve status of switches
#2. Turn switches on/off


#All devices that have been 'discovered'
devices = {}

def discoverDevices(user):
    global devices
    
    print "Discovering devices for " + user

    lights=yeelight_controller.discover(user)
    for light in lights:
        devices[light['name']] =  light
        
    switches = switch_controller.getAllSwitchStatuses(user)
    for switch in switches:
        devices[switch['name']] = switch
        
    return devices

def getDevice(deviceName, username):
    if deviceName not in devices.keys(): 
        raise Exception("No device '" + deviceName + "' present")
    return devices[deviceName]
