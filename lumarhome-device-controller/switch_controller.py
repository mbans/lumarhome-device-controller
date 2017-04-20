import requests
import json


#Provides functionality for:
#1. Retrieve status of switches
#2. Turn switches on/off


#TODO: Make this controller retrieve content from the DB
accounts = [{
    'username' : 'lumarhome',
    'devices': [ 
                 {"name" : "fairy_lights",  "id" : "80064C21FFCC2F64CFA53EF3EE714E87184F0CAC", "type" : "switch", "url" : "https://aps1-wap.tplinkcloud.com/?token=8b21ded7-142a33c15ef64708b16e443"},
                 {"name" : "dehumidifier",  "id" : "8006468CE9EDF43E290FCCCC0996574D1850A119", "type" : "switch", "url" : "https://aps1-wap.tplinkcloud.com/?token=8b21ded7-142a33c15ef64708b16e443"},
                 {"name" : "strip_light",   "id" : "8006CB9F94205A1158634A1607E237F217B03112", "type" : "switch", "url" : "https://aps1-wap.tplinkcloud.com/?token=8b21ded7-142a33c15ef64708b16e443"},
                 {"name" : "oven",          "id" : "800606813DAFD15C131CECBEA16707DD17CB082B", "type" : "switch", "url" : "https://aps1-wap.tplinkcloud.com/?token=8b21ded7-142a33c15ef64708b16e443"}
               ]
    }]

#
#Retrieve the statuses of all switches for a given user
#
def getAllSwitchStatuses():
    statusReponses=[]
    acc = {}
    for account in accounts:
        username = account['username']
        if username == "lumarhome":
            acc=account
            break
        
    #Search for switch with name/type
    devices = acc['devices']
    for device in devices:
        if device['type'] == 'switch': 
            statusReponses.append(getSwitchStatus(device))
    
    print ("Discovered " + str(len(statusReponses)) + " switches: ") 
    return statusReponses

#
# set switch to on or off
#
def power(switchName,state):
    switch = getSwitch(switchName)
    statusResp = getSwitchStatus(switch)
    setState(switch, state)
    
    statusResp['state'] = state    
    return statusResp
#
# POST a request to obtain the status of the given switch belonging to a given account 
#
def getSwitchStatusByN(switchName):
    switch = getSwitch(switchName)
    statusResponse = postStatusRequest(switch)
    return convertStatusResponse(statusResponse, switch)

def getSwitchStatus(switch):
    statusResponse = postStatusRequest(switch)
    return convertStatusResponse(statusResponse, switch)

#
# Constructs HTTP POST request to set the status for a given switch
#
def postStatusRequest(switch):
        deviceId = switch['id']
        url = switch['url']
        statusReq = {"method":"passthrough", "params": {"deviceId": '', "requestData": "{\"system\":{\"get_sysinfo\":null},\"emeter\":{\"get_realtime\":null}}" }}    
        statusReq['params']['deviceId'] = deviceId
        theResponse =  requests.post(url, json=statusReq)
        return theResponse.json()

# Retrieve a given switch details for user
#
def getSwitch(switchName):
    print "Retrieving " + switchName  + " from db (TODO - harwired at moment)"
    
    for account in accounts:
        username = account['username']
        if username != "lumarhome":
            continue
        
        #Search for switch with name/type
        devices = account['devices']
        for device in devices:
            deviceName = device['name']
            if deviceName == switchName and device['type'] == 'switch': 
                return device
    
    raise Exception ("No switch " + switchName + " present")  
         

#Sets the switch to given state
def setState(switch, state):
    stateResponse = requests.post(switch['url'], json=createStateRequest(switch, state))
    jsonResp=stateResponse.json()

    errorCode=jsonResp['error_code']
    if(errorCode != 0):
        switchId = switch['id']
        raise Exception("Exception attempting to turn " + switchId + " " + state + ". Message=" + str(jsonResp['msg']))
    return stateResponse.json()

# 
# Takes the original status response (from TPLink) and converts into our own ffpostzf structure 
#
def convertStatusResponse(statusResponse, switch):
    ourResponse={}
    ourResponse['id'] = switch['id']
    ourResponse['name'] = switch['name']
    ourResponse['type'] = 'switch'
    
    name=ourResponse['name']
    
    errorCode = int(statusResponse['error_code'])
    if(errorCode != 0): #error
        ourResponse['message'] = statusResponse['msg']
        ourResponse['state'] = "offline"
    else:               #success   
        result = statusResponse['result']
        responseData = result['responseData']
        responseDateJson = json.loads(responseData)
        state = responseDateJson['system']['get_sysinfo']['relay_state']
        ourResponse['capabilities'] = {}
        ourResponse['capabilities']['power_on'] = '/devices/'+name+'/state/on'
        ourResponse['capabilities']['power_off'] = '/devices/'+name+'/state/off'

        if state == 0: 
            ourResponse['state'] = "off"
        elif state == 1:
            ourResponse['state'] = "on"
        else:
            ourResponse['state'] = "offline"
        
    return ourResponse
   
#
# Constructs a 'change state' request for the switch
#
def createStateRequest(switch, state):
    stateInt = 0
    if(state == "on"):
        stateInt = 1

    stateReq = {"method":"passthrough", "params": {"deviceId": "", "requestData": "" } }
    stateReq['params']['deviceId' ] = switch['id'] 
    stateReq['params']['requestData'] = "{\"system\":{\"set_relay_state\":{\"state\":"+str(stateInt) + "} } }"
    return stateReq

    
