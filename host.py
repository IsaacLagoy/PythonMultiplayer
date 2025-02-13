import socket
import json
import threading
import basilisk as bsk
from player_client import PlayerClient
import time


class Host():

    def __init__(self, engine: bsk.Engine):
        self.engine = engine
        self.host = self.get_local_ip()
        self.port = 5555
        self.clients: dict[... : PlayerClient] = {}
        self.server = None
        self.timer = 0
        
        thread = threading.Thread(target=self.start_server)
        thread.start()

    def get_local_ip(self):
        return "127.0.0.1"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to Google DNS
            return s.getsockname()[0]   # Get the local IP used for the connection

    def start_server(self):
        """
        Starts the server and waits for client connections.
        """
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
        self.server.bind((self.host, self.port))

        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")

        while self.engine.running:
            # manage player and their sockets
            self.timer += self.engine.delta_time
            if self.timer < 1/30: continue
            
            to_remove = []
            for address, client in self.clients.items():
                client.time_since_last_message += self.timer
                if client.time_since_last_message > 1: to_remove.append(address)
            for address in to_remove: self.clients.pop(address)
            
            self.timer = 0
            
            # listen for signals and complete actions based on what is recieved
            message, address = self.server.recvfrom(1024)
            message = message.decode('utf-8')
            if not message: continue
            
            print(address, message, time.time())
            
            if address not in self.clients: self.clients[address] = PlayerClient(address)
            self.clients[address].time_since_last_message = 0
            message = json.loads(message)
            
            if 'name' in message:
                self.clients[address].name = message["name"]
                
                
            if 'position' in message: ...
                
            if 'bullets' in message: ...
            
        else:
            self.server.close()

    def broadcast(self, message: str):
        """Sends a JSON message to all clients except the sender."""
        for address, client in self.clients.items():
            try:
                self.server.sendto(message.encode('utf-8'), address)
            except:
                pass
        
# change recv to recvfrom - allow only one server thread, allows you to know whose talking
# change socket.SOCK_STREAM to socket.DGRAM
# 
# look for send broadcast message for "im joinable" on port that people should join on. Figure out how to recieve this on Python
# look at how to do a network broadcast