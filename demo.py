import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Care.QAP_1016 import QAP_1016
from test_cases.eq.Care.QAP_5000 import QAP_5000
from test_cases.eq.Care.QAP_5337 import QAP_5337
from test_cases.eq.Care.QAP_5593 import QAP_5593
from test_cases.eq.Care.QAP_5835 import QAP_5835
from test_cases.eq.Care.QAP_5858 import QAP_5858
from test_cases.eq.PostTrade.QAP_3359 import QAP_3359
from test_cases.eq.PostTrade.QAP_3362 import QAP_3362
from test_cases.eq.PostTrade.QAP_5002 import QAP_5002
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('test ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()

    try:
        configuration = ComponentConfiguration("DMA")
        base_main_window = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)
        fe_environment = configuration.environment.get_list_fe_environment()[0]
        print(fe_environment.user, fe_environment.password, fe_environment.path)
        base_main_window.open_fe(report_id, fe_environment.path, fe_environment.user, fe_environment.password, True)
        QAP_3359(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                 environment=configuration.environment).execute()
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
