import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from stubs import Stubs
from custom import basic_custom_actions as bca
from quod_qa.web_admin import QAP_758, login_logout_example

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

test_cases = {
    '303': [login_logout_example,
            QAP_758,
            ],
    '305': [login_logout_example,
            ]
}


def test_run():
    # Generation ID and time for test run
    report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
                                 + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
    wait_driver = WebDriverWait(chrome_driver, 15)
    # Start session
    chrome_driver.maximize_window()

    login_page = LoginPage(chrome_driver, wait_driver)
    login_page.set_login("adm04")
    login_page.set_password("adm04")
    login_page.click_login_button()
    login_page.check_is_login_successful()


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
