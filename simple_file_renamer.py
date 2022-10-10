import os

def renamefile(file,ext):
    if file.endswith(ext):
        os.rename(file,file[:-4]+".webp")


if __name__ == '__main__':
    for root,dirs,files in os.walk('./'):
        for file in files:
            renamefile(file,".wav")