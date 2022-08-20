#!/usr/bin/env python3
from PIL import Image
import zlib
import os,sys,struct

#Available for MO6，MO7,CHLCC,SGDarling PS3 version
#Not available for 花咲くまにまに，SGPhenogam

def main(inputfilename,piece=True,Total=True):
    #if filename.endswith(".png"):
    #   filename=filename[:-4]+"_.lay"
    #elif not filename.endswith("_.lay"):
    #   filename=filename+"_.lay"
    filenamepic = ""
    filenamelay = ""
    strlen = 0
    ## deal with input file
    if inputfilename.find(".") == -1:
        from RNEIC import bin2png
        strlen = len(inputfilename)
        if parseint(inputfilename)%2 == 0:#input bin
            filenamepic = inputfilename
            bin2png(filenamepic, '.')
            filenamepic = filenamepic + ".png"
            if not os.path.exists(filenamepic):
                print("Error input bin convert fail")
                return
            os.rename(filenamepic[:-4],filenamepic[:-4]+".bin")
            filenamelay = inttostrfill(parseint(inputfilename)+1,strlen)
            if not os.path.exists(filenamelay):
                print("Error input bin and lay-file without extension not found")
                return
        else:#input lay
            filenamelay = inputfilename
            filenamepic = inttostrfill(parseint(inputfilename)-1,strlen)
            if os.path.exists(filenamepic+".png"):
                if os.path.exists(filenamepic):
                    os.rename(filenamepic,filenamepic+".bin")
                filenamepic = filenamepic + ".png"
            else:
                if not os.path.exists(filenamepic):
                    print("Error input lay and bin not found")
                    return
                bin2png(filenamepic, '.')
                filenamepic = filenamepic + ".png"
                if not os.path.exists(filenamepic):
                    print("Error input lay convert fail")
                    return
                os.rename(filenamepic[:-4],filenamepic[:-4]+".bin")
    elif inputfilename.endswith(".png"):
        filenamepic = inputfilename
        strlen = len(inputfilename[:-4])
        filenamelay = inttostrfill(parseint(inputfilename[:-4])+1,strlen)
        if not os.path.exists(filenamelay):
            print("Error input png and lay-file without extension not found")
            return
    elif inputfilename.endswith("_.lay"):
        filenamelay = inputfilename
        filenamepic = inputfilename[:-5] + ".png"
        if not os.path.exists(filenamepic):
            print("Error input formatted lay and png not found")
            return
    else:
        print("Error unknown file type")
        return
    ###
    infile = open(filenamelay, 'rb')
    if not infile:
        print("cannot find ",ilename)
        return
    #using zlib to decompress
    b=b''
    sg0=False
    data = infile.read()
    if data[:2]==b'\x78\x9c':
        decompress = zlib.decompressobj()
        b+=decompress.decompress(data)
    else :
        sg0=True
        b+=data
    #creat a folder 
    p=0
    folder=filenamepic[0:filenamepic.index('.')]
    os.system("mkdir "+folder)
    #the head of the file is the number of images and piece blocks 
    imageNum,pieceNum = struct.unpack(">2I",b[p:p+8])
    p+=8
    #image information following
    partNum=[]
    partTree=[]
    j=0
    for i in range(imageNum):
        a=struct.unpack(">4b",b[p:p+4])
        partTree.append(a)
        partNum.append(struct.unpack(">I",b[p+4:p+8])[0])#the block number of image
        p+=12
        j+=1
    partNum.append(pieceNum)
    #init the Canvas
    dx=[0]*pieceNum
    dy=[0]*pieceNum
    parts=[0]*pieceNum
    pngs=[]
    pos=[]
    minx,miny,maxx,maxy=0,0,0,0#get the range of drawing block
    img=Image.open(filenamepic)#orign png file
    can=Image.new ("RGBA", (6000,6000))
    #get the images
    j=0
    l=len(b)
    for i in range(pieceNum+1):
        f1,f2=0,0
        f3,f4=0.0,0.0
        if p<l:
            f1,f2=struct.unpack('>2f',b[p:p+8])
            #f3,f4 need +5 in higher digit
            f3=unknownf3(b[p+8:p+12])
            f4=unknownf4(b[p+12:p+16])
        f1,f2=f1+3000.0,f2+3000.0  #center
        p+=16
        if i==partNum[j]:
            if i !=0 :
                part=can.crop((minx,miny,maxx+30,maxy+30))
                pngs.append(part)#images
                pos.append((minx,miny,maxx+30,maxy+30))
                if piece:
                    part.save(folder+"/"+str(j)+".png")
                    print("\tImage ",j," complete.")
                can=Image.new("RGBA", (6000,6000))#reset the Canvas
            j+=1
            minx,miny,maxx,maxy=int(f1),int(f2),int(f1),int(f2)
        tmp=img.crop((int(f3)-1,int(f4)-1,int(f3)+29,int(f4)+29))#piece block
        #tmp=img.crop((int(f3),int(f4),int(f3)+30,int(f4)+30))
        x,y=int(f1),int(f2)
        can.paste(tmp,(x,y))
        minx,maxx=min(minx,x),max(maxx,x)
        miny,maxy=min(miny,y),max(maxy,y)
    if Total:
        #get the total pictures
        if imageNum==1:
            pngs[0].save(folder+"/"+filenamepic[0:-4]+".png")
            return
        partType=[0]*imageNum
        partroot=[]
        partindex=[]
        j=0
        path=[-1]*7
        last=-1
        for i in range(imageNum+1):
            if i>=imageNum or int(partTree[i][3]/0x10)<=last :#last image is a leaf
                can=Image.new("RGBA", (6000,6000))
                minx,miny,maxx,maxy=pos[0]
                for k in range(last+1):
                    if path[k]!=-1:
                        x,y,z,w=pos[path[k]]
                        minx,maxx=min(minx,x),max(maxx,x)
                        miny,maxy=min(miny,y),max(maxy,y)
                        can.paste(pngs[path[k]],(x,y),mask=pngs[path[k]])
                part=can.crop((minx,miny,maxx,maxy))
                part.save(folder+"/"+filenamepic[0:-4]+"_"+str(j)+".png")
                print("\t"+filenamepic[0:-4]+"_"+str(j)+".png")
                j+=1
            if i<imageNum:
                last=int(partTree[i][3]/0x10)
                path[last]=i
        
            
def unknownf3(data):
    #data = struct.pack(">f",*fl)
    uni = struct.unpack("<i",data)[0]
    uni = uni + 5
    data = struct.pack("<i",uni)
    return struct.unpack(">f",data)[0]*2
    #I don't know why it needs to multiply by two, but it just works

def unknownf4(data):
    #data = struct.pack(">f",*fl)
    uni = struct.unpack("<i",data)[0]
    uni = uni + 5
    data = struct.pack("<i",uni)
    return struct.unpack(">f",data)[0]

def parseint(string):
    return int(''.join([x for x in string if x.isdigit()]))

def inttostrfill(inint, leng):
    string = str(inint)
    while(len(string) < leng):
        string = "0" + string
    return string
    
if __name__ =="__main__":
    if len(sys.argv) < 2 :
        print("usage: python",sys.argv[0]," layfile ")
        exit()
    files=[]
    files=sys.argv[1:]
    for k in files:
        main(k,piece=False)
    #os.system("pause")
