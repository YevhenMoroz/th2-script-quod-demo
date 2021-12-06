import logging
from datetime import datetime

from ExactPro_examples.examples import example_java_api
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Basket.QAP_4648 import QAP4648
from test_cases.eq.Basket.QAP_6114 import QAP6114
from test_cases.eq.Counterpart.QAP_3503 import QAP3503
from test_cases.eq.Counterpart.QAP_3509 import QAP3509
from test_cases.eq.Counterpart.QAP_3510 import QAP3510
from test_cases.eq.PostTrade.QAP_5386 import QAP5386
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('test ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()

    try:
        #example_java_api.TestCase(report_id).execute()

        QAP3503(report_id, session_id, None).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
