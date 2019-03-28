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
