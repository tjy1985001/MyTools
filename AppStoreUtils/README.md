# appstore.py
A tool to request apps' basic info from iOS App Store

## Usage

```
LOOK_UP_BASE_URL = 'https://itunes.apple.com/cn/lookup?'
```
This is a url for China market in iOS App Store. You can change it to any country if you want.

```
appstore.py [-b bundleId] [-i appId] [-a apps] [-s save]
-b, --bundleId  Request info by bundle id.
-i, --appId     Request info by app id.
-a, --apps      Request infos from a file which contains many bundle ids or app ids.
                Each line example:
                    bundle id, app id
                    , app id
                    bundle id,
-s, --save      Save infos to file.
```

### Examples
```Bash
./appstore.py -b com.netease.qnyh
./appstore.py -i 1033387365
./appstore.py -a ./test_data/apps.txt -s ./test_data/infos.json
```

# check.py
A tool to check update for some offered apps.

## Usage

```
DATA_DIR = 'test_data/'
```
It's the default folder for saving app infos automatically. You can change it if you want.

```
check.py [-a apps] [-o old]
-a --apps   Same with appstore.py
-o --old    Old app infos to compare with new app infos. (Requested before)
```

### Examples
```
./check.py -a ./test_data/apps.txt -o ./test_data/infos.json
lookup:  com.netease.qnyh 1033387365
lookup:   1047961826
lookup:  com.gaeamobile.cn.xja2
The compared result was save in test_data/diff-2017-08-16 11.18.json
```