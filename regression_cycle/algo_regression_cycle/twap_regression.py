from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime
from quod_qa.eq.Algo_TWAP import QAP_2864, QAP_2865, QAP_3121, QAP_3117, QAP_3120, QAP_3119, QAP_2478, QAP_3532, QAP_2977, QAP_1318, QAP_1319, QAP_3032, QAP_2955, QAP_3123, QAP_2706, QAP_3122, QAP_3124
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
    report_id = bca.create_event('TWAP ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    try:
        session_id = set_session_id()
        if not Stubs.frontend_is_open:
            prepare_fe(report_id, session_id, work_dir, username, password)
        else:
            get_opened_fe(report_id, session_id, work_dir)

        QAP_2706.execute(report_id)
        QAP_2478.execute(report_id)
        QAP_2955.execute(report_id)
        QAP_2977.execute(report_id)
        QAP_3032.execute(report_id)
        QAP_3117.execute(report_id)
        QAP_3119.execute(report_id)
        QAP_3120.execute(report_id)
        QAP_3121.execute(report_id)
        QAP_3122.execute(report_id)
        QAP_3123.execute(report_id)
        QAP_3124.execute(report_id)
        QAP_3532.execute(report_id)
        # #FIX/FE
        QAP_2864.execute(report_id, session_id)
        QAP_2865.execute(report_id, session_id)
        # #end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
