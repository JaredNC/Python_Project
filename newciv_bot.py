import requests
import time
import hashlib
import sensitive_info as si
from bs4 import BeautifulSoup


class NewcivLogin:
    def __init__(self):
        self.url = "https://forums.novociv.org/login.php?do=login"
        self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}

        # Grab security credentials from external file.
        self.creds = si.SecurityCreds()
        self.salt = self.creds.salt
        self.md5_pass = self.creds.md5_pass
        # self.securitytoken = self.creds.securitytoken

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
        self.r = self.session.post(self.url, headers=self.headers, data=self.data)

        print("\nNew URL", self.r.url)
        print("Status Code:", self.r.status_code)

        response = self.session.get('https://forums.novociv.org/showthread.php?1001177', headers=self.headers, data=None)
        a = response.text.split('form')
        b = a[1].split('securitytoken" value="')
        c = b[1].split('"')
        self.securitytoken = c[0]

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

        k = self.session.post('https://forums.novociv.org/newthread.php', headers=self.headers, data=post_data)

        print("\nNew URL", k.url)
        print("Status Code:", k.status_code)
        # print(k.text)
        return k

    def get_thread_contents(self, thread):
        response = self.session.get('https://forums.novociv.org/showthread.php?' + str(thread), headers=self.headers, data=None)
        # response = self.session.get('https://forums.novociv.org/showthread.php?'+str(thread)).text

        print("\nNew URL", response.url)
        print("Status Code:", response.status_code)
        # print(response.text)
        return response

    def get_post_contents(self, post):
        response = self.session.get('https://forums.novociv.org/showthread.php?p=' + str(post) + '&viewfull=1#post' +
                                    str(post), headers=self.headers, data=None)
        # p1 = response.text.split('<div class="Oldwindowbg2" id="post' + str(post) + '">')[1]
        # p2 = p1.split('<!-- attachments -->')[0]
        # p3 = p2.split('member.php?')[1]
        soup = BeautifulSoup(response.text, 'html.parser')
        p1 = soup.find(id='post' + str(post))
        p2 = p1.findNext('div')

        text = dict()
        t1 = p1.get_text().strip() + ': ' + p2.get_text()
        text['text'] = t1.rsplit("\n", 6)[0]
        text['url'] = response.url
        print("\nNew URL", response.url)
        print("Status Code:", response.status_code)
        # print(p3)
        return text

    def get_team(self, team_id):
        if str(team_id).split('*')[0] == "Random":
            response = self.session.get('https://forums.novociv.org/pokemon.php?section=team&do=view_raw_r&lvl=' +
                                        team_id.split('*')[1], headers=self.headers, data=None)
        elif str(team_id).split('*')[0] == "Gym":
            response = self.session.get('https://forums.novociv.org/pokemon.php?section=team&do=view_raw_g&lvl=' +
                                        team_id.split('*')[1] + '&gen=' + team_id.split('*')[2] + '&gym=' +
                                        team_id.split('*')[3], headers=self.headers, data=None)
        else:
            response = self.session.get('https://forums.novociv.org/pokemon.php?section=team&do=view_raw&deck=' +
                                        str(team_id), headers=self.headers, data=None)

        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(id='team_dump')

        if div.get_text() == '0':
            return False
        else:
            ps = div.findAll('p')
            out = []
            for x in ps:
                out.append(x.get_text())
            name = soup.find(id='team_owner').get_text()
            user_id = soup.find(id='team_owner_id').get_text()
            return out, name, user_id

    def reward_team(self, team, lvl):

        post_data = {
            'team': team,
            'exp': lvl
        }

        k = self.session.post('https://forums.novociv.org/pokemon.php?section=battle&do=battle', headers=self.headers, data=post_data)

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

        k = self.session.post('https://forums.novociv.org/newreply.php', headers=self.headers, data=post_data)

        print("\nNew URL", k.url)
        print("Status Code:", k.status_code)
        # print(k.text)
        return k


# TO DO LIST:
'''
    - Make easy page print function that outputs current view.
    - Make function for Python_Bot to like a post.
    - Post a Battle Royale Simulation directly to forum with newciv_bot script.
    - Grab threadid when making new thread, so bot can reply to his own thread.
'''