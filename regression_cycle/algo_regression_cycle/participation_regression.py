from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_PercentageVolume import QAP_T4912, QAP_T4911, QAP_T4913, QAP_T4914, QAP_T4933, QAP_T4879, QAP_T5088, QAP_T5089, QAP_T4890, QAP_T5064, QAP_T4915, QAP_T4761

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"POV" if version is None else f"POV (cloned) | {version}", parent_id)
    try:
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)
            
        QAP_T5089.execute(report_id)
        QAP_T5088.execute(report_id)
        QAP_T5064.execute(report_id)
        QAP_T4933.execute(report_id)
        QAP_T4915.execute(report_id)
        QAP_T4914.execute(report_id)
        QAP_T4913.execute(report_id)
        QAP_T4912.execute(report_id)
        QAP_T4911.execute(report_id)
        QAP_T4890.execute(report_id)
        QAP_T4879.execute(report_id)
        QAP_T4761.execute(report_id)
        # FIX/FE
        # QAP_T5113.execute(report_id, session_id)
        # QAP_T5097.execute(report_id, session_id)
        # QAP_T5096.execute(report_id, session_id)
        # QAP_T5095.execute(report_id, session_id)
        # QAP_T5084.execute(report_id, session_id)
        # QAP_T5050.execute(report_id, session_id)
        # QAP_T5049.execute(report_id, session_id)
        # QAP_T4950.execute(report_id, session_id)
        # end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
