import requests
from bs4 import BeautifulSoup
import keys


class HTMLParser:
    def __int__(self):
        pass

    def parse_url_title(self):
        self.html = requests.get(keys.url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })
        self.htmlParse = BeautifulSoup(self.html.content, "html.parser")
        # https://www.reddit.com/r/learnpython/comments/7r4xd9/beautifulsoup_returning_nonetype_on_a_find_method/
        # was returning nonetype, answer from c17r w/ headers & etc solved it
        title = self.htmlParse.select_one("div > h1:nth-of-type(1)", class_="_eYtD2XCVieq6emjKBH3m")

        return title.getText()

    def find_p_tag_instance(self, p_tag_instance):
        self.html = requests.get(keys.url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })
        self.htmlParse = BeautifulSoup(self.html.content, "html.parser")
        # Find number of p tags present on this individual page (p_tag_instance)
        keep_looping = True
        while keep_looping:
            for value in self.htmlParse.select_one("div > p:nth-of-type(" + str(p_tag_instance) + ")",
                                              class_="_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM Post t3_ocx94s "):
                if p_tag_instance != None or value != None:
                    p_tag_instance += 1
                if self.htmlParse.select_one("div > p:nth-of-type(" + str(p_tag_instance) + ")",
                                        class_="_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM Post t3_ocx94s ") is None:
                    print("This is the end")
                    keep_looping = False
        # Original code had p_tag_instance = p_tag_instance  - 1, had to add 2 additional because it was getting extra paragraphs with bot & etc.
        print(f" P_tag_instance from line 159 is: {p_tag_instance}")

        return p_tag_instance

    def parse_p_tag(self, p_tag):
        self.html = requests.get(keys.url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })
        self.htmlParse = BeautifulSoup(self.html.content, "html.parser")
        # https://www.reddit.com/r/learnpython/comments/7r4xd9/beautifulsoup_returning_nonetype_on_a_find_method/
        # was returning nonetype, answer from c17r w/ headers & etc solved it
        # para = htmlParse.select_one("div > p:nth-of-type(" + str(p_tag) + ")",
        #                            class_="_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM Post t3_ocx94s ")
        para = self.htmlParse.select_one("div > p:nth-of-type(" + str(p_tag) + ")",
                                    class_="_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM Post t3_ocx94s ")
        return para.getText()


