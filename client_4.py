import socket

def recvall(sock):
    data = b""
    while True:
        part = sock.recv(4096)
        data += part
        if len(part) < 4096:
            break
    return data


def main():
    HOST = 'localhost'
    PORT = 9021
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((HOST, PORT))
                client_socket.sendall("Подключен вариант 4".encode())
                print("Подключение к серверу установлено.")
                print("Меню:")
                print("1. var4 - обновить и получить данные")
                print("2. exit - завершить программу")
                choice = input("Выберите команду: ")
                if choice == 'var4':
                    client_socket.sendall(choice.encode())
                    data = b""
                    while True:
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            break
                        data += chunk
                    print("Полученные данные:")
                    print(data.decode()) 
                elif choice == 'exit':
                    break
                else:
                    print("Неверная команда. Попробуйте еще раз.")
            except ConnectionRefusedError:
                print("Не удалось подключиться к серверу.")
                break
if __name__ == "__main__":
    main()