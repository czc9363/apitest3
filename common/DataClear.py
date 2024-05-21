import requests


# 通用删除数据方法
class DataClear:
    def group_clear(self, sid, user_id):
        # 获取当前用户所有有效分组
        url = 'http://note-api.wps.cn/v3/notesvr/get/notegroup'
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-user-key': f'{user_id}'
        }
        data = {'excludeInvalid': True}
        get_res = requests.post(url, headers=headers, json=data)
        for group in get_res.json()['noteGroups']:
            group_id = group['groupId']

            del_url = 'https://note-api.wps.cn/notesvr/delete/notegroup'
            data = {
                'groupId': group_id
            }
            del_res = requests.post(url=del_url, headers=headers, json=data)
            if del_res.status_code != 200:
                return False
        return 'delete success'

    def remove_notes(self, user_id, sid):
        get_notes_url = f'http://note-api.wps.cn/v3/notesvr/user/{user_id}/home/startindex/0/rows/100/notes'
        headers = {
            'Cookie': f'wps_sid={sid}'
        }
        get_res = requests.get(url=get_notes_url, headers=headers)
        # print(get_res)
        for note_id_dict in get_res.json()['webNotes']:
            note_id = note_id_dict['noteId']
            delete_url = 'http://note-api.wps.cn/v3/notesvr/delete'
            headers = {
                'X-user-key': f'{user_id}',
                'Cookie': f'wps_sid={sid}',
            }
            data = {'noteId': note_id}
            requests.post(url=delete_url, headers=headers, json=data)
        return '删除便签成功'


if __name__ == '__main__':
    pass
    # user_id: '256598815'
    # wps_sid: 'V02StTPnwgvk3rbGSutq35jH5O5VvkQ00aeb6adf000f4b631f'
    # # res = DataClear().remove_notes(user_id='256598815',sid='V02StTPnwgvk3rbGSutq35jH5O5VvkQ00aeb6adf000f4b631f')
    # # print(res)
    # get_notes_url = 'http://note-api.wps.cn/v3/notesvr/user/256598815/home/startindex/0/rows/100/notes'
    # headers = {
    #     'Cookie': 'wps_sid=V02StTPnwgvk3rbGSutq35jH5O5VvkQ00aeb6adf000f4b631f'
    # }
    # get_res = requests.get(url=get_notes_url, headers=headers)
    # # print(get_res.json())
    # for note_id_dict in get_res.json()['webNotes']:
    #     noteids = note_id_dict['noteId']
    #     print(noteids)
    # get_notes_url = 'http://note-api.wps.cn/v3/notesvr/user/256598815/home/startindex/0/rows/100/notes'
    # headers = {
    #     'Cookie': 'wps_sid=V02StTPnwgvk3rbGSutq35jH5O5VvkQ00aeb6adf000f4b631f'
    # }
    # get_res = requests.get(url=get_notes_url, headers=headers)
    # print(get_res.json())
    # for note_id_dict in get_res.json()['webNotes']:
    #     note_id = note_id_dict['noteId']
    #     print(type(note_id))
    #     delete_url = 'http://note-api.wps.cn/v3/notesvr/delete'
    #     headers = {
    #         'Cookie': 'wps_sid=V02StTPnwgvk3rbGSutq35jH5O5VvkQ00aeb6adf000f4b631f',
    #         'X-user-key': '256598815'
    #     }
    #     data = {'noteId': '1715781934306_noteId'}
    #     res = requests.post(url=delete_url, headers=headers, json=data)
    #     print(res.json())
