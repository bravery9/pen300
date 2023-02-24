└─$ nmap -sV -sC  10.10.10.15 
Starting Nmap 7.92 ( https://nmap.org ) at 2023-02-22 12:16 EST
Nmap scan report for 10.10.10.15
Host is up (0.29s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
| http-methods: 
|_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND PROPPATCH SEARCH MKCOL LOCK UNLOCK PUT
| http-webdav-scan: 
|   Server Type: Microsoft-IIS/6.0
|   Server Date: Wed, 22 Feb 2023 17:17:04 GMT
|   WebDAV type: Unknown
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|_  Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK
|_http-title: Under Construction
|_http-server-header: Microsoft-IIS/6.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.08 seconds

```
200      GET       39l      159w     1433c http://10.10.10.15/
301      GET        2l       10w      149c http://10.10.10.15/images => http://10.10.10.15/images/
301      GET        2l       10w      158c http://10.10.10.15/aspnet_client => http://10.10.10.15/aspnet%5Fclient/
301      GET        2l       10w      153c http://10.10.10.15/_private => http://10.10.10.15/%5Fprivate/
301      GET        2l       10w      155c http://10.10.10.15/_vti_log => http://10.10.10.15/%5Fvti%5Flog/
301      GET        2l       10w      155c http://10.10.10.15/_vti_bin => http://10.10.10.15/%5Fvti%5Fbin/
301      GET        2l       10w      149c http://10.10.10.15/Images => http://10.10.10.15/Images/
301      GET        2l       10w      149c http://10.10.10.15/IMAGES => http://10.10.10.15/IMAGES/
301      GET        2l       10w      158c http://10.10.10.15/Aspnet_client => http://10.10.10.15/Aspnet%5Fclient/
301      GET        2l       10w      153c http://10.10.10.15/_Private => http://10.10.10.15/%5FPrivate/
301      GET        2l       10w      158c http://10.10.10.15/aspnet_Client => http://10.10.10.15/aspnet%5FClient/
301      GET        2l       10w      158c http://10.10.10.15/ASPNET_CLIENT => http://10.10.10.15/ASPNET%5FCLIENT/
301      GET        2l       10w      153c http://10.10.10.15/_PRIVATE => http://10.10.10.15/%5FPRIVATE/
301      GET        2l       10w      155c http://10.10.10.15/_VTI_LOG => http://10.10.10.15/%5FVTI%5FLOG/

```

