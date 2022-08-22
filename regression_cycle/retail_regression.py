from regression_cycle.retail_regression_cycle import trading_rest_api_dma

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


def test_run(parent_id=None):
    report_id = bca.create_event('Retail regression_cycle', parent_id)
    try:
        trading_rest_api_dma.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
