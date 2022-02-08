import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from stubs import Stubs
from pathlib import Path
from test_cases.eq.Care.QAP_1071 import QAP_1071
from test_cases.eq.Care.QAP_1072 import QAP_1072
from test_cases.eq.Care.QAP_1073 import QAP_1073
from test_cases.eq.Care.QAP_1074 import QAP_1074
from test_cases.eq.Care.QAP_1075 import QAP_1075
from test_cases.eq.Care.QAP_1076 import QAP_1076
from test_cases.eq.Care.QAP_1077 import QAP_1077
from test_cases.eq.Care.QAP_1078 import QAP_1078
from test_cases.eq.Care.QAP_1079 import QAP_1079
from test_cases.eq.Care.QAP_1080 import QAP_1080
from test_cases.eq.Care.QAP_1364 import QAP_1364
from test_cases.eq.Care.QAP_1406 import QAP_1406
from test_cases.eq.Care.QAP_1717 import QAP_1717
from test_cases.eq.Care.QAP_1718 import QAP_1718
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('skomanova ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()
    data_set = OmsDataSet()
    main_win = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)


    try:
        main_win.open_fe(report_id)
        # example_java_api.TestCase(report_id).execute()
        QAP_1718(report_id, session_id, data_set).execute()
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
