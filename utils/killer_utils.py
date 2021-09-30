# ===============================================================
# Copyright 2021. Codex Laboratories LLC
# Created By: Tyler Fedrizzi
# Authors: Tyler Fedrizzi
# Created On: September 6th, 2020
# Updated On: August 10th, 2021
# 
# Description: A class to properly kill a running process and allowing
#              the program to shut down properly.
# ===============================================================
import signal
import socket

class KillerClient:

    def __init__(self, HOST, PORTS):
        self.clients = []
        for PORT in PORTS:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            flag = client.connect_ex((HOST, PORT))
            print("Killer connected to PORT: ", PORT)
            self.clients.append(client)

    def kill(self):
        print(len(self.clients))
        for client in self.clients:
            client.sendall(b'255')
            client.close()

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        
    def exit_gracefully(self, signum, frame):
        self.kill_now = True