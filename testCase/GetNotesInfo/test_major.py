import time
import unittest

from common.BaseRequestsMethods import get, post
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import step, class_case_log


@class_case_log
class GetNotesInfoMajor(unittest.TestCase):
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    get_notes_info_path = data_info['GetNotesInfoApi'][
        'path']  # '/v3/notesvr/set/noteinfo'
    get_notes_info_url = host + get_notes_info_path  # 获取便签内容的url
    get_notes_info_body = data_info['GetNotesInfoApi']['body base']  # 更新便签内容的Body,是一个字典

    def setUp(self):
        res = DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)
        print(res)

    def testCase01_GetNotesInfoMajor(self):
        """上传便签内容"""
        step('前置创建一条消息')
        create_note_resp = CreateNote().create_note(userid=self.userid, sid=self.wps_sid, num=1)
        first_note_id = create_note_resp[0]['noteId']  # 提出来的第一条消息ID
        step('定义一个空列表')
        lst = []
        step('把提取出来的便签ID放到列表里面')
        lst.append(first_note_id)
        self.get_notes_info_body['noteIds'] = lst
        step('发送获取便签内容的请求')
        get_notes_info_res = post(url=self.get_notes_info_url, userid=self.userid, sid=self.wps_sid,
                                  json=self.get_notes_info_body)
        step('断言响应状态码')
        self.assertEqual(get_notes_info_res.status_code, 200)
        # step('body信息')，expect还要继续调试
        # expect = {"responseTime": int, "webNotes": [
        #     {"noteId": create_note_resp[0]['noteId'], "createTime": int, "star": int, "remindTime": int,
        #      "remindType": int,
        #      "infoVersion": create_note_resp[0]['localContentVersion'], "infoUpdateTime": int, "groupId": None,
        #      "title": create_note_resp[0]['title'], "summary": create_note_resp[0]['summary'],
        #      "thumbnail": None, "contentVersion": create_note_resp[0]['localContentVersion'],
        #      "contentUpdateTime": int}]}
        # CheckOutPut().output_check(expect, get_notes_list.json())