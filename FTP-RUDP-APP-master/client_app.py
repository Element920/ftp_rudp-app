import socket
import time
import os
import sender
import receiver

FORMAT = "utf-8"
PACKET_SIZE = 1024
CLIENT_DATA_PATH = "client_files"
SERVER_DATA_PATH = 'server_files'


class client_app:
    def __init__(self):
        self.ip_client_tcp = socket.gethostbyname(socket.gethostname())
        self.port_client_tcp = 5555
        self.ADDR_client = (self.ip_client_tcp, self.port_client_tcp)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_ftp = False
        self.run()

    def uploadFile(self, file_path):
        file_name = os.path.basename(file_path)
        files = os.listdir(SERVER_DATA_PATH)
        send_data = ""
        for f in files:
            if f == file_name:
                send_data += f"The file: {file_name} is already exists in server file"
                return send_data
        self.socket_client.send(f"UPLOAD@{file_name}".encode(FORMAT))
        sender.send_file(file_path, self.ADDR_client[0], 9999)
        send_data = self.socket_client.recv(PACKET_SIZE).decode(FORMAT)
        return send_data

    def downloadFile(self, file_name):
        file_path = f"{CLIENT_DATA_PATH}/{file_name}"
        files = os.listdir(CLIENT_DATA_PATH)
        send_data = ""
        for f in files:
            if f == file_name:
                send_data += f"The file: {file_name} is already exists in client files"
                return send_data
        self.socket_client.send(f"DOWNLOAD@{file_name}".encode(FORMAT))
        receiver.receive_file(file_path, self.ADDR_client[0], 9999)
        send_data = self.socket_client.recv(PACKET_SIZE).decode(FORMAT)
        return send_data

    def get_list(self):
        cmd = "LIST@"
        self.socket_client.send(cmd.encode(FORMAT))
        send_data = self.socket_client.recv(PACKET_SIZE).decode(FORMAT)
        return send_data

    def deleteFile(self, file_name):
        send_data = f"DELETE@{file_name}"
        self.socket_client.send(send_data.encode(FORMAT))
        data = self.socket_client.recv(PACKET_SIZE).decode(FORMAT)
        return data

    def disconnected(self):
        self.socket_client.send("DISCONNECTED@".encode(FORMAT))
        print("the client_app has been disconnected")
        self.socket_client.close()

    def run(self):
        self.socket_client.connect(self.ADDR_client)
        print(f"client_app connected to server")

