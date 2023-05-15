DOMAIN = "157.245.192.141:5244"
# DOMAIN = "localhost:5244" # 本地部署则为 localhost:port 或 127.0.0.1:port

USER_NAME = "admin"

PASSWORD = "admin"

DOWNLOAD_PATH = "pikpak1/anime"

REGEX_PATTERN = {
    "简体": r"(简体)|(简中)|(简日)|(CHS)",
    "繁体": r"(繁体)|(繁中)|(繁日)|(CHT)",
    "1080": r"(1080[pP])",
    "非合集": r"^((?!合集).)*$",
}

SUBSCRIBE_URL = "https://mikanani.me/RSS/MyBangumi?token=VE7krtVGIaixJ7oBSHaSzg%3d%3d"

FILTERS = ["1080", "非合集"]

INTERVAL_TIME = 0  # 定时执行的间隔时间，单位为秒，0 为只运行一次

# ==================== Telegram Bot ====================
TELEGRAM_NOTIFICATION = False  # 是否开启 Telegram 通知, True 开启, False 关闭
BOT_TOKEN = ""  # 你的 Telegram 用户 ID
USER_ID = ""  # 你的 Telegram Bot Token
