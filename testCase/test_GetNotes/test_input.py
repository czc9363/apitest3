import unittest

from common.BaseRequestsMethods import get
from common.CheckOutPut import CheckOutPut
from common.DataClear import DataClear
from common.ReadFiles import YamlRead
from common.logger import class_case_log, step
from parameterized import parameterized


@class_case_log
class GetNotesInput(unittest.TestCase):
    env_info = YamlRead().env_config()
    data_info = YamlRead().data_config()
    host = env_info['host']
    userid = env_info['user_id']
    wps_sid = env_info['wps_sid']
    headers_mustKeys = data_info['GetNotesApi']['headers_mustKeys']  # 请求头必传参数'Cookie'
    # '/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
    get_notes_info_path = data_info['GetNotesApi']['path']
    get_notes_info_url = host + get_notes_info_path
    start_index = 0
    rows = 100

    def setUp(self) -> None:
        DataClear().remove_notes(sid=self.wps_sid, user_id=self.userid)

    def testCase01_miss_userid_params(self):
        """url路径中userid缺失的场景"""
        url = f'/v3/notesvr/user/home/startindex/{self.start_index}/rows/{self.rows}/notes'
        step('获取url')
        get_notes_url = self.host + url
        step('发送请求')
        get_notes_list = get(url=get_notes_url, sid=self.wps_sid)
        step('断言状态码不等于200，预期等于404')
        self.assertEqual(get_notes_list.status_code, 404)

    def testCase02_miss_startindex_params(self):
        """url路径中startindex缺失的场景"""
        url = f'/v3/notesvr/user/{self.userid}/home/startindex/rows/{self.rows}/notes'
        step('获取url')
        get_notes_url = self.host + url
        step('发送请求')
        get_notes_list = get(url=get_notes_url, sid=self.wps_sid)
        step('断言状态码不等于200，预期等于404')
        self.assertEqual(get_notes_list.status_code, 404)

    def testCase03_miss_rows_params(self):
        """url路径中rows缺失的场景"""
        url = f'/v3/notesvr/user/{self.userid}/home/startindex/{self.start_index}/rows/notes'
        step('获取url')
        get_notes_url = self.host + url
        step('发送请求')
        get_notes_list = get(url=get_notes_url, sid=self.wps_sid)
        step('断言状态码不等于200，预期等于404')
        self.assertEqual(get_notes_list.status_code, 404)

    @parameterized.expand(headers_mustKeys)
    def testCase04_miss_header_params(self, keys):
        """header中必传参数为空的场景"""
        step('先定义一个请求头正常传参')
        headers = {
            'Cookie': f'wps_sid={self.wps_sid}'
        }
        headers.pop(keys)
        step('获取url')
        get_notes_url = self.get_notes_info_url.format(userid=self.userid, startindex=self.start_index, rows=self.rows)
        step('发送请求')
        get_notes_list = get(url=get_notes_url, sid=self.wps_sid, headers=headers)
        step('断言状态码不等于200')
        self.assertNotEquals(get_notes_list.status_code, 200)

    def testCase05_headers_invalid_key(self):
        """无效wps_sid"""
        step("查询首页便签,无效wps_sid")
        get_notes_url = self.get_notes_info_url.format(userid=self.userid, startindex=self.start_index, rows=self.rows)
        res = get(url=get_notes_url, sid="abc")
        expect = {
            "errorCode": -2010,
            "errorMsg": ""
        }
        self.assertEqual(401, res.status_code)
        CheckOutPut().output_check(expect, res.json())

    def testCase06_headers_no_key(self):
        """请求头中sid为空场景"""
        step("查询首页便签,sid为空字符串")
        get_notes_url = self.get_notes_info_url.format(userid=self.userid, startindex=self.start_index, rows=self.rows)
        headers = {"Cookie": ""}
        res = get(url=get_notes_url, sid=self.wps_sid, headers=headers)
        expect = {
            "errorCode": -2009,
            "errorMsg": ""
        }
        self.assertEqual(401, res.status_code)
        CheckOutPut().output_check(expect, res.json())

    @parameterized.expand(["01234567890123456789012345678901234567890123456789", None])
    def testCase07_userid(self, key):
        """userid值异常情况"""
        step(f"查询首页便签,userid值为{key}")
        get_notes_url = self.get_notes_info_url.format(userid=key, startindex=self.start_index, rows=self.rows)
        res = get(url=get_notes_url, sid=self.wps_sid)
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        self.assertEqual(500, res.status_code)
        CheckOutPut().output_check(expect, res.json())

    @parameterized.expand(["01234567890123456789012345678901234567890123456789", None])
    def testCase08_startIndex(self, key):
        """startindex值异常情况s值为"""
        step(f"查询首页便签,startindex值为{key}")
        get_notes_url = self.get_notes_info_url.format(userid=self.userid, startindex=key, rows=10)
        res = get(url=get_notes_url, sid=self.wps_sid)
        expect = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.assertEqual(500, res.status_code)
        CheckOutPut().output_check(expect, res.json())

    @parameterized.expand(["01234567890123456789012345678901234567890123456789", None])
    def testCase09_rows(self, key):
        """rows值异常情况"""
        step(f"查询首页便签,rows值为{key}")
        get_notes_url = self.get_notes_info_url.format(userid=self.userid, startindex=0, rows=key)
        res = get(url=get_notes_url, sid=self.wps_sid)
        expect = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.assertEqual(500, res.status_code)
        CheckOutPut().output_check(expect, res.json())
