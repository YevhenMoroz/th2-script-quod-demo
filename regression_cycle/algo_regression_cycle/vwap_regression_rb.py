from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_VWAP import QAP_4699, QAP_4940, QAP_4700, QAP_4735, QAP_4801, QAP_4800, QAP_4734, QAP_4756, QAP_4733

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
        QAP_4699.execute(report_id)
        QAP_4700.execute(report_id)
        QAP_4733.execute(report_id)
        QAP_4734.execute(report_id)
        QAP_4735.execute(report_id)
        QAP_4940.execute(report_id)
        QAP_4800.execute(report_id)
        QAP_4801.execute(report_id)
        QAP_4756.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
