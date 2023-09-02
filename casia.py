#!/usr/bin/python
# -*- coding: UTF-8 -*-

from util import *
import xlwt
import os


if __name__ == "__main__":
    # 固定值的字段设定
    university_value = "中科院自动化所"
    college_value = "无"
    # 创建表格与表头
    save_dir = "./teacher_info/" + university_value + "/"
    os.makedirs(save_dir, exist_ok=True)
    excel_save_path = save_dir + college_value + ".xls"
    excel = xlwt.Workbook(encoding="utf-8")
    sheet = excel.add_sheet(college_value, cell_overwrite_ok=True)
    for i in range(len(CARED_CONTENT)):
        sheet.write(0, i, CARED_CONTENT[i])
    # 定义目标网页的URL
    url = "http://www.ia.cas.cn/yjsjy/dsjj/"
    soup = DecodeHtmlPage(url)
    # 定位到包含老师资料的HTML元素
    teachers = soup.find_all("p", class_="MsoNormal")
    # 遍历每个老师资料元素并提取信息
    for i in range(len(teachers)):
        teacher = teachers[i]
        info_text_map = {}
        try:
            teacher_name = teacher.a.find('span').get_text()
            teacher_link = teacher.a.attrs['href']
            teacher_soup = DecodeHtmlPage(teacher_link)

            basic_info = teacher_soup.find('div', class_='bp-enty')
            basic_text = basic_info.get_text().split(' ')
            for text in basic_text:
                if text[:4] == '电子邮件':
                    info_text_map[EMAIL] = text[5:]
                if '博' in text or '硕' in text:
                    info_text_map[TITLE] = text
            # 打印老师基本资料
            info_text_map[NAME] = teacher_name
            info_text_map[UNIVERSITY] = university_value
            info_text_map[COLLEGE] = college_value
            info_text_map[HOMEPAGE] = teacher_link
            # 获得老师个人网页并解析
            other_info = teacher_soup.find_all("div", class_="m-itme")
            for info in other_info:
                title = info.find('h3', class_="mi-t").get_text().strip()
                content = info.find_all('div', class_="mib-c")
                if '研究' in title:
                    info_text_map[MAJOR_RESEARCH] = '\n'.join(c.get_text().strip() for c in content)[:MAX_NUM_CHAR]
                elif '工作' in title or '教育' in title:
                    info_text_map[EDUCATION] = '\n'.join(c.get_text().strip() for c in content)[:MAX_NUM_CHAR]
                elif '出版' in title or '论文' in title:
                    info_text_map[PAPER] = '\n'.join(c.get_text().strip() for c in content)[:MAX_NUM_CHAR]
                elif '专利' in title:
                    info_text_map[PATENT] = '\n'.join(c.get_text().strip() for c in content)[:MAX_NUM_CHAR]
        except:
            continue
        # 存储信息
        for key, value in info_text_map.items():
            if key in CARED_CONTENT:
                index = CARED_CONTENT.index(key)
                sheet.write(i + 1, index, value)
        # 打印老师详细信息
        for key, value in info_text_map.items():
            print(f"{key}:\n {value}\n")
        print("--------------------")
    # 保存excel
    excel.save(excel_save_path)
