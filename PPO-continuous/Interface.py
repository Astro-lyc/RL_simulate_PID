import socket
import time
import sys

# Define Host IP
HOST_IP = "155.198.47.207"
HOST_PORT = 26000
print("Starting socket:TCP...ok")

# 1. create socket object: socket = socket.socket(family,type)

socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("TCP server listen @ %s:%d!" % (HOST_IP, HOST_PORT))
host_addr = (HOST_IP, HOST_PORT)

# 2. bind socket to address: socket.bind(address)
socket_tcp.bind(host_addr)

# 3. listen connection request:socket.listen(backlog)
socket_tcp.listen(1)

# 4.wait for client:connection,address=socket.accept()
socket_con, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s." % client_ip)

# 5. handle
print("Receiving package...")
while True:
    try:
        data = socket_con.recv(512)
        if len(data) > 0:
            print("Received:%s" % data)
            # sum = len(data)
            # str = str("%04d" % sum)
            # data = str + data
            data = str("%04d" % len(data)) + data
            print("send:%s" % data)
            socket_con.send(data)
            time.sleep(1)
            continue
    except Exception:
        socket_tcp.close()
        sys.exit(1)
