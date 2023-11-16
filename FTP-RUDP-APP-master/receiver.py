import socket


def receive_file(filename, ip, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"{ip}, {port}")

    with open(filename, "wb") as f:
        expectedseqnum = 0
        while True:
            data, addr = sock.recvfrom(1024)
            seqnum = int.from_bytes(data[:4], byteorder="big", signed=True)
            print(f"the seqnum is: {seqnum}")
            packet = data[4:]
            if seqnum == -1:
                break
            # print(data)
            if seqnum == expectedseqnum:
                f.write(packet)
                f.flush()
                expectedseqnum += 1
                print(f"send ACK: {seqnum}")
                sock.sendto(data[:4], addr)
            elif seqnum < expectedseqnum:
                print(f"send ACK: {seqnum}")
                sock.sendto(data[:4], addr)
    print("close connection")
    sock.close()


if __name__ == "__main__":
    receive_file("delete_big.png", "localhost", 1234)
#
# def extract(packet):
#     # decode the data from the packet that the sender send
#     return packet[0].decode('utf-8')
#
#
# def corrupt(data, check_sum):
#     rcv_checksum = checksum(data)
#     if rcv_checksum == check_sum:
#         return True
#     else:
#         return False
#
#
# def rdt_rcv(packet, address_source):
#     # reliable data transfer receive from the sender
#     data = exstract(packet)
#     if not corrupt(data, packet[1]):
#         deliver_data(data)
#     else:
#         pass
