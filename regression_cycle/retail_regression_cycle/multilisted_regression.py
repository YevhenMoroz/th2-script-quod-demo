from test_cases.ret.Algo.Algo_Multilisted import QAP_T4148, QAP_T4146, QAP_T4145, QAP_T4141, QAP_T4140, QAP_T4105, QAP_T4103, \
    QAP_T4101, QAP_T4100
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Multilisted regression', parent_id)
    try:
        QAP_T4148.execute(session_id, report_id)
        QAP_T4146.execute(session_id, report_id)
        QAP_T4145.execute(session_id, report_id)
        QAP_T4141.execute(session_id, report_id)
        QAP_T4140.execute(session_id, report_id)
        QAP_T4105.execute(session_id, report_id)
        QAP_T4103.execute(session_id, report_id)
        QAP_T4101.execute(session_id, report_id)
        QAP_T4100.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
