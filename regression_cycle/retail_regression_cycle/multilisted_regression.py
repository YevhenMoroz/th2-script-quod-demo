from quod_qa.RET.Algo.Algo_Multilisted import QAP_1801, QAP_1803, QAP_1804, QAP_1808, QAP_1809, QAP_1989, QAP_1991, \
    QAP_1993, QAP_1994
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('DMA', parent_id)
    try:
        QAP_1801.execute(session_id, report_id)
        QAP_1803.execute(session_id, report_id)
        QAP_1804.execute(session_id, report_id)
        QAP_1808.execute(session_id, report_id)
        QAP_1809.execute(session_id, report_id)
        QAP_1989.execute(session_id, report_id)
        QAP_1991.execute(session_id, report_id)
        QAP_1993.execute(session_id, report_id)
        QAP_1994.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
