import logging
import time
from datetime import timedelta

from custom import basic_custom_actions as bca
from regression_cycle.web_trading_cycle.run_general import RunGeneral
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from stubs import Stubs

logging.basicConfig(format='%(asctime)s - %(message)s')
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARN)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Web Admin regression_cycle', parent_id)
    try:
        start_time = time.monotonic()
        # Generation ID and time for test run
        # report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
        #                              + datetime.now().strftime('%Y%m%d-%H:%M:%S'),parent_id)
        # logger.info(f"Root event was created (id = {report_id.id})")

        # content
        web_driver_container = WebDriverContainer(url="http://10.0.22.38:6780/quodtrading/qakharkiv320Trading/#/signin")


        # RunGeneral(web_driver_container, parent_id).execute() just for e.g.


        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))

    except Exception as e:
        print(e.__class__.__name__)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
