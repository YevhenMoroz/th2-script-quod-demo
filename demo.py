import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Basket.QAP_3882 import QAP3882
from test_cases.eq.Basket.QAP_4648 import QAP4648
from test_framework.core.example_of_ideal_test_case_ui import QAP_Example
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('test ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()

    try:
        # example_java_api.TestCase(report_id).execute()
        QAP4648(report_id, session_id, None).execute()

        # example of test with usage class TestCase, data_sets and UI wrappers
        fx_data_set = FxDataSet()
        QAP_Example(report_id, session_id, fx_data_set).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
