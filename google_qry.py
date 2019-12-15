# Original Code from:
# https://towardsdatascience.com/build-a-simple-chatbot-with-python-and-google-search-c000aa3f73f0

import requests
import string
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup

# to search
# print(chatbot_query('how old is samuel l jackson'))


def chatbot_query(query, index=0, tries=5):
    fallback = 'Sorry, I cannot think of a reply for that.'
    result = ''

    try:
        search_result_list = list(search(query+" -site:youtube.com", tld="co.in", num=10, stop=tries, pause=1))

        # page1 = requests.get(search_result_list[index])
        # page2 = requests.get(search_result_list[index+1])
        # page3 = requests.get(search_result_list[index+2])
        # page = page1 + page2 + page3

        counter = index
        while (counter < tries) & (result == ''):
            page = requests.get(search_result_list[counter])

            # tree = html.fromstring(page.content)

            soup = BeautifulSoup(page.content, features="lxml")
            # print(soup)

            article_text = ''
            article = soup.findAll('p')
            for element in article:
                article_text += '\n' + ''.join(element.findAll(text = True))
            article_text = article_text.replace('\n', '')
            first_sentence = article_text.split('.')
            first_sentence = first_sentence[0]
            # first_sentence = first_sentence[0] + " " + first_sentence[1] + " " + first_sentence[2]
            # first_sentence = article_text[:500] + '..'

            chars_without_whitespace = first_sentence.translate(
                { ord(c): None for c in string.whitespace }
            )

            if len(chars_without_whitespace) > 0:
                result = first_sentence + '.'
                return result
            else:
                result = ''
                print('Failed '+str(counter))
                counter += 1
        return fallback
    except:
        if len(result) == 0: result = fallback
        return result
