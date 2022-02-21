import logging
import time
from datetime import timedelta
from xml.etree import ElementTree

from custom import basic_custom_actions as bca
from regression_cycle.web_trading_cycle.run_order_book import RunOrderBook
from stubs import Stubs, ROOT_DIR

logging.basicConfig(format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.WARN)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Web Admin regression_cycle', parent_id)
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    try:
        start_time = time.monotonic()
        if eval(root.find(".//component[@name='WebTradingOrderBook']").attrib["run"]):
            RunOrderBook(report_id).execute()
        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))

    except Exception as e:
        print(e.__class__.__name__)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
