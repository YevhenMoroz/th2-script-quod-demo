from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_positions import QAP_2505, QAP_2378, QAP_2491, QAP_2492, QAP_2494, QAP_2496, QAP_2497, \
    QAP_1897, QAP_1898, QAP_2506, QAP_2508, QAP_2500
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('RFQ Taker regression', parent_id)
    session_id = set_session_id()
    try:
        QAP_1897.execute(report_id, session_id)
        QAP_1898.execute(report_id, session_id)
        QAP_2378.execute(report_id, session_id)
        QAP_2491.execute(report_id, session_id)
        QAP_2492.execute(report_id, session_id)
        QAP_2494.execute(report_id, session_id)
        QAP_2496.execute(report_id, session_id)
        QAP_2497.execute(report_id, session_id)
        QAP_2500.execute(report_id, session_id)
        QAP_2505.execute(report_id, session_id)
        QAP_2506.execute(report_id, session_id)
        QAP_2508.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
