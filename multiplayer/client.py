import socket
import threading
import json
import time


class Client():
    
    def __init__(self) -> None:
        self.host = None
        self.port = 5555
        self.data = {}
        
    def join(self, ip: str) -> None:
        self.host = ip
        
        # Connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
            # listeen for messages from the host
            message, address = self.client.recvfrom(1024)
            message = message.decode('utf-8')
            if not message: continue
            
            # do something with the message
            
            
            if not message:
                break
            
            self.data = json.loads(message)
            
    def send_message(self, message: str) -> None:
        """
        Sends a message to the host
        """
        try:
            self.client.send(message.encode("utf-8"))
        except:
            pass
        
    def close(self) -> None:
        """
        Closes the client connection
        """
        self.client.close()