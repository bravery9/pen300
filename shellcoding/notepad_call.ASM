mov eax,1
push eax
call there
db "notepad.exe c:\windows\system32\drivers\etc\hosts",0
there:
call WinExec