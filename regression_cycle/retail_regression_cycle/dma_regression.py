from quod_qa.RET.DMA import QAP_4290, QAP_4302, QAP_4309, QAP_4323, QAP_4326, QAP_4327, QAP_4297, QAP_4304, QAP_4310
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
        QAP_4290.execute(session_id, report_id)
        QAP_4302.execute(session_id, report_id)
        QAP_4309.execute(session_id, report_id)
        QAP_4323.execute(session_id, report_id)
        QAP_4326.execute(session_id, report_id)
        QAP_4327.execute(session_id, report_id)
        QAP_4297.execute(session_id, report_id)
        QAP_4304.execute(session_id, report_id)
        QAP_4310.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
