import requests

from common.logger import info


def get(url, sid, headers=None):
    if headers is None:
        headers = {
            'Cookie': f'wps_sid={sid}'
        }
    info(f'【requests】url:{url}')
    info(f'【headers】headers:{headers}')
    try:
        res = requests.get(url=url, headers=headers, timeout=30)
    except TimeoutError:
        return 'requests timeout!'
    info(f'【response】code:{res.status_code}')
    info(f'【response】body:{res.text}')
    return res


def post(url, sid, userid, headers=None, json=None):
    if headers is None:
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-user-key': f'{userid}'
        }
    info(f'【requests】url:{url}')
    info(f'【headers】headers:{headers}')
    info(f'【json】json:{json}')
    try:
        res = requests.post(url=url, headers=headers, json=json, timeout=30)
    except TimeoutError:
        return 'requests timeout!'
    info(f'【response】code:{res.status_code}')
    info(f'【response】body:{res.text}')
    return res
