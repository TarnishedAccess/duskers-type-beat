import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)

client_sockets = []
server_socket.bind(server_address)
server_socket.listen(5)

print(f"Server is running on {server_address}")

def handle_client(client_socket, address):
    print('waiting for data')
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print(f"Received from {address}: {data.decode('utf-8')}")
                for sock in client_sockets:
                    if sock != client_socket:
                        try:
                            sock.sendall(data)
                            print(f'broadcasted {data} to {sock}')
                        except socket.error:
                            print("Error broadcasting data to a client.")
        except ConnectionResetError:
            print("Connection reset by peer")
            break

def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")
        client_sockets.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
