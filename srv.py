import select
import socket
import sys


def printUserCount(users):
    if len(users) > 1:
        print("> New user ", address, "entered (", len(users), " users online)")
    else:
        print("> New user ", address, "entered (", len(users), " user online)")


while True:
    # Take Host IP and Port # from cli arguments
    if len(sys.argv) > 3:
        raise Exception("ERROR! Usage: script, IP addr, Port #")
    cli_args = sys.argv
    host, port = cli_args[1], cli_args[2]

    # User counter
    users = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    print("Chat Server started on port ", port)

    sock.listen(5)
    connection, address = sock.accept()
    with connection:
        users += 1
        printUserCount(users)

        while True:
            data = sock.recv(1024)
            print("[", connection, "] ", str(data))
            if not data:
                users -= 1
                printUserCount(users)
            break
