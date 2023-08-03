#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlwt
from util import *

if __name__ == "__main__":
  # 固定值的字段设定
  tsinghua_web = "https://www.cs.tsinghua.edu.cn"
  university_value = "清华大学"
  college_value = "计算机科学与技术"
  # 创建表格与表头
  excel_save_path = "/Users/mohuiyu/Desktop/teacher_info/" + university_value + "/" + college_value + ".xls"
  excel = xlwt.Workbook(encoding="utf-8")
  sheet = excel.add_sheet(college_value, cell_overwrite_ok=True)
  for i in range(len(CARED_CONTENT)):
    sheet.write(0, i, CARED_CONTENT[i])
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
    info_text_map[NAME] = teacher_name
    info_text_map[UNIVERSITY] = university_value
    info_text_map[COLLEGE] = college_value
    info_text_map[TITLE] = teacher_title
    info_text_map[NUMBER] = teacher_number
    info_text_map[EMAIL] = teacher_email
    # 获得老师个人网页并解析
    link = teacher.find("a").attrs['href'].split("/")
    link = [tsinghua_web] + link[1:]
    link = '/'.join(link)
    info_text_map[HOMEPAGE] = link
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
      if key in CARED_CONTENT:
        index = CARED_CONTENT.index(key)
        sheet.write(i+1, index, value)
    # 打印老师详细信息
    for key, value in info_text_map.items():
      print(f"{key}: {value}")
    print("--------------------")
  # 保存excel
  excel.save(excel_save_path)