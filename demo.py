import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from my_methods import send_md, send_rfq
from rule_management import RuleManager
from test_cases.fx.fx_mm_esp import QAP_1643, QAP_6145
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389

from stubs import Stubs
from test_cases.fx.fx_mm_rfq import QAP_4505, for_test_77679, QAP_5848, QAP_5856
from test_cases.fx.fx_taker_esp import QAP_5564, QAP_5589, QAP_5591, QAP_5598, QAP_5600
from test_cases.fx.qs_fx_routine import QAP_5176
from test_cases.fx.ui_wrappers import wrapper_test
from win_gui_modules.utils import set_session_id, get_opened_fe, prepare_fe_2

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run

    report_id = bca.create_event("ostronov" + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id()
    start_time = datetime.now()
    print(f"Start time :{start_time}")

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)


        # rm = RuleManager()
        # rm.add_TRADE_ESP("fix-bs-esp-314-luna-standard")
        # rm.add_fx_md_to("fix-fh-314-luna")
        # rm.remove_rule_by_id(48)
        # rm.print_active_rules()
        # send_md.execute(report_id, 1.19, 1.21)
        # QAP_4505.execute(report_id)
        # QAP_5856.execute(report_id)
        # QAP_5564.execute(report_id, session_id)
        # QAP_5589.execute(report_id, session_id)
        # QAP_5591.execute(report_id, session_id)
        # QAP_5598.execute(report_id, session_id)
        # QAP_5176.execute(report_id)
        # send_rfq.execute(report_id)
        # send_rfq.execute(report_id)
        QAP_6145.execute(report_id)
        # wrapper_test.execute(report_id, session_id)
        # wrapper_test.execute(report_id, session_id)
        # QAP_5856.execute(report_id)
        # for_test_77679.execute(report_id, session_id)
        # QAP_1643.execute(report_id, session_id)
        # QAP_5389().execute(report_id)

        # SendMD.execute(report_id)
        # send_rfq.execute(report_id)

        # QAP_5369_not_ready.execute(report_id)
        print(f"Duration is {datetime.now()-start_time}")
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
