import requests
import bs4
import re


def fusejiSearch(keyword):
	if keyword.count("○") == 0:
		return

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
	r = requests.get("http://fuseji.net/" + keyword, headers=headers)
	r.encoding = r.apparent_encoding

	if "解読できません" in r.text:
		return
	
	ret = []
	s = bs4.BeautifulSoup(r.content, "html.parser")
	hit = re.search("[0-9]+件hit", r.text).group().replace("件hit", "")
	img = s.find_all("img")[1]["src"]
	contents = str(s.find("div", id="contents")).split("<br/>")

	if len(contents) <= 6:
		del contents[:3], contents[-1], contents[-1]
	else:
		del contents[:5], contents[-1], contents[-1]

	for i in contents:
		s = bs4.BeautifulSoup(i, "html.parser")
		name = [s.find("tt").string]
		urls = [i["href"] for i in s.find_all("a")]
		if not urls[0].startswith("http://www"):
			urls.insert(0, "なし (Google)")
		if not urls[1].startswith("http://ja"):
			urls.insert(1, "なし (Wikipedia)")
		if not urls[2].startswith("http://d"):
			urls.insert(2, "なし (はてなキーワード)")
		if not urls[3].startswith("http://search"):
			urls.insert(3, "なし (Yahoo)")
		ret.append(name + urls)
	
	ret.insert(0, [hit, img])
	return ret
