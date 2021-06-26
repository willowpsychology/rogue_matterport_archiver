# rogue\_matterport\_archiver
## Convert matterport .dam files to plaintext .obj


DAM files are just protobuf files. The file "damfile.proto" is a incomplete schema but is valid for all DAM files I have seen.


Setup:
Compile protobuf file
```
protoc --python\_out=. damfile.proto
```

```
usage: damfile2obj.py [-h] [--out-dir OUT_DIR] dam_pth

Convert matterport .dam file to .obj

positional arguments:
  dam_pth            Path of .dam file

optional arguments:
  -h, --help         show this help message and exit
  --out-dir OUT_DIR  output directory

example: python damfile2obj.py --out-dir=8800BLR_dollhouse da1a5ccd99d044f586788232864f0004_50k.dam
```
Any texture images need to be copied to the output directory.


Dependencies:
- Numpy
- Protocol Buffers
