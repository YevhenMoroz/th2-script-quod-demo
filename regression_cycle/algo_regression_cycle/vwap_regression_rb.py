from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_VWAP import QAP_T4616, QAP_T4563, QAP_T4615, QAP_T4611, QAP_T4583, QAP_T4584, QAP_T4612, QAP_T4601, QAP_T4613

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None):
    report_id = bca.create_event('Algo_VWAP: Additional Features', parent_id)
    try:              
        QAP_T4616.execute(report_id)
        QAP_T4615.execute(report_id)
        QAP_T4613.execute(report_id)
        QAP_T4612.execute(report_id)
        QAP_T4611.execute(report_id)
        QAP_T4563.execute(report_id)
        QAP_T4584.execute(report_id)
        QAP_T4583.execute(report_id)
        QAP_T4601.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
