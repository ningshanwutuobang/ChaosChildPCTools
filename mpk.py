#!/usr/bin/env python3
import os,sys,struct

def main(filename):	
	infile = open(filename, 'rb')
	if not infile:
		print("cannot find ",ilename)
		return
	data = struct.unpack("4c",infile.read(4))
	if data != (b'M',b'P',b'K',b'\x00'):
		print("unknow file type!")
		return
	version, number = struct.unpack("<2I", infile.read(8))
	# if version == 0x00010000(65536) --> PSV special format
	# version == 0x00020000 --> normal
	
	infile.read(0x34)
	# start from 0x40
	
	#creat a folder 
	folder=filename[:-4]
	os.system("mkdir "+folder)
	#index table
	files=[]
	l=len(folder)-1
	count=[0]*number
	index=[0]*number
	length=[0]*number
	name=[0]*number
	floders=set()
	for i in range(number):
		if (version == 65536):
			tmp,index[i],length[i],tmp2,tmp3,tmp4,name[i]=struct.unpack("IIIIQQ224s",infile.read(0x100))
		else:
			tmp,count[i],index[i],length[i],tmp2,name[i]=struct.unpack("IIQQQ224s",infile.read(0x100))
		a=name[i].find(b'\x00')
		name[i]=name[i][:a]
		if a==0:
			number-=1
	for i in range(number):
		a=name[i].rfind(b'\\')
		fd=name[i][:a]
		#subdirectory
		if a>0 and not fd in floders:
			os.system("mkdir "+folder+"\\"+str(name[i][:a],"sjis"))
			floders.add(fd)
			a=fd.rfind(b'\\')-1
			while a>0:
				fd=fd[:a]
				floders.add(fd)
				a=fd.rfind(b'\\')-1
		infile.seek(index[i])
		print(str(name[i],"sjis"))
		out=open(folder+"\\"+str(name[i],"sjis"),"wb")
		out.write(infile.read(length[i]))
		out.close()
	infile.close()
		
		
	
	
	
if __name__ =="__main__":
	if len(sys.argv) < 2 :
		print("usage: python ",sys.argv[0]," mpkfiles ")
		exit()
	files=[]
	files=sys.argv[1:]
	for k in files:
		main(k)
	#os.system("pause")