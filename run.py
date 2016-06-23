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
import threading

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

class Player(object):
    def __init__(self, name, ip, port = 5005):
        self.name = name
        self.ip = ip
        self.port = port
        self.client = udp_client.UDPClient(self.ip, self.port)
    def send(self, msg):
        self.client.send(msg)
    def __str__(self):
        return self.name + " " + self.ip

class Messages(object):
    hack = osc_message_builder.OscMessageBuilder(address="/hack").build()
    clock = osc_message_builder.OscMessageBuilder(address="/clock").build()

class Server(object):
    def __init__(self):

        self.dispatcher = dispatcher.Dispatcher()
        #self.dispatcher.map("/register", self.register_player, "Register")
        #self.server = osc_server.ForkingOSCUDPServer(("0.0.0.0", 5006), self.dispatcher)
        self.server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 5006), self.dispatcher)

        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def on(self, address, callback):
        self.dispatcher.map(address, callback)
    def shutdown(self):
        self.server.shutdown()


class GameController(object):
    players = []
    def __init__(self):
        self.server = Server()
        self.server.on("/register", self.register_player)

    def register_player(self, address, name, ip):
        print(threading.current_thread())
        p = Player(name, ip)
        print(self)
        GameController.players.append(p)
        print(GameController.players)
        p.send(Messages.hack)
    def shutdown(self):
        self.server.shutdown()
    def send_clock(self):
        print(GameController.players)
        for p in GameController.players:
            p.send(Messages.clock)
    def send_hack_to(self, player):
        pass
    def send_hack(self):
        pass


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('{}x{}'.format(200, 500))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.run = False
        self.label = tk.Label(text = "Server")
        self.label.pack()

        self.controller = GameController()


        #self.client = udp_client.UDPClient("255.255.255.255", 5005)
        #if hasattr(socket,'SO_BROADCAST'):
        #    self.client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
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
    def on_closing(self):
        print("Closing")
        self.controller.shutdown()
        self.root.destroy()
    def update_game(self):
        print(threading.current_thread())
        if self.run:
            self.controller.send_clock()
        else:
            print("Game is paused !")
        self.root.after(ROBOT_UPDATE_TIME * 1000, self.update_game)


if __name__ == "__main__":
    app = App()
