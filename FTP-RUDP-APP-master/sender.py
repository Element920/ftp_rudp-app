import socket
import os
import threading
import time

MAX_PACKETS = 10
MAX_PACKET_SIZE = 1020


def send_packet(packet, host, port, sock):
    sock.sendto(packet, (host, port))
    print(f"number packet send is: {int.from_bytes(packet[:4], byteorder='big',signed=True)}")


def send_file(filename, host, port):
    finish = -1
    finish = finish.to_bytes(4, byteorder="big", signed=True)
    with open(filename, "rb") as f:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        packets = []
        base = 0
        index = 0
        last_ack = -1

        while True:
            data = f.read(MAX_PACKET_SIZE)
            suq = index.to_bytes(4, byteorder="big",signed=True)
            if not data:
                break
            packets.append(suq + data)
            index += 1

        while last_ack + 1 < len(packets):
            flag = True
            while flag:
                flag = False
                count = 0
                for i in range(base, min(base + MAX_PACKETS, len(packets))):
                    if last_ack < i:
                        print("packet")
                        packet = packets[i]
                        send_packet(packet, host, port, sock)
                        count += 1
                for j in range(count):
                    try:
                        data, addr = sock.recvfrom(4)
                        num = int.from_bytes(data[:4], byteorder="big", signed=True)
                        print(f"expected ACK {num}")
                        if last_ack < num:
                            last_ack = num
                    except socket.timeout:
                        flag = True
            base = last_ack
        print("close connection")
        sock.sendto(finish, (host, port))
        sock.close()
        
        
# def send_file(filename, host, port):
#     PACKETS_WINDOW = 1
#     finish = -1
#     finish = finish.to_bytes(4, byteorder="big", signed=True)
#     packets = []
#     list_acks = []
#     base = 0
#     index = 0
#     last_ack = -1
#     timeout = 1.0
#     last_size = 0
#     duplicates_ack = 0
#     avoieds = False
#
#     with open(filename, "rb") as f:
#         while True:
#             data = f.read(MAX_PACKET_SIZE)
#             index += MAX_PACKET_SIZE
#             suq = index.to_bytes(4, byteorder="big",signed=True)
#             if not data:
#                 break
#             packets.append(suq + data)
#             list_acks.append(False)
#             index += 1
#
#         while last_ack + 1 < len(packets):
#             flag = True
#             print(f"size of sliding window is :{PACKETS_WINDOW}")
#             while flag:
#                 flag = False
#                 for i in range(base, min(base + PACKETS_WINDOW, len(packets))):
#                     if last_ack < i:
#                         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#                         sock.settimeout(timeout)
#                         print(f"the time out is: {timeout}")
#                         packet = packets[i]
#                         start_time = time.time()
#                         sock.sendto(packet, (host, port))
#
#                         try:
#                             data, addr = sock.recvfrom(4)
#                             num = int.from_bytes(data[:4], byteorder="big", signed=True)
#                             if last_size < num:
#                                 timeout = (timeout-(time.time()-start_time))
#                                 last_size = num
#                                 if avoieds == True:
#                                     PACKETS_WINDOW += 1
#                                 else:
#                                     PACKETS_WINDOW *= 2
#                             else:
#                                 timeout = timeout - (time.time() - start_time)
#                                 duplicates_ack += 1
#                                 if duplicates_ack == 3:
#                                     PACKETS_WINDOW = int(PACKETS_WINDOW / 2)
#                                     avoieds = True
#                                     duplicates_ack = 0
#
#                         except sock.timeout:
#                             flag = True
#                             timeout = 2*(timeout - (time.time() - start_time))
#                             PACKETS_WINDOW = 1
#             base = last_ack
#         print("close connection")
#         sock.sendto(finish, (host, port))
#         sock.close()
