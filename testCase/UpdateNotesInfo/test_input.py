import time
import unittest

from common.BaseRequestsMethods import get, post
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import class_case_log, step
from parameterized import parameterized


@class_case_log
class UpdateNotesInfoMajor(unittest.TestCase):
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    update_notes_body_path = data_info['UpDateNotesBodyApi'][
        'path']  # '/v3/notesvr/set/noteinfo'
    update_notes_body_url = host + update_notes_body_path  # 上传消息主体的url
    update_notes_info_path = data_info['UpDateNotesInfoApi'][
        'path']
    update_notes_info_url = host + update_notes_info_path  # 更新便签内容的URL
    update_notes_info_body = data_info['UpDateNotesInfoApi']['body base']  # 更新便签内容的Body,是一个字典
    mustKeys = data_info['UpDateNotesInfoApi']['mustKeys']
    headers_mustKeys = data_info['UpDateNotesInfoApi']['headers_mustKeys']

    def setUp(self):
        res = DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)
        print(res)

    @parameterized.expand(mustKeys)
    def testCase01_miss_body_params(self, params):
        """body中必传参数为空的场景"""
        step('前置处理便签body')
        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }
        step('上传消息便签body')
        res = post(url=self.update_notes_body_url, userid=self.userid, sid=self.wps_sid, json=body)
        info_version = res.json()['infoVersion']
        # body = {
        #     'noteId': note_id,
        #     'title': 'test',
        #     'summary': 'test',
        #     'body': 'test',
        #     'localContentVersion': info_version,
        #     'BodyType': 0
        # }
        step('更新便签内容的note_id及版本号字段,前置接口数据准备完毕')
        self.update_notes_info_body['noteId'] = note_id
        self.update_notes_info_body['localContentVersion'] = info_version
        step('重新构造body请求参数')
        self.update_notes_info_body.pop(params)
        update_notes_info_res = post(url=self.update_notes_info_url, userid=self.userid, sid=self.wps_sid,
                                     json=self.update_notes_info_body)
        step('断言响应状态码不等于200')
        self.assertNotEquals(update_notes_info_res.status_code, 200)

    @parameterized.expand(headers_mustKeys)
    def testCase02_miss_header_params(self, keys):
        """header中必传参数分别空的场景"""
        step('前置处理便签body')
        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }
        step('上传消息便签body')
        res = post(url=self.update_notes_body_url, userid=self.userid, sid=self.wps_sid, json=body)
        info_version = res.json()['infoVersion']
        step('更新便签内容的note_id及版本号字段,前置接口数据准备完毕')
        self.update_notes_info_body['noteId'] = note_id
        self.update_notes_info_body['localContentVersion'] = info_version
        step('重新构造headers请求参数')
        headers = {
            'Cookie': f'wps_sid={self.wps_sid}',
            'X-user-key': f'{self.userid}'
        }
        headers.pop(keys)
        update_notes_info_res = post(url=self.update_notes_info_url, userid=self.userid, sid=self.wps_sid,
                                     json=self.update_notes_info_body, headers=headers)
        step('断言响应状态码不等于200')
        self.assertNotEquals(update_notes_info_res.status_code, 200)
