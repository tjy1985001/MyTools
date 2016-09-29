notepadExe = "C:\Program Files (x86)\Notepad++\notepad++.exe"
scriptFile = "C:\Program Files\AutoHotkey\MyAutoHotKey.ahk"
tortoiseSvnExe = "C:\Program Files\TortoiseSVN\bin\TortoiseProc.exe"
projectDir = "TODO"


; 打开快捷键脚本文件
#z::
	Run %notepadExe% %scriptFile%
Return

#n::
	Run %notepadExe%
Return

; SVN更新
#u::
	Run %tortoiseSvnExe% /command:update /path:%projectDir%
Return

; SVN提交
#c::
	Run %tortoiseSvnExe% /command:commit /path:%projectDir%
Return

; SVN日志
#g::
	Run %tortoiseSvnExe% /command:log /path:%projectDir%
Return

; TeamToy
#t::
	Run "http://192.168.110.4:10086/?c=dashboard"
Return

; Baidu
#b::
	Run "http://www.baidu.com"
Return

; 一键安装APK文件
#i::
    fullName := GetSelectedFileFullName()
	SplitPath, fullName, , , ext
    If ext = apk
    {
        ;MsgBox , %fullName%
		Run, %comspec% /k adb install -r %fullName%
    }
	else
	{
	    MsgBox , 不是APK文件
	}
    Return


;获取选中文件的路径（包含文件名）
GetSelectedFileFullName()
{
    send ^c
	sleep,200
	Return clipboard
}

;获取选中文件的路径（不包含文件名）
GetSelectedFilePath()
{
    fullName := GetSelectedFileFullName()
    SplitPath, fullName, , dir
    Return dir
}

;获取选文件的文件名
GetSelectedFileName()
{
    fullName := GetSelectedFileFullName()
    SplitPath, fullName, name
    Return name
}

;获取选中的文件夹路径
GetSelectedFolderPath()
{
    Return GetSelectedFileName()
}