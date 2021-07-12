from quod_qa.fx.fx_taker_rfq import QAP_568, QAP_569, QAP_574, QAP_2826, QAP_2835, QAP_2847
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Acceptance list', parent_id)
    session_id = set_session_id()
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

            # QAP_568.execute(report_id, session_id)
            # QAP_569.execute(report_id, session_id)
            QAP_574.execute(report_id, session_id)
            # QAP_2826.execute(report_id, session_id)
            # QAP_2835.execute(report_id, session_id)
            # QAP_2847.execute(report_id, session_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
