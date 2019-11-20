import requests
#import sys

URL = "https://forums.novociv.org/login.php?do=login"

def main():
    session = requests.Session()

    # This is the form data that the page sends when logging in
    login_data = {
        'ips_username': '.',
        'ips_password': '.',
        'signin_options': 'submit',
        'redirect':'index.php?'
    }

    r = session.post(URL, data=login_data)

    # Try accessing a page that requires you to be logged in
    q = session.get('https://forums.novociv.org/newsearch.php')
    print(session.cookies)
    print(r.status_code)
    print(q.status_code)

    threadid = 0
    v = session.post('https://forums.novociv.org/newreply.php?do=postreply&t='.join(thread_id), data={
        'title': '',
        'message': 'This is posted from python',
        'wysiwyg': 0,
        'iconid': 0,
        'securitytoken': '.',
        'do': 'postreply',
        'loggedinuser': 0,
        'sbutton': 'Submit Reply',
        'parseurl': 1
    })
    print(v.status_code)
    print(v.text)


if __name__ == '__main__':
    main()