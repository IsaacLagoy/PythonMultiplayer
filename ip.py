import socket

hostname = socket.gethostname()
server = socket.gethostbyname(hostname)

print(server)