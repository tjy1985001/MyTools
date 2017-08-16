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