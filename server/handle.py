import glob
import hashlib
import reply
import receive
import web
import xlrd

from server_util import *

# # 定义关心的字段
# NAME = "姓名"
# UNIVERSITY = "学校"
# COLLEGE = "学院"
# MAJOR_RESEARCH = "研究领域"
# NUMBER = "电话"
# EMAIL = "邮箱"
# TITLE = "职称"
# HOMEPAGE = "个人主页"
# CARED_CONTENT = [NAME, UNIVERSITY, COLLEGE, MAJOR_RESEARCH, NUMBER, EMAIL, TITLE, HOMEPAGE]


class Handle(object):
    def __init__(self) -> None:
        super().__init__()
        self._data_path = "./teacher"
        self._path_list = traverse_dir("./teacher_info")
        self._teacher_info = load_xls_data(self._path_list)

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "JustTest"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(list[0].encode('utf-8'))
            sha1.update(list[1].encode('utf-8'))
            sha1.update(list[2].encode('utf-8'))
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

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
            return "请输入正确的格式：\'模式，大学名称，院系名称，老师名称/研究方向\'! 不确定的部分可以使用\'*\'代替！\n其中模式\'a\'代表老师名称，\'b\'代表研究方向，如：\'a，清华，*，邱勇\' 或者 \'b，清华，*，人工智能\'"
        elif result == kNoUniversity:
            return "没找到此大学，请检查大学名称是否正确!"
        elif result == kNoCollege:
            return "没找到此院系，请检查院系名称是否正确!"
        elif result == kNoTeacher:
            return "没找到此老师，请检查此老师名称是否正确!"
        elif result == kNoMajor:
            return "没找到相关专业的老师，请检查这个专业是否正确!"
        elif isinstance(result, str):
            return result
        else:
            teacher_count = 0
            output = ''
            teacher_list = result.keys()
            for teacher in teacher_list:
                teacher_count += 1
                info = result[teacher]
                output = output + f"姓名: {teacher}\n"
                if teacher_count <= KMaxNumTeacherDisplay:
                    for key, value in info.items():
                        if key in kCaredContent:
                            output = output + f"{key}: {value}\n"
                else:
                    output = output + f"{kHomePage}: {info[kHomePage]}\n"
                output = output + "--------------\n"
                
        return output
