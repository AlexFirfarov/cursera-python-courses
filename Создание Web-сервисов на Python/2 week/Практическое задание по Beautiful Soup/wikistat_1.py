from bs4 import BeautifulSoup
import unittest


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


def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError

    with open(path_to_file, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        body = soup.find('div', id='bodyContent')

        imgs = number_of_images(body, lambda tag: tag.has_attr('width') and float(tag['width']) >= 200)
        headers = number_of_headers(body, lambda tag: list(tag.strings)[0][0] in ('E', 'T', 'C'))
        linkslen = max_links_len(body)
        lists = number_of_lists(body)

    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
