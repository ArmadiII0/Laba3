import socket

def recvall(sock):
    data = b""
    while True:
        part = sock.recv(4096)
        data += part
        if len(part) < 4096:
            break
    return data

def send_command_to_server(host, port, command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode())
        response = recvall(s)
        s.shutdown(socket.SHUT_RD)
    return response.decode()

if __name__ == "__main__":
    host = 'localhost'
    port = 12345

    command = input("Enter command (update to update data): ")
    response = send_command_to_server(host, port, command)
    print("Response from server:", response)