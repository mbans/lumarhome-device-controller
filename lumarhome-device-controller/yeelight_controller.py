from yeelight import discover_bulbs
from yeelight import Bulb

import json
from yeelight.main import BulbException

bulbDict={}
bulbs=[]


def getStatuses():
    print "Retrieving bulb statuses"
    if len(bulbs) == 0: 
        discover()
    
    statuses = []
    
    for b in bulbs:
        bulb=json.loads(json.dumps(b))
        statuses.append({"name" : bulb['name'], "powerStatus" : bulb['powerStatus']})
    return statuses


def getBulb(bulbName):
        
    if bulbName not in bulbDict.keys:
        discover()
    
    ip=bulbDict[bulbName];
    return Bulb(ip)
      

def brightness(bulbName, brightness):
    print "Setting bulbName brightness to " + brightness
    bulb=getBulb(bulbName)
    bulb.turn_on()
    bulb.set_brightness(int(brightness))    

def hue(bulbName, hue):
    print "Setting bulbName hue to " + str(hue)
    bulb=getBulb(bulbName)
    bulb.set_hsv(int(hue), 100) #hue (0-359)

def power(bulbName, status):
    bulb = getBulb(bulbName)
    if(status == "on"):
        bulb.turn_on()
        print "Turning " + bulbName + " on"
    else:
        bulb.turn_off()
        print "Turning " + bulbName + " off"


def powerAll(power):
    if len(bulbDict)==0:
        discover()
        
    for bulbName in bulbDict:
        power(bulbName,power)
        

def discover(username):
    global bulbs 
    global bulbDict
    
    bulbDict={}
    
    discoveredBulbs = discover_bulbs()

    bulbs=[]
    idx=0
    for b in discoveredBulbs:
        bulbInfo={} #this bulb
        bulb=json.loads(json.dumps(b))
        capabilities=json.loads(json.dumps(bulb['capabilities']))
        
        #Build up the bulb info we'll send back
        #Check the name of the bulb here
        bulbName=str(capabilities['name'])
        bulbIp = bulb['ip']

        bulbInfo['ip'] = bulbIp
        bulbInfo['name'] = bulbName
        bulbInfo['port'] = bulb['port']
        bulbInfo['id'] = capabilities['id']
        bulbInfo['powerStatus'] = capabilities['power']
        bulbInfo['bright'] = capabilities['bright']
        bulbInfo['state'] = capabilities['power']
        bulbInfo['type'] = 'yeelight'
        
        #Operarions available
        bulbInfo['capabilities'] = {'power' : '/power/',
                                    'brightness' : '/brightness/',
                                    'hue' : '/hue/',
                                    'rgb' : '/rgb/'}
                                            
        bulbs.append(bulbInfo)
        bulbDict[bulbName] = bulbIp;
        idx=idx+1
    
    print ("Discovered " + str(len(discoveredBulbs)) + " bulbs: " + str(bulbDict.keys()))

    return bulbs