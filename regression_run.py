from xml.etree import ElementTree
from custom import basic_custom_actions as bca
from regression_cycle import algo_regression
from stubs import Stubs, ROOT_DIR
import logging
from datetime import datetime


def regression_run():
    logging.getLogger().setLevel(logging.WARN)
    start = datetime.now()
    try:
        print(f'start time = {start}')
        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()

        report_id = bca.create_event(root.find("name").text + start.strftime(' %Y%m%d-%H:%M:%S'))

        if eval(root.find("algo").attrib["run"]):
            algo_regression.test_run(report_id)
        # if eval(root.find("fx").attrib["run"]):
        #     algo_regression.test_run(report_id)
        # if eval(root.find("oms").attrib["run"]):
        #     algo_regression.test_run(report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        print('duration time = ' + str(datetime.now() - start))


if __name__ == '__main__':
    regression_run()
    Stubs.factory.close()
