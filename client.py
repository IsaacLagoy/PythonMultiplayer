import socket
import threading
import json


class Client():
    
    def __init__(self) -> None:
        self.host = None
        self.port = 5555
        self.data = {}
        
    def join(self, ip: str) -> None:
        self.host = ip
        
        # Connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        # Start a thread to receive messages
        thread = threading.Thread(target=self.receive_messages)
        thread.daemon = True
        thread.start()
        
    def receive_messages(self):
        """
        Handles receiving messages from the server.
        """
        while True:
            try:
                print('listening')
                message = self.client.recv(1024).decode("utf-8")
                print('recieved')
                if not message:
                    break
                
                self.data = json.loads(message)  # Decode JSON
                print(self.data)
                    
            except (socket.error, json.error) as e:
                print(f"Connection lost. {e}")
                break
            
    def send_message(self, message: str) -> None:
        """
        Sends a message to the host
        """
        self.client.send(message.encode("utf-8"))
        
    def close(self) -> None:
        """
        Closes the client connection
        """
        self.client.close()