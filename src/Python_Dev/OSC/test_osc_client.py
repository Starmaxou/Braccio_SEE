
import argparse
import random
import time
import math
from pickle import FALSE, TRUE
from pythonosc import udp_client


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.145.172",
    help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
    help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    activation = TRUE
    targetAngle = 0
    timeToReach = 3600
    for x in range(3600):
        activation = not activation
        accelTime = timeToReach/4
        timeToReach = timeToReach-1
        targetAngle =targetAngle+1
        if targetAngle > 360:
            targetAngle = 0
        client.send_message("/EggControl", [activation])
        client.send_message("/Move/Base",[targetAngle,timeToReach])
        client.send_message("/Move/Shoulder",[targetAngle,timeToReach])
        client.send_message("/Move/Elbow",[targetAngle,timeToReach])
        client.send_message("/Move/WristVer",[targetAngle,timeToReach])
        client.send_message("/Move/WristRot",[targetAngle,timeToReach])
        client.send_message("/Move/Gripper",[targetAngle,timeToReach])
        activation = not activation
        client.send_message("/EggControl", [activation])
        time.sleep(1)
