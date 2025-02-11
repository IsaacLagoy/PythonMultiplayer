import socket

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS
        return s.getsockname()[0]   # Get the local IP used for the connection

print("Local IP Address:", get_local_ip())
