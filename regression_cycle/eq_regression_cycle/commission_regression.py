from custom.basic_custom_actions import timestamps
from test_cases.eq.Commissions import QAP_2998, QAP_3285, QAP_4373, QAP_4489, QAP_4231, QAP_3351

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None):
    report_id = bca.create_event('Commission ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    session_id = set_session_id()
    seconds, nanos = timestamps()  # Store case start time
    try:
        QAP_2998.execute(report_id, session_id)
        QAP_3285.execute(report_id, session_id)
        QAP_3351.execute(report_id, session_id)
        QAP_4231.execute(report_id, session_id)
        QAP_4373.execute(report_id, session_id)
        QAP_4489.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Commission regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
