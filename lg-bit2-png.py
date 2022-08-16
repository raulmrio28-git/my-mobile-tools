import struct
import os
import sys
from PIL import Image
from io import BytesIO


if len(sys.argv) < 4:
	print(f"Not enough arguments! usage: {sys.argv[0]} file width height", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

width = int(sys.argv[2])
height = int(sys.argv[3])

frames = struct.unpack("<H", fd.read(2))[0]
for i in range(int(frames)):
        datasize = struct.unpack("<L", fd.read(4))[0]
        data = BytesIO(fd.read(datasize))
        outp = bytearray()
        while data.tell() < datasize:
            tt = struct.unpack("<H", data.read(2))[0]

            if tt == (0x8000+width) or tt == (0x8000+height):
                continue                        
                                
            compressed = tt >> 15 # 1 bit: 0x0: Raw, 0x1: RLE
            cnt = tt % 0x8000 # 15 bit: length
                                    
            if not compressed:
                outp += data.read(cnt*2)
            else:
                bit = data.read(2)
                outp += bit*cnt

        imTmp = Image.frombytes("RGB", (width, height), bytes(outp) ,"raw", "BGR;16")
        imTmp.save(f"{sys.argv[1]}_{i}.png")
        
fd.close()
        
