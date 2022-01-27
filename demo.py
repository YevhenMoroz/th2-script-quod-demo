import logging
import time
from datetime import datetime

from MyFiles.MyTest import MyTest
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_cases.fx.fx_mm_esp.QAP_3537 import QAP_3537
from test_cases.fx.fx_mm_esp.QAP_6149 import QAP_6149
from test_cases.fx.fx_mm_esp.QAP_6153 import QAP_6153
from test_cases.fx.fx_taker_rfq.QAP_6 import QAP_6
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)
timeouts = False

channels = dict()

def test_run():

    # Generation id and time for test run
    report_id = bca.create_event('Aleksey tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"

    session_id = set_session_id()
    data_set = FxDataSet()

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)
        #
        # QAP_6153(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_3537(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_6149(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_6(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # MyTest(report_id=report_id, session_id=session_id, data_set=data_set).execute()

        # rm = RuleManager()
        # rm.print_active_rules()
        # rm.print_active_rules_sim_test()
        # time.sleep(5)
        # send_rfq.execute(report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








