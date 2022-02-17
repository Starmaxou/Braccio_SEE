from os import O_SYNC

import argparse
import math

from defs import OscCallbacks

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

Call = OscCallbacks

parser = argparse.ArgumentParser()
parser.add_argument("--ip",default="192.168.145.172", help="the ip to listen on")
parser.add_argument("--port", type=int, default=5005,help="the ip to listen on")
args = parser.parse_args()

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/EggControl",Call.egg_control,"activation")
dispatcher.map("/Move/Base",Call.move_base,"targetAngle", "timeToReach", "accelTime")
dispatcher.map("/Move/Shoulder",Call.move_shoulder,"targetAngle", "timeToReach", "accelTime")
dispatcher.map("/Move/Elbow",Call.move_elbow,"targetAngle", "timeToReach", "accelTime")
dispatcher.map("/Move/WristVer",Call.move_wrist_ver,"targetAngle", "timeToReach", "accelTime")
dispatcher.map("/Move/WristRot",Call.move_wrist_rot,"targetAngle", "timeToReach", "accelTime")
dispatcher.map("/Move/Gripper",Call.move_gripper,"targetAngle", "timeToReach", "accelTime")

server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
#client = udp_client.SimpleUDPClient(args.ip, args.port)

print("Serving on {}".format(server.server_address))

server.serve_forever()