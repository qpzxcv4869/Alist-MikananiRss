import api
import config
import rss
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    handlers=[
        logging.FileHandler("log.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

rss_list = []

for each in config.RSS:
    sub_folder = each["subFolder"] if "subFolder" in each else None
    rss_list.append(rss.Rss(each["url"], each["filter"], sub_folder))

alist = api.Alist(config.DOMAIN)
resp = alist.login(config.USER_NAME, config.PASSWORD)
notification_bot = None
if config.TELEGRAM_NOTIFICATION:
    notification_bot = api.TelegramBot(config.BOT_TOKEN, config.USER_ID)
manager = rss.Manager(
    rss_list,
    download_path=config.DOWNLOAD_PATH,
    alist=alist,
    notification_bot=notification_bot,
)
manager.check_update()
