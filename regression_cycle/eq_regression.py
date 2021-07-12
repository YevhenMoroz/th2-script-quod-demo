from regression_cycle.eq_regression_cycle import dma_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime


def test_run(parent_id= None):
    report_id = bca.create_event('Equity regression_cycle', parent_id)
    try:
        dma_regression.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()