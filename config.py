from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()
@dataclass
class Config:
    proxy: str = os.getenv("PROXY")
    proxy_user: str = os.getenv("PROXY_USER")
    proxy_pass: str = os.getenv("PROXY_PASS")
    imap_server: str = os.getenv("IMAP_SERVER")
    ozon_url: str = os.getenv("OZON_URL")
    excel_path: str = os.getenv("EXCEL_PATH")
    wait_timeout: int = os.getenv("WAIT_TIMEOUT")