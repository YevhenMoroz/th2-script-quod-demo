import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from web_admin_modules.web_wrapper import call, login, logout
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_cases.web_admin import login_logout_example, QAP_758, QAP_760, test

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation ID and time for test run
    report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
                                 + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    # Drivers
    chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
    wait_driver = WebDriverWait(chrome_driver, 10)

    # Start session
    call(login, report_id, 'Start session (Login, 303 env)', chrome_driver, wait_driver, '303')
    # call(login, report_id, 'Start session (Login, 305 env)', chrome_driver, wait_driver, '305')
    chrome_driver.maximize_window()

    try:
        # login_logout_example.TestCase(report_id, chrome_driver, wait_driver).execute()
        # QAP_758.TestCase(report_id, chrome_driver, wait_driver).execute()
        QAP_760.TestCase(report_id, chrome_driver, wait_driver).execute()
        # test.TestCase(report_id, chrome_driver, wait_driver).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        # End session
        call(logout, report_id, 'End session (Logout)', wait_driver)
        chrome_driver.close()


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
