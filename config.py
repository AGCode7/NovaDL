import os
from pathlib import Path

# ========== مسیرهای فایل ==========
BASE_DIR = Path(__file__).parent
APP_DATA_DIR = Path(os.getenv("LOCALAPPDATA")) / "NovaDL"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

ICON_PATH = BASE_DIR / "icon" / "icon.ico"
DATABASE_PATH = APP_DATA_DIR / "database.db"
JSON_PATH = APP_DATA_DIR / "setting.json"

# ========== تنظیمات پنجره ==========
WINDOW_TITLE = "NovaDL"
WINDOW_SIZE = "600x350"
WINDOW_RESIZABLE = (False, False)

# ========== تنظیمات فونت ==========
FONT_SIZE = 11
FONT_WEIGHT = "bold"

# ========== رنگ‌های اصلی ==========
COLOR_PRIMARY = "#4F46E5"
COLOR_PRIMARY_HOVER = "#6366F1"
COLOR_BG_DARK = "#2B2B2B"
COLOR_BG_LIGHT = "#383838"
COLOR_TEXT_WHITE = "white"
COLOR_TEXT_GRAY = "#BDBDBD"

# ========== رنگ‌های ورودی‌ها ==========
FG_ENTRY_COLOR = COLOR_BG_DARK
BORDER_ENTRY_COLOR = COLOR_PRIMARY

# ========== رنگ‌های دکمه‌ها ==========
BTN_DOWNLOAD_COLOR = "#00ff26"
BTN_DOWNLOAD_HOVER = "#00bd1c"
BTN_START_COLOR = "#22c55e"
BTN_START_HOVER = "#16A34A"
BTN_PAUSE_COLOR = "#ff0000"
BTN_PAUSE_HOVER = "#ff3d3d"
BTN_FOLDER_COLOR = COLOR_PRIMARY
BTN_FOLDER_HOVER = COLOR_PRIMARY_HOVER
BTN_SHUTDOWN_COLOR = COLOR_BG_DARK
BTN_SHUTDOWN_HOVER = "#3b3b3b"
BTN_SHUTDOWN_TEXT = COLOR_TEXT_GRAY
BTN_SHUTDOWN_ACTIVE_COLOR = COLOR_PRIMARY
BTN_SHUTDOWN_ACTIVE_HOVER = COLOR_PRIMARY_HOVER
BTN_SHUTDOWN_ACTIVE_TEXT = COLOR_TEXT_WHITE

# ========== رنگ نوار پیشرفت و باکس لاگ ==========
PROGRESS_COLOR = COLOR_PRIMARY
LOG_BOX_COLOR = COLOR_BG_LIGHT

# ========== ابعاد و اندازه‌ها ==========
BTN_WIDTH = 107
PROGRESS_WIDTH = 550
LOG_BOX_HEIGHT = 150
ENTRY_WIDTH = 88

# ========== فاصله‌ها ==========
PADY_MAIN = 20
PADY_SMALL = 5
PADX_MAIN = 20
PADX_SMALL = 6

# ========== مسیر پیش‌فرض دانلود ==========
DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads" / "NovaDL"
TEMPLATE_PATH = BASE_DIR / "templates"

# ========== تنظیمات دانلود ==========
DEFAULT_PAGE_COUNT = 1
SHUTDOWN_DELAY_MINUTES = 1

# ========== تنظیمات شبکه ==========
REQUEST_TIMEOUT = 10  # تایم‌اوت برای دریافت HTML (ثانیه)
DOWNLOAD_TIMEOUT = 20  # تایم‌اوت برای دانلود فایل (ثانیه)

# ========== آدرس‌های سایت ==========
BASE_URL = "https://iromusic.app"
ENDPOINT = "/singles"
QUERY_PARAMS = params = {"countries": "iran", "sort": "latest", "page": None}
DOWNLOAD_DOMAIN = "https://irolive.ir/"
MUSIC_PATH_PREFIX = "/music/"

# ========== متن‌های ثابت ==========
TEXT_APP_TITLE = "Nova DownLoader"
TEXT_FOLDER_PLACEHOLDER = "File Storage Path"
TEXT_PAGES_PLACEHOLDER = "Like 3"
TEXT_BTN_DOWNLOAD = "Download"
TEXT_BTN_START = "Start"
TEXT_BTN_RESUME = "Resume"
TEXT_BTN_PAUSE = "Pause"
TEXT_BTN_FOLDER = "Browse"
TEXT_BTN_SHUTDOWN_ON = "ShutDown: On"
TEXT_BTN_SHUTDOWN_OFF = "ShutDown: Off"
TEXT_LABEL_PAGES = "Number Pages:"

# ========== پیام‌های لاگ ==========
LOG_SHUTDOWN_SYSTEM = "System will shut down in {} Minutes..."
LOG_DOWNLOADING = "Downloading: {} ..."
LOG_DUPLICATE_MUSIC = "{} Duplicated."
LOG_DOWNLOAD_SUCCESS = "{} Downloaded.\n"
LOG_ERROR_DATABASE = "ERROR In Database.\n"
LOG_READING_PAGE = "Reading Page: {} ..."
LOG_PAGE_NOT_FOUND = "Page {} Not Found, Continue..."
LOG_MUSIC_NOT_FOUND = "Music Not Found."
LOG_DOWNLOADING_MUSIC = "{} Downloading Music..."
LOG_DOWNLOAD_PAUSSED = "Download Stoped."
LOG_END_OPERATION = "End Operation."
LOG_ERROR_DOWNLOAD = "ERROR Download File ({}): {}"
LOG_ERROR_SAVE = "ERROR Save File ({}): {}"
LOG_ERROR_UNKNOWN = "ERROR Unknown ({}): {}"
LOG_PAGE_MUSIC_NOT_FOUND = "Page {} Not Found."
LOG_SHUTDOWN_ERROR = "سیستم‌عامل {} پشتیبانی نمی‌شود."
LOG_SAVE_PDF = "PDF Last Music Saved."
LOG_SAVE_PDF_ERROR = "Error To Save PDF."
MESSAGEBOX_SUCCESSFULY = "The download completed successfully."
