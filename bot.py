from config import *
from utils import *
from uuid import uuid4
import telegram
import time
from os import path, remove
from pyshorteners import Shortener

bot = telegram.Bot(token=bot_token)
shortener = Shortener('Bitly', bitly_token=bitly_access_token)
last_article_link = ""

while True:
    new_article_link = get_last_article()
    if new_article_link != last_article_link:
        output_name = "{}.png".format(uuid4())
        generate_wordcloud(new_article_link[0], output_name)

        # shorturl = shortener.short(new_article_link[0])
        shorturl = new_article_link[0]
        caption = "{}\n{}".format(new_article_link[1], shorturl)

        bot.send_photo(chat_id=channel_id, photo=open(path.join(d, output_name), 'rb'), caption=caption)
        remove(output_name)

        last_article_link = new_article_link
    time.sleep(waiting_timeout)

virgool_article = 'https://virgool.io/@f680122/%D8%AA%D8%BA%D8%B0%DB%8C%D9%87-%D9%85%D9%86%D8%A7%D8%B3%D8%A8-%D8%A8%D8%B1%D8%A7%DB%8C-%D9%85%D9%82%D8%A7%D8%A8%D9%84%D9%87-%D8%A8%D8%A7-%D8%A2%D9%84%D9%88%D8%AF%DA%AF%DB%8C-%D9%87%D9%88%D8%A7-gyabu5maoi2n'
generate_wordcloud(virgool_article, "{}.png".format(uuid4()))
