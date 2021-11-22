import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_autohedging import QAP_2159, QAP_2228, QAP_2255, QAP_2322, QAP_3939, QAP_2470, QAP_3146, QAP_3147, \
    QAP_5551, QAP_3354, QAP_3067, QAP_2326
from quod_qa.fx.fx_mm_esp import QAP_1554, QAP_2872, QAP_1518
from quod_qa.fx.fx_mm_rfq import for_test_77679

from quod_qa.fx.fx_taker_rfq import QAP_568
from quod_qa.fx.my_methods import send_rfq
from quod_qa.fx.ui_wrappers import wrapper_test
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run

    report_id = bca.create_event("ostronov" + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 309"
    session_id = set_session_id()
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        # QAP_5635.execute(report_id, session_id)
        wrapper_test.execute(report_id, session_id)
        # QAP_5537_not_ready.execute(report_id)
        # for_Daria.execute(report_id,session_id)
        # SendMD.execute(report_id)
        # for_test_77679.execute(report_id, session_id)
        # QAP_2872.execute(report_id)
        # send_rfq.execute(report_id)

        # QAP_5369_not_ready.execute(report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
