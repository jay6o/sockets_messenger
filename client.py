import sys
import socket
import threading
from colorama import Fore, Back, Style

def connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    user = input("Enter your username: ")
    s.send((user.strip()).encode('utf-8'))
    return s, user

def send_message(s, message):
    s.send(message.encode('utf-8'))
    return

def recv_message(s, user):
    while True:
        r = s.recv(4096).decode('utf-8')
        if not r:
            print("Server disconnected, exiting.")
            s.close()
            exit(0)
        i = 0
        while r[i] != ':':
            i += 1
        sender = r[:i]
        msg = r[i+1:]
        
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()

        print("")
        print(f"\r{Fore.BLUE}{sender}{Style.RESET_ALL}:{msg}")
        print("")
        print("> ", end="", flush=True)

if __name__ == "__main__":
    try:
        s, user = connect('localhost', 5001)
        print(f"Connected to server as {user}. Type 'exit' or 'quit' to leave.\n\n")
        recv_thread = threading.Thread(target=recv_message, args=(s, user))
        recv_thread.daemon = True
        recv_thread.start()

        while 1:
            message = input("> ")
            if message.strip().lower() == "exit" or message.strip().lower() == "quit":
                print("Exiting.")
                s.close()
                exit(0)
            send_message(s, message)
        s.close()
    except:
        print("failure, exiting.")
        exit(0)
