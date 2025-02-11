import socket
import threading
import json

HOST = socket.gethostbyname(socket.gethostname())  # Host's local IP
PORT = 5555
clients = []  # Store connected clients

def handle_client(client_socket: socket.socket, address):
    """Handles communication with a single client."""
    print(f"[NEW CONNECTION] {address} connected.")
    clients.append(client_socket)

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
            broadcast(json.dumps({"type": "broadcast", "from": str(address), "data": data}), client_socket)
        except:
            break

    print(f"[DISCONNECTED] {address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    """Sends a JSON message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                pass

def start_server():
    """Starts the server and waits for client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

start_server()
