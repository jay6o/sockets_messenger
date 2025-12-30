import socket
import threading

sockets = []
sockets_lock = threading.Lock()

def handle_client(client_socket, addr):
    user = None
    try:
        user = client_socket.recv(1024).decode('utf-8')
        print(f"Connection from: {user} at {addr}")
        while True:
            m = client_socket.recv(4096).decode('utf-8')
            if not m:
                break
            print(f"{user}: {m}")
            with sockets_lock:
                for s in sockets:
                    try:
                        if s != client_socket:
                            s.send(f"{user}: {m}".encode('utf-8'))
                    except:
                        pass
    except Exception as e:
        print(f"Exception: {e}")

    finally:
        with sockets_lock:
            if client_socket in sockets:
                sockets.remove(client_socket)
        try:
            client_socket.close()
        except:
            pass

        print(f"Connection closed from: {user} at {addr}")
                
    return

def server_program():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 5001))
    s.listen(5)
    print(f"Server listening on {s.getsockname()}")

    try:
        while True:
            c_sock, addr = s.accept()
            sockets.append(c_sock)
            client_handler = threading.Thread(target=handle_client, args=(c_sock, addr))
            client_handler.start()
    except Exception:
        print(Exception)
        s.close()
        s.shutdown(0)


if __name__ == "__main__":
    server_program()
