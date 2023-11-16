import socket
import threading

SIZE_PACKET = 1024


class client_dns:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip_dest = socket.gethostbyname(socket.gethostname())
        self.port_dest = 9998
        self.connected = True
        self.run()

    def get_req(self, data)->str:
        self.socket.sendto(data.encode('utf-8'), (self.ip_dest, self.port_dest))
        print(f"massege sent:{data}")
        ip_address, addr = self.socket.recvfrom(SIZE_PACKET)
        print(f"ip:{ip_address}")
        ip_address.decode('utf-8')
        print(f"ip:{ip_address}")
        return ip_address.decode('utf-8')

    def run(self):
        self.socket.bind((self.ip_dest, 9999))
        print("the client is connected to the server")

    def disconnect(self):
        print("the client disconnected from the server")
        self.socket.close()
