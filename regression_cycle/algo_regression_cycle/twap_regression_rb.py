from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TWAP import QAP_T4666, QAP_T4690, QAP_T4687, QAP_T4693, QAP_T4579, QAP_T4700, QAP_T4702, QAP_T4664, QAP_T4697, QAP_T4695, QAP_T4691, QAP_T4605, QAP_T4698, QAP_T4692, QAP_T4600, QAP_T4572, \
    QAP_T4665, QAP_T4696, QAP_T4694, QAP_T4701, QAP_T4699, QAP_T4655, QAP_T4557

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None):
    report_id = bca.create_event('Algo_TWAP: Additional Features', parent_id)
    try:              
        QAP_T4655.execute(report_id)
        QAP_T4702.execute(report_id)
        QAP_T4666.execute(report_id)
        QAP_T4665.execute(report_id)
        QAP_T4664.execute(report_id)
        QAP_T4572.execute(report_id)
        QAP_T4557.execute(report_id)
        QAP_T4701.execute(report_id)
        QAP_T4700.execute(report_id)
        QAP_T4699.execute(report_id)
        QAP_T4698.execute(report_id)
        QAP_T4697.execute(report_id)
        QAP_T4579.execute(report_id)
        QAP_T4696.execute(report_id)
        QAP_T4695.execute(report_id)
        QAP_T4694.execute(report_id)
        QAP_T4693.execute(report_id)
        QAP_T4692.execute(report_id)
        QAP_T4691.execute(report_id)
        QAP_T4690.execute(report_id)
        QAP_T4687.execute(report_id)
        QAP_T4605.execute(report_id)
        QAP_T4600.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
