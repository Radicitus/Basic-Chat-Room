import select
import socket
import sys


def welcomeUserPrint(conn):
    if len(conn) - 1 > 1:
        return "> Connected to the chat server (" + str(len(conn) - 1) + " users online)"
    else:
        return "> Connected to the chat server (" + str(len(conn) - 1) + " user online)"


def newUserPrint(cli, c):
    if len(c) - 1 > 1:
        return "> New user " + cli + " entered (" + str(len(c) - 1) + " users online)"
    else:
        return "> New user " + cli + " entered (" + str(len(c) - 1) + " user online)"


def leftUserPrint(cli, c):
    if len(c) - 1 > 1:
        return "< The user " + cli + " left (" + str(len(c) - 1) + " users online)"
    else:
        return "< The user " + cli + " left (" + str(len(c) - 1) + " user online)"


# Take Host IP and Port # from cli arguments
if len(sys.argv) != 3:
    raise Exception("ERROR! Usage: script, IP addr, Port #")
cli_args = sys.argv
host, port = str(cli_args[1]), int(cli_args[2])
srv_addr = (host, port)

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setblocking(0)
srv.bind(srv_addr)
srv.listen(5)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Chat Server started on port " + str(port) + ".")

# Client vars
connections = [srv]

while True:
    try:
        sr, sw, se = select.select(connections, [], [])
        for s in sr:
            if s is srv:
                connection, address = s.accept()
                connections.append(connection)

                # Server log user joined message with user count
                ip, port = connection.getpeername()[0], connection.getpeername()[1]
                print(newUserPrint(str(ip) + ":" + str(port), connections))

                # Send welcome message with user count
                connection.send(welcomeUserPrint(connections).encode())

                # Send user joined message with user count
                for c in connections:
                    if c is not srv and c is not connection:
                        c.send(newUserPrint(str(ip) + ":" + str(port), connections).encode())
            else:
                data = s.recv(1024)
                if data:
                    ip, port = s.getpeername()[0], s.getpeername()[1]
                    print("[" + str(ip) + ":" + str(port) + "] " + data.decode('ascii'))
                    for c in connections:
                        if c is not srv and c is not s:
                            ip, port = s.getpeername()[0], s.getpeername()[1]
                            message = "[" + str(ip) + ":" + str(port) + "] " + data.decode('ascii')
                            c.send(message.encode())
                else:

                    # Remove the disconnected client
                    connections.remove(s)

                    # Server log user left message with user count
                    ip, port = s.getpeername()[0], s.getpeername()[1]
                    print(leftUserPrint(str(ip) + ":" + str(port), connections))

                    # Send user left message with user count
                    for c in connections:
                        if c is not srv and c is not s:
                            ip, port = s.getpeername()[0], s.getpeername()[1]
                            c.send(leftUserPrint(str(ip) + ":" + str(port), connections).encode())

                    # Close the socket
                    s.close()
    except KeyboardInterrupt:
        print("\nexit")
        srv.close()
        sys.exit()
