import requests
import time
import hashlib
import sensitive_info as si

class NewcivLogin:
    def __init__(self):
        self.url = "https://forums.novociv.org/login.php?do=login"
        self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}

        # Grab security credentials from external file.
        self.creds = si.SecurityCreds()
        self.salt = self.creds.salt
        self.md5_pass = self.creds.md5_pass
        self.securitytoken = self.creds.securitytoken

        self.data = {
            'vb_login_username': 'Python_Bot',
            'vb_login_password_hint': 'Password',
            'vb_login_password': '',
            's': '',
            'securitytoken': 'guest',
            'do': 'login',
            'vb_login_md5password': self.md5_pass,
            'vb_login_md5password_utf': self.md5_pass
        }
        self.session = requests.Session()
        self.r = self.session.post(self.url, headers=self.headers, data=self.data, verify=False)

        print("\nNew URL", self.r.url)
        print("Status Code:", self.r.status_code)

    def get_thread_contents(self, thread):
        response = self.session.get('https://forums.novociv.org/showthread.php?'+str(thread), headers=self.headers, data=None, verify=False)
        # response = self.session.get('http://forums.novociv.org/showthread.php?'+str(thread)).text

        print("\nNew URL", response.url)
        print("Status Code:", response.status_code)
        print(response.text)
        return response


new = NewcivLogin()
body = new.get_thread_contents(1054675).text
a = body.split('form')
b = a[1].split('securitytoken" value="')
c = b[1].split('"')
print(c[0])
