import requests

# Fill in your details here to be posted to the login form.
url = "https://forums.novociv.org/login.php?do=login"
data = {
    'vb_login_username':'A',
    'vb_login_password_hint':'Password',
    'vb_login_password':'',
    's':'',
    'securitytoken':'1574248986-ca61a635192e4a54a8edbff241038ff2268b46b1',
    'do':'login',
    'vb_login_md5password':'7e9150ec2ee7cd544b719db1ff2cbbef',
    'vb_login_md5password_utf':'7e9150ec2ee7cd544b719db1ff2cbbef'
}

session = requests.Session()
r = session.post(url, headers=headers, data=data)