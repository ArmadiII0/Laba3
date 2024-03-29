import socket
import json
import psutil
from datetime import datetime

def get_process_info():
    process_info = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            process_info.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_info

def update_and_send_data(client_socket):
    process_info = get_process_info()
    current_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    file_name = f"./{current_time}.json"
    with open(file_name, 'w') as f:
        json.dump(process_info, f)
    with open(file_name, 'rb') as f:
        data = f.read()
        client_socket.sendall(data)
    client_socket.close()

def main():
    HOST = '127.0.0.1'
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("Сервер ожидает подключения...")
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print('Подключен клиент:', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("Соединение с клиентом разорвано.")
                        break
                    elif data.decode() == 'update':
                        update_and_send_data(conn)
                        print("Данные обновлены и отправлены клиенту.")
                        break
                    else:
                        print("Неверная команда от клиента.")
                        break

if __name__ == "__main__":
    main()
