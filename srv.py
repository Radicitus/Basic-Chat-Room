import select
import socket
import sys


def welcomeUserPrint(conn):
    if len(conn - 1) > 1:
        return "> Connected to the chat server (", len(conn - 1), " users online"
    else:
        return "> Connected to the chat server (", len(conn - 1), " user online"


def newUserPrint(c, cli):
    if len(c) > 1:
        return "> New user ", cli, "entered (", len(c), " users online)"
    else:
        return "> New user ", cli, "entered (", len(c), " user online)"


def leftUserPrint(c, cli):
    if len(c) > 1:
        return "< The user ", cli, "left (", len(c), " users online)"
    else:
        return "< The user ", cli, "left (", len(c), " user online)"


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

print("Chat Server started on port", port)

# Client vars
connections = [srv]

while True:
    try:
        sr, sw, se = select.select(connections, [], [])
        print(sr)
        for s in sr:
            if s is srv:
                connection, address = s.accept()
                connections.append(connection)

                # Send welcome message with user count
                connection.send(welcomeUserPrint(connections).encode())

                # Send user joined message with user count
                for c in connections:
                    if c is not srv and c is not s:
                        ip, port = s.getsockname()[0], s.getsockname()[1]
                        c.send(newUserPrint(str(ip) + ":" + str(port), connections).encode())
            else:
                data = s.recv(1024)
                print("rcv data: ", data)
                if data:
                    for c in connections:
                        if c is not srv and c is not s:
                            ip, port = s.getsockname()[0], s.getsockname()[1]
                            message = "[" + str(ip) + ":" + str(port) + "] " + data.decode('ascii')
                            c.send(message.encode())
                else:

                    # Send user left message with user count
                    for c in connections:
                        if c is not srv and c is not s:
                            ip, port = s.getsockname()[0], s.getsockname()[1]
                            c.send(leftUserPrint(str(ip) + ":" + str(port), connections).encode())

                    connections.remove(s)
                    s.close()
    except Exception as e:
        print("PROGRAM EXIT: ", e)
        srv.close()
        sys.exit()



