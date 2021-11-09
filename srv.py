import select
import socket
import sys


def printUserCount(c, cli):
    if len(c) > 1:
        print("> New user ", cli.getsockname(), "entered (", len(c), " users online)")
    else:
        print("> New user ", cli.getsockname(), "entered (", len(c), " user online)")


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
            else:
                data = s.recv(1024)
                print("rcv data: ", data)
                if data:
                    print("if data")
                    for c in connections:
                        print("If data: ", c)
                        if c is not srv and c is not s:
                            print("Sockname: ", s.getsockname())
                            message = "[" + str(s.getsockname()[0]) + ":" + str(s.getsockname[1]) + "] " + str(data)
                            c.send(message.encode())
                else:
                    connections.remove(s)
                    s.close()
    except:
        print("PROGRAM EXIT")
        srv.close()
        sys.exit()



