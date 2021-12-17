from test_cases.algo.algo_acceptance_list import QAP_2995, QAP_2994, QAP_2839, QAP_2996, QAP_2842, QAP_2997
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.utils import set_session_id, prepare_fe, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None):
    report_id = bca.create_event('Algo regression_cycle', parent_id)
    try:
        session_id = set_session_id()
        if not Stubs.frontend_is_open:
            prepare_fe(report_id, session_id, work_dir, username, password)
        else:
            get_opened_fe(report_id, session_id, work_dir)
            
        QAP_2839.execute(report_id, session_id)
        QAP_2842.execute(report_id, session_id)
        QAP_2994.execute(report_id, session_id)
        QAP_2995.execute(report_id, session_id)
        QAP_2996.execute(report_id, session_id)
        QAP_2997.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()