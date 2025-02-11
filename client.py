import socket
import threading
import json

HOST = input("Enter the host IP: ")  # Ask for the host's local IP
PORT = 5555

def receive_messages(client_socket):
    """Handles receiving messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            data = json.loads(message)  # Decode JSON

            if data["type"] == "echo":
                print(f"\n[SERVER] {data['message']}")
            elif data["type"] == "broadcast":
                print(f"\n[{data['from']}] {data['data']}")
        except:
            print("Connection lost.")
            break

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Start a thread to receive messages
thread = threading.Thread(target=receive_messages, args=(client,))
thread.daemon = True
thread.start()

while True:
    message = input("You: ")
    if message.lower() == "quit":
        break

    # Send JSON message
    json_message = json.dumps({"type": "chat", "player": "Player1", "message": message})
    client.send(json_message.encode("utf-8"))

client.close()
