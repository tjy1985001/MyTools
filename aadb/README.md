When multiple Android devices are connected to computer, you must execute 'adb devices' to get device serial numbers and use '-s' to specify a device.<br/>
aadb could list all connected Android device serial numbers. You just need to input a prefix of any serial number and press enter key.

```Bash
export AADB=/Users/zongjingyao/Tools/MyTools/aadb #path for aadb
export PATH=$AADB:$PATH
alias aadb='aadb.py'
```

Example
```Bash
MyTools git:(master) ✗ aadb shell
1f588x50
9a5f4xc2

1	//input 1. Enter
shell@kenzo:/ $
