import socket,base64
import threading
import cachehandler
BUFFER=2048
TCP_HOST = '0.0.0.0'
TCP_PORT = 1212

UDP_HOST = '0.0.0.0'
UDP_PORT = 3144

THREAD_LIMIT = 15
TIMEOUT = 20

tcp_connections = 0

class UniqueIntegerGenerator:
    def __init__(self):
        self.counter = 0

    def get_next_unique_integer(self):
        self.counter += 1
        return self.counter


def handle_tcp_client(client_socket, addr,indexer:UniqueIntegerGenerator):
    
    global tcp_connections
    print(f"Accepted TCP connection from {addr}")
    while True:
        data = client_socket.recv(BUFFER)
        if not data:
            break
        #client_socket.sendall(data)
        data=base64.b85encode(data)
        cachehandler.insert_data_to_memcached(str(indexer.get_next_unique_integer()),data,120)
        print(data.decode('utf-8'))
    client_socket.close()
    tcp_connections -= 1

def handle_udp_client(udp_socket,indexer:UniqueIntegerGenerator):
    print("Waiting for UDP data...")
    while True:
        data, addr = udp_socket.recvfrom(BUFFER)
        data=base64.b85encode(data)
        cachehandler.insert_data_to_memcached(str(indexer.get_next_unique_integer()),data,120)
        print(f"Received UDP data from {addr}: {data}")

def main():
    global tcp_connections

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((TCP_HOST, TCP_PORT))
    tcp_socket.listen(15)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((UDP_HOST, UDP_PORT))
    new_counter=UniqueIntegerGenerator()
    udp_thread = threading.Thread(target=handle_udp_client, args=(udp_socket,new_counter,))
    udp_thread.start()

    while True:
        if tcp_connections < THREAD_LIMIT:
            client_socket, addr = tcp_socket.accept()
            client_socket.settimeout(TIMEOUT)
            TCP_new_counter=UniqueIntegerGenerator()
            tcp_connections += 1
            tcp_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, addr,TCP_new_counter,))
            tcp_thread.start()
        else:
            print("Thread limit reached, cannot accept more connections.")

if __name__ == '__main__':
    main()
