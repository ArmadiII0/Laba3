import socket
import json
import psutil
from datetime import datetime
import threading
import os


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
    current_time = datetime.now().strftime("var3%d-%m-%Y_%H:%M:%S")
    file_name = f"./{current_time}.json"
    with open(file_name, 'w') as f:
        json.dump(process_info, f)
    with open(file_name, 'rb') as f:
        data = f.read()
        client_socket.sendall(data)
    client_socket.close()

def handle_client(conn, addr):
    try:
        print('Подключение клиента', addr)
        data = conn.recv(1024)
        print(data.decode())
        with conn:
            print('Подключен клиент:', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    print("Соединение с клиентом разорвано.")
                    break
                elif data.decode() == 'var3':
                    update_and_send_data(conn)
                    print("Данные обновлены и отправлены клиенту.")
                    break
                elif data.decode() == "var4":
                    executable_info = find_executables_in_path()
                    json_data = json.dumps(executable_info, ensure_ascii=False, indent=4)
                    data_bytes = json_data.encode()
                    conn.send(data_bytes)
                    conn.shutdown(socket.SHUT_WR)
                elif data.decode() == 'var1':
                    data = conn.recv(1024)
                    print(data.decode())
                    update_and_send_data_var1(conn, data.decode())
                    break
                else:
                    print("Неверная команда от клиента.")
                    break
            
    except socket.error as e:
        print(f"Ошибка при работе с клиентом {addr}: {e}")
        
    finally:
        conn.close()
        print('Отключение клиента', addr)


def update_and_send_data_var1(client_socket, n):
    ls_info = list_files_recursive(n)
    current_time = datetime.now().strftime("var1%d-%m-%Y_%H:%M:%S")
    file_name = f"./{current_time}.json"
    with open(file_name, 'w') as f:
        json.dump(ls_info, f)
    with open(file_name, 'rb') as f:
        data = f.read()
        client_socket.sendall(data)
    client_socket.close()


def list_files_recursive(path):
    result = []
    for root, dirs, files in os.walk(path):
        directory_info = {"Directory": root, "Files": [], "Directories": []}
        for directory in dirs:
            directory_info["Directories"].append({"Name": directory, "Type": "Directory"})
        for file in files:
            file_path = os.path.join(root, file)
            file_stat = os.stat(file_path)
            file_info = {
                "Name": file,
                "Type": "File",
                "Permissions": file_stat.st_mode & 0o777,
                "Owner": file_stat.st_uid,
                "Group": file_stat.st_gid,
                "Size": file_stat.st_size,
                "Last Modified": file_stat.st_mtime
            }
            directory_info["Files"].append(file_info)
        result.append(directory_info)
    return result

def find_executables_in_path():
    executables = {}
    path_dirs = os.getenv("PATH").split(os.pathsep)
    for directory in path_dirs:
        try:
            filenames = os.listdir(directory)
        except OSError:
            continue
        for filename in filenames:
            filepath = os.path.join(directory, filename)
            try:
                if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                    executables.setdefault(directory, []).append(filename)
            except OSError:
                continue
    return executables


def create_socket_and_listen():
    global sock
    sock = socket.socket()
    sock.bind(('', 9021))
    sock.listen(5)
    print('Начало прослушивания порта')
    while True:
        conn, addr = sock.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        

create_socket_and_listen()


