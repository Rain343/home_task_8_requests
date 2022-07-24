import requests
import os
import datetime
from pprint import pprint


class Superheroes():
    def __init__(self):
        self.url = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'
        self.res = requests.get(self.url).json()

    def get_intelligence(self, list_superheroes):
        superheroes = []
        for superhero in self.res:            
            if superhero['name'] in list_superheroes:
                superheroes.append(superhero)
                continue
        best_intelligence = max(superheroes, key=lambda x: x['powerstats']['intelligence'])
        return f'Самый умный супергерой - {best_intelligence["name"]}'


class YaUploader:
    def __init__(self, token):
        self.token = token
    
    def __get_header(self):
        return {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def __get_link_to_upload(self, file_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.__get_header()
        params = {'path': file_path, 'overwrite': 'true'}
        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def upload(self, file_path, filename):
        """Метод загружает файл на яндекс диск"""
        url = self.__get_link_to_upload(filename)
        res = requests.put(url['href'], files={'file':open(file_path, 'rb')})
        res.raise_for_status()
        if res.status_code == 201:
            print("Success")


class StackOverflow():
    def __init__(self):
        self.url = 'https://api.stackexchange.com/2.3/questions'

    def __get_unix_time(self, day_offset=0):
        date = datetime.datetime.today()
        date_unix = round(datetime.datetime(
            date.year, date.month, date.day-day_offset, 0, 0).timestamp())
        return date_unix

    def get_questions_last_2_day(self):
        params = {
            'fromdate': self.__get_unix_time(),
            'todate': self.__get_unix_time(-2),
            'order': 'desc',
            'sort': 'creation',
            'tagged': 'python',
            'site': 'stackoverflow'
        }
        res = requests.get(self.url, params=params).json()
        return res

    def get_title_in_questions(self):
        questions = []
        for title in self.get_questions_last_2_day()['items']:
            questions.append(title['title'])
        return questions


if __name__ == '__main__':
    list_superheroes = ['Hulk', 'Captain America', 'Thanos']
    superheroes = Superheroes()

    print(superheroes.get_intelligence(list_superheroes))


    filename = 'i_want_to_yandex.txt'
    token = 'ваш_токен'
    path_to_file = os.path.join(os.getcwd(), filename)
    uploader = YaUploader(token)

    uploader.upload(path_to_file, filename)


    stackoverflow = StackOverflow()

    pprint(stackoverflow.get_title_in_questions())

