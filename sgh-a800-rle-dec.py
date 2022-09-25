import struct
import os
import sys

if len(sys.argv) < 3:
        print(f"Not enough arguments! usage: {sys.argv[0]} file output", file=sys.stderr)
        sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

out = open(sys.argv[2], "wb")
obuf = bytearray()

while fd.tell() < sz:
        p = int.from_bytes(fd.read(1), "little")
        if p >= 0x80:
            data = fd.read(2)
            for i in range((p+2)-128):
                obuf += data
        if p < 0x80:
            data = fd.read((p+1)*2)
            obuf += data 
out.write(obuf)
