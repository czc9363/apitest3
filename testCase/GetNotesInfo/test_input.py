import time
import unittest

from common.BaseRequestsMethods import get, post
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import class_case_log, step
from parameterized import parameterized


@class_case_log
class GetNotesInfoInput(unittest.TestCase):
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    mustKeys = data_info['GetNotesInfoApi']['mustKeys']  # 请求body必传参数'noteId'
    headers_mustKeys = data_info['GetNotesInfoApi']['headers_mustKeys']  # 请求头必传参数'Cookie'
    get_notes_info_path = data_info['GetNotesInfoApi'][
        'path']  # '/v3/notesvr/set/noteinfo'
    get_notes_info_url = host + get_notes_info_path
    get_notes_info_body = data_info['GetNotesInfoApi']['body base']

    def setUp(self) -> None:
        DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)

    @parameterized.expand(mustKeys)
    def testCase01_miss_body_params(self, params):
        """body中必传参数为空的场景"""
        step('前置先造一条消息')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        first_note_id = create_note_resp[0]['noteId']  # 提出来的第一条消息ID
        step('body传参')
        self.get_notes_info_body['noteIds'] = [first_note_id]
        self.get_notes_info_body.pop(params)  # 移除必传参数
        step('发送请求')
        get_notes_info = post(url=self.get_notes_info_url, sid=self.wps_sid, userid=self.userid,
                              json=self.get_notes_info_body)
        step('断言状态码不等于200')
        self.assertNotEquals(get_notes_info.status_code, 200)

    @parameterized.expand(headers_mustKeys)
    def testCase02_miss_header_params(self, keys):
        """header中必传参数分别空的场景"""
        step('前置先造一条消息')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        first_note_id = create_note_resp[0]['noteId']  # 提出来的第一条消息ID
        step('body传参')
        self.get_notes_info_body['noteIds'] = [first_note_id]
        step('先定义一个请求头正常传参')
        headers = {
            'Cookie': f'wps_sid={self.wps_sid}',
            'X-user-key': f'{self.userid}'
        }
        step('移除请求头里面的参数')
        headers.pop(keys)
        step('发送请求')
        get_notes_info = post(url=self.get_notes_info_url, sid=self.wps_sid, userid=self.userid,
                              json=self.get_notes_info_body, headers=headers)
        step('断言状态码不等于200')
        self.assertNotEquals(get_notes_info.status_code, 200)

    @parameterized.expand(["abc", "V02SYcBmaFIDwBD_KnJzgB9GLmfMJqM00a7273800017eb5dbe"])
    def testCase03_input_sid(self, key):
        """获取便签内容，wps_sid无效和过期"""
        step(f"获取便签内容,wps_sid值为{key}")
        note_id = f"{str(int(time.time() * 1000))}_note_id"  # 便签id
        self.get_notes_info_body["noteIds"] = [note_id]
        res = post(url=self.get_notes_info_url, userid=self.userid, sid=key, json=self.get_notes_info_body)
        expect = {"errorCode": -2010, "errorMsg": ""}
        self.assertEqual(401, res.status_code)
        CheckOutPut().output_check(expect, res.json())

    @parameterized.expand(["aBcd", ""])
    def testCase04_input_noteIds(self, key):
        """noteIds必填字段异常值校验"""
        step(f"获取便签内容,noteIds值为{key}")
        self.get_notes_info_body["noteIds"] = [key]
        res = post(url=self.get_notes_info_url, userid=self.userid, sid=self.wps_sid, json=self.get_notes_info_body)
        expect = {"responseTime": int, "noteBodies": []}
        self.assertEqual(200, res.status_code)
        CheckOutPut().output_check(expect, res.json())
