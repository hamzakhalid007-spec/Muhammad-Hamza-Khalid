import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

clients = {}
clients_lock = threading.Lock()

def send_safe(connect, text):
    try:
        connect.sendall(text.encode('utf-8'))
    except Exception:
        pass

def broadcast(text, exclude_username=None):
    with clients_lock:
        for user, connect in list(clients.items()):
            if user == exclude_username:
                continue
            send_safe(connect, text)

def client_handler(connect, addr):
    username = None
    try:
        username = connect.recv(1024).decode('utf-8').strip()
        if not username:
            connect.close()
            return

        with clients_lock:
            if username in clients:
                send_safe(connect, "SERVER: Username already taken. Disconnecting.")
                connect.close()
                return
            clients[username] = connect

        print(f'[+] {username} connected from {addr}')
        broadcast(f"SERVER: {username} has joined the chat.", exclude_username=username)
        send_safe(connect, "SERVER: Connected. Use @username for private messages. /quit to leave.")

        while True:
            data = connect.recv(4096)
            if not data:
                break
            msg = data.decode('utf-8').strip()
            if msg == '':
                continue
            if msg == '/quit':
                break

            # Private message
            if msg.startswith('@'):
                parts = msg.split(' ', 1)
                if len(parts) == 1:
                    send_safe(connect, "SERVER: Invalid private message. Use: @username message")
                    continue
                target_token, content = parts[0], parts[1]
                target = target_token[1:]
                with clients_lock:
                    target_conn = clients.get(target)
                if target_conn:
                    send_safe(target_conn, f"[Private] {username}: {content}")
                    send_safe(connect, f"[Private to {target}] You: {content}")
                else:
                    send_safe(connect, f"SERVER: User '{target}' not found.")
            else:
                # Public broadcast
                broadcast(f"{username}: {msg}", exclude_username=username)

    except Exception as e:
        print("Error handling client:", e)
    finally:
        if username:
            with clients_lock:
                if username in clients and clients[username] is connect:
                    del clients[username]
        try:
            connect.close()
        except:
            pass
        print(f"[-] {username} disconnected.")
        broadcast(f'SERVER: {username} has left the chat.')

def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            connect, addr = server_sock.accept()
            thread = threading.Thread(target=client_handler, args=(connect, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    start_server()