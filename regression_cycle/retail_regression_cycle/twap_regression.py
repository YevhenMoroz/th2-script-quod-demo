from quod_qa.RET.Algo.Algo_TWAP import QAP_4295, QAP_4317
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Algo TWAP', parent_id)
    try:
        QAP_4295.execute(session_id, report_id)
        QAP_4317.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
