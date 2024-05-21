import time

import requests


# 通用创建数据方法
class CreateNote:
    host = 'http://note-api.wps.cn'

    def create_note(self, userid, sid, num):
        note_list = []
        for i in range(num):
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(userid)
            }
            note_id = str(int(time.time() * 1000)) + '_noteId'
            body = {
                'noteId': note_id
            }
            res = requests.post(url=self.host + '/v3/notesvr/set/noteinfo', headers=headers, json=body)
            infoVersion = res.json()['infoVersion']
            body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': infoVersion,
                'BodyType': 0
            }
            note_list.append(body)
            res = requests.post(url=self.host + '/v3/notesvr/set/notecontent', headers=headers, json=body)
        return note_list
