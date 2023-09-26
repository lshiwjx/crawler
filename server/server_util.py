import xlrd
import glob
import difflib
import re
from server_params import *


def traverse_dir(path):
    file_list = []
    for file_path in glob.glob(path + "/**", recursive=True):
        if glob.os.path.isfile(file_path):
            file_list.append(file_path)
    return file_list


def load_xls_data(path_list):
    teacher_info = {}
    for path in path_list:
        # 读取xls文件中所有内容
        data = xlrd.open_workbook(path)
        sheet = data.sheet_by_index(0)
        titles = sheet.row_values(0)
        ncols = sheet.nrows
        ntitles = len(titles)
        # 将数据进行存储
        split_path = path.split('/')
        university_name = split_path[-2].strip()
        teacher_info[university_name] = {}
        college_name = split_path[-1].split('.')[0].strip()
        teacher_info[university_name][college_name] = {}
        for i in range(1, ncols):
            teacher_name = sheet.cell_value(i, 0)
            teacher_info[university_name][college_name][teacher_name] = {}
            for j in range(1, ntitles):
                teacher_info[university_name][college_name][teacher_name][titles[j]] = sheet.cell_value(i, j)
    return teacher_info


def key_match(query_key, key_list, cutoff=0.0):
    matched_keys = difflib.get_close_matches(query_key, key_list, cutoff=cutoff)
    return matched_keys

def search_based_on_query(query_key, teacher_info):
    # Format: "university，college，teacher_name，major", "*" can be used to represent all.
    try:
        university_name, college_name, teacher_name, major = re.split('、|，|,| ', query_key)
    except:
        return kInputError
    university_list = teacher_info.keys()
    
    if '*' not in university_name:
        university_list = key_match(university_name, university_list, 0.2)
        if len(university_list) == 0:
            return kNoUniversity

    output_str = ''
    if '*' in college_name and '*' in teacher_name and '*' in major:
        for university_name in university_list:
            output_str += university_name + '\n' + kUniversityUrl[university_name] + '\n' + '----------'
        return output_str
    elif '*' not in college_name and '*' in teacher_name and '*' in major:
        for university_name in university_list:
            college = teacher_info[university_name]
            college_list = college.keys()
            college_list = key_match(college_name, college_list, cutoff=0.2)
            if len(college_list) == 0:
                return kNoCollege
            for college_name in college_list:
                output_str += university_name + '\n' + college_name + '\n' + kUniversityCollegeUrl[university_name][college_name] + '\n' + '----------'
        return output_str

    for university_candidate in university_list:
        college = teacher_info[university_candidate]
        college_list = college.keys()
        if '*' not in college_name:
            college_list = key_match(college_name, college_list, cutoff=0.2)
            if len(college_list) == 0:
                return kNoCollege
        for college_candidate in college_list:
            if '*' not in teacher_name:
                return search_teacher_name(university_candidate, college_candidate, teacher_name, teacher_info)
            elif '*' not in major:
                return search_major_research(university_candidate, college_candidate, major, teacher_info)
            else:
                return kInputError
                

def search_teacher_name(university_candidate, college_candidate, search_key, teacher_info):
    search_result = {}
    teacher = teacher_info[university_candidate][college_candidate]
    teacher_name_list = teacher.keys()
    if '*' not in search_key:
        teacher_name_list = key_match(search_key, teacher_name_list, cutoff=0.6)
        if len(teacher_name_list) == 0:
            return kNoTeacher
    for teacher_name_candidate in teacher_name_list:
        search_result[teacher_name_candidate] = \
                teacher_info[university_candidate][college_candidate][teacher_name_candidate]
    return search_result


def search_major_research(university_candidate, college_candidate, search_key, teacher_info):
    search_result = {}
    teacher = teacher_info[university_candidate][college_candidate]
    teacher_name_list = teacher.keys()
    for teacher_name_candidate in teacher_name_list:
        major_research = teacher_info[university_candidate][college_candidate][teacher_name_candidate][kMajorReaserch].strip()
        major_research_list = re.split('、|，|,| ', major_research)
        matched_major_research = key_match(search_key, major_research_list, cutoff=0.4)
        if len(matched_major_research) > 0:
            search_result[teacher_name_candidate] = \
                    teacher_info[university_candidate][college_candidate][teacher_name_candidate]
    if len(search_result) == 0:
        search_result = kNoMajor
    return search_result


if __name__ == '__main__':
    path_list = traverse_dir("./teacher_info")
    teacher_info = load_xls_data(path_list)
    query_key = "清华，*，*,人机交互"
    matched_keys = key_match(query_key, teacher_info.keys())
    result = search_based_on_query(query_key, teacher_info)
    if result == kInputError:
        print(f"Please Give Right Input: University,College,Teacher,Major!")
    elif result == kNoUniversity:
        print(f"No University is Founded! Please Check the Input University!")
    elif result == kNoCollege:
        print(f"No College is Founded! Please Check the Input College!")
    elif result == kNoTeacher:
        print(f"No Teacher is Founded! Please Check the Input Teacher!")
    elif result == kNoMajor:
        print(f"No Major is Founded! Please Check the Input Major!")
    else:
        teacher_list = result.keys()
        for teacher in teacher_list:
            info = result[teacher]
            print(f"姓名: {teacher}\n")
            for key, value in info.items():
                print(f"{key}: {value}\n")
