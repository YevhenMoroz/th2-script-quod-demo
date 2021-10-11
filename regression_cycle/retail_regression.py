from regression_cycle.retail_regression_cycle import dma_regression, care_regression, iceberg_regression

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


from win_gui_modules.utils import prepare_fe, set_session_id


def test_run(parent_id=None):
    session_id = set_session_id()
    report_id = bca.create_event('Retail regression_cycle', parent_id)
    try:
        care_regression.test_run(session_id, report_id)
        dma_regression.test_run(session_id, report_id)
        iceberg_regression.test_run(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
