import argparse
import math
import os
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
import pickle

import tkinter as tk
import time
import random
import socket


users = {}


"""
def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass



def register_user(unused_addr, args, user_name):
    print(unused_addr, args, user_name)
    if user_name not in users:
        users[user_name] = 0
    print(users)


client = udp_client.UDPClient("localhost", 5006)

def send_players(unused_addr, args):
    print("Send player list...")
    msg = osc_message_builder.OscMessageBuilder(address="/players")
    msg.add_arg(pickle.dumps(users))
    msg = msg.build()
    print("Sending", msg.dgram)
    client.send(msg)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
  parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/debug", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)



  dispatcher.map("/register", register_user, "REGISTER")


  dispatcher.map("/players", send_players, "PLAYERS")

  server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
"""


# Mise à jour du robit (en secondes)
ROBOT_UPDATE_TIME = 5
WIDTH = 200
HEIGHT = 500

player = os.getenv("USERNAME")

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.run = False
        self.label = tk.Label(text = "Server")
        self.label.pack()
        self.client = udp_client.UDPClient("255.255.255.255", 5005)
        if hasattr(socket,'SO_BROADCAST'):
            self.client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.start_stop_button = tk.Button(self.root, text="Start", command=self.start_stop)
        self.start_stop_button.pack()
        self.update_game()

        self.root.mainloop()
    def start_stop(self):
        self.run = not self.run
        if self.run:
            t = "Stop"
        else:
            t = "Start"
        self.start_stop_button.config(text=t)

    def update_game(self):
        if self.run:
            print("update game")
            msg = osc_message_builder.OscMessageBuilder(address="/clock")
            msg = msg.build()
            self.client.send(msg)
        else:
            print("Game is paused !")
        self.root.after(ROBOT_UPDATE_TIME * 1000, self.update_game)


if __name__ == "__main__":
    app = App()
