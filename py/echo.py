#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter – 1
# This program is optimized for Python 2.7. It may run on any
# other Python version with/without modifications.

import socket
import sys
import argparse

host = 'localhost'
#host = '192.168.86.49'
data_payload = 2048
backlog = 5 

def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (host, port)
    print("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    sock.listen(backlog) 
    while True: 
        client, address = sock.accept() 
        data = client.recv(data_payload) 
        if data:
            print(data)
            client.send(b"Hello!\n")
            client.send(data)
        client.close() 
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', type=int, required=False, default='3000')
    args = parser.parse_args() 
    echo_server(args.port)

