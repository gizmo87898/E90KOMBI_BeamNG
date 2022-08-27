# Create UDP socket.
import socket
import struct
import select

class OutGauge:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    outgauge_pack = struct
    def getPack(self):
        return self.outgauge_pack

    sock.bind(('127.0.0.1', 4444))

    while True:
        r, _, _ = select.select([sock], [], [])
        if r:
            # ready to receive
            data = sock.recv(96)
            selfoutgauge_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)