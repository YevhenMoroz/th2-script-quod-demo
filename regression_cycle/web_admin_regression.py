import time

from quod_qa.web_admin import login_logout_example, QAP_758
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from regression_cycle.web_admin_cycle.run_fx_market_making import RunFxMarketMaking
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

# test_cases = {
#     '303': [login_logout_example,
#             QAP_758,
#             ],
#     '305': [login_logout_example,
#             ]
# }


def test_run(parent_id= None):
    report_id = bca.create_event('Web Admin regression_cycle', parent_id)
    try:
        start_time = time.monotonic()
        # Generation ID and time for test run
        report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
                                     + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
        logger.info(f"Root event was created (id = {report_id.id})")

        # content
        web_driver_container = WebDriverContainer()
        # RunPositions(web_driver_container, report_id).execute()
        # RunClientsAccounts(web_driver_container, report_id).execute()
        # print(timedelta(seconds=end_time - start_time))
        # RunOthers(web_driver_container, report_id).execute()
        # RunOrderManagement(web_driver_container, report_id).execute()
        # RunUsers(web_driver_container, report_id).execute()
        RunFxMarketMaking(web_driver_container, report_id).execute()
        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))
    except Exception as e:
        print(e.__class__.__name__)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()