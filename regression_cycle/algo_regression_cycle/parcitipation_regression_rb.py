from quod_qa.eq.Algo_PercentageVolume.QAP_4646 import execute
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime
from quod_qa.eq.Algo_PercentageVolume import QAP_4751, QAP_4952, QAP_4624, QAP_4605, QAP_4606, QAP_4607, QAP_4608, QAP_4752, QAP_4761, QAP_4644, QAP_4929, QAP_4933, QAP_4890, QAP_4930, QAP_4934, QAP_4889, QAP_4868, QAP_4784

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None):
    report_id = bca.create_event('Algo_POV: Additional Features', parent_id)
    try:        
        QAP_4624.execute(report_id)
        QAP_4605.execute(report_id)
        QAP_4606.execute(report_id)
        QAP_4607.execute(report_id)
        QAP_4608.execute(report_id)
        QAP_4752.execute(report_id)
        QAP_4761.execute(report_id)
        QAP_4644.execute(report_id)
        QAP_4929.execute(report_id)
        QAP_4933.execute(report_id)
        QAP_4890.execute(report_id)
        QAP_4930.execute(report_id)
        QAP_4934.execute(report_id)
        QAP_4889.execute(report_id)
        QAP_4868.execute(report_id)
        QAP_4784.execute(report_id)
        QAP_4751.execute(report_id)
        QAP_4952.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
