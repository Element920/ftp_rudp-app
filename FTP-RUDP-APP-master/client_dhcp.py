
# import socket
#
#
#
# class client_dhcp:

    #   def __init__(self, port_dhcp):
    #
import socket
import threading

FORMAT = 'utf-8'


class client_dhcp:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 68
        self.ip_table = {}
        self.ip_rcv = ""
        self.is_connected = True

    def send_message(self):
        print("Discovery Message")
        self.socket.sendto("discovery".encode(FORMAT), (self.ip, self.port))
        print("message sent")

    def get_ip(self):
        self.socket.sendto("discovery".encode(FORMAT), (self.ip, self.port))
        new_ip, addr = self.socket.recvfrom(1024)
        new_ip = new_ip.decode(FORMAT)
        print(f"the new ip is{new_ip}")
        print("I want this IP")
        self.socket.sendto("ACK".encode(FORMAT), (self.ip, self.port))
        return new_ip

    def run(self):
        self.socket.bind((self.ip, self.port))
        print("the client is connected to the server")

    def disconnect(self):
        print("the client disconnected from the server")
        self.socket.close()


if __name__ == "__main__":
    client_dhcp().get_ip()
