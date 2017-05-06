from sys import argv
import getopt
import simulator

def convert_bool_value(opVal):
    if opVal == "True":
        return True
    elif opVal == "False":
        return False
    else:
        exit()

try:
    optlist,args = getopt.getopt(argv[1:],'vt:', ["solar_panels=",
        "smart_battery=",
        "smart_home=",
        "look_ahead_depth="])
except getopt.error:
    print("Usage: python %s {-v} {-t time} player1 player2" % (sys.argv[0]))
    exit()

solar_panels = None
smart_battery = None
smart_home = None
look_ahead_depth = None

for (op,opVal) in optlist:
    if (op == "--solar_panels"):
        solar_panels = convert_bool_value(opVal)
    elif (op == "--smart_battery"):
        smart_battery = convert_bool_value(opVal)
    elif (op == "--smart_home"):
        smart_home = convert_bool_value(opVal)
    elif (op == "--look_ahead_depth"):
        look_ahead_depth = int(opVal)

simulator.main(solar_panels, smart_battery, smart_home, look_ahead_depth)