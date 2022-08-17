import struct
import os
import sys
from PIL import Image


if len(sys.argv) < 2:
        print(f"Not enough arguments! usage: {sys.argv[0]} file", file=sys.stderr)
        sys.exit(1)

fd = open(sys.argv[1], "rb")
size = os.path.getsize(sys.argv[1])
magic = fd.read(4)
if magic != b'RUNE':
        print("Cannot convert the image. Not in LG RUNE format.")
        sys.exit(1)
width = struct.unpack("<L", fd.read(4))[0]
height = struct.unpack("<L", fd.read(4))[0]
bpp = struct.unpack("<L", fd.read(4))[0]
outp = bytearray()
while fd.tell() < size:
	pixel = fd.read(2)
	len = struct.unpack("<H", fd.read(2))[0]
	outp += pixel*len
if bpp == 16:
                imTmp = Image.frombytes("RGB", (width, height), bytes(outp) ,"raw", "BGR;16")
                imTmp.save(f"{sys.argv[1]}.png")          
fd.close()
