import select
import socket
import sys


# Take Host IP and Port # from cli arguments
if len(sys.argv) != 3:
    raise Exception("ERROR! Usage: script, IP addr, Port #")
cli_args = sys.argv
host, port = str(cli_args[1]), int(cli_args[2])
cli_addr = (host, port)
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli.connect(cli_addr)

while True:
    try:
        sr, sw, se = select.select([sys.stdin, cli], [], [])
        for s in sr:
            print(s)
            if s is cli:
                data = s.recv(1024)
                if data:
                    print(data.decode('ascii'))
                else:
                    s.close()
            else:
                message = input()
                print("[You] ", message)
                cli.send(input().encode())
    except Exception as e:
        print("PROGRAM EXIT: ", e)
        cli.close()
        sys.exit()

