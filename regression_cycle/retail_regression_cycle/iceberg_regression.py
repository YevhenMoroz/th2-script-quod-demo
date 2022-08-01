from test_cases.ret.Algo.Algo_Iceberg import QAP_T4546, QAP_T4545, QAP_T4544, QAP_T4540, QAP_T4539, QAP_T4532, QAP_T4520
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Iceberg regression', parent_id)
    try:
        QAP_T4546.execute(session_id, report_id)
        QAP_T4545.execute(session_id, report_id)
        QAP_T4544.execute(session_id, report_id)
        QAP_T4540.execute(session_id, report_id)
        QAP_T4539.execute(session_id, report_id)
        QAP_T4532.execute(session_id, report_id)
        QAP_T4520.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
