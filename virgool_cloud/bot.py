from config import *
from utils import *
from uuid import uuid4
import telegram
import time
from os import path, remove
from pyshorteners import Shortener

bot = telegram.Bot(token=bot_token)
shortener = Shortener('Bitly', bitly_token=bitly_access_token)
last_article_link = get_vars(vars_file)

while True:
    try:
        new_article_link = get_last_article()
    except:
        time.sleep(waiting_timeout)
        continue
    if new_article_link != last_article_link:
        TMP_DIR = create_temp()
        output_name = "{}.png".format(uuid4())
        generate_wordcloud(new_article_link[0], path.join(TMP_DIR, output_name))

        try:
            shorturl = shortener.short(new_article_link[0])
        except:
            shorturl = new_article_link[0]
            print("cannot shorten link :(")

        caption = "{}\n{}".format(new_article_link[1], shorturl)

        try:
            bot.send_photo(chat_id=channel_id, photo=open(path.join(TMP_DIR, output_name), 'rb'), caption=caption)
        except:
            print("failed =))")
            time.sleep(waiting_timeout)
            continue
            
        remove_dir(TMP_DIR)

        last_article_link = new_article_link
        persist(vars_file, last_article_link)
    time.sleep(waiting_timeout)
