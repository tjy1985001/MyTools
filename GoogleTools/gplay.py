#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from bs4 import BeautifulSoup
import requests


class GooglePlay(object):
    def __init__(self, package_name):
        self.__package_name = package_name
        self.__app_title = 'none'
        self.__author = 'none'
        self.__genre = 'none'
        self.__updated = 'none'
        self.__current_version = 'none'
        self.__get_app_info()

    @property
    def package_name(self):
        return self.__package_name

    @property
    def app_title(self):
        return self.__app_title

    @property
    def author(self):
        return self.__author

    @property
    def genre(self):
        return self.__genre

    @property
    def updated(self):
        return self.__updated

    @property
    def current_version(self):
        return self.__current_version

    def __get_app_info(self):
        base_url = 'https://play.google.com/store/apps/details'
        params = {'id': self.__package_name, 'hl': 'en'}
        resp = requests.get(url=base_url, params=params)
        soup = BeautifulSoup(resp.text, 'html.parser')
        app_title = soup.select('div[class="id-app-title"]')
        if app_title and app_title[0].text:
            self.__app_title = app_title[0].text
        author = soup.select('span[itemprop="name"]')
        if author and author[0].text:
            self.__author = author[0].text
        genre = soup.select('span[itemprop="genre"]')
        if genre and genre[0].text:
            self.__genre = genre[0].text
        updated = soup.select('div[itemprop="datePublished"]')
        if updated and updated[0].text:
            tmp_time = time.strptime(updated[0].text, "%B %d, %Y")
            self.__updated = time.strftime("%Y-%m-%d", tmp_time)
        current_version = soup.select('div[itemprop="softwareVersion"]')
        if current_version and current_version[0].text:
            self.__current_version = current_version[0].text.strip()


def main():
    app = GooglePlay('com.android.chrome')
    print app.package_name
    print app.app_title
    print app.author
    print app.genre
    print app.updated
    print app.current_version


if __name__ == '__main__':
    main()
