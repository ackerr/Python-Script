import re

import requests

res = requests.get("https://www.douban.com"
                   "/group/topic/115427253/",
                   verify=False)
pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]" \
          r"+\.[a-zA-Z0-9-.]+)"
for i in re.findall(pattern, res.text):
    print(i)
