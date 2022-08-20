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

It supports webp format input now, which used by _Chaos Child Switch Version_.

View the final result with [MvlView](https://github.com/Manicsteiner/mvl_preview) for a better experience.

It supports some PS3 games now. Although it cannot be done in one step like lay.py, at least humans can understand it now. It uses methods from [RNE_image_converter](https://github.com/Manicsteiner/RNE_image_converter).

* lay_ps3_CC.py   for .lay files in chara.mpk , Available for _Chaos Child_,_Steins Gate 0_ PS3 vesion
need .png file in the same folder of .lay file
```
python3 lay_ps3_CC.py <layfile>
```
* lay_ps3_MO.py   for files without extension in chara.mpk , Available for _MO6，MO7,Chaos Head Love Chuchu,SGDarling_ PS3 vesion, Not available for _花咲くまにまに，SGPhenogam_
need those files in the same folder, just leave them and do not rename them. There is a small chance that some of those files will have an extension name of ".gax" or else, you even need to remove it manually.
```
python3 lay_ps3_MO.py <file>
```