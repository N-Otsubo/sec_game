import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5555

rooms = {}
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


def handle_client(client, room_name):
    try:
        while True:
            message = client[0].recv(1024).decode('utf-8')

            if not message:
                break

            for c in rooms[room_name]:
                if c != client[0]:
                    message = f"{client[1]}: {message}"
                    c.sendall(message.encode('utf-8'))
    finally:
        print(f"{client[1]} disconnect")
        rooms[room_name].remove(client[0])
        client[0].close()


def wait_for_clients():
    server.listen()
    print("Waiting for clients...")

    while True:
        client, addr = server.accept()
        clients.append(client)

        room_name = client.recv(1024).decode('utf-8')
        client_name = client.recv(1024).decode('utf-8')

        # 部屋が存在しない場合は新規作成
        if room_name not in rooms:
            rooms[room_name] = []

        # クライアントを部屋に追加
        rooms[room_name].append(client)

        client_thread = threading.Thread(target=handle_client, args=([client, client_name], room_name))
        client_thread.start()

        print(f"{client_name} connected to room {room_name} from {addr}")


if __name__ == '__main__':
    try:
        wait_for_clients()
    except KeyboardInterrupt:
        print("Shutdown Server")
    finally:
        for clients in rooms.values():
            for client in clients:
                client.close()
        server.close()
        sys.exit()
