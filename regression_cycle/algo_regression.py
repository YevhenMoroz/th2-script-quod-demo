from regression_cycle.algo_regression_cycle import multilisted_regression, twap_regression, parcitipation_regression, iceberg_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime


def test_run(parent_id= None):
    report_id = bca.create_event('Algo regression_cycle', parent_id)
    try:
        iceberg_regression.test_run(report_id)
        multilisted_regression.test_run(report_id)
        twap_regression.test_run(report_id)
        parcitipation_regression.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()