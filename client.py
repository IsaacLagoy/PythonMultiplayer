import socket
import threading

HOST = input("Enter the host IP: ")  # Ask for the host's local IP
PORT = 5555

def receive_messages(client_socket: socket.socket):
    """Handles receiving messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print("\n" + message)  # Print received messages
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
    client.send(message.encode("utf-8"))

client.close()
