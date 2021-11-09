from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime
from quod_qa.eq.Algo_Iceberg import QAP_3056, QAP_3029, QAP_3054, QAP_3055
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None):
    report_id = bca.create_event('Algo', parent_id)
    try:                
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)
            
        QAP_3056.execute(report_id)
        QAP_3055.execute(report_id)
        QAP_3054.execute(report_id)
        QAP_3029.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
