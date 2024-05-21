import unittest

from common.BaseRequestsMethods import get
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import step, class_case_log

import unittest

from common.BaseRequestsMethods import get
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import step, class_case_log


@class_case_log
class GetNotesMajor(unittest.TestCase):  # 获取首页便签列表
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    get_notes_info_path = data_info['GetNotesApi']['path']
    get_notes_info_url = host + get_notes_info_path

    def setUp(self):
        DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)

    def testCase01_GetNotesMajor(self):
        """获取便签主流程"""
        step('创建一条便签数据')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        # print(create_note_resp)
        step('查询首页便签列表')
        startindex = 0
        rows = 100
        url = self.get_notes_info_url.format(userid=self.userid, startindex=startindex, rows=rows)
        get_notes_list = get(url=url, sid=self.wps_sid)
        self.assertEqual(get_notes_list.status_code, 200)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": create_note_resp[0]['noteId'], "createTime": int, "star": int, "remindTime": int,
             "remindType": int,
             "infoVersion": create_note_resp[0]['localContentVersion'], "infoUpdateTime": int, "groupId": None,
             "title": create_note_resp[0]['title'], "summary": create_note_resp[0]['summary'],
             "thumbnail": None, "contentVersion": create_note_resp[0]['localContentVersion'],
             "contentUpdateTime": int}]}
        CheckOutPut().output_check(expect, get_notes_list.json())
