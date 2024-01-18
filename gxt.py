#!/usr/bin/env python3
from PIL import Image, ImageFile, ImagePalette
from PIL import __version__ as pil_version
import zlib, struct, io

class GxtHeader:
    def __init__(self,data):
        assert data[0:4] == b"GXT\x00", "unknown magic of GXT header"
        self.ver = struct.unpack("2H",data[4:8])
        assert self.ver == (3,0x1000),"version unsupport"
        (self.textures_num,
            self.texture_offset,
            self.texture_size,
            self.palette_4_len,
            self.palette_8_len,
            self.Padding) = struct.unpack("6I",data[8:0x20])
        assert self.palette_4_len == 0, self.palette_4_len
        assert self.palette_8_len == 1, self.palette_8_len
        
    def get_offset(self):
        return self.texture_offset
    
    def get_palette_offset(self):
        return self.texture_offset + self.texture_size \
                -(self.palette_4_len*0x40 + self.palette_8_len*0x400)

class GxtTextureInfo:
    def __init__(self,data):
        (self.offset ,self.size,
        self.palette_index,self.flags,
        self.texture_type,self.texture_format) = struct.unpack("6I",data[:24])
        self.width,self.height = struct.unpack("2H",data[24:28])
        #P8_ARGB
        assert self.texture_format == 0x95001000,hex(self.texture_format)

class GxtImageFile(ImageFile.ImageFile):
    """
    --------
    head
    --------
    textures
    --------
    piexls
    --------
    palettes
    """
    format = "GXT"
    format_description = "GXT file"
    
    def _open(self):
        data = self.fp.read(2)
        if data == b"\x78\x9c":
            self.fp.seek(0)
            data = zlib.decompress(self.fp.read())
            self.fp = io.BytesIO(data)
        self.fp.seek(0)
        self.header = GxtHeader(self.fp.read(0x20))
        assert self.header.textures_num == 1,"multi textures unsupport"
        self.texture = GxtTextureInfo(self.fp.read(0x20))
        self._size = (self.texture.width, self.texture.height)
        
        # self.mode will not be supported since pillow 10.1.0
        major, minor, patch = pillow_version()
        if (major < 10) or (major == 10 and minor == 0):
            self.mode = "P"
        else:
            self._mode = "P"
        
        self.tile = [
            ("gxt", (0, 0) + self.size,0, (self.header,self.texture))
        ]

class GxtDecoder(ImageFile.PyDecoder):
    def __init__(self,mode,header,texture_info):
        super(GxtDecoder,self).__init__(mode)
        self.header = header
        self.texture = texture_info
        self.datasize = header.texture_size
        
    def decode(self,buf):
        if len(buf) < self.datasize:
            return 0, 0
        else :
            palette_offset = self.header.get_palette_offset()
            palette = buf[palette_offset:]
            buf = buf[self.texture.offset:self.texture.size + self.texture.offset]
            buf = aligned(buf,self.texture.width)
            self.set_as_raw(self.order_texture(buf,self.texture.texture_type))
            self.im.putpalette("BGRX",palette)
            self.im.putpalettealphas(palette[3::4])
        return -1, 0
    
    def order_texture(self,data,texture_type):
        if texture_type == 0x60000000:
            return data
        if texture_type == 0x00000000:
            return unswizzle(data,self.im.size[0],self.im.size[1])
        return data

def aligned(buf,width):
    if width % 8 ==0:
        return buf
    r = width + 8 - width%8
    ret = b""
    while len(buf) > 0:
        ret += buf[:width]
        buf = buf[r:]
    return ret

def _compact(x):
    x &= 0x55555555                 # x = -f-e -d-c -b-a -9-8 -7-6 -5-4 -3-2 -1-0
    x = (x ^ (x >> 1)) & 0x33333333 # x = --fe --dc --ba --98 --76 --54 --32 --10
    x = (x ^ (x >> 2)) & 0x0f0f0f0f # x = ---- fedc ---- ba98 ---- 7654 ---- 3210
    x = (x ^ (x >> 4)) & 0x00ff00ff # x = ---- ---- fedc ba98 ---- ---- 7654 3210
    x = (x ^ (x >> 8)) & 0x0000ffff # x = ---- ---- ---- ---- fedc ba98 7654 3210
    return x

def unswizzle(data,width,height):
    import math
    m = min(width,height)
    k = int(math.log(m,2))
    assert 2**k == m,""
    m = m - 1 #0xf...f
    head = 0xffffffff ^ m
    if width>height:
        def get_xy(i):
            # XXXyxyxyx → XXXxxx,yyy
            return (i >> k) & head \
                |  (_compact(i >>1) & m) \
                ,  (_compact(i    ) & m)
    else :
        def get_xy(i):
            # YYYyxyxyx → xxx,YYYyyy
            return (_compact(i    ) & m) \
                ,  (_compact(i >>1) & m) \
                |  (i >> k) & head
    
    ret = [0]*width*height
    for i in range(len(data)):
        x,y = get_xy(i)
        ret[y*width+x] = data[i]
    return bytes(ret)
    
def pillow_version() -> tuple[int]:
    return tuple(int(x) for x in pil_version.split("."))

Image.register_open("GXT", GxtImageFile)
Image.register_decoder("gxt", GxtDecoder)
Image.register_extension("GXT", ".gxt")

if __name__ == "__main__":
    import argparse
    from PIL import Image
    parser = argparse.ArgumentParser("python3 gxt.py")
    parser.add_argument("filename")
    args = parser.parse_args()
    tmp = Image.open(args.filename)
    tmp.save(args.filename[:-4]+".png")
