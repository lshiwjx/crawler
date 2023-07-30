#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re
import xlwt
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getCharList(url = None):
  newURL = urlopen(url)
  bsObj = BeautifulSoup(newURL, "html.parser")

  metaTagList = bsObj.findAll('meta')
  charsetList = []

  for metaTag in metaTagList:
    #attribution = metaTag.get('content')
    #charData = str(attribution)
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

if __name__ == "__main__":
  # 定义关心的字段
  name = "姓名"
  university = "学校"
  college = "学院"
  major_research = "研究领域"
  number = "电话"
  email = "邮箱"
  title = "职称"
  education = "教育背景"
  patent = "专利"
  paper = "学术成果"
  homepage = "个人主页"
  cared_content = [name, university, college, major_research, number, email, title, education, patent, paper, homepage]
  # 固定值的字段设定
  tsinghua_web = "https://www.cs.tsinghua.edu.cn"
  university_value = "清华大学"
  college_value = "计算机科学与技术"
  # 创建表格与表头
  excel_save_path = "/Users/mohuiyu/Desktop/teacher_info/" + university_value + "/" + college_value + ".xls"
  excel = xlwt.Workbook(encoding="utf-8")
  sheet = excel.add_sheet(college_value, cell_overwrite_ok=True)
  for i in range(len(cared_content)):
    sheet.write(0, i, cared_content[i])
  # 定义目标网页的URL
  url = "https://www.cs.tsinghua.edu.cn/szzk/jzgml.htm"
  soup = DecodeHtmlPage(url)
  # 定位到包含老师资料的HTML元素
  teachers = soup.find_all("div", class_="text")
  # 遍历每个老师资料元素并提取信息
  for i in range(len(teachers)):
  # for teacher in teachers:
    teacher = teachers[i]
    info_text_map = {}
    teacher_name = teacher.find("h2").get_text()
    text = teacher.find_all("p")
    teacher_title = text[0].text
    teacher_number = text[1].text
    teacher_email = text[2].text
    # 打印老师基本资料
    info_text_map[name] = teacher_name
    info_text_map[university] = university_value
    info_text_map[college] = college_value
    info_text_map[title] = teacher_title
    info_text_map[number] = teacher_number
    info_text_map[email] = teacher_email
    # 获得老师个人网页并解析
    link = teacher.find("a").attrs['href'].split("/")
    link = [tsinghua_web] + link[1:]
    link = '/'.join(link)
    info_text_map[homepage] = link
    soup = DecodeHtmlPage(link)
    # 获得关键段落信息
    info = soup.find_all("div", class_="v_news_content")[0]
    # 获得其中包含title的字段
    info_titles = info.find_all("h4")
    info_title_list = []
    for info_title in info_titles:
      info_title_list.append(info_title.get_text())
    # 获得所有信息
    info_texts = info.find_all("p")
    info_text_key = ""
    count = 0
    for info_text in info_texts:
      info_text_p = info_text.get_text()
      if info_text_p in info_title_list:
        info_text_key = info_text_p
        info_text_map[info_text_key] = []
        count += 1
      elif count > 0:
        info_text_map[info_text_key].append(info_text_p)
    # 存储信息
    for key, value in info_text_map.items():
      if key in cared_content:
        index = cared_content.index(key)
        sheet.write(i+1, index, value)
    # 打印老师详细信息
    for key, value in info_text_map.items():
      print(f"{key}: {value}")
    print("--------------------")
  # 保存excel
  excel.save(excel_save_path)