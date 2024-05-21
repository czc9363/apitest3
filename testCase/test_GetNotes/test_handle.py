import unittest

from common.BaseRequestsMethods import get
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import class_case_log, step


@class_case_log
class GetNotesInputHandle(unittest.TestCase):
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    headers_mustKeys = data_info['GetNotesApi']['headers_mustKeys']  # 请求头必传参数'Cookie'
    # '/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
    get_notes_info_path = data_info['GetNotesApi']['path']
    get_notes_info_url = host + get_notes_info_path

    def setUp(self) -> None:
        DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)

    def testCase01_rows_limit(self):
        """创建2条便签，startIndex=0，rows=1，只返回1条数据"""
        step("创建2条便签")
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=2)

        step("查询首页便签,rows=1")
        get_notes_info_url = self.get_notes_info_url.format(userid=self.userid, startindex=0, rows=1)
        res = get(url=get_notes_info_url, sid=self.wps_sid)
        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": create_note_resp[1]["noteId"],
                    "createTime": int,
                    "star": 0,
                    "remindTime": 0,
                    "remindType": 0,
                    "infoVersion": 1,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "a",
                    "summary": "a",
                    "thumbnail": None,
                    "contentVersion": 1,
                    "contentUpdateTime": int
                }
            ]
        }
        self.assertEqual(200, res.status_code)
        CheckOutPut().output_check(expect, res.json())