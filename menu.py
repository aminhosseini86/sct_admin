from flask import url_for


class Menu:
    def __init__(self):
        self.__menu = [
            {'title': 'صفحه اصلی', 'icon': 'zmdi-home', 'link': url_for('index')},
            {'title': 'مدیریت اسکوتر', 'icon': 'zmdi-file', 'link': url_for('devices')},
        ]

    def generate(self):
        return self.__menu
