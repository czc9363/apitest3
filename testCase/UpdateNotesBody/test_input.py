import unittest

from common.BaseRequestsMethods import get, post
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import class_case_log, step
from parameterized import parameterized


@class_case_log
class UpdateNotesBodyInput(unittest.TestCase):
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    mustKeys = data_info['UpDateNotesBodyApi']['mustKeys']  # 请求body必传参数'noteId'
    headers_mustKeys = data_info['UpDateNotesBodyApi']['headers_mustKeys']  # 请求头必传参数'Cookie'
    update_notes_body_path = data_info['UpDateNotesBodyApi'][
        'path']  # '/v3/notesvr/set/noteinfo'
    update_notes_body_url = host + update_notes_body_path

    def setUp(self) -> None:
        DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)

    @parameterized.expand(mustKeys)
    def testCase01_miss_body_params(self, params):
        """body中必传参数为空的场景"""
        step('前置先造一条消息')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        first_note_id = create_note_resp[0]['noteId']  # 提出来的第一条消息ID
        step('body传参')
        body = {"noteId": first_note_id}
        body.pop(params)  # 移除必传参数
        step('发送请求')
        update_notes_body = post(url=self.update_notes_body_url, sid=self.wps_sid, userid=self.userid, json=body)
        step('断言状态码不等于200')
        self.assertNotEquals(update_notes_body.status_code, 200)

    @parameterized.expand(headers_mustKeys)
    def testCase02_miss_header_params(self, keys):
        """header中必传参数分别空的场景"""
        step('前置先造一条消息')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        first_note_id = create_note_resp[0]['noteId']  # 提出来的第一条消息ID
        step('body传参')
        body = {"noteId": first_note_id}
        step('先定义一个请求头正常传参')
        headers = {
            'Cookie': f'wps_sid={self.wps_sid}',
            'X-user-key': f'{self.userid}'
        }
        step('移除请求头里面的参数')
        headers.pop(keys)
        step('发送请求')
        update_notes_body = post(url=self.update_notes_body_url, sid=self.wps_sid, userid=self.userid, json=body,
                                 headers=headers)
        step('断言状态码不等于200')
        self.assertNotEquals(update_notes_body.status_code, 200)