import socket
import json
import threading
import basilisk as bsk
from player_client import PlayerClient


class Host():

    def __init__(self, engine: bsk.Engine):
        self.engine = engine
        self.host = self.get_local_ip()
        self.port = 5555
        self.clients: list[PlayerClient] = []
        
        thread = threading.Thread(target=self.start_server)
        thread.start()
        
    def get_local_ip(self):
        return "127.0.0.1"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to Google DNS
            return s.getsockname()[0]   # Get the local IP used for the connection

    def start_server(self):
        """Starts the server and waits for client connections."""
        try:
        
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 
            server.bind((self.host, self.port))
            server.listen()

            print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server.accept() # waits to recieve a new client
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.start()
                if not self.engine.running: raise RuntimeError('Engine stopped')
                
        except:
            print("\nShutting down server...")
        finally:
            server.close()
            assert False, 'Game Closing :)'

    def broadcast(self, message: str, sender_socket = None):
        """Sends a JSON message to all clients except the sender."""
        for client in self.clients:
            if client.socket != sender_socket:
                try:
                    client.socket.send(message.encode("utf-8"))
                except:
                    pass

    def handle_client(self, client_socket: socket.socket, address):
        """Handles communication with a single client."""
        print(f"[NEW CONNECTION] {address} connected.")
        player_client = PlayerClient(client_socket)
        self.clients.append(player_client)

        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break

                # Decode JSON message
                data = json.loads(message)
                
                if 'name' in data: 
                    player_client.name = data['name']
                    
            except:
                break
            
        print(f"[DISCONNECTED] {address} disconnected.")
        client_socket.close()
        
        
# change recv to recvfrom - allow only one server thread, allows you to know whose talking
# change socket.SOCK_STREAM to socket.DGRAM
# 
# look for send broadcast message for "im joinable" on port that people should join on. Figure out how to recieve this on Python
# look at how to do a network broadcast