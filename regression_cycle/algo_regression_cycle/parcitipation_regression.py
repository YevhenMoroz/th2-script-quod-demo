from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime
from quod_qa.eq.Algo_PercentageVolume import  QAP_1324, QAP_1750, QAP_1510, QAP_1515, QAP_1516, QAP_3070, QAP_2479, QAP_3116, QAP_3065, QAP_3063, QAP_3127, QAP_1633, QAP_2980, QAP_3061, QAP_3062, QAP_2838, QAP_2552, QAP_2553,QAP_1634, QAP_2583, QAP_3062, QAP_3530
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
            
        QAP_1633.execute(report_id)
        QAP_1634.execute(report_id)
        QAP_2479.execute(report_id)
        QAP_2980.execute(report_id)
        QAP_3061.execute(report_id)
        QAP_3062.execute(report_id)
        QAP_3063.execute(report_id)
        QAP_3065.execute(report_id)
        QAP_3070.execute(report_id)
        QAP_3116.execute(report_id)
        QAP_3127.execute(report_id)
        QAP_3530.execute(report_id)
        # FIX/FE
        # QAP_1324.execute(report_id, session_id)
        # QAP_1510.execute(report_id, session_id)
        # QAP_1515.execute(report_id, session_id)
        # QAP_1516.execute(report_id, session_id)
        # QAP_1750.execute(report_id, session_id)
        # QAP_2552.execute(report_id, session_id)
        # QAP_2553.execute(report_id, session_id)
        # QAP_2838.execute(report_id, session_id)
        # end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
