from test_cases.ret.DMA import QAP_T3757, QAP_T3745, QAP_T3739, QAP_T3725, QAP_T3722, QAP_T3721, QAP_T3750, QAP_T3743, QAP_T3738,\
    QAP_T3727, QAP_T3736, QAP_T3746, QAP_T3751, QAP_T3732
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
        QAP_T3732.TestCase(report_id).execute()
        QAP_T3757.execute(session_id, report_id)
        QAP_T3751.execute(session_id, report_id)
        QAP_T3750.execute(session_id, report_id)
        QAP_T3746.execute(session_id, report_id)
        QAP_T3745.execute(session_id, report_id)
        QAP_T3743.execute(session_id, report_id)
        QAP_T3739.execute(session_id, report_id)
        QAP_T3738.execute(session_id, report_id)
        QAP_T3736.execute(session_id, report_id)
        QAP_T3727.execute(session_id, report_id)
        QAP_T3725.execute(session_id, report_id)
        QAP_T3722.execute(session_id, report_id)
        QAP_T3721.execute(session_id, report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
