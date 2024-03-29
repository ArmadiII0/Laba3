import socket

def main():
    HOST = '127.0.0.1'
    PORT = 12345
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((HOST, PORT))
                print("Подключение к серверу установлено.")
                print("Меню:")
                print("1. update - обновить и получить данные")
                print("2. exit - завершить программу")
                choice = input("Выберите команду: ")
                if choice == 'update':
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
