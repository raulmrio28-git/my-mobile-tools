import struct
import os
import sys
from io import BytesIO

def create_int_array(items, data):
	myarray = items * [0]
	for i in range(int(items)):
		myarray[i] = res_file_size = struct.unpack("<L", data[(i*4):(i*4)+4])[0]
	return myarray

if len(sys.argv) < 2:
	print(f"Not enough arguments! usage: {sys.argv[0]} <.res file>", file=sys.stderr)
	sys.exit(1)

res_img_info = BytesIO()
sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")
os.makedirs(f"{sys.argv[1]}_ext", exist_ok=True)
fd.read(2)
date = fd.read(4).decode("ascii")
fd.read(2)
print(f"{sys.argv[1]} date: {date}")
res_file_size = struct.unpack("<L", fd.read(4))[0]
res_items = struct.unpack("<L", fd.read(4))[0]
if res_file_size != sz:
	print("WARN: file size of res file != actual size")
res_file_info_file_offs = struct.unpack("<L", fd.read(4))[0]
res_file_info_data_offs_size = struct.unpack("<L", fd.read(4))[0]
res_file_info_data_offs_info_size = struct.unpack("<L", fd.read(4))[0]
fd.seek(res_file_info_file_offs)
offs_array = create_int_array(res_items, fd.read(res_file_info_data_offs_size))
res_img_info.write(fd.read(res_file_info_data_offs_info_size-res_file_info_data_offs_size))
res_img_data = fd.read(res_file_size-res_file_info_file_offs-res_file_info_data_offs_info_size-res_file_info_data_offs_size)
for i in range(int(res_items)):
	res_img_info.seek(offs_array[i])
	img_format = struct.unpack("<L", res_img_info.read(4))[0]
	img_width = struct.unpack("<L", res_img_info.read(4))[0]
	img_height = struct.unpack("<L", res_img_info.read(4))[0]
	img_frames = struct.unpack("<L", res_img_info.read(4))[0]
	img_transpbool = struct.unpack("<L", res_img_info.read(4))[0]
	img_transpcolor = struct.unpack("<L", res_img_info.read(4))[0]
	if img_transpbool == 1:
		img_transpcolor_r = ((img_transpcolor >> 11) & 0x1f) << 3
		img_transpcolor_g = ((img_transpcolor >> 5) & 0x3f) << 2
		img_transpcolor_b = (img_transpcolor & 0x1f) << 3
	img_data_offs_sz_ptr = struct.unpack("<L", res_img_info.read(4))[0]
	res_img_info.seek(img_data_offs_sz_ptr)
	image_info_str = f"Image {i}: width={img_width}, height={img_height}, frames={img_frames}"
	if img_transpbool == 1:
		image_info_str += f", transparency: R={img_transpcolor_r}, G={img_transpcolor_g}, B={img_transpcolor_b}"
	print(image_info_str)
	for j in range(int(img_frames)):
		frame_data_offs = struct.unpack("<L", res_img_info.read(4))[0]
		frame_data_size = struct.unpack("<L", res_img_info.read(4))[0]
		frame_data = res_img_data[frame_data_offs:frame_data_offs+frame_data_size]
		print(f"Frame {j}: offs={frame_data_offs}, size={frame_data_size}")
		filename = f"IMG_{i}_frame{j}_{img_width}_{img_height}"
		if img_transpbool == 1:
			filename += f"_alpha_r_{img_transpcolor_r}_g_{img_transpcolor_g}_b_{img_transpcolor_b}"
		if img_format == 7:
			filename += ".ifg"
		elif img_format == 13:
			filename += ".im"
		else:
			filename += ".bin"
		open(f"{sys.argv[1]}_ext/{filename}", "wb").write(frame_data)
fd.close()