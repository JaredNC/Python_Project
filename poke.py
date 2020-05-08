import requests
import shutil
import sensitive_info as si
from bs4 import BeautifulSoup


class Bulba:
    def __init__(self):
        self.url = "https://bulbapedia.bulbagarden.net/wiki/Main_Page"
        self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}

        # Grab security credentials from external file.
        # self.creds = si.SecurityCreds()
        # self.salt = self.creds.salt

        self.session = requests.Session()
        self.r = self.session.get(self.url, headers=self.headers, data=None)

        print("\nNew URL", self.r.url)
        print("Status Code:", self.r.status_code)

    def get_pokemon_by_number(self, number):
        response = self.session.get('https://bulbapedia.bulbagarden.net/wiki/' + str(number).zfill(3), headers=self.headers, data=None)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = 'https://bulbapedia.bulbagarden.net' + soup.find(id='mw-content-text').li.a.get('href')
        return link

    def get_page_by_number(self, number):
        response = self.session.get(self.get_pokemon_by_number(number), headers=self.headers, data=None)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_image_by_number(self, number):
        page = self.get_page_by_number(number)
        path = page.find('a', title=page.h1.get_text().split(" ")[0]).get('href')
        link = 'https://bulbapedia.bulbagarden.net' + path
        response = self.session.get(link, headers=self.headers, data=None)
        soup = BeautifulSoup(response.text, 'html.parser')
        image = 'http:' + soup.find('div', id='file').img.get('src')
        return image

    def get_type_by_number(self,number):
        page = self.get_page_by_number(number)
        ptype = page.find('a', title="Type")
        return ptype.find_next('b').get_text()

    # def get_evo_by_number(self,number):
    #     page = self.get_page_by_number(number)
    #     table = page.find('span', id="Evolution").find_next('table')

    def create_query_string(self,n1,n2):
        qry = 'INSERT INTO\n' \
              '`poke_mon` (`monname`, `type`, `evolution`)\n' \
              'VALUES\n'
        values = []
        for poke in range(n1, n2+1):
            page = self.get_page_by_number(poke)
            name = page.h1.get_text().split(" ")[0]
            p_type = self.get_type_by_number(poke)
            values.append('("{}","{}",0)'.format(name, p_type))
            image = self.get_image_by_number(poke)
            r = requests.get(image, stream=True)
            if r.status_code == 200:
                with open("imgs/" + image.split('/')[-1], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                print(name + ": " + image)
        qry += ' , \n' \
               ''.join(values)
        return qry


def scrape_icons(loop):
    creds = si.SecurityCreds()

    a = creds.string

    loop = loop

    claims = a.splitlines()
    for claim in claims:
        mmm = claim.split()
    #    print(mmm)
        name = str(loop)
        r = requests.get(mmm[5][10:-1], stream=True)
        if r.status_code == 200:
            with open("img/"+name+".png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        #urllib.request.urlretrieve(mmm[5][10:-1], name)
        loop += 1
        print(mmm[5][10:-1])