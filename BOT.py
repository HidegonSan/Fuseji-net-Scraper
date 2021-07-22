import discord
import requests
import bs4
import datetime
import random
import re


TOKEN = "PASTE YOUR TOKEN HERE"


def fusejiSearch(keyword):
	rCount = keyword.count("○")
	if not rCount or len(keyword) == squareCount:
		return 0

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
	r = requests.get("http://fuseji.net/" + keyword, headers = headers)
	r.encoding = r.apparent_encoding

	if "解読できません" in r.text:
		return

	ret = []
	s = bs4.BeautifulSoup(r.content, "html.parser")
	hit = re.search("[0-9]+件hit", r.text).group().replace("件hit", "")
	img = s.find_all("img")[1]["src"]
	contents = str(s.find("div", id = "contents")).split("<br/>")

	if len(contents) <= 6:
		del contents[:3], contents[-1], contents[-1]
	else:
		del contents[:5], contents[-1], contents[-1]

	for i in contents:
		s = bs4.BeautifulSoup(i, "html.parser")
		name = [s.find("tt").string]
		urls = [i["href"] for i in s.find_all("a")]
		if not urls[0].startswith("http://www"):
			urls.insert(0, "該当なし (Google)")
		if not urls[1].startswith("http://ja"):
			urls.insert(1, "該当なし (Wikipedia)")
		if not urls[2].startswith("http://d"):
			urls.insert(2, "該当なし (はてなキーワード)")
		if not urls[3].startswith("http://search"):
			urls.insert(3, "該当なし (Yahoo)")
		ret.append(name + urls)

	ret.insert(0, [hit, img])
	return ret



client = discord.Client()

@client.event
async def on_message(msg):
	if msg.author.bot or msg.author == client.user:
		return


	if str.lower(msg.content).startswith("fsearch "):
		tmp = msg.content.split()

		if len(tmp) == 1:
			embed = discord.Embed(
				title = "⚠️ エラー ⚠️",
				description = "ㅤ\n引数が足りません。\n\n例 : `fsearch たけ○こ`",
				color = 0xFF0000
			)
			await msg.channel.send(embed = embed)
			return

		get = fusejiSearch(tmp[1])

		if get:
			tmp2 = get.pop(0)
			embed = discord.Embed(
				title = f"{tmp[1]} の伏せ字検索結果",
				description = f"ㅤ\n`{tmp2[0]}件Hitしました。`\nㅤ",
				color = random.randint(0, 16777215)
			)

			for i in get:
				names = ["Google", "Wikipedia", "はてなキーワード", "Yahoo"]
				g_name = i.pop(0)
				value = "\n".join([url if url.startswith("該当なし") else f"[{name}]({url})" for name, url in zip(names, i)])
				embed.add_field(name = g_name, value = value, inline = False)

			embed.add_field(name = "ㅤ", value = "ㅤ", inline = False)

			embed.set_image(url = tmp2[1])
			embed.set_footer(
				text = f"Used by {msg.author}",
				icon_url = msg.author.avatar_url_as(format = "png")
			)

			try:
				await msg.channel.send(embed = embed)
			except:
				embed = discord.Embed(
					title = "⚠️エラー⚠️",
					description = "ㅤ\n送信可能な文字数を超えました。\n" + 
					"もう少し候補を少なくしてください。",
					color = 0xFF0000
				)
				await msg.channel.send(embed = embed)

		else:
			embed = discord.Embed(
				title = "⚠️エラー⚠️",
				description = "ㅤ\n引数が不正です。\n\n" + 
				"`Hint : ○を入れていますか？また、○だけになっていませんか？`\n" + 
				"`       また、'○' には \\u25CB を使用して下さい。`"
				if get == 0 else "解読できませんでした。",
				color = 0xFF0000
			)
			await msg.channel.send(embed = embed)


client.run(TOKEN)
