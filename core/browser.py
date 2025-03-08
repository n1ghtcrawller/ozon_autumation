import undetected_chromedriver as uc
import requests
from selenium import webdriver


class BrowserAutomation:
    def __init__(self, config):
        self.config = config
        self.driver = None

    def test_proxy(self):
        proxy = {
            'http': f'http://{self.config.proxy_user}:{self.config.proxy_pass}:{self.config.proxy}',
            'https': f'http://{self.config.proxy_user}:{self.config.proxy_pass}:{self.config.proxy}'
        }

        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=10)
            print("Прокси работает:", response.json())
        except Exception as e:
            print("Прокси не работает:", str(e))

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-data-dir=./chromeprofile")
        options.add_argument('--disable-extensions')
        options.add_argument("--incognito")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--disable-web-security")
        driver = webdriver.Chrome()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                  const newProto = navigator.__proto__
                  delete newProto.webdriver
                  navigator.__proto__ = newProto
                  """
        })
        self.driver = uc.Chrome(options=options)

        return self.driver

    def quit(self):
        if self.driver:
            self.driver.quit()