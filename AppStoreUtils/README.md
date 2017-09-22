# appstore.py
A tool to request apps' basic info from iOS App Store

## Usage

```
LOOK_UP_BASE_URL = 'https://itunes.apple.com/cn/lookup?'
```
This is a url for China market in iOS App Store. You can change it to any country if you want.

```
appstore.py [-b bundleId] [-i appId] [-c configs] [-s save]
-b, --bundleId  Request info by bundle id.
-i, --appId     Request info by app id.
-c, --configs   Request infos from a configs file which contains many bundle ids or app ids.
-s, --save      Save infos to file.
```

### Examples
```Bash
./appstore.py -b com.netease.qnyh
./appstore.py -i 1033387365
./appstore.py -c ./configs.json -s ./test_data/infos.json
```

# check.py
A tool to check update for some offered apps.

## Usage
Add some bundle ids and app ids in configs.json.

```
check.py [-a apps] [-o old]
-c --configs   Same with appstore.py
-o --old       Old app infos to compare with new app infos. (Requested before)
```

### Examples
```
./check.py -c ./configs.json -o ./test_data/infos.json
lookup:  com.netease.qnyh 1033387365
lookup:   1047961826
lookup:  com.gaeamobile.cn.xja2
The compared result was save in test_data/diff-2017-08-16 11.18.json
```