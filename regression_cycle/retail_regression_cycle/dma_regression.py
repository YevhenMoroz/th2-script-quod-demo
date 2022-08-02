from test_cases.ret.DMA import RIN_1188, RIN_1189, QAP_T3790, QAP_T3788, QAP_T3705, QAP_T3662, QAP_T3661, QAP_5425, QAP_5426
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('DMA regression', parent_id)
    try:
        RIN_1188.execute(session_id, report_id)
        RIN_1189.execute(session_id, report_id)
        QAP_T3790.execute(session_id, report_id)
        QAP_T3788.execute(session_id, report_id)
        QAP_T3705.execute(session_id, report_id)
        QAP_T3662.execute(session_id, report_id)
        QAP_T3661.execute(session_id, report_id)
        QAP_5425.execute(report_id)
        QAP_5426.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
