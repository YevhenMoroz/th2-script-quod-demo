from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_PercentageVolume import QAP_T4556, QAP_T4580, QAP_T4599, QAP_T4568, QAP_T4604, QAP_T4567, QAP_T4574, QAP_T4590, QAP_T4648, QAP_T4662, QAP_T4569, QAP_T4573, QAP_T4660, QAP_T4661, QAP_T4659, \
    QAP_T4603, QAP_T4631, QAP_T4566

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
        QAP_T4648.execute(report_id)
        QAP_T4662.execute(report_id)
        QAP_T4661.execute(report_id)
        QAP_T4660.execute(report_id)
        QAP_T4659.execute(report_id)
        QAP_T4603.execute(report_id)
        QAP_T4599.execute(report_id)
        QAP_T4631.execute(report_id)
        QAP_T4569.execute(report_id)
        QAP_T4567.execute(report_id)
        QAP_T4573.execute(report_id)
        QAP_T4568.execute(report_id)
        QAP_T4566.execute(report_id)
        QAP_T4574.execute(report_id)
        QAP_T4580.execute(report_id)
        QAP_T4590.execute(report_id)
        QAP_T4604.execute(report_id)
        QAP_T4556.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
