from yeelight import Bulb
import json

#This is a horrible manual set up step to assign names to the bulbs 
#The YeeLight names didn't appear for some reason, so manually added here
#Will add a step that makes user register a name with the bulb via UI

#bulb = Bulb(ip="192.168.0.102",effect="smooth")
#bulb.set_name("livingroom_biglight")

#bulb = Bulb(ip="192.168.0.104", effect="smooth")
#bulb.set_name("livingroom_biglight")

#bulb = Bulb(ip="192.168.0.100",effect="smooth")
#bulb.set_name("livingroom_littlelight")

#bulb = Bulb("192.168.0.101")
#bulb.set_name("bedroom_lucy")

#bulb = Bulb("192.168.0.105")
#bulb.set_name("office")

bulb = Bulb("192.168.0.105")
bulb.set_name("office_lamp")

#bulb = Bulb("192.168.0.112")
#bulb.set_name("bedroom_martin")


#id=0x00000000035aba47, ip=192.168.0.102 => Thai lamp
#id=0x0000000002be3385, ip=192.168.0.104 => BigLight
#id=0x0000000000c9f231, ip=192.168.0.100 => Corner Lamp
##id=0x00000000035abeb6, ip=192.168.0.101 => LucyLamp
#id=0x00000000035a0e5d  ip=192.168.0.105 => Office
#id=0x00000000035a0f28, ip=192.168.0.103    => Bedroom
