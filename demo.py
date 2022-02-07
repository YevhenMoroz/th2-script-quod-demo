import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Care.QAP_1016 import QAP_1016
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('test ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()
    base_main_window = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)
    data_set = OmsDataSet()

    try:
        base_main_window.open_fe(report_id=report_id)
        QAP_1016(report_id, data_set).execute()
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
