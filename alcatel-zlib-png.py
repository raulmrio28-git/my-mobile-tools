import struct
import os
import zlib, sys
from PIL import Image


if len(sys.argv) < 1:
        print(f"Not enough arguments! usage: {sys.argv[0]} file", file=sys.stderr)
        sys.exit(1)

fd = open(sys.argv[1], "rb")
datasize = struct.unpack(">L", fd.read(4))[0]
magic = fd.read(4)
if magic != b'ZLIB':
        print("Cannot convert the image. Not in Alcatel ZLIB format.")
        sys.exit(1)
width = struct.unpack("<H", fd.read(2))[0]
height = struct.unpack("<H", fd.read(2))[0]
uncsize = struct.unpack(">L", fd.read(4))[0]
bpp = struct.unpack("<H", fd.read(2))[0]
data = fd.read(datasize)
unc_data = zlib.decompress(data)
if bpp == 16:
        imTmp = Image.frombytes("RGB", (width, height), bytes(unc_data) ,"raw", "BGR;16")
        imTmp.save(f"{sys.argv[1]}.png")
fd.close()
