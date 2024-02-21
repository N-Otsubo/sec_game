import threading
import signal


# スレッドの関数
def thread_function():
    try:
        while True:
            print("Thread is running...")
            input("> ")
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting thread...")


# スレッドを開始
thread = threading.Thread(target=thread_function)
thread.start()

# メインスレッドでスレッドの終了を待機
thread.join()

print("Main thread exiting...")
