import logging
import time
from datetime import timedelta
from xml.etree import ElementTree

from custom import basic_custom_actions as bca
from regression_cycle.web_admin_cycle.run_order_management_palgo import RunOrderManagement
from regression_cycle.web_admin_cycle.run_risk_limits_palgo import RunRiskLimits
from stubs import Stubs, ROOT_DIR

logging.basicConfig(format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.WARN)
timeouts = False
channels = dict()


def test_run(parent_id=None):

    mode = "Verification"
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    name = root.find(".//name").text
    version = root.find(".//version").text
    report_id = bca.create_event(f'{name} | {version}', parent_id)
    try:
        start_time = time.monotonic()
        RunOrderManagement(report_id, mode, version).execute()
        RunRiskLimits(report_id, mode, version).execute()
        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))

    except Exception as e:
        print(e.__class__.__name__)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
