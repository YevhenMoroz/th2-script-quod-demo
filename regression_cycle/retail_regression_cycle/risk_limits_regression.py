from quod_qa.RET.Risk_Limits import QAP_4299, QAP_4311, QAP_4314, QAP_4306, QAP_4291, QAP_4322, QAP_4300
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Risk Limits regression', parent_id)
    try:
        QAP_4299.execute(session_id, report_id)
        QAP_4311.execute(session_id, report_id)
        QAP_4314.execute(session_id, report_id)
        QAP_4306.execute(session_id, report_id)
        QAP_4291.execute(session_id, report_id)
        QAP_4322.execute(session_id, report_id)
        QAP_4300.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
