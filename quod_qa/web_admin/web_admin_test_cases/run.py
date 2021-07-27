import logging
import time
from datetime import datetime
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.client_accounts.run_client_accounts import RunClientsAccounts

from quod_qa.web_admin.web_admin_test_cases.general.run_general import RunGeneral
from quod_qa.web_admin.web_admin_test_cases.order_management.run_order_management import RunOrderManagement
from quod_qa.web_admin.web_admin_test_cases.others.run_other import RunOthers
from quod_qa.web_admin.web_admin_test_cases.positions.run_positions import RunPositions
from quod_qa.web_admin.web_admin_test_cases.users.run_users import RunUsers
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


# NOTE: for now the following code is using only to check implementation of pages. It will be updated in the future
def test_run():
    start_time = time.monotonic()
    # Generation ID and time for test run
    report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
                                 + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    # content
    web_driver_container = WebDriverContainer()
    # RunPositions(web_driver_container, report_id).execute()
    RunClientsAccounts(web_driver_container, report_id).execute()
    # print(timedelta(seconds=end_time - start_time))
    # RunOthers(web_driver_container, report_id).execute()
    # RunOrderManagement(web_driver_container, report_id).execute()
    # RunUsers(web_driver_container, report_id).execute()
    end_time = time.monotonic()
    print("Test cases completed\n" +
          "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
