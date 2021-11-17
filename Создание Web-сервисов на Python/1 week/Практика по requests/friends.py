import requests
from datetime import date

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'


def calc_age(uid):
    params_user_get = {'access_token': ACCESS_TOKEN, 'user_ids': uid, 'v': '5.71'}
    resp_id = requests.get('https://api.vk.com/method/users.get', params=params_user_get)
    id = resp_id.json()['response'][0]['id']

    params_friends_get = {'access_token': ACCESS_TOKEN, 'user_id': id, 'fields': 'bdate', 'v': '5.71'}
    resp_friends = requests.get('https://api.vk.com/method/friends.get', params=params_friends_get)
    friends = resp_friends.json()['response']['items']

    ages = {}
    for friend in friends:
        if 'bdate' in friend.keys():
            bdate = friend['bdate'].split(sep='.')
            if len(bdate) == 3:
                age = date.today().year - int(bdate[2])
                if age in ages.keys():
                    ages[age] += 1
                else:
                    ages[age] = 1

    ages = [(key, value) for key, value in ages.items()]
    ages.sort(key=lambda x: (-x[1], x[0]))
    return ages


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
