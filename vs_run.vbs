Option Explicit
' 无控制台启动 vs_run.py，隐藏窗口
Dim fso, sh, folder, script
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")

folder = fso.GetParentFolderName(WScript.ScriptFullName)

' 优先使用 .pyw（若存在），否则用 .py
If fso.FileExists(folder & "\vs_run.pyw") Then
  script = folder & "\vs_run.pyw"
Else
  script = folder & "\vs_run.py"
End If

' 使用 pythonw 启动（无控制台），0=隐藏窗口，False=不等待
sh.Run "pythonw """ & script & """", 0, False