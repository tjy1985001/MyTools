# MakeGif
使用Python将一整张图的序列帧合成gif图片，目前还只是个Demo。

## 依赖库
* PIL
* numpy
* images2gif<br>
直接使用pip或者easy_install安装的images2gif有问题，最好下载源码包，做如下修改后放在makeGif.py同级目录直接引用即可。<br>
images2gif.py中第426行
```Python
425 for im in images:
426    palettes.append( getheader(im)[1] )
```
改为
```Python
425 for im in images:
426    palettes.append( im.palette.getdata()[1] )
```
## 使用方法
```Bash
./makeGif.py 源图片路径 行数 列数 目标图片路径
./makeGif.py test.png 1 4 result.gif
```