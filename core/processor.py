from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import logger
import requests


class OzonAccountProcessor:
    def __init__(self, config, browser, email_client):
        self.config = config
        self.browser = browser
        self.email_client = email_client

    def test_proxy(self):
        proxy = {
            'http': f'http://{self.config.proxy}:{self.config.proxy_user}:{self.config.proxy_pass}',
        }

        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=10)
            print("Прокси работает:", response.json())
        except Exception as e:
            print("Прокси не работает:", str(e))
    def process_account(self, account_data):
        try:
            self.test_proxy()
            driver = self.browser.start_browser()
            self._login_flow(driver, account_data)
        except KeyError as e:
            logger.error(f"Missing key in account data: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing account {account_data.get('Телефон', 'unknown')}: {str(e)}")  # Используем логгер
        finally:
            self.browser.quit()

    def _login_flow(self, driver, account):
        driver.get('https://bot.sannysoft.com')

        phone_input = WebDriverWait(driver, self.config.wait_timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']"))
        )
        phone_input.send_keys(account["Телефон"])

        login_button = WebDriverWait(driver, self.config.wait_timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Войти')]"))
        )
        login_button.click()

        # Получение и ввод кода
        code = self.email_client.get_verification_code(
            account["Привязанная почта"],
            account["Пароль IMAP почты"]
        )
        self._enter_verification_code(driver, code)

    def _enter_verification_code(self, driver, code):
        code_inputs = WebDriverWait(driver, self.config.wait_timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        for i, digit in enumerate(code):
            code_inputs[i].send_keys(digit)