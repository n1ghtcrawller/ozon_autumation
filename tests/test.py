import requests
from config import Config

class TestProxy:
    def __init__(self, config):
        self.config = config

    def test_proxy(self):
        proxy = {
            'http': f'http://{self.config.proxy_user}:{self.config.proxy_pass}@{self.config.proxy}',
            'https': f'http://{self.config.proxy_user}:{self.config.proxy_pass}@{self.config.proxy}'
        }

        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=10)
            print("Прокси работает:", response.json())
        except Exception as e:
            print("Прокси не работает:", str(e))

# Пример использования
config = Config()
test_proxy = TestProxy(config)
test_proxy.test_proxy()