from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TWAP import QAP_T4936, QAP_T4883, QAP_T4886, QAP_T4887, QAP_T4882, QAP_T4760, QAP_T4935, QAP_T4889, QAP_T4884, QAP_T4924, QAP_T5065, QAP_T4988, QAP_T4885

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None, version = None):

    report_id = bca.create_event(f"TWAP" if version is None else f"TWAP (cloned) | {version}", parent_id)
    try:
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)

        QAP_T4988.execute(report_id)
        QAP_T5065.execute(report_id)
        QAP_T4936.execute(report_id)
        QAP_T4935.execute(report_id)
        QAP_T4924.execute(report_id)
        QAP_T4889.execute(report_id)
        QAP_T4887.execute(report_id)
        QAP_T4886.execute(report_id)
        QAP_T4885.execute(report_id)
        QAP_T4884.execute(report_id)
        QAP_T4883.execute(report_id)
        QAP_T4882.execute(report_id)
        QAP_T4760.execute(report_id)
        # #FIX/FE
        # QAP_T4946.execute(report_id, session_id)
        # QAP_T4945.execute(report_id, session_id)
        # #end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
