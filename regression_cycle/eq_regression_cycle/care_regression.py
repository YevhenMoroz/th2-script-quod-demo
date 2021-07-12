from custom.basic_custom_actions import timestamps
from quod_qa.eq.Care import QAP_477, QAP_478, QAP_1012, QAP_1014, QAP_1013, QAP_1016, QAP_1015, QAP_1017, QAP_1020, \
    QAP_1019, QAP_1021
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
    report_id = bca.create_event('dma ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    session_id = set_session_id()
    seconds, nanos = timestamps()  # Store case start time
    try:
        QAP_477.execute(report_id, session_id)
        QAP_478.execute(report_id, session_id)
        QAP_1012.execute(report_id, session_id)
        QAP_1013.execute(report_id, session_id)
        QAP_1014.execute(report_id, session_id)
        QAP_1015.execute(report_id, session_id)
        QAP_1016.execute(report_id, session_id)
        QAP_1017.execute(report_id, session_id)
        QAP_1019.execute(report_id, session_id)
        QAP_1020.execute(report_id, session_id)
        QAP_1021.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"post trade regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
