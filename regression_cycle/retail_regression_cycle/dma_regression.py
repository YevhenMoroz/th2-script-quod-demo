from test_cases.ret.DMA import RIN_1188, RIN_1189, QAP_4169, QAP_4172, QAP_4654, QAP_5106, QAP_5170, QAP_5425, QAP_5426
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
        QAP_4169.execute(session_id, report_id)
        QAP_4172.execute(session_id, report_id)
        QAP_4654.execute(session_id, report_id)
        QAP_5106.execute(session_id, report_id)
        QAP_5170.execute(session_id, report_id)
        QAP_5425.execute(report_id)
        QAP_5426.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
