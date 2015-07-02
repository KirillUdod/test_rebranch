import sys
import requests
import datetime
import json
import yaml

from lxml import html
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QApplication, QPushButton, QTextEdit
from datetime import date, timedelta



_SECTIONS_REF = {
    'За сутки': '/top/',
    'За неделю': '/top/weekly/',
    'За месяц': '/top/monthly/',
    'За все время': '/top/alltime/',
}

_FORMAT = {
    'JSON': '.json',
    'YAML': '.yml',
}

SITE_REF = 'http://habrahabr.ru'
FILE_NAME = 'text'


class Parser(object):

    def __init__(self):
        self.site_refer = SITE_REF

    def parse_site(self, page_ref, format):

        refer = self.site_refer + page_ref
        if format[-5:] == ".json":
            with open("text.json", mode='w', encoding='utf-8') as f:
                json.dump([], f)
        elif format[-4:] == ".yml":
            with open("text.yml", mode='w', encoding='utf-8') as f:
                yaml.dump([], f)

        while True:
            response = requests.get(refer)
            parsed_body = html.fromstring(response.text)
            result = ''
            for post in parsed_body.cssselect('div.post'):

                hubs = ''

                for p_t in post.cssselect('a.post_title'):
                    post_title = p_t.text_content()
                    post_href = p_t.get('href')

                for hub in post.cssselect('a.hub'):
                    hubs = hubs + hub.text_content() + ', '

                for author in post.cssselect('div.author'):
                    for i in author.cssselect('a'):
                        name_author = i.text_content()
                #рейтинг поста или автора?
                #автора
                    for i in author.cssselect('span.rating'):
                        rating = i.text_content()
                #поста
                for i in post.cssselect('span.score'):
                    post_rating = i.text_content()

                post_date = ''
                for i in post.cssselect('published'):
                    date = i.text_content()
                    t = datetime
                    if date.find('вчера'):
                        t.date.day = date.today() - timedelta(1)
                    elif date.find('сегодня'):
                        t.date.day = date.today()
                    # else:
                    #     t.date.day =

                result += post_title + '\n' + post_date + '\n' + hubs[:-2] + '\n' + name_author + '\n' + post_rating \
                          + '\n\n'
                self.write_to(format, post_title, post_date, hubs[:-2], name_author, rating, post_href)

            next_page = parsed_body.cssselect('a.next')
            if not next_page:
                break
            else:
                for i in next_page:
                    refer = self.site_refer + i.get('href')
        return result

    def write_to(self, file_name, n, d, t, a, r, u):
        if file_name[-5:] == ".json":
            with open(file_name, mode='r', encoding='utf-8') as feedsjson:
                f = json.load(feedsjson)
            with open(file_name, "w+") as outfile:
                f.append({'name': n,
                           'publication_date': d,
                           'tags': t,
                           'author': a,
                           'rating': r,
                           'url': u
                           })
                json.dump(f, outfile, indent=4)
        elif file_name[-4:] == ".yml":
            with open(file_name, mode='r', encoding='utf-8') as feeds:
                f = yaml.load(feeds)
                f.append({'name': n,
                           'publication_date': d,
                           'tags': t,
                           'author': a,
                           'rating': r,
                           'url': u
                           })
            with open(file_name, 'w+') as outfile:
                outfile.write(yaml.dump(f, default_flow_style=True))



class MenuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.href = '/top/'
        self.file_name = FILE_NAME + '.json'
        self.window2 = None
        self.create_main_window()

    def create_main_window(self):

        lbl1 = QLabel("Choose needed section", self)
        lbl1.setGeometry(40, 0, 200, 35)

        self.sections_combo = QComboBox(self)
        for ref in _SECTIONS_REF:
            self.sections_combo.addItem(ref)
        self.sections_combo.setGeometry(40, 35, 200, 35)

        lbl2 = QLabel("Choose needed format", self)
        lbl2.setGeometry(40, 70, 200, 35)

        self.format_combo = QComboBox(self)
        for form in _FORMAT:
            self.format_combo.addItem(form)
        self.format_combo.setGeometry(40, 105, 200, 35)

        self.sections_combo.activated[str].connect(self.sections_combo_Activated)
        self.sections_combo.setCurrentIndex(int(self.sections_combo.findText('За сутки')))

        self.format_combo.activated[str].connect(self.format_combo_Activated)
        self.format_combo.setCurrentIndex(int(self.format_combo.findText('JSON')))

        btn1 = QPushButton("GO", self)
        btn1.setGeometry(40, 140, 200, 35)

        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Main')
        self.show()

    def buttonClicked(self):
        pars = Parser()

        if self.window2 is None:
            self.window2 = OutputWindow(str(pars.parse_site(self.href, self.file_name)))
        self.window2.show()
        self.close()

    def sections_combo_Activated(self, text):
        self.href = _SECTIONS_REF.get(text)

    def format_combo_Activated(self, text):
        self.file_name = FILE_NAME + _FORMAT.get(text)


class OutputWindow(QMainWindow):

    def __init__(self, text):
        super().__init__()
        self.create_output_window(text)

    def create_output_window(self, text):

        self.output = QTextEdit(self)
        self.output.move(150, 25)
        self.output.setReadOnly(True)
        self.output.setGeometry(10, 10, 690, 350)
        self.output.setLineWrapMode(QTextEdit.NoWrap);
        self.output.insertPlainText(text)

        btn1 = QPushButton("Exit", self)
        btn1.setGeometry(40, 365, 200, 35)

        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('Result')
        self.show()

    def buttonClicked(self):
        self.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = MenuWindow()
    sys.exit(app.exec_())

    #site_refer = ""
    #pars = Parser(site_refer)

