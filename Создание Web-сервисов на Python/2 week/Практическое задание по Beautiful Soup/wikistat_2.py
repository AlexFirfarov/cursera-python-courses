from bs4 import BeautifulSoup
import unittest
import os
import re


def number_of_images(html, cond=lambda tag: True):
    cnt = 0
    images = html.find_all('img')
    for img in images:
        if cond(img):
            cnt += 1
    return cnt


def number_of_headers(html, cond=lambda tag: True):
    cnt = 0
    headers = html.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for h in headers:
        if cond(h):
            cnt += 1
    return cnt


def max_links_len(html):
    max_len = 0
    links = html.find_all('a')

    for link in links:
        siblings = link.find_next_siblings()
        cur_len = 0
        for tag in siblings:
            if tag.name == 'a':
                cur_len += 1
            else:
                break
        if cur_len > max_len:
            max_len = cur_len
    return max_len + 1


def number_of_lists(html):
    cnt = 0
    lists = html.find_all(['ol', 'ul'])
    for l in lists:
        parents = l.find_parents()
        parents_names = [tag.name for tag in parents]
        if 'ol' not in parents_names and 'ul' not in parents_names:
            cnt += 1
    return cnt


def parse(path, page):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError

    with open(os.path.join(path, page), encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        body = soup.find('div', id='bodyContent')

        imgs = number_of_images(body, lambda tag: tag.has_attr('width') and float(tag['width']) >= 200)
        headers = number_of_headers(body, lambda tag: list(tag.strings)[0][0] in ('E', 'T', 'C'))
        linkslen = max_links_len(body)
        lists = number_of_lists(body)

    return [imgs, headers, linkslen, lists]


def get_adj_pages(path, page):
    with open(os.path.join(path, page), encoding='utf-8') as f:
        links = re.findall(r"(?<=/wiki/)[\w()]+", f.read())
    return links


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    pages_in_dir = set(os.listdir(path))

    queue = [start_page]
    used = {page: False for page in pages_in_dir}
    p = {page: -1 for page in pages_in_dir}

    used[start_page] = True
    while len(queue):
        v = queue.pop(0)
        adj_pages = get_adj_pages(path, v)
        for adj_page in adj_pages:
            if adj_page in pages_in_dir and not used[adj_page]:
                used[adj_page] = True
                queue.append(adj_page)
                p[adj_page] = v

    path_to_page = []
    v = end_page
    while v != -1:
        path_to_page.append(v)
        v = p[v]

    path_to_page.reverse()
    return path_to_page


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    path_to_page = build_bridge(path, start_page, end_page)
    statistics = {page: parse(path, page) for page in path_to_page}

    return statistics


# Набор тестов для проверки студентами решений по заданию "Практическое задание
# по Beautiful Soup - 2". По умолчанию файл с решением называется solution.py,
# измените в импорте название модуля solution, если файл с решением имеет другое имя.


STATISTICS = {
    'Artificial_intelligence': [8, 19, 13, 198],
    'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
    'Brain': [19, 5, 25, 11],
    'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
    'Hidamari_no_Ki': [1, 5, 5, 35],
    'IBM': [13, 3, 21, 33],
    'Iron_Age': [4, 8, 15, 22],
    'London': [53, 16, 31, 125],
    'Mei_Kurokawa': [1, 1, 2, 7],
    'PlayStation_3': [13, 5, 14, 148],
    'Python_(programming_language)': [2, 5, 17, 41],
    'Second_Intifada': [9, 13, 14, 84],
    'Stone_Age': [13, 10, 12, 40],
    'The_New_York_Times': [5, 9, 8, 42],
    'Wild_Arms_(video_game)': [3, 3, 10, 27],
    'Woolwich': [15, 9, 19, 38]}

TESTCASES = (
    ('wiki/', 'Stone_Age', 'Python_(programming_language)',
     ['Stone_Age', 'Brain', 'Artificial_intelligence', 'Python_(programming_language)']),

    ('wiki/', 'The_New_York_Times', 'Stone_Age',
     ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),

    ('wiki/', 'Artificial_intelligence', 'Mei_Kurokawa',
     ['Artificial_intelligence', 'IBM', 'PlayStation_3', 'Wild_Arms_(video_game)',
      'Hidamari_no_Ki', 'Mei_Kurokawa']),

    ('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing",
     ['The_New_York_Times', 'Second_Intifada', 'Haifa_bus_16_suicide_bombing',
      'Binyamina_train_station_suicide_bombing']),

    ('wiki/', 'Stone_Age', 'Stone_Age',
     ['Stone_Age', ]),
)


class TestBuildBrige(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = build_bridge(path, start_page, end_page)
                self.assertEqual(result, expected)


class TestGetStatistics(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = get_statistics(path, start_page, end_page)
                self.assertEqual(result, {page: STATISTICS[page] for page in expected})


if __name__ == '__main__':
    unittest.main()
