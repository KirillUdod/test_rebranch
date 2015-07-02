import requests  
from lxml import html


HREFS = {

}

class Parser(object):

    def __init__(self):
        self.site_refer = 'http://habrahabr.ru'

    def parse_site(self, page_ref):
        refer = self.site_refer + page_ref
        while True:
            response = requests.get(refer)
            parsed_body = html.fromstring(response.text)
            for post in parsed_body.cssselect('div.post'):
                hubs = ''
                for post_title in post.cssselect('a.post_title'):
                    print(post_title.text_content())
                    print(post_title.get('href'))
                for hub in post.cssselect('a.hub'):
                    hubs = hubs + hub.text_content() + ', '
                print(hubs[:-2])
                for author in post.cssselect('div.author'):
                    for name_author in author.cssselect('a'):
                        print(name_author.text_content())
                #рейтинг поста или автора?
                #автора
                    for rating in author.cssselect('span.rating'):
                       print(rating.text_content())
                #поста
                for post_rating in post.cssselect('span.score'):
                    print(post_rating.text_content())
            next_page = parsed_body.cssselect('a.next')
            if not next_page:
                break
            else:
                for i in next_page:
                    refer = self.site_refer + i.get('href')


if __name__ == "__main__":
    pars = Parser()
    pars.parse_site('/top/')

