import time
import unittest

from common.BaseRequestsMethods import get, post
from common.CheckOutPut import CheckOutPut
from common.CreateData import CreateNote
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import step, class_case_log


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

    def setUp(self):
        res = DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)
        print(res)

    def testCase01_UpdateNotesInfoMajor(self):
        """上传便签内容"""
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
        step('更新便签内容的note_id及版本号字段')
        self.update_notes_info_body['noteId'] = note_id
        self.update_notes_info_body['localContentVersion'] = info_version
        step('发送更新标签内容的请求')
        update_notes_info_res = post(url=self.update_notes_info_url, userid=self.userid, sid=self.wps_sid,
                                     json=self.update_notes_info_body)
        step('断言响应状态码')
        self.assertEqual(update_notes_info_res.status_code, 200)
        # step('body信息')，expect还要继续调试
        # expect = {"responseTime": int, "webNotes": [
        #     {"noteId": create_note_resp[0]['noteId'], "createTime": int, "star": int, "remindTime": int,
        #      "remindType": int,
        #      "infoVersion": create_note_resp[0]['localContentVersion'], "infoUpdateTime": int, "groupId": None,
        #      "title": create_note_resp[0]['title'], "summary": create_note_resp[0]['summary'],
        #      "thumbnail": None, "contentVersion": create_note_resp[0]['localContentVersion'],
        #      "contentUpdateTime": int}]}
        # CheckOutPut().output_check(expect, get_notes_list.json())