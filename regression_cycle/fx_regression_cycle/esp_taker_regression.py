from quod_qa.fx.fx_taker_esp import QAP_110, QAP_1115, QAP_3364, QAP_382, QAP_2854, QAP_2947, QAP_231, QAP_3042, \
    QAP_492, QAP_2948, QAP_1591, QAP_2949, QAP_833, QAP_4156, QAP_404, QAP_2373, QAP_2416
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('ESP Taker regression', parent_id)
    session_id = set_session_id()

    try:
        QAP_110.execute(report_id, session_id)
        QAP_231.execute(report_id, session_id)
        QAP_382.execute(report_id, session_id)
        QAP_404.execute(report_id, session_id)
        QAP_492.execute(report_id, session_id)
        QAP_833.execute(report_id, session_id)
        QAP_1115.execute(report_id, session_id)
        QAP_1591.execute(report_id, session_id)
        QAP_2373.execute(report_id, session_id)
        QAP_2416.execute(report_id, session_id)
        QAP_2854.execute(report_id, session_id)
        QAP_2947.execute(report_id, session_id)
        QAP_2948.execute(report_id, session_id)
        QAP_2949.execute(report_id, session_id)
        QAP_3042.execute(report_id, session_id)
        QAP_3364.execute(report_id, session_id)
        QAP_4156.execute(report_id, session_id)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
