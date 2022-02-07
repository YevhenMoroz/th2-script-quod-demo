from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle import iceberg_regression, multilisted_regression, twap_regression
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from test_framework.core.environment import Environment
from test_framework.data_sets.environment_type import EnvironmentType



def test_run(parent_id=None):
    try:
        logging.getLogger().setLevel(logging.WARN)
        report_id = bca.create_event('Algo regression_cycle', parent_id)

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()


        # if eval(root.find(".//component[@name='twap']").attrib["run"]):
        #     twap_regression.test_run(report_id)
        # if eval(root.find(".//component[@name='multilisted']").attrib["run"]):
        #     multilisted_regression.test_run(report_id)
        # if eval(root.find(".//component[@name='parcitipation']").attrib["run"]):
        #     participation_regression.test_run(report_id)
        if eval(root.find(".//component[@name='iceberg']").attrib["run"]):
            iceberg_regression.test_run(parent_id=report_id)

        #RB
        #twap_regression_rb.test_run(report_id)
        #parcitipation_regression_rb.test_run(report_id)
        #vwap_regression_rb.test_run(report_id)

        #UAT
        # iceberg_regression.test_run(report_id)
        # multilisted_regression.test_run(report_id)
        # twap_regression.test_run(report_id)
        # parcitipation_regression.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()