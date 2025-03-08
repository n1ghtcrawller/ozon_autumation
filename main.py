from config import Config
from services.email import EmailClient
from services.excel import ExcelHandler
from core.browser import BrowserAutomation
from core.processor import OzonAccountProcessor
from utils.logger import setup_logger


def main():
    logger = setup_logger()
    config = Config()

    try:
        # Инициализация компонентов
        email_client = EmailClient(config)
        excel_handler = ExcelHandler(config)
        browser = BrowserAutomation(config)

        # Создание процессора
        processor = OzonAccountProcessor(config, browser, email_client)

        # Обработка аккаунтов
        for index, account in excel_handler.get_accounts():
            logger.info(f"Processing account: {account['Фамилия Имя']}")
            try:
                processor.process_account(account)
                cookies = browser.driver.get_cookies()
                excel_handler.update_cookies(index, cookies)
                logger.info("Successfully processed account")
            except Exception as e:
                logger.error(f"Error processing account: {str(e)}")

    except Exception as e:
        logger.critical(f"Critical error: {str(e)}")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()