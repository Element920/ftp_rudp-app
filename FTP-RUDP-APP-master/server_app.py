import sender
import os
import socket
import threading
import receiver
import time

MAX_PACKET_SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = 'server_files'
CLIENT_DATA_PATH = "client_files"


class server_app:
    def __init__(self):
        self.ip_server_tcp = socket.gethostbyname(socket.gethostname())
        self.port_server_tcp = 5555
        self.ADDR_server = (self.ip_server_tcp, self.port_server_tcp)
        self.list_files = []
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        files = os.listdir('server_files')
        if not len(files) == 0:
            for f in files:
                self.list_files.append(f)

    def downloadFile(self, msg):
        file_path = f"{SERVER_DATA_PATH}/{msg}"
        time.sleep(10)
        sender.send_file(file_path, self.ip_server_tcp, 9999)
        send_data = f"The file: {msg} downloaded"
        return send_data

    def uploadFile(self, msg):
        file_path = f"{SERVER_DATA_PATH}/{msg}"
        receiver.receive_file(file_path, self.ip_server_tcp, 9999)
        send_data = f"The file: {msg} uploaded"
        return send_data

    def deleteFile(self, file_name):
        send_data = ""
        if file_name in self.list_files:
            os.remove(f"{SERVER_DATA_PATH}/{file_name}")
            send_data += "File deleted successfully."
        else:
            send_data += "File not found."
        return send_data

    def getList(self):
        send_data = ""
        if len(self.list_files) == 0:
            send_data = "The server directory is empty"
        else:
            for file in self.list_files:
                send_data += f"{file}\n"
        return send_data

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        while True:
            data = conn.recv(MAX_PACKET_SIZE).decode(FORMAT)
            cmd, msg = data.split("@")

            if cmd == "LIST":
                send_data = self.getList()
                conn.send(send_data.encode(FORMAT))

            elif cmd == "DELETE":
                file_name = msg
                send_data = self.deleteFile(file_name)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "UPLOAD":
                send_data = self.uploadFile(msg)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "DOWNLOAD":
                send_data = self.downloadFile(msg)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "DISCONNECTED":
                break
        print(f"[DISCONNECTED] {addr} disconnected")
        conn.close()


    def run(self):
        print("[STARTING] Server is starting")
        print(f"{self.ADDR_server}")
        self.socket_server.bind(self.ADDR_server)
        self.socket_server.listen()
        print(f"[LISTENING] Server is listening on IP:{self.ip_server_tcp} PORT:{self.port_server_tcp}")

        while self.running:
            conn, addr = self.socket_server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        self.socket_server.close()


if __name__ == "__main__":
    server_app().run()

