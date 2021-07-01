from regression_cycle.fx_regression_cycle import rfq_taker_regression, esp_mm_regression, esp_taker_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


def test_run(parent_id=None):
    report_id = bca.create_event('Forex regression_cycle', parent_id)
    try:
        # rfq_taker_regression.test_run(report_id)
        esp_mm_regression.test_run(report_id)
        # esp_taker_regression.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
