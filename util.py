import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

# 定义关心的字段
NAME = "姓名"
UNIVERSITY = "学校"
COLLEGE = "学院"
MAJOR_RESEARCH = "研究领域"
NUMBER = "电话"
EMAIL = "邮箱"
TITLE = "职称"
EDUCATION = "教育背景"
PATENT = "专利"
PAPER = "学术成果"
HOMEPAGE = "个人主页"
CARED_CONTENT = [NAME, UNIVERSITY, COLLEGE, MAJOR_RESEARCH, NUMBER, EMAIL, TITLE, EDUCATION, PATENT, PAPER,
                 HOMEPAGE]

MAX_NUM_CHAR = 32767

def getCharList(url=None):
    newURL = urlopen(url)
    bsObj = BeautifulSoup(newURL, "html.parser")

    metaTagList = bsObj.findAll('meta')
    charsetList = []

    for metaTag in metaTagList:
        # attribution = metaTag.get('content')
        # charData = str(attribution)
        charData = str(metaTag)
        if 'charset' in charData:
            position = charData.find('charset')
            charset = charData[(position + 8):]
            charsetList.append(re.findall(r'"(.*?)"', charset)[0])

    return charsetList


def DecodeHtmlPage(url):
    charset = getCharList(url)[0]

    # 发起HTTP请求并获取网页内容
    response = requests.get(url)
    response.encoding = charset
    html = response.text

    # 使用BeautifulSoup解析网页内容
    return BeautifulSoup(html, "html.parser")