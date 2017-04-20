from yeelight import discover_bulbs
from yeelight import Bulb

import json

yeelightDict={}

def getStatuses():
    if len(yeelightDict.keys()) == 0: 
        discover()
    
    statuses = []
    for bulb in yeelightDict:
        currentBulb=convertYeelight(bulb)
        statuses.append({"name" : currentBulb['name'], "state" : currentBulb['state']})
    return statuses


def getBulb(bulbName):
    bulb = yeelightDict[bulbName]
    if bulb is None: 
        raise Exception("Could not find bulb " + bulbName)

    return convertYeelight(bulb)


#Give a 'Bulb' produced a Dict representation of the bulb
def convertYeelight(bulb):
    thisBulb={} #this bulb
    bulbJson=json.loads(json.dumps(bulb))
    capabilities=json.loads(json.dumps(bulbJson['capabilities']))
    
    #Build up the bulb info we'll send back
    #Check the name of the bulb here
    bulbName=str(capabilities['name'])
    bulbIp = bulb['ip']

    thisBulb['ip'] = bulbIp
    thisBulb['name'] = bulbName
    thisBulb['port'] = bulb['port']
    thisBulb['id'] = capabilities['id']
    thisBulb['bright'] = capabilities['bright']
    thisBulb['state'] = capabilities['power']
    thisBulb['type'] = 'yeelight'
    
    #Operarions available
    
    thisBulb['capabilities'] = {
                                'power_on' :   '/devices/'+bulbName+'/state/on',
                                'power_off' :  '/devices/'+bulbName+'/state/off',
                                'brightness' : '/devices/'+bulbName+'/brightness/',
                                'hue' :        '/devices/'+bulbName+'/hue'
                             }
    return thisBulb

def brightness(bulbName, brightness):
    bulb=getBulb(bulbName)
    bulb.turn_on()
    bulb.set_brightness(int(brightness))    
    return bulb

def hue(bulbName, hue):
    bulb=getBulb(bulbName)
    bulb.set_hsv(int(hue), 100) #hue (0-359)
    return bulb
    
def rgb(bulbName, hue):
    bulb=getBulb(bulbName)
    bulb.set_hsv(int(hue), 100) #hue (0-359)
    return bulb

def power(bulbName, status):
    global yeelightDict
    actualBulb = getRealYeelightBulb(bulbName)

    if(status == "on"):
        actualBulb.turn_on()
        yeelightDict[bulbName]["state"] = "on"
        print "Turning " + bulbName + " on"
    else:
        actualBulb.turn_off()
        yeelightDict[bulbName]["state"] = "off"
        print "Turning " + bulbName + " off"
    
    return yeelightDict[bulbName]

def powerAll(power):
    if len(yeelightDict)==0:
        discover()
        
    for bulbName in yeelightDict.keys():
        power(bulbName,power)

    return yeelightDict

def discover():
    global yeelightDict 
    yeelightDict={}
    
    #Retrieves the yeelights from the network
    yeeLights = discover_bulbs()
    
    toReturn = []
    for yeeLight in yeeLights: 
        myYeelight = convertYeelight(yeeLight)
        
        #Add into the global dict
        bulbName = myYeelight["name"]
        yeelightDict[bulbName] = myYeelight

        toReturn.append(myYeelight)
        print "Found " + bulbName
    
    print "Discovered " + str(len(yeeLights)) + " YeeLights " + str(yeelightDict.keys())
    
    return toReturn
    
#Creates a representation of the 'real' Yeelights into our own representation and returns in a list
def convertYeelights():
    toReturn = []
    for bulb in yeelightDict.values():
        toReturn.append(convertYeelight(bulb))

    return toReturn

def getRealYeelightBulb(bulbName):
    if(len(yeelightDict.keys()) == 0):
        discover()
    
    if bulbName not in yeelightDict.keys():
        raise Exception("No Yeelight named " + bulbName)
    
    return Bulb(yeelightDict[bulbName]["ip"])
