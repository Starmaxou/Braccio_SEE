from os import O_SYNC

import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

parser = argparse.ArgumentParser()
parser.add_argument("--ip",default="127.0.0.1", help="the ip to listen on")
parser.add_argument("--port", type=int, default=5005,help="the ip to listen on")
args = parser.parse_args()

dispatcher = dispatcher.Dispatcher()

dispatcher.map("")