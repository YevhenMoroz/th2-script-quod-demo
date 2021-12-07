from regression_cycle.algo_regression_cycle import iceberg_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime


def test_run(parent_id= None):
    logging.getLogger().setLevel(logging.WARN)
    report_id = bca.create_event('Algo regression_cycle', parent_id)
    try:
        #RB
        #twap_regression_rb.test_run(report_id)
        #parcitipation_regression_rb.test_run(report_id)
        #vwap_regression_rb.test_run(report_id)

        #UAT
        iceberg_regression.test_run(report_id)
        # multilisted_regression.test_run(report_id)
        # twap_regression.test_run(report_id)
        # parcitipation_regression.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()