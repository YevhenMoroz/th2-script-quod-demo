import time

from quod_qa.web_admin import login_logout_example, QAP_758
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from regression_cycle.web_admin_cycle.run_client_accounts import RunClientsAccounts
from regression_cycle.web_admin_cycle.run_fx_market_making import RunFxMarketMaking
from regression_cycle.web_admin_cycle.run_general import RunGeneral
from regression_cycle.web_admin_cycle.run_middle_office import RunMiddleOffice
from regression_cycle.web_admin_cycle.run_order_management import RunOrderManagement
from regression_cycle.web_admin_cycle.run_other import RunOthers
from regression_cycle.web_admin_cycle.run_positions import RunPositions
from regression_cycle.web_admin_cycle.run_reference_data import ReferenceData
from regression_cycle.web_admin_cycle.run_risk_limits import RunRiskLimits
from regression_cycle.web_admin_cycle.run_site import RunSite
from regression_cycle.web_admin_cycle.run_users import RunUsers
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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
        web_driver_container = WebDriverContainer()
        #RunGeneral(web_driver_container, parent_id).execute()
        #RunSite(web_driver_container, report_id).execute()
        #RunUsers(web_driver_container, parent_id).execute()
        #ReferenceData(web_driver_container, parent_id).execute()
        #RunClientsAccounts(web_driver_container, parent_id).execute()
        #RunOrderManagement(web_driver_container, parent_id).execute()
        RunMiddleOffice(web_driver_container, parent_id).execute()
        #RunFxMarketMaking(web_driver_container, parent_id).execute()
        #RunRiskLimits(web_driver_container, parent_id).execute()
        #RunPositions(web_driver_container, parent_id).execute()
        #RunOthers(web_driver_container, parent_id).execute()

        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))

    except Exception as e:
        print(e.__class__.__name__)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
