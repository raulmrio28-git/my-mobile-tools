import struct
import os
import sys

if len(sys.argv) < 2:
	print(f"Not enough arguments! usage: {sys.argv[0]} img_out.bin", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")
date = fd.read(4).decode("ascii")
print(f"IMG_Out date: {date}")
res_items = struct.unpack("<L", fd.read(4))[0]
for i in range(int(res_items)):
	res_file_offs = struct.unpack("<L", fd.read(4))[0]
	res_file_size = struct.unpack("<L", fd.read(4))[0]
	res_file_name = fd.read(40)
	null_idx = res_file_name.find(b'\x00')
	res_file_name = res_file_name[:null_idx].decode('euc-kr')
	print(f"IMG_Out item {i}: offs={res_file_offs}, size={res_file_size}, filename={res_file_name}")
	old_addr = fd.tell()
	fd.seek(res_file_offs)
	os.makedirs(f"{sys.argv[1]}_ext", exist_ok=True)
	open(f"{sys.argv[1]}_ext/{res_file_name}", "wb").write(fd.read(res_file_size))
	fd.seek(old_addr)
fd.close()
