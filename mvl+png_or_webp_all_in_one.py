#!/usr/bin/env python3
from PIL import Image

import zlib
import struct
import os

class Mvl:
    """
    mvl format :
    ------------
    head
    ------------0x60
    pictures
    ------------
    blocks
    x,y,z,u,v 
    ------------
    block_indexs of picturess
    
    """
    def __init__(self,data):
        # 初始化，可能算是构造函数的作用 ？
        if data.startswith(b"\x78\x9c"):
            data = zlib.decompress(data)
        #     如果二进制数据以指定的 prefix 开头则返回 True，否则返回 False。 prefix 也可以为由多个供查找的前缀构成的元组。
        self.data = data
        assert self.data[0:4] == b"MVL1","Magic ERROR: {}".format(self.data[0:4])
        self.n, = struct.unpack("<I",self.data[4:8])
        assert self.data[0x20:0x2a] == b"XFYF0FUFVF","unknown type {}".format(self.data[0x20:0x2a])
        self.get_pictures()
        
    def get_pictures(self):
        self.pic = []
        for i in range(self.n) :
            data = self.data[0x60+i*0x40:0xa0+i*0x40]
            assert data[0x8:0x10]==b'\x04\x01\x00\x01\x00\x00\x00\x00',data[0x8:0x10]
            # about picture data
            l_o,p_o = struct.unpack("<2I",data[0x10:0x18])
            # in mvl file
            l,p = struct.unpack("<2I",data[0x18:0x20])
            assert i <1 or p - self.pic[-1]["length"]*2 == self.pic[-1]["index"]
            s = cstr(data[0x20:])
            tmp  = {"name": s,
                    "block_len": l_o, 
                    "first_block": p_o,
                    "index": p, 
                    "length": l} 
            
            self.pic.append(tmp)
        self.get_blocks()
    
    def get_blocks(self):
        for i in range(self.n):
            tmp = self.pic[i]
            bi = tmp["first_block"]
            bl = tmp["block_len"]
            
            blocks = []
            block_data = self.data[bi:bi+5*4*bl]
            data = self.data[tmp["index"]:tmp["index"]+tmp["length"]*5*4]
            for j in range(0,tmp["length"]*2,2):
                k = struct.unpack("H",data[j:j+2])[0]
                assert k<= bl,"out blocks %d"%j
                block = block_data[k*20:k*20+20]
                #points and UV
                x,y,z,u,v = struct.unpack("<5f",block)
                assert z==0,"z!=0"
                blocks.append((f2int(x),f2int(y),f2int(z),u,v))
            
            self.pic[i]["block"] = blocks
    
    def combine(self,pic):
        w,h = pic.size
        block = self.pic[0]["block"]
        dx = abs(block[0][0] - block[1][0])
        dy = abs(block[0][1] - block[2][1])
        dw = abs(block[0][3] - block[1][3])*w
        dh = abs(block[0][4] - block[2][4])*h
        rx,ry = dx/dw,dy/dh
        pic_i = 0
        ret = {}
        for i in self.pic:
            if i["length"] <=0 :
                continue
            img = Image.new(size = (6000,10000),mode= "RGBA",color="#00000000")
            name = i["name"]
            point = i["block"][0]
            
            x,y = (point[0]/rx+2000,point[1]/ry+1000)
            min_x,max_x,min_y,max_y = (x,y,x,y)
            #step ever two triangles
            for j in range(0,len(i["block"]),6):
                point = i["block"][j]
                # resize to orignal
                x,y = (point[0]/rx+2000,point[1]/ry+1000)
                cp = pic.crop((point[3]*w,point[4]*h,point[3]*w+dw,point[4]*h+dh)).convert("RGBA")
                img.paste(cp,(f2int(x),f2int(y)),mask = cp)
                min_x = min(x,min_x)
                max_x = max(x,max_x)
                min_y = min(y,min_y)
                max_y = max(y,max_y)
            max_x += dw
            max_y += dh
            ret[name] = {"min_x": f2int((min_x-1000)*rx),
                         "min_y": f2int((min_y-1000)*ry),
                         "max_x": f2int((max_x-1000)*rx),
                         "max_y": f2int((max_y-1000)*ry),
                         "image": img.crop((min_x,min_y,max_x,max_y))}
        return ret

def f2int(x):
    if abs(int(x)-x) > 0.5:
        return int(x+0.5)
    return int(x)

def find_filename(filename):
    if filename.endswith("_.mvl"):
        namewe = filename[:-5]+".webp"
        namepn = filename[:-5]+".png"
        if os.path.exists(namewe):
            return (filename,namewe)
        elif os.path.exists(namepn):
            return (filename,namepn)
        else:
            import gxt
            return (filename,filename[:-5]+".gxt")
    elif filename.endswith(".png") or filename.endswith(".webp"):
        return (filename[:-4]+"_.mvl",filename)
    elif filename.endswith(".gxt"):
        import gxt
        return (filename[:-4]+"_.mvl",filename)
    return (filename,filename[:-4]+".png")

def cstr(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    return str(s.replace(b"\x00",b"").replace(b"\xFE",b""),encoding = "sjis")           
        
def process_data(mvl_data,pic):
    mvl = Mvl(mvl_data)
    return mvl.combine(pic)


def get_path_file(files_path):
    data = []
    for root, dirs, files in os.walk(files_path, topdown=False):
        for name in files:
            f_p = os.path.join(name).replace("\\", "/")
            if f_p.endswith("_.mvl"):
                pack(f_p)
                print(f_p+"转换完成！")
                print('\n')
    print("finish")


def pack(fileName):

    mvl,pic = find_filename(fileName)
    # 根据函数内容可知，第一个参数返回的是mvl，第二个参数返回的是png格式的图片

    with open(mvl,"rb") as f:
        mvl_data = f.read()
    pic = Image.open(pic)
    '''
    读文件，将mvl文件读取到mvl_data，再将pic文件打开，载入到pic变量中
    '''

    dir = mvl[:-5]
    if not os.path.exists(dir) :
        os.mkdir(dir)
    #     将目录转到相应的文件夹，如果没有，则创建一个
    data = process_data(mvl_data,pic)
    # mvl_data读取的是mvl文件
    for i in data:
        data[i]["image"].save(dir+"/"+i+".png")

    for i in data:
        del data[i]["image"]
    import json
    with open(dir+"/index.json","w") as f:
        json.dump(data, f)

def main():
    print("开始转换咯~")
    get_path_file('./')

if __name__ == "__main__":
    main()
    
    
