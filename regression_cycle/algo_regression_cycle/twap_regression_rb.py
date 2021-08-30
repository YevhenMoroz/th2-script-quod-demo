from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime
from quod_qa.eq.Algo_TWAP import QAP_4750, QAP_4760, QAP_4335, QAP_4405, QAP_4338, QAP_4612, QAP_4274, QAP_4582, QAP_4583, QAP_4584, QAP_4893, QAP_4876, QAP_4951, QAP_4333, QAP_4336, QAP_4340, QAP_4395, QAP_4402, QAP_4403, QAP_4404, QAP_4406, QAP_4407, QAP_4413

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
        QAP_4612.execute(report_id)
        QAP_4274.execute(report_id)
        QAP_4582.execute(report_id)
        QAP_4583.execute(report_id)
        QAP_4584.execute(report_id)
        QAP_4893.execute(report_id)
        QAP_4951.execute(report_id)
        QAP_4333.execute(report_id)
        QAP_4335.execute(report_id)
        QAP_4336.execute(report_id)
        QAP_4338.execute(report_id)
        QAP_4340.execute(report_id)
        QAP_4876.execute(report_id)
        QAP_4395.execute(report_id)
        QAP_4402.execute(report_id)
        QAP_4403.execute(report_id)
        QAP_4404.execute(report_id)
        QAP_4405.execute(report_id)
        QAP_4406.execute(report_id)
        QAP_4407.execute(report_id)
        QAP_4413.execute(report_id)
        QAP_4750.execute(report_id)
        QAP_4760.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
