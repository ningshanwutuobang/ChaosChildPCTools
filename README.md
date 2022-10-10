# ChaosChildPCTools

Tools for Chaos;Child PC files.

dealing with following file format:
* mpk.py   for .mpk files 
```
python3 mpk.py <mpkfile>
```
* lay.py   for .lay files in chara.mpk
need .png file in the same folder of .lay file
```
python3 lay.py <layfile>
```
* mvl.py   for .mvl files in chara.mpk
need .png file in the same folder of .mvl file
```
python3 mvl.py <mvlfile>
```
* gxt.py   for .mvl files
convert .gxt file to .png file
```
python3 gxt.py <gxtfile>
```

* view.html for index.json and *.png
A simple viewer for *.png file located by index.json .
Copy it into the location of index.json and open it.


## What's New
Use mvl+png_or_webp_all_in_one.py to convert all in one click.

It's developed by sfjsdgf@tieba in 2021.7.1. [View the original post](https://tieba.baidu.com/p/7430852836 "[教程向]一步一步教你提取Mo8、Mo8fd的立绘")

It supports webp format input now, which used by _Chaos Head Noah_ and _Chaos Child_ Switch Version.

View the final result with [MvlView](https://github.com/Manicsteiner/mvl_preview) for a better experience.

It supports some PS3 games now, and works almost perfectly. It uses methods from [RNE_image_converter](https://github.com/Manicsteiner/RNE_image_converter).

* lay_ps3_CC.py   for .lay files in chara.mpk , Available for _Chaos Child_,_Steins Gate 0_ PS3 vesion

Need .png file in the same folder of .lay file
```
python3 lay_ps3_CC.py <layfile>
```
* lay_ps3_MO.py   for files without extension in chara.mpk , Available for _Memories Off 6,Memories Off 7,Chaos Head Love Chuchu,Steins Gate,SGDarling,花咲くまにまに_ PS3 vesion, Not available for _SGPhenogam_

Need those files in the same folder, just leave them and do not rename them.

There is a small chance that some of those files will have an extension name of ".gax" or else, you even need to remove it manually.
```
python3 lay_ps3_MO.py <file>
```

* mvl_steam_CHN.py , simple_file_renamer.py  for _Chaos Head Noah_ Steam Version. 

Need those files in the same folder.

 _Chaos Head Noah_ Steam Version used .wav extension name for all webp files, just use the simple file renamer to change the file extension name or change it by yourself, it will become the same as a normal webp file. Whether you renamed it or not, mvl\_steam\_CHN.py will work, but please do not change the numbers.
```
python3 mvl_steam_CHN.py <file>
```