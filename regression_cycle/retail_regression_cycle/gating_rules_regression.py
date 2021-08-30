from quod_qa.RET.Gating_Rules import QAP_4280, QAP_4282, QAP_4288, QAP_4307
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Gating Rules', parent_id)
    try:
        QAP_4280.execute(session_id, report_id)
        QAP_4282.execute(session_id, report_id)
        QAP_4288.execute(session_id, report_id)
        QAP_4307.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
