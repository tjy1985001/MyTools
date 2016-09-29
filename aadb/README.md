存在多台手机连接电脑时需要使用-s指定设备，每次都要执行adb devices获取设备号，aadb可以列出当前所有的设备号，只需要输入设备号的前缀即可选择当前设备，然后继续执行命令。

```Bash
export AADB=/Users/zongjingyao/Tools/MyTools/aadb
export PATH=$AADB:$PATH
alias aadb='aadb.py'

```Bash
MyTools git:(master) ✗ aadb shell
1f588x50
9a5f4xc2

1	//输入1，回车
shell@kenzo:/ $