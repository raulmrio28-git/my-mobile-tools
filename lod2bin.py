import struct
import os
import sys

if len(sys.argv) < 2:
	print(f"Not enough arguments! usage: {sys.argv[0]} file", file=sys.stderr)
	sys.exit(1)

flash_out = bytearray()
flash_out_init = False
c_offset = 0
base = 0

num_lines = sum(1 for _ in open(sys.argv[1]))

with open(sys.argv[1]) as file:
	text_splitted = file.read().splitlines()
	file.close()
	for i in range(num_lines) :
		if text_splitted[i][0] == '@':
			c_offset = int(text_splitted[i][1:], 16) - base
		else:
			if text_splitted[i][0] == '#':
				pb = text_splitted[i][1:]
				if pb.find("$base=") != -1:
					base_addr = text_splitted[i][len("$base=")+1:]
					base = int(base_addr[2:], 16)
				if pb.find("$FLASH_SIZE=") != -1 and flash_out_init == False:
					size = text_splitted[i][len("$FLASH_SIZE=")+1:]
					flash_out = bytearray([255] * int(size[2:], 16))
					flash_out_init = True
			else:
				write = int(text_splitted[i], 16)
				flash_out[c_offset] = write&0xff
				flash_out[c_offset+1] = (write>>8)&0xff
				flash_out[c_offset+2] = (write>>16)&0xff
				flash_out[c_offset+3] = (write>>24)&0xff
				c_offset += 4

open(f"{sys.argv[1]}.bin", "wb").write(flash_out)

