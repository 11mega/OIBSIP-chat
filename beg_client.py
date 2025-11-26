
import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def receive_loop(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Disconnected from server.")
                break
            print(data.decode('utf-8'), end='')
    except Exception as e:
        print("Receive error:", e)
    finally:
        sock.close()
        sys.exit(0)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    try:
        while True:
            msg = input()
            if msg.strip().lower() == '/quit':
                sock.sendall('/quit'.encode('utf-8'))
                break
            sock.sendall(msg.encode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()

if __name__ == '__main__':
    main()
