import unittest

from common.BaseRequestsMethods import get, post
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import class_case_log, step


@class_case_log
class GetNotesInfoHandle(unittest.TestCase):
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

    def testCase01_getNoteContent_same_data(self):
        """获取便签内容，重复数据"""
        step("新建1条便签")
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        note_id = create_note_resp[0]["noteId"]
        step("获取便签内容，传入重复note_id")
        self.get_notes_info_body['noteIds'] = [note_id, note_id]
        res = post(self.get_notes_info_url, userid=self.userid, sid=self.wps_sid, json=self.get_notes_info_body)
        expect = {'responseTime': int, 'noteBodies': [
            {'summary': 'a', 'noteId': note_id, 'infoNoteId': note_id, 'bodyType': 0,
             'body': 'a', 'contentVersion': 1, 'contentUpdateTime': int, 'title': 'a', 'valid': 1}]}
        self.assertEqual(200, res.status_code)
        CheckOutPut().output_check(expect=expect, actual=res.json())