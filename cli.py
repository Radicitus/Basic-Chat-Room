import select
import socket
import sys

while True:
    # Take Host IP and Port # from cli arguments
    if len(sys.argv) > 3:
        raise Exception("Too many arguments.")
    cli_args = sys.argv
    host, port = cli_args[1], cli_args[2]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        sr, sw, se = select.select([sys.stdin, sock], [], [])
        for s in sr:
            if s == sock:
                data = s.recv(1024)
                print(data)
            else:
                sock.send(input())