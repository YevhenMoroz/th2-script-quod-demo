from test_cases.ret.Care import QAP_T7624, QAP_4286, QAP_4313, QAP_5087, QAP_5088, QAP_T7694, QAP_5139, QAP_5142, QAP_5143, \
    QAP_T7692, QAP_T7693, QAP_T7691, QAP_T7690, QAP_5144, QAP_5145, QAP_5146, QAP_5147, QAP_5148, QAP_5149, QAP_5152, QAP_5154,\
    QAP_5155, QAP_5162
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Care regression', parent_id)

    try:
        QAP_T7624.execute(session_id, report_id)
        QAP_4286.execute(session_id, report_id)
        QAP_4313.execute(session_id, report_id)
        QAP_4313.execute(session_id, report_id)
        QAP_5087.execute(session_id, report_id)
        QAP_5088.execute(report_id)
        QAP_T7694.execute(session_id, report_id)
        QAP_5139.execute(session_id, report_id)
        QAP_5142.execute(session_id, report_id)
        QAP_5143.execute(session_id, report_id)
        QAP_T7692.execute(session_id, report_id)
        QAP_T7693.execute(session_id, report_id)
        QAP_T7691.execute(session_id, report_id)
        QAP_T7690.execute(session_id, report_id)
        QAP_5144.execute(session_id, report_id)
        QAP_5145.execute(session_id, report_id)
        QAP_5146.execute(session_id, report_id)
        QAP_5147.execute(session_id, report_id)
        QAP_5148.execute(session_id, report_id)
        QAP_5149.execute(session_id, report_id)
        QAP_5152.execute(session_id, report_id)
        QAP_5154.execute(session_id, report_id)
        QAP_5155.execute(session_id, report_id)
        QAP_5162.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()

