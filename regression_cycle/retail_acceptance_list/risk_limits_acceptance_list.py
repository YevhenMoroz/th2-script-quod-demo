from test_cases.ret.Risk_Limits import QAP_T3748, QAP_T3756, QAP_T3747, QAP_T3742, QAP_T3737, QAP_T3734, QAP_T3726
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Risk Limits', parent_id)
    try:
        QAP_T3748.execute(session_id, report_id)
        QAP_T3756.execute(session_id, report_id)
        QAP_T3747.execute(session_id, report_id)
        QAP_T3742.execute(session_id, report_id)
        QAP_T3737.execute(session_id, report_id)
        QAP_T3734.execute(session_id, report_id)
        QAP_T3726.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
