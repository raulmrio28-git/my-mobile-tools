import re
import os
import sys

if len(sys.argv) < 2:
        print(f"Not enough arguments! usage: {sys.argv[0]} <RFS meta> <RFS data>", file=sys.stderr)
        sys.exit(1)

fdm = open(sys.argv[1])
fdd = open(sys.argv[2], "rb")
meta = fdm.read()     
dir_regex = r"D>(.*?)>"
file_regex = r"F>(.*?)>(\d+)>" 
dirs = re.findall(dir_regex, meta)
files = re.findall(file_regex, meta)

print("Directories:")
for d in dirs:
    dir = d
    if not os.path.exists(dir):
        os.makedirs(d, exist_ok=True)
    print(dir)
    
print("\nFiles:")
for f in files:
    filename, size = f
    print(filename, size)
    data = fdd.read(int(size))
    open(filename, "wb").write(data)
