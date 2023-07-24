import requests
import re

root_url = 'http://www.ia.cas.cn/yjsjy/dsjj/'
root = requests.get(root_url, timeout=30)
root.raise_for_status()
root.encoding = root.apparent_encoding

match_person = re.compile(r'<a href="http://people.ucas.ac.cn/~[^"]*')
person_list = match_person.findall(root.text)

for person in person_list:
    url = person[len('<a href="'):]
    print(url)
