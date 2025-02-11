import socket
import json
import threading
import basilisk as bsk


class Host():

    def __init__(self, engine: bsk.Engine):
        self.engine = engine
        self.host = self.get_local_ip()
        self.port = 5555
        self.clients = []
        
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
        
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen()

            print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.start()
                if not self.engine.running: raise RuntimeError('Engine stopped')
                
        except:
            print("\nShutting down server...")
        finally:
            server.close()
            assert False, 'Game Closing :)'

    def broadcast(self, message, sender_socket):
        """Sends a JSON message to all clients except the sender."""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    pass

    def handle_client(self, client_socket: socket.socket, address):
        """Handles communication with a single client."""
        print(f"[NEW CONNECTION] {address} connected.")
        self.clients.append(client_socket)

        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break

                # Decode JSON message
                data = json.loads(message)
                print(f"[{address}] {data}")

                # Send back the message to the sender
                response = json.dumps({"type": "echo", "message": f"You said: {data}"})
                client_socket.send(response.encode("utf-8"))

                # Broadcast to other clients
                self.broadcast(json.dumps({"type": "broadcast", "from": str(address), "data": data}), client_socket)
            except:
                break
            
        print(f"[DISCONNECTED] {address} disconnected.")
        self.clients.remove(client_socket)
        client_socket.close()