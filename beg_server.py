
import socket
import threading

HOST = '0.0.0.0'   # listen on all interfaces
PORT = 5000

clients = []  # list of (conn, addr, name)

def broadcast(message, sender_conn=None):
    for conn, addr, name in clients:
        try:
            if conn != sender_conn:
                conn.sendall(message.encode('utf-8'))
        except:
            pass

def handle_client(conn, addr):
    try:
        conn.sendall("Enter your name: ".encode())
        name = conn.recv(1024).decode().strip()
        clients.append((conn, addr, name))
        broadcast(f"[{name} joined the chat]\n", conn)
        print(f"{addr} as {name} connected.")
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode('utf-8').strip()
            if text.lower() == '/quit':
                break
            broadcast(f"{name}: {text}\n", conn)
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()
        # remove client
        for c in clients:
            if c[0] == conn:
                clients.remove(c)
                broadcast(f"[{c[2]} left the chat]\n")
                print(f"{addr} disconnected.")
                break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
