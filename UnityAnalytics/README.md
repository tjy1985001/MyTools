# A tool to check Unity Analytics state.

## Android
If Unity Analytics is turned on:
1. [>=5.2]assets/bin/Data/Managed/UnityEngine.Analytics.dll exists.
2. [< 5.2]assets/bin/Data/Managed/UnityEngine.Cloud.Analytics.dll exists.


## iOS
If Unity Analytics is turned on:
1. [>=5.2]Classes/Native/Bulk_UnityEngine.Analytics_0.cpp exists.
2. [< 5.2]Classes/Native/Bulk_UnityEngine.Cloud.Analytics_0.cpp exists.

## Usage
### Android
```Bash
ua.py -android apk_path
```

### iOS
```Bash
ua.py -ios exported_ios_project_path
```

# AnalyticsCheck.cs
A script to notice you in Editor if Analytics is not enabled.
