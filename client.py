import socket
import threading
import queue
import sys

HOST = '127.0.0.1'
PORT = 5555


# サーバーとの接続を監視し、サーバーからのメッセージを受信する関数
def monitor_connection(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print("\r\033[K" + message)  # メッセージを上書きして表示
            print("> ", end="", flush=True)  # 入力プロンプトを表示

    except ConnectionResetError:
        print("\nConnection to server lost.")
    except OSError:
        pass


# ユーザーの入力を処理し、サーバーにメッセージを送信する関数
def handle_user_send_message(client_socket, q):
    while True:
        if not q.empty():
            message = q.get(timeout=1)

            if message == "":
                continue
            else:
                if client_socket.fileno() != -1:
                    client_socket.sendall(message.encode('utf-8'))
                else:
                    print("\nConnection to server lost.")
                    break


def handle_user_input(client_socket, q):
    try:
        while True:
            cmd = input("> ")
            if cmd == "q":
                break
            else:
                q.put(cmd)
    finally:
        client_socket.close()
        sys.exit()


# クライアントを起動
if __name__ == '__main__':
    # サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    message = input("ROOM> ")
    client_socket.sendall(message.encode('utf-8'))

    message = input("NAME> ")
    client_socket.sendall(message.encode('utf-8'))

    q = queue.Queue()

    try:
        # サーバーとの接続を監視するスレッドを開始
        connection_thread = threading.Thread(target=monitor_connection, args=(client_socket, ))
        connection_thread.daemon = True
        connection_thread.start()

        # ユーザーの入力を処理するスレッドを開始
        send_message_thread = threading.Thread(target=handle_user_send_message, args=(client_socket, q))
        send_message_thread.daemon = True
        send_message_thread.start()

        input_thread = threading.Thread(target=handle_user_input, args=(client_socket, q))
        input_thread.start()

        input_thread.join()

    except KeyboardInterrupt:
        print("\nExiting...")
