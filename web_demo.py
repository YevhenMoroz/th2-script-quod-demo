import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from web_admin_modules.web_wrapper import call, login, logout
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_cases.web_admin import login_logout_example, QAP_758, QAP_760, QAP_761, QAP_763, QAP_801

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

    for environment in test_cases:
        # Drivers
        chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
        wait_driver = WebDriverWait(chrome_driver, 10)
        # Start session
        call(login, report_id, f'Start session (Login, {environment} env)', chrome_driver, wait_driver, environment)
        chrome_driver.maximize_window()
        try:
            for test in test_cases[environment]:
                test.TestCase(report_id, chrome_driver, wait_driver).execute()
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
