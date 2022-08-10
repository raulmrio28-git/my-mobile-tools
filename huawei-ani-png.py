import struct
import os
import zlib, sys
from PIL import Image


if len(sys.argv) < 1:
        print(f"Not enough arguments! usage: {sys.argv[0]} file", file=sys.stderr)
        sys.exit(1)

fd = open(sys.argv[1], "rb")
magic = fd.read(4)
if magic != b'RI\0\0':
        print("Cannot convert the animation. Not in Huawei .ani format.")
        sys.exit(1)
unknown = struct.unpack("<L", fd.read(4))[0] #Header size?
frames = struct.unpack("<H", fd.read(2))[0]
unknown2 = struct.unpack("<H", fd.read(2))[0] #Speed?
height = struct.unpack("<L", fd.read(4))[0]
width = struct.unpack("<L", fd.read(4))[0]
bpp = struct.unpack("<L", fd.read(4))[0]
for i in range(int(frames)):
        datasize = struct.unpack("<L", fd.read(4))[0]
        data = fd.read(datasize)
        unc_data = zlib.decompress(data)
        if bpp == 16:
                imTmp = Image.frombytes("RGB", (width, height), bytes(unc_data) ,"raw", "BGR;16")
                imTmp.save(f"{sys.argv[1]}_{i}.png")
fd.close()
