import argparse
import socket

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-x', '--host', default='localhost', required=False)
arg_parser.add_argument('-p', '--port', default='40123', required=False)
arg_parser.add_argument('-s', '--server', default=False, required=False, action='store_true')

args = arg_parser.parse_args()


def client():
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        target = (args.host, int(args.port))
        sock.connect(target)
        print("Connected to ", sock.getsockname())
        print("To quit, send '$exit'")

        while True:
            input_data = input("> ")
            sock.send(input_data.encode())

            if input_data == '$exit':
                sock.close()
                break

            data = sock.recv(1024).decode()

            if data == '$exit':
                sock.close()
                print('Connection closed by the server')
                break

            print(f'[SERVER]: {data}')

    except ConnectionRefusedError:
        print('There was an error while connecting to the server')


def server():
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((args.host, int(args.port)))
    sock.listen()

    print(f'Server started at {sock.getsockname()}')
    print("To quit, send '$exit'")
    print("Waiting for connection...")

    while True:
        conn, addr = sock.accept()
        print(f'Connection received {addr}')

        while conn:
            data = conn.recv(1024).decode()

            if data == '$exit':
                print('Connection closed by the client')
            else:
                print(f'[CLIENT]: {data}')

            input_data = input("> ")

            if input_data == '$exit':
                conn.send('$exit'.encode())
                conn.close()
                break

            conn.send(input_data.encode('utf-8'))


if __name__ == '__main__':
    if args.server:
        server()
    else:
        client()
