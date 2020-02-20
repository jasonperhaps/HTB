from cmd import Cmd
import requests
import pprint as pp
import json

class Terminal(Cmd):
    prompt = '> '

    def __init__(self):
        self.auth = self.do_login("zapper zapper")
        Cmd.__init__(self)

    def api_call(self, method, params, auth, id):
        url = 'http://10.10.10.108/zabbix/api_jsonrpc.php'
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "auth": auth,
            "id": id,
        }
        headers = {'content-type': 'application/json', }
        response = requests.post(url, data=json.dumps(payload), headers=(headers))
        return response.json()

    def do_login(self, args):
        user, password = args.split()
        params = {
            "user": user,
            "password": password,
        }
        auth = self.api_call("user.login", params, None, 0)
        return auth["result"]

    def do_userCreate(self, args):
        user, passwd = args.split()
        params = {
            "alias": user,
            "name": user,
            "passwd": passwd,
            "usrgrps": [{ "usrgrpid": "7" }]
        }
        output = self.api_call("user.create", params, self.auth, 0)
        pp.pprint(output)

    def do_jason(self, args):
        print(self.auth)


terminal = Terminal()
terminal.cmdloop()

