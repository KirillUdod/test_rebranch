import sys
import requests
from lxml import html
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QApplication, QPushButton, QTextEdit


_SECTIONS_REF = {
    'За сутки': '/top/',
    'За неделю': '/top/weekly/',
    'За месяц': '/top/monthly/',
    'За все время': '/top/alltime/',
}

_FORMAT = {
    'JSON',
    'YAML',
}

SITE_REF = 'http://habrahabr.ru'


class Parser(object):

    def __init__(self, page_ref):
        self.site_refer = SITE_REF
        self.parse_site(page_ref)

    def parse_site(self, page_ref):
        refer = self.site_refer + page_ref
        while True:
            response = requests.get(refer)
            parsed_body = html.fromstring(response.text)
            for post in parsed_body.cssselect('div.post'):
                hubs = ''
                for post_title in post.cssselect('a.post_title'):
                    post_title.text_content()
                    post_title.get('href')
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


class MenuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.href = '/top/'
        self.format = 'JSON'
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
        self.format_combo.activated[str].connect(self.format_combo_Activated)

        btn1 = QPushButton("Button 1", self)
        btn1.setGeometry(40, 140, 200, 35)

        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def buttonClicked(self):
        #Parser(self.href)
        if self.window2 is None:
            self.window2 = OutputWindow()
        self.window2.show()
        self.close()

    def sections_combo_Activated(self, text):
        self.href = _SECTIONS_REF.get(text)

    def format_combo_Activated(self, text):
        self.format = text


class OutputWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.create_output_window()

    def create_output_window(self):

        self.output = QTextEdit(self)
        self.output.move(150, 25)
        self.output.setReadOnly(True)
        self.output.setGeometry(10, 10, 695, 395)
        self.output.setLineWrapMode(QTextEdit.NoWrap);

        btn1 = QPushButton("Button 1", self)
        btn1.setGeometry(40, 140, 200, 35)

        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('QComboBox')
        self.show()

    def buttonClicked(self):
        self.close()

    def print_in(self, string):
        string += '\n'
        self.output.insertPlainText(string)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = MenuWindow()
    sys.exit(app.exec_())

    #site_refer = ""
    #pars = Parser(site_refer)

