from PIL import Image
import zlib
import os,sys,struct

def main(filename,piece=True,Total=True):
	if filename.endswith(".png"):
		filename=filename[:-4]+"_.lay"
	elif not filename.endswith("_.lay"):
		filename=filename+"_.lay"	
	infile = open(filename, 'rb')
	if not infile:
		print("cannot find ",ilename)
		return
	#使用zlib解压
	b=b''
	decompress = zlib.decompressobj()
	data = infile.read(1024)
	while data:
		b+=decompress.decompress(data)
		data = infile.read(1024)
	#建立文件夹
	p=0
	folder=filename[0:filename.index('_.')]
	os.system("mkdir "+folder)
	#文件头为数量信息
	imageNum,pieceNum = struct.unpack("<2I",b[p:p+8])
	print("Image have ",imageNum," parts.")
	p+=8
	#接着为像素块信息
	partNum=[]
	partTree=[]
	j=0
	for i in range(imageNum):
		a=struct.unpack("<4b",b[p:p+4])
		partTree.append(a)
		partNum.append(struct.unpack("<I",b[p+4:p+8])[0])#每大块的小块数
		p+=12
		j+=1
	partNum.append(pieceNum)
	#初始画板#像素块
	dx=[0]*pieceNum
	dy=[0]*pieceNum
	parts=[0]*pieceNum
	pngs=[]
	pos=[]
	minx,miny,maxx,maxy=0,0,0,0#确定还原后的图片大小
	img=Image.open(filename[0:filename.index('_.')]+'.png')#未还原的原始图片
	can=Image.new ("RGBA", (4000,2000))
	#获得每个大块
	j=0
	for i in range(pieceNum+1):
		f1,f2,f3,f4=struct.unpack('<4f',b[p:p+16])
		f1,f2=f1+2000.0,f2+1000.0  #居中
		p+=16
		if i==partNum[j]:
			if i !=0 :
				part=can.crop((minx,miny,maxx+30,maxy+30))
				pngs.append(part)#大块
				pos.append((minx,miny,maxx+30,maxy+30))
				if piece:
					part.save(folder+"/"+str(j)+".png")
					print("\tImage ",j," complete.")
				can=Image.new("RGBA", (4000,2000))#重置画板
			j+=1
			minx,miny,maxx,maxy=int(f1),int(f2),int(f1),int(f2)
		tmp=img.crop((int(f3)-1,int(f4)-1,int(f3)+31,int(f4)+31))#裁剪小块
		x,y=int(f1),int(f2)
		can.paste(tmp,(x,y))
		minx,maxx=min(minx,x),max(maxx,x)
		miny,maxy=min(miny,y),max(maxy,y)
	if Total:
		#组合大块得到立绘
		if imageNum==1:
			pngs[0].save(folder+"/"+filename[0:-4]+".png")
			return
		partType=[0]*imageNum
		partroot=[]
		partindex=[]
		j=0
		path=[0]*2
		for i in range(imageNum):
			if (partTree[i][3]==0x40 or partTree[i][3]==0x60) :
				can=Image.new("RGBA", (4000,2000))
				can.paste(pngs[path[0]],(pos[path[0]][0],pos[path[0]][1]))
				can.paste(pngs[path[1]],(pos[path[1]][0],pos[path[1]][1]))
				can.paste(pngs[i],(pos[i][0],pos[i][1]))
				part=can.crop(pos[path[0]])
				part.save(folder+"/"+filename[0:-4]+"_"+str(j)+".png")
				print("\t"+filename[0:-4]+"_"+str(j)+".png")
				j+=1
				continue
			path[int(partTree[i][3]/0x20)]=i
			
			
	
if __name__ =="__main__":
	if len(sys.argv) < 2 :
		print("usage: python",sys.argv[0]," layfile ")
		exit()
	files=[]
	files=sys.argv[1:]
	for k in files:
		main(k,piece=False)
	#os.system("pause")