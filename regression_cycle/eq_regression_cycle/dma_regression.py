from custom.basic_custom_actions import timestamps
from quod_qa.eq.DMA import QAP_2000, QAP_2001
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


def test_run(parent_id=None):
    report_id = bca.create_event('dma regression', parent_id)
    session_id = set_session_id()
    seconds, nanos = timestamps()  # Store case start time
    try:
        QAP_2000.execute(report_id, session_id)
        QAP_2001.execute(report_id, session_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"dma regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
