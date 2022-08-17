import os
import sys

def main():
	if len(sys.argv) < 2:
		print("Not enough arguments")
		sys.exit(1)
	ftmp = bytearray()
	inp = open(sys.argv[1], "rb")
	dtbuf = inp.read()
	while dtbuf != b"":
		ftmp += dtbuf
		dtbuf = inp.read()
	offset = ftmp.find(b"RUNE")
	if not (os.path.exists(sys.argv[1] + "_ext_img")):	os.mkdir(sys.argv[1] + "_ext_img")	
	cnt = 0	
	while offset != -1:
		cnt += 1
		nextRUNE = ftmp.find(b"RUNE", offset+1)
		if nextRUNE == -1:
			nextRUNE = None
		open(f"{sys.argv[1]}_ext_img/IMG_{cnt}.lrf", "wb").write(ftmp[offset:nextRUNE])
		offset = ftmp.find(b"RUNE", offset+1)	

if __name__ == "__main__":
	main()
