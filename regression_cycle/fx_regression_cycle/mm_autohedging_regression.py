from quod_qa.fx.fx_mm_autohedging import QAP_2290, QAP_2228, QAP_2113, QAP_2250, QAP_2251, QAP_2252
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
    report_id = bca.create_event('FX MM Positions regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        QAP_2290.execute(report_id, session_id)
        QAP_2228.execute(report_id, session_id)
        QAP_2113.execute(report_id, session_id)
        QAP_2250.execute(report_id, session_id)
        QAP_2251.execute(report_id, session_id)
        QAP_2252.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)
        # close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
