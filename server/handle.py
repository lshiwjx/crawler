import glob
import hashlib
import reply
import receive
import web
import xlrd

from server_util import *

# 定义关心的字段
NAME = "姓名"
UNIVERSITY = "学校"
COLLEGE = "学院"
MAJOR_RESEARCH = "研究领域"
NUMBER = "电话"
EMAIL = "邮箱"
TITLE = "职称"
HOMEPAGE = "个人主页"
CARED_CONTENT = [NAME, UNIVERSITY, COLLEGE, MAJOR_RESEARCH, NUMBER, EMAIL, TITLE, HOMEPAGE]


class Handle(object):
    def __init__(self) -> None:
        super().__init__()
        self._data_path = "./teacher"
        self._path_list = traverse_dir("./teacher_info")
        self._teacher_info = load_xls_data(self._path_list)

    def POST(self):
        try:
            webData = web.data()
            print(f"Handle Post webdata is {webData}")
            #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                query_key = recMsg.Content
                content = self.analyze_result(query_key)
                print(f"<----------content: {content}")
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print("暂且不处理")
                return "success"
        except Exception as Argment:
            return Argment

    def analyze_result(self, query_key):
        result = search_based_on_query(query_key, self._teacher_info)
        if result == kInputError:
            return "请输入正确的格式：\'大学名称，院系名称，老师名称\'! 不确定的部分可以使用\'*\'代替！如：\'清华，*，邱勇\'"
        elif result == kNoUniversity:
            return "没找到此大学，请检查大学名称是否正确!"
        elif result == kNoCollege:
            return "没找到此院系，请检查院系名称是否正确!"
        elif result == kNoTeacher:
            return "没找到此老师，请检查此老师名称是否正确!"
        elif isinstance(result, str):
            return result
        else:
            output = ''
            teacher_list = result.keys()
            for teacher in teacher_list:
                info = result[teacher]
                output = output + f"姓名: {teacher}\n"
                for key, value in info.items():
                    if key in CARED_CONTENT:
                        output = output + f"{key}: {value}\n"
                output = output + "--------------"
        return output
