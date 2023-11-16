import socket
import threading

SIZE_PACKET = 1024


class server_dns:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dns_table = {}
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 9998
        self.connected = True
        self.run()

    def run(self):
        self.socket.bind((self.ip, 9998))
        print(f"[LISTENING] Server is listening on IP:{self.ip} PORT:{self.port}")

        while self.connected:
            data, addr = self.socket.recvfrom(SIZE_PACKET)
            domain_name = data.decode('utf-8')
            if domain_name in self.dns_table:
                self.socket.sendto(self.dns_table[domain_name].encode('utf-8'), addr)
                print(f"in if: domain_name:{domain_name}, ip domain_name:{self.dns_table[domain_name]}")
            else:
                try:
                    ip_address = socket.gethostbyname(domain_name)
                    self.dns_table[domain_name] = ip_address
                except:
                    ip_address = "NO VALUE, PLEASE TRY AGAIN"
                self.socket.sendto(ip_address.encode('utf-8'), addr)
                print(f"domain_name:{domain_name}, ip with port:{addr}")
        print("Server DNS close")
        self.socket.close()


if __name__ == "__main__":
    server_dns().run()


