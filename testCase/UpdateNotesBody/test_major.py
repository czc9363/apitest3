import unittest

from common.BaseRequestsMethods import get, post
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import step, class_case_log


@class_case_log
class UpdateNotesBodyMajor(unittest.TestCase):  # 更新便签信息主题
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    update_notes_body_path = data_info['UpDateNotesBodyApi'][
        'path']  # '/v3/notesvr/set/noteinfo'
    update_notes_body_url = host + update_notes_body_path

    def setUp(self):
        res = DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)
        print(res)

    def testCase01_UpdateNotesBodyMajor(self):
        """获取便签主流程"""
        step('前置创建一条便签数据')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        first_note_id = create_note_resp[0]['noteId']  # 提出来的第一条消息ID
        step('更新便签信息主题')
        body = {'noteId': first_note_id}
        update_notes_body = post(url=self.update_notes_body_url, sid=self.wps_sid, userid=self.userid, json=body)
        step('断言响应状态码')
        self.assertEqual(update_notes_body.status_code, 200)
        # step('body信息')，expect还要继续调试
        # expect = {"responseTime": int, "webNotes": [
        #     {"noteId": create_note_resp[0]['noteId'], "createTime": int, "star": int, "remindTime": int,
        #      "remindType": int,
        #      "infoVersion": create_note_resp[0]['localContentVersion'], "infoUpdateTime": int, "groupId": None,
        #      "title": create_note_resp[0]['title'], "summary": create_note_resp[0]['summary'],
        #      "thumbnail": None, "contentVersion": create_note_resp[0]['localContentVersion'],
        #      "contentUpdateTime": int}]}
        # CheckOutPut().output_check(expect, get_notes_list.json())