import requests
import time
import hashlib
import sensitive_info as si


class NewcivLogin:
    def __init__(self):
        self.url = "http://forums.novociv.org/login.php?do=login"
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

    # Not working
    def get_pagetext(self, post):
        print(self.post.text)

    def make_newthread(self, subject, message, forum):
        hash_str = str(int(time.time()))+'1690'+self.salt
        print(hash_str)

        m = hashlib.md5()
        m.update(hash_str.encode('utf-8'))
        posthash = m.hexdigest()
        print(posthash)

        post_data = {
            'subject': subject,
            'message': message,
            's': '',
            'securitytoken': self.securitytoken,
            'f': str(forum),
            'do': 'postthread',
            'posthash': posthash,
            'poststarttime': str(int(time.time())),
            'loggedinuser': '1690',
            'sbutton': 'Submit New Thread'
        }

        k = self.session.post('http://forums.novociv.org/newthread.php', headers=self.headers, data=post_data, verify=False)

        print("\nNew URL", k.url)
        print("Status Code:", k.status_code)
        # print(k.text)
        return k

    def make_newpost(self, message, thread):
        hash_str = str(int(time.time()))+'1690'+self.salt
        print(hash_str)

        m = hashlib.md5()
        m.update(hash_str.encode('utf-8'))
        posthash = m.hexdigest()
        print(posthash)

        post_data = {
            'message': message,
            'wysiwyg': '0',
            'fromquickreply': '1',
            's': '',
            'securitytoken': self.securitytoken,
            'do': 'postreply',
            't': str(thread),
            'p': 'who cares',
            'parseurl': '1',
            'loggedinuser': '1690'
        }

        k = self.session.post('http://forums.novociv.org/newreply.php', headers=self.headers, data=post_data, verify=False)

        print("\nNew URL", k.url)
        print("Status Code:", k.status_code)
        # print(k.text)
        return k


# TO DO LIST:
'''
    - Make easy page print function that outputs current view.
    - https://github.com/Damgaard/PyImgur - Make script upload images to imgur and produce bbcode.
    - Make function for Python_Bot to like a post.
    - Post a Battle Royale Simulation directly to forum with newciv_bot script.
    - Grab threadid when making new thread, so bot can reply to his own thread.
'''