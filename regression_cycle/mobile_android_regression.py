import logging

from test_framework.mobile_android_core.utils.driver import AppiumDriver
from stubs import Stubs
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None):
    report_id = bca.create_event(f"Sorping" if version is None else f"Sorping | {version}", parent_id)
    try:
        driver = AppiumDriver()

        RunLogin(driver, parent_id).execute()

    except Exception as e:
        print(e.__class__.__name__)

if __name__ == '__main__':
    test_run()
    Stubs.factory.close()

