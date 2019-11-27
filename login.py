import requests
import time
import hashlib
import sensitive_info as si

# Fill in your details here to be posted to the login form.
url = "http://forums.novociv.org/login.php?do=login"
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}

# Grab security credentials from external file.
creds = si.SecurityCreds()
salt = creds.salt
md5_pass = creds.md5_pass
securitytoken = creds.securitytoken

data = {
    'vb_login_username': 'Python_Bot',
    'vb_login_password_hint': 'Password',
    'vb_login_password': '',
    's': '',
    'securitytoken': 'guest',
    'do': 'login',
    'vb_login_md5password': md5_pass,
    'vb_login_md5password_utf': md5_pass
}

session = requests.Session()

r = session.post(url, headers=headers, data=data, verify=False)

print("\nNew URL", r.url)
print("Status Code:", r.status_code)
print("History:", r.history)

print(r.text)

hash_str = str(int(time.time()))+'1690'+salt
print(hash_str)

m = hashlib.md5()
m.update(hash_str.encode('utf-8'))
posthash = m.hexdigest()
print(posthash)

post_data = {
    'subject': 'Sorry, another test',
    'message': 'Testing some security',
    's': '',
    'securitytoken': securitytoken,
    'f': '517',
    'do': 'postthread',
    'posthash': posthash,
    'poststarttime': str(int(time.time())),
    'loggedinuser': '1690',
    'sbutton': 'Submit New Thread'
}

r = session.post('http://forums.novociv.org/newthread.php', headers=headers, data=post_data, verify=False)

print("\nNew URL", r.url)
print("Status Code:", r.status_code)
print("History:", r.history)

print(r.text)